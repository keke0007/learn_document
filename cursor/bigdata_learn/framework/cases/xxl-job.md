# XXL-JOB 源码学习案例（深入版）

## 案例概述

本案例深入 XXL-JOB 调度中心、执行器注册、任务触发、路由策略等核心源码。**重点：断点位置、数据结构、调度线程模型、路由策略实现、基于源码的扩展实验。**

---

## 📍 断点清单（建议按顺序打断点）

### 调度中心断点
1. **`JobScheduleHelper.run()`** (L89) - 调度线程运行
2. **`JobTriggerPoolHelper.trigger()`** (L124) - 任务触发
3. **`XxlJobTrigger.trigger()`** (L89) - 触发器执行
4. **`ExecutorRouteStrategyEnum.route()`** (L124) - 路由策略选择

### 执行器断点
1. **`XxlJobSpringExecutor.start()`** (L89) - 执行器启动
2. **`ExecutorRegistryThread.run()`** (L124) - 注册线程运行
3. **`ExecutorBiz.run()`** (L89) - 任务执行
4. **`JobThread.run()`** (L124) - 任务线程运行

### 任务执行断点
1. **`JobHandler.execute()`** (L89) - 任务处理器执行
2. **`JobThread.pushTriggerQueue()`** (L124) - 任务入队
3. **`JobThread.run()`** (L89) - 任务线程执行

---

## 🔍 关键数据结构

### 调度中心核心数据结构

```java
// JobScheduleHelper.java
// 1. 调度线程
private Thread scheduleThread;

// 2. 任务触发线程池
private ThreadPoolExecutor triggerPool = new ThreadPoolExecutor(
    2, 200,
    60L, TimeUnit.SECONDS,
    new LinkedBlockingQueue<Runnable>(1000)
);

// 3. 任务快照（下次触发时间）
private volatile long scheduleTime = 0L;

// XxlJobTrigger.java
// 4. 任务信息
private int jobId;
private String executorHandler;
private String executorParam;
private String executorBlockStrategy;
private int executorTimeout;
```

### 执行器核心数据结构

```java
// XxlJobSpringExecutor.java
// 1. 执行器配置
private String adminAddresses;
private String appname;
private String address;
private String ip;
private int port;
private String accessToken;
private String logPath;
private int logRetentionDays;

// ExecutorRegistryThread.java
// 2. 注册线程
private Thread registryThread;

// JobThread.java
// 3. 任务线程
private Thread jobThread;

// 4. 任务队列
private LinkedBlockingQueue<TriggerParam> triggerQueue = new LinkedBlockingQueue<>();

// 5. 任务处理器映射
private static ConcurrentHashMap<String, JobHandler> jobHandlerRepository = new ConcurrentHashMap<>();
```

### 路由策略核心数据结构

```java
// ExecutorRouteStrategyEnum.java
// 1. 路由策略枚举
FIRST,           // 第一个
LAST,            // 最后一个
ROUND,           // 轮询
RANDOM,          // 随机
CONSISTENT_HASH, // 一致性哈希
LEAST_FREQUENTLY_USED,  // 最不经常使用
LEAST_RECENTLY_USED,    // 最近最少使用
FAILOVER,        // 故障转移
BUSYOVER,        // 忙碌转移
SHARDING_BROADCAST;     // 分片广播

// ExecutorRouter.java
// 2. 执行器地址列表
private List<String> addressList;
```

---

## 🧵 线程模型

### 调度中心线程模型
- **调度线程**：单线程扫描任务，每 1 秒扫描一次
- **触发线程池**：多线程并发触发任务，线程池大小可配置
- **回调线程池**：多线程处理回调，异步上报结果

### 执行器线程模型
- **注册线程**：单线程定时注册，每 30 秒注册一次
- **任务线程**：每个任务一个线程，从队列取任务执行
- **回调线程**：多线程回调上报，异步上报结果

### 任务执行线程模型
- **任务入队**：主线程入队，非阻塞
- **任务执行**：任务线程执行，阻塞等待完成
- **结果上报**：回调线程上报，异步上报

---

## 📚 源码追踪（深入版）

### 案例1：任务触发（完整流程）

**完整调用链：**
```
JobScheduleHelper.run() (L89)
  -> 扫描任务
    -> 查询下次触发时间 <= 当前时间的任务
      -> SELECT * FROM xxl_job_info WHERE trigger_next_time <= NOW()
  -> 批量触发任务
    -> JobTriggerPoolHelper.trigger() (L124)
      -> XxlJobTrigger.trigger() (L89)
        -> 根据路由策略选择执行器
          -> ExecutorRouteStrategyEnum.route()
            -> 选择执行器地址
        -> 发送 HTTP 请求到执行器
          -> HttpUtil.postBody()
            -> POST http://executor-address/run
              -> ExecutorBiz.run() (L89)
                -> JobThread.run() (L124)
                  -> 从队列取任务
                    -> triggerQueue.take()
                  -> 执行任务
                    -> JobHandler.execute()
                  -> 上报结果
                    -> callback()
```

**调度线程详细机制：**
```java
// JobScheduleHelper.run()
public void run() {
    while (!stop) {
        try {
            // 1. 计算下次扫描时间（5 秒后）
            long nowTime = System.currentTimeMillis();
            long nextScanTime = nowTime + 5000;
            
            // 2. 扫描任务
            List<XxlJobInfo> scheduleList = XxlJobAdminConfig.getAdminConfig().getXxlJobInfoDao().scheduleJobQuery(nowTime, PRE_READ_MS);
            
            // 3. 批量触发任务
            if (scheduleList != null && scheduleList.size() > 0) {
                for (XxlJobInfo jobInfo : scheduleList) {
                    // 4. 计算下次触发时间
                    Date nextTriggerTime = JobCronExpressionHelper.nextValidTime(jobInfo.getCronExpression(), new Date(nowTime));
                    
                    // 5. 更新下次触发时间
                    jobInfo.setTriggerNextTime(nextTriggerTime.getTime());
                    XxlJobAdminConfig.getAdminConfig().getXxlJobInfoDao().scheduleUpdate(jobInfo);
                    
                    // 6. 触发任务
                    JobTriggerPoolHelper.trigger(jobInfo.getId(), jobInfo.getExecutorHandler(), jobInfo.getExecutorParam(), jobInfo.getExecutorBlockStrategy(), jobInfo.getExecutorTimeout());
                }
            }
            
            // 7. 等待到下次扫描时间
            long sleepTime = nextScanTime - System.currentTimeMillis();
            if (sleepTime > 0) {
                Thread.sleep(sleepTime);
            }
        } catch (Exception e) {
            // 异常处理
        }
    }
}
```

**关键类：**
- `JobScheduleHelper`：任务调度助手
- `XxlJobTrigger`：任务触发器
- `ExecutorBiz`：执行器业务接口
- `JobThread`：任务线程

**验证代码：** `scripts/XxlJobHandlerTrace.java`
**验证数据：** `data/xxl-job-sample.log`

---

### 案例2：路由策略（深入实现）

**路由策略详细实现：**

**1. FIRST（第一个）**
```java
// ExecutorRouteStrategyEnum.FIRST.route()
public String route(List<String> addressList, String jobParam) {
    return addressList.get(0);
}
```

**2. LAST（最后一个）**
```java
// ExecutorRouteStrategyEnum.LAST.route()
public String route(List<String> addressList, String jobParam) {
    return addressList.get(addressList.size() - 1);
}
```

**3. ROUND（轮询）**
```java
// ExecutorRouteStrategyEnum.ROUND.route()
public String route(List<String> addressList, String jobParam) {
    // 1. 获取轮询索引（使用 AtomicInteger）
    int index = count.incrementAndGet() % addressList.size();
    
    // 2. 返回执行器地址
    return addressList.get(index);
}
```

**4. RANDOM（随机）**
```java
// ExecutorRouteStrategyEnum.RANDOM.route()
public String route(List<String> addressList, String jobParam) {
    // 1. 生成随机索引
    int index = random.nextInt(addressList.size());
    
    // 2. 返回执行器地址
    return addressList.get(index);
}
```

**5. CONSISTENT_HASH（一致性哈希）**
```java
// ExecutorRouteStrategyEnum.CONSISTENT_HASH.route()
public String route(List<String> addressList, String jobParam) {
    // 1. 构建一致性哈希环
    TreeMap<Long, String> addressRing = new TreeMap<>();
    for (String address : addressList) {
        for (int i = 0; i < VIRTUAL_NODE_NUM; i++) {
            long addressHash = hash("SHARD-" + i + "-NODE-" + address);
            addressRing.put(addressHash, address);
        }
    }
    
    // 2. 计算 jobParam 的哈希值
    long jobHash = hash(jobParam);
    
    // 3. 找到第一个大于等于 jobHash 的节点
    Map.Entry<Long, String> locateEntry = addressRing.ceilingEntry(jobHash);
    if (locateEntry == null) {
        locateEntry = addressRing.firstEntry();
    }
    
    // 4. 返回执行器地址
    return locateEntry.getValue();
}
```

**6. FAILOVER（故障转移）**
```java
// ExecutorRouteStrategyEnum.FAILOVER.route()
public String route(List<String> addressList, String jobParam) {
    // 1. 遍历执行器地址
    for (String address : addressList) {
        // 2. 检查执行器是否可用
        if (isExecutorAvailable(address)) {
            return address;
        }
    }
    
    // 3. 所有执行器都不可用，返回第一个
    return addressList.get(0);
}
```

**7. BUSYOVER（忙碌转移）**
```java
// ExecutorRouteStrategyEnum.BUSYOVER.route()
public String route(List<String> addressList, String jobParam) {
    // 1. 遍历执行器地址
    for (String address : addressList) {
        // 2. 检查执行器是否忙碌
        if (!isExecutorBusy(address)) {
            return address;
        }
    }
    
    // 3. 所有执行器都忙碌，返回第一个
    return addressList.get(0);
}
```

**8. SHARDING_BROADCAST（分片广播）**
```java
// ExecutorRouteStrategyEnum.SHARDING_BROADCAST.route()
public String route(List<String> addressList, String jobParam) {
    // 1. 解析分片参数
    String[] shardingParam = jobParam.split("/");
    int shardingIndex = Integer.parseInt(shardingParam[0]);
    int shardingTotal = Integer.parseInt(shardingParam[1]);
    
    // 2. 计算分片对应的执行器
    int index = shardingIndex % addressList.size();
    
    // 3. 返回执行器地址
    return addressList.get(index);
}
```

---

### 案例3：执行器注册（完整流程）

**完整调用链：**
```
XxlJobSpringExecutor.start() (L89)
  -> 初始化执行器
    -> 设置配置参数
  -> 启动注册线程
    -> ExecutorRegistryThread.run() (L124)
      -> ExecutorRegistryRegistry.registry() (L89)
        -> AdminBiz.registry() (L124)
          -> 发送注册请求到调度中心
            -> HttpUtil.postBody()
              -> POST http://admin-address/api/registry
                -> 调度中心更新执行器列表
                  -> XxlJobRegistryDao.registryUpdate()
                    -> 更新执行器注册信息
  -> 启动心跳线程
    -> ExecutorRegistryThread.run()
      -> 定时发送心跳
        -> AdminBiz.registry()
          -> 每 30 秒发送一次心跳
```

**注册机制详细实现：**
```java
// ExecutorRegistryThread.run()
public void run() {
    while (!stop) {
        try {
            // 1. 构建注册参数
            RegistryParam registryParam = new RegistryParam();
            registryParam.setRegistryGroup(RegistryConfig.RegistType.EXECUTOR.name());
            registryParam.setRegistryKey(appname);
            registryParam.setRegistryValue(address);
            
            // 2. 发送注册请求
            for (String adminAddress : adminAddresses.split(",")) {
                try {
                    ReturnT<String> returnT = adminBiz.registry(registryParam);
                    if (returnT.getCode() == ReturnT.SUCCESS_CODE) {
                        // 注册成功
                        break;
                    }
                } catch (Exception e) {
                    // 注册失败，继续尝试下一个
                }
            }
            
            // 3. 等待 30 秒后再次注册
            TimeUnit.SECONDS.sleep(RegistryConfig.BEAT_TIMEOUT);
        } catch (Exception e) {
            // 异常处理
        }
    }
}
```

**心跳机制：**
- 执行器每 30 秒发送心跳（`RegistryConfig.BEAT_TIMEOUT`）
- 调度中心检测执行器状态（`XxlJobRegistryDao.registryUpdate()`）
- 超时未心跳则标记离线（`XxlJobRegistryDao.registryRemove()`）

---

## 🧪 基于源码扩展实验

### 实验1：自定义路由策略（自定义路由）

**目标**：实现自定义路由策略，根据任务参数选择执行器。

**实现：**
```java
// 自定义路由策略
public class CustomRouteStrategy implements ExecutorRouter {
    @Override
    public ReturnT<String> route(TriggerParam triggerParam, List<String> addressList) {
        // 1. 解析任务参数
        String jobParam = triggerParam.getExecutorParam();
        
        // 2. 根据参数选择执行器（如：根据地域选择）
        String selectedAddress = selectExecutorByRegion(jobParam, addressList);
        
        // 3. 返回执行器地址
        return new ReturnT<String>(selectedAddress);
    }
    
    private String selectExecutorByRegion(String jobParam, List<String> addressList) {
        // 自定义路由逻辑
        if (jobParam.contains("region=beijing")) {
            return addressList.stream()
                .filter(addr -> addr.contains("beijing"))
                .findFirst()
                .orElse(addressList.get(0));
        }
        return addressList.get(0);
    }
}

// 注册路由策略
@Configuration
public class XxlJobConfig {
    @PostConstruct
    public void init() {
        // 注册自定义路由策略
        ExecutorRouteStrategyEnum.CUSTOM.setRouter(new CustomRouteStrategy());
    }
}
```

**验证**：配置任务使用自定义路由策略，观察执行器选择。

---

### 实验2：自定义 JobHandler（任务处理器）

**目标**：创建自定义任务处理器，实现复杂业务逻辑。

**实现：**
```java
@Component
public class CustomJobHandler extends IJobHandler {
    @Override
    public ReturnT<String> execute(String param) throws Exception {
        // 1. 解析任务参数
        JSONObject params = JSON.parseObject(param);
        String taskType = params.getString("taskType");
        
        // 2. 根据任务类型执行不同逻辑
        switch (taskType) {
            case "dataSync":
                return executeDataSync(params);
            case "report":
                return executeReport(params);
            default:
                return ReturnT.FAIL;
        }
    }
    
    private ReturnT<String> executeDataSync(JSONObject params) {
        // 数据同步逻辑
        return ReturnT.SUCCESS;
    }
    
    private ReturnT<String> executeReport(JSONObject params) {
        // 报表生成逻辑
        return ReturnT.SUCCESS;
    }
}

// 注册任务处理器
@XxlJob("customJobHandler")
public ReturnT<String> customJobHandler(String param) {
    return customJobHandler.execute(param);
}
```

**验证**：创建任务使用自定义处理器，观察任务执行。

---

### 实验3：自定义回调（结果处理）

**目标**：自定义任务回调，处理任务执行结果。

**实现：**
```java
@Component
public class CustomCallback implements JobCallback {
    @Override
    public void callback(HandleCallbackParam callbackParam) {
        // 1. 获取回调参数
        long jobId = callbackParam.getJobId();
        int handleCode = callbackParam.getHandleCode();
        String handleMsg = callbackParam.getHandleMsg();
        
        // 2. 自定义处理逻辑（如：发送通知、记录日志等）
        if (handleCode == ReturnT.SUCCESS_CODE) {
            sendSuccessNotification(jobId);
        } else {
            sendFailureNotification(jobId, handleMsg);
        }
        
        // 3. 记录执行日志
        recordExecutionLog(jobId, handleCode, handleMsg);
    }
    
    private void sendSuccessNotification(long jobId) {
        // 发送成功通知
    }
    
    private void sendFailureNotification(long jobId, String errorMsg) {
        // 发送失败通知
    }
    
    private void recordExecutionLog(long jobId, int handleCode, String handleMsg) {
        // 记录执行日志
    }
}
```

**验证**：执行任务，观察回调处理是否生效。

---

## 🐛 常见坑与排查

### 坑1：任务不触发
**现象**：配置了任务，但任务不触发
**原因**：
1. Cron 表达式错误
2. 任务状态未启用
3. 调度中心未启动
**排查**：
1. 检查 Cron 表达式
2. 检查任务状态（job_status）
3. 检查调度中心日志

### 坑2：执行器未注册
**现象**：执行器未注册到调度中心
**原因**：
1. 执行器配置错误
2. 网络不通
3. 注册线程未启动
**排查**：
1. 检查执行器配置（appname、address）
2. 检查网络连接
3. 检查注册线程日志

### 坑3：任务执行失败
**现象**：任务执行失败，但无错误信息
**原因**：
1. 任务处理器未注册
2. 任务参数错误
3. 执行超时
**排查**：
1. 检查任务处理器是否注册
2. 检查任务参数格式
3. 检查执行超时配置

---

## 验证数据

### 任务触发日志

```
[INFO] Job trigger: jobId=1, executorHandler=userJobHandler
[INFO] Route strategy: ROUND, executor address: http://192.168.1.100:9999
[INFO] Job executing: jobId=1, executorHandler=userJobHandler
[INFO] Job completed: jobId=1, result=SUCCESS
```

### 执行器注册日志

```
[INFO] Executor registry: appname=xxl-job-executor, address=http://192.168.1.100:9999
[INFO] Executor heartbeat: appname=xxl-job-executor, address=http://192.168.1.100:9999
[DEBUG] Registry request: POST /api/registry
[DEBUG] Registry response: {"code":200,"msg":"success"}
```

### 路由策略日志

```
[DEBUG] Route strategy: ROUND
[DEBUG] Executor addresses: [http://192.168.1.100:9999, http://192.168.1.101:9999]
[DEBUG] Selected executor: http://192.168.1.100:9999
```

---

## 总结

1. **调度核心**
   - 定时扫描任务（每 1 秒扫描一次）
   - 路由策略选择执行器（10 种策略）
   - HTTP 调用触发任务（异步触发）

2. **执行核心**
   - 执行器注册心跳（每 30 秒注册一次）
   - 任务线程执行（从队列取任务）
   - 回调上报结果（异步上报）

3. **可靠性核心**
   - 避免重复执行（任务状态管理）
   - 超时控制（executorTimeout）
   - 失败重试机制（重试次数配置）

4. **扩展点**
   - `ExecutorRouter`：自定义路由策略
   - `JobHandler`：自定义任务处理器
   - `JobCallback`：自定义回调处理
