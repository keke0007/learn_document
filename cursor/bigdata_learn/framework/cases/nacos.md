# Nacos 源码学习案例（深入版）

## 案例概述

本案例深入 Nacos 注册发现、配置中心、长轮询推送等核心源码。**重点：断点位置、数据结构、线程模型、一致性机制、基于源码的扩展实验。**

---

## 📍 断点清单（建议按顺序打断点）

### 注册发现断点
1. **`NacosServiceRegistry.register()`** (L65) - 服务注册入口
2. **`NacosNamingService.registerInstance()`** (L89) - 实例注册
3. **`NamingProxy.registerService()`** (L329) - HTTP 注册请求
4. **`BeatReactor.addBeatInfo()`** (L73) - 心跳发送
5. **`HostReactor.getServiceInfo()`** (L89) - 服务发现

### 配置中心断点
1. **`NacosConfigService.getConfig()`** (L124) - 配置获取入口
2. **`ClientWorker.getServerConfig()`** (L89) - 服务器配置获取
3. **`LongPollingRunnable.run()`** (L124) - 长轮询任务
4. **`ConfigController.getConfig()`** (L89) - 服务端配置获取
5. **`LocalConfigInfoProcessor.saveSnapshot()`** (L89) - 本地缓存保存

---

## 🔍 关键数据结构

### 注册发现核心数据结构

```java
// NacosNamingService.java
// 1. 服务实例映射
private final Map<String, Instance> instanceMap = new ConcurrentHashMap<>();

// 2. 服务信息缓存
private final Map<String, ServiceInfo> serviceInfoMap = new ConcurrentHashMap<>();

// BeatReactor.java
// 3. 心跳任务映射
private final Map<String, BeatInfo> beatInfoMap = new ConcurrentHashMap<>();

// HostReactor.java
// 4. 服务信息缓存（客户端）
private final Map<String, ServiceInfo> serviceInfoMap = new ConcurrentHashMap<>();

// 5. 更新任务队列
private final BlockingQueue<ServiceInfo> changedServices = new LinkedBlockingQueue<>();
```

### 配置中心核心数据结构

```java
// NacosConfigService.java
// 1. 配置缓存
private final Map<String, CacheData> cacheMap = new ConcurrentHashMap<>();

// ClientWorker.java
// 2. 长轮询任务列表
private final List<LongPollingRunnable> longPollingTasks = new ArrayList<>();

// 3. 配置变更监听器
private final Map<String, List<ManagerListener>> listeners = new ConcurrentHashMap<>();

// LocalConfigInfoProcessor.java
// 4. 本地快照缓存
private final Map<String, String> snapshotCache = new ConcurrentHashMap<>();
```

### 服务端核心数据结构

```java
// ServiceManager.java
// 1. 服务映射
private final Map<String, Service> serviceMap = new ConcurrentHashMap<>();

// 2. 实例映射
private final Map<String, Instance> instanceMap = new ConcurrentHashMap<>();

// ConfigService.java
// 3. 配置存储
private final Map<String, Config> configMap = new ConcurrentHashMap<>();

// 4. 配置变更监听器
private final Map<String, List<ConfigChangeListener>> listeners = new ConcurrentHashMap<>();
```

---

## 🧵 线程模型

### 注册发现线程模型
- **注册线程**：主线程同步注册，HTTP 请求阻塞
- **心跳线程**：`BeatReactor` 使用 `ScheduledExecutorService` 定时发送心跳
- **服务发现线程**：`HostReactor` 使用 `ScheduledExecutorService` 定时更新服务列表
- **更新线程**：`UpdateTask` 异步更新服务信息

### 配置中心线程模型
- **配置拉取线程**：主线程同步拉取，HTTP 请求阻塞
- **长轮询线程**：`LongPollingRunnable` 使用线程池执行长轮询任务
- **配置更新线程**：`ClientWorker` 使用 `ScheduledExecutorService` 定时检查配置变更
- **本地缓存线程**：`LocalConfigInfoProcessor` 使用独立线程保存快照

### 服务端线程模型
- **HTTP 处理线程**：使用 Netty 的 EventLoopGroup 处理 HTTP 请求
- **配置推送线程**：使用线程池推送配置变更
- **服务列表更新线程**：使用 `ScheduledExecutorService` 定时清理过期实例

---

## 📚 源码追踪（深入版）

### 案例1：服务注册（完整流程）

**完整调用链：**
```
NacosServiceRegistry.register() (L65)
  -> NamingService.registerInstance() (L89)
    -> NacosNamingService.registerInstance() (L89)
      -> NamingProxy.registerService() (L329)
        -> HTTP POST /nacos/v1/ns/instance
          -> InstanceController.register() (L89)
            -> ServiceManager.registerInstance() (L124)
              -> Service.addInstance() (L89)
                -> 更新服务列表
              -> 发布实例变更事件
      -> BeatReactor.addBeatInfo() (L73)
        -> 创建心跳任务
          -> ScheduledExecutorService.schedule() (L89)
            -> 定时发送心跳
```

**关键源码位置：**
- `NacosServiceRegistry.register()` - `spring-cloud-alibaba-nacos-discovery-2.x.x.jar`
- `NacosNamingService.registerInstance()` - `nacos-client-2.x.x.jar`
- `ServiceManager.registerInstance()` - `nacos-naming-2.x.x.jar`

**注册请求参数：**
```java
// NamingProxy.registerService()
Map<String, String> params = new HashMap<>();
params.put("namespaceId", namespaceId);
params.put("serviceName", serviceName);
params.put("groupName", groupName);
params.put("ip", instance.getIp());
params.put("port", String.valueOf(instance.getPort()));
params.put("weight", String.valueOf(instance.getWeight()));
params.put("healthy", String.valueOf(instance.isHealthy()));
params.put("enabled", String.valueOf(instance.isEnabled()));
params.put("ephemeral", String.valueOf(instance.isEphemeral()));
params.put("metadata", JSON.toJSONString(instance.getMetadata()));
```

**心跳机制：**
```java
// BeatReactor.addBeatInfo()
public void addBeatInfo(String serviceName, BeatInfo beatInfo) {
    // 1. 创建心跳任务
    BeatTask beatTask = new BeatTask(beatInfo);
    
    // 2. 定时执行心跳
    executorService.schedule(beatTask, 0, TimeUnit.MILLISECONDS);
    
    // 3. 缓存心跳信息
    beatInfoMap.put(buildKey(serviceName, beatInfo.getIp(), beatInfo.getPort()), beatInfo);
}

// BeatTask.run()
public void run() {
    // 1. 发送心跳请求
    String result = serverProxy.sendBeat(beatInfo);
    
    // 2. 解析心跳间隔
    long interval = JSON.parseObject(result).getLong("clientBeatInterval");
    
    // 3. 调度下次心跳
    executorService.schedule(this, interval, TimeUnit.MILLISECONDS);
}
```

**验证代码：** `scripts/NacosConfigTrace.java`

---

### 案例2：配置拉取（长轮询机制）

**完整调用链：**
```
NacosConfigService.getConfig() (L124)
  -> ClientWorker.getServerConfig() (L89)
    -> HttpAgent.httpGet() (L124)
      -> 请求配置服务器
        -> ConfigController.getConfig() (L89)
          -> ConfigService.getConfig() (L124)
            -> 返回配置内容
    -> LocalConfigInfoProcessor.saveSnapshot() (L89)
      -> 保存本地缓存
```

**长轮询机制：**
```
ClientWorker.checkUpdateDataIds() (L89)
  -> LongPollingRunnable.run() (L124)
    -> HttpAgent.httpPost() (L200)
      -> 长轮询请求（30s 超时）
        -> ConfigController.listener() (L124)
          -> 检查配置变更
            -> 有变更：立即返回变更的 DataId
            -> 无变更：等待 30 秒后返回空
    -> 处理配置变更
      -> 触发监听器
        -> ManagerListener.receiveConfigInfo()
      -> 更新本地缓存
        -> LocalConfigInfoProcessor.saveSnapshot()
```

**长轮询请求参数：**
```java
// LongPollingRunnable.run()
Map<String, String> params = new HashMap<>();
params.put("ListeningConfigs", listeningConfigs);  // 监听的配置列表
params.put("Probe-Modify-Request", "true");       // 长轮询标识

// 请求超时：30 秒
HttpResult result = httpAgent.httpPost(serverList.get(0) + "/v1/cs/configs/listener", params, 30000);
```

**配置变更推送：**
```java
// ConfigController.listener()
public String listener(HttpServletRequest request, HttpServletResponse response) {
    // 1. 解析监听配置
    String probeModify = request.getHeader("Probe-Modify-Request");
    
    // 2. 检查配置变更
    List<String> changedGroups = checkConfigChange(listeningConfigs);
    
    // 3. 有变更：立即返回
    if (!changedGroups.isEmpty()) {
        return String.join(",", changedGroups);
    }
    
    // 4. 无变更：等待 30 秒
    try {
        Thread.sleep(30000);
    } catch (InterruptedException e) {
        // 被中断，说明有变更
    }
    
    return "";
}
```

**关键类：**
- `NacosConfigService`：配置服务
- `ClientWorker`：客户端工作线程
- `LongPollingRunnable`：长轮询任务

---

### 案例3：服务发现（缓存机制）

**完整调用链：**
```
NacosServiceDiscovery.getInstances() (L89)
  -> NamingService.selectInstances() (L124)
    -> NacosNamingService.selectInstances() (L89)
      -> HostReactor.getServiceInfo() (L89)
        -> 从缓存获取
          -> ServiceInfo serviceInfo = serviceInfoMap.get(serviceName);
        -> 缓存未命中：从服务器拉取
          -> NamingProxy.queryList() (L200)
            -> HTTP GET /nacos/v1/ns/instance/list
              -> InstanceController.list() (L124)
                -> ServiceManager.getService() (L89)
                  -> 返回服务实例列表
        -> 更新缓存
          -> serviceInfoMap.put(serviceName, serviceInfo);
        -> 定时更新缓存
          -> UpdateTask.run() (L89)
            -> 定时从服务器拉取最新服务列表
```

**缓存更新机制：**
```java
// HostReactor.getServiceInfo()
public ServiceInfo getServiceInfo(String serviceName, String clusters) {
    // 1. 从缓存获取
    ServiceInfo serviceInfo = serviceInfoMap.get(serviceName);
    
    // 2. 缓存未命中或过期：从服务器拉取
    if (serviceInfo == null || serviceInfo.getLastRefTime() + cacheMillis < System.currentTimeMillis()) {
        serviceInfo = namingProxy.queryList(serviceName, clusters);
        serviceInfoMap.put(serviceName, serviceInfo);
    }
    
    // 3. 返回服务信息
    return serviceInfo;
}

// UpdateTask.run()
public void run() {
    // 1. 遍历所有服务
    for (String serviceName : serviceInfoMap.keySet()) {
        // 2. 从服务器拉取最新服务列表
        ServiceInfo serviceInfo = namingProxy.queryList(serviceName, "");
        
        // 3. 更新缓存
        ServiceInfo oldServiceInfo = serviceInfoMap.get(serviceName);
        if (!serviceInfo.getHosts().equals(oldServiceInfo.getHosts())) {
            // 4. 服务列表变更：触发监听器
            changedServices.offer(serviceInfo);
        }
        serviceInfoMap.put(serviceName, serviceInfo);
    }
}
```

**健康检查机制：**
- **客户端心跳**：每 5 秒发送心跳（`BeatReactor`）
- **服务端超时**：15 秒未收到心跳则标记不健康（`InstanceManager`）
- **自动摘除**：30 秒未收到心跳则移除实例（`ServiceManager`）

**服务端健康检查：**
```java
// InstanceManager.checkInstanceHealth()
public void checkInstanceHealth() {
    // 1. 遍历所有实例
    for (Instance instance : instanceMap.values()) {
        // 2. 检查最后心跳时间
        long lastHeartbeat = instance.getLastHeartbeat();
        long now = System.currentTimeMillis();
        
        // 3. 15 秒未心跳：标记不健康
        if (now - lastHeartbeat > 15000) {
            instance.setHealthy(false);
        }
        
        // 4. 30 秒未心跳：移除实例
        if (now - lastHeartbeat > 30000) {
            serviceManager.removeInstance(instance.getServiceName(), instance);
        }
    }
}
```

---

## 🧪 基于源码扩展实验

### 实验1：自定义 NamingService（扩展注册逻辑）

**目标**：在服务注册时添加自定义元数据。

**实现：**
```java
@Component
public class CustomNamingService extends NacosNamingService {
    @Override
    public void registerInstance(String serviceName, String groupName, Instance instance) throws NacosException {
        // 1. 添加自定义元数据
        Map<String, String> metadata = instance.getMetadata();
        metadata.put("custom-key", "custom-value");
        metadata.put("register-time", String.valueOf(System.currentTimeMillis()));
        
        // 2. 调用父类方法
        super.registerInstance(serviceName, groupName, instance);
    }
}
```

**验证**：注册服务后，检查实例元数据是否包含自定义字段。

---

### 实验2：自定义 ConfigListener（配置变更监听）

**目标**：监听配置变更并执行自定义逻辑。

**实现：**
```java
@Component
public class CustomConfigListener implements ManagerListener {
    @Override
    public void receiveConfigInfo(String configInfo) {
        System.out.println("Config changed: " + configInfo);
        // 自定义逻辑：重新加载配置、刷新 Bean 等
        refreshConfiguration(configInfo);
    }
    
    private void refreshConfiguration(String configInfo) {
        // 解析配置并更新应用配置
    }
}

// 使用监听器
@Autowired
private NacosConfigService configService;

public void addListener() {
    configService.addListener("application.yml", "DEFAULT_GROUP", new CustomConfigListener());
}
```

**验证**：修改 Nacos 配置，观察监听器是否被触发。

---

### 实验3：自定义 ServiceInfoUpdateCallback（服务列表更新回调）

**目标**：在服务列表更新时执行自定义逻辑。

**实现：**
```java
@Component
public class CustomServiceInfoUpdateCallback implements ServiceInfoUpdateCallback {
    @Override
    public void onServiceInfoUpdate(ServiceInfo serviceInfo) {
        System.out.println("Service info updated: " + serviceInfo.getName());
        System.out.println("Instances: " + serviceInfo.getHosts().size());
        
        // 自定义逻辑：更新负载均衡器、刷新服务列表等
        updateLoadBalancer(serviceInfo);
    }
    
    private void updateLoadBalancer(ServiceInfo serviceInfo) {
        // 更新负载均衡器服务列表
    }
}

// 使用回调
@Autowired
private HostReactor hostReactor;

public void addCallback() {
    hostReactor.subscribe("user-service", "", new CustomServiceInfoUpdateCallback());
}
```

**验证**：启动/停止服务实例，观察回调是否被触发。

---

## 🐛 常见坑与排查

### 坑1：服务注册失败
**现象**：服务注册到 Nacos 失败
**原因**：
1. Nacos 服务器不可用
2. 网络问题
3. 命名空间/分组不匹配
**排查**：
1. 检查 Nacos 服务器地址和端口
2. 检查网络连接
3. 检查命名空间和分组配置

### 坑2：配置拉取失败
**现象**：配置拉取失败或超时
**原因**：
1. DataId/Group 不匹配
2. 长轮询超时
3. 本地缓存损坏
**排查**：
1. 检查 DataId 和 Group 配置
2. 检查长轮询超时设置
3. 清除本地缓存重试

### 坑3：服务发现不及时
**现象**：服务实例变更后，客户端未及时更新
**原因**：
1. 缓存更新间隔过长
2. 心跳失败
3. 服务端健康检查延迟
**排查**：
1. 检查缓存更新间隔配置
2. 检查心跳发送是否成功
3. 检查服务端健康检查配置

---

## 验证数据

### 注册日志

```
[INFO] Registering service: user-service
[INFO] Instance registered: 192.168.1.100:8080
[INFO] Heartbeat sent: 192.168.1.100:8080
[DEBUG] Register request: POST /nacos/v1/ns/instance?serviceName=user-service&ip=192.168.1.100&port=8080
[DEBUG] Register response: {"code":200,"message":"success"}
```

### 配置拉取日志

```
[DEBUG] Fetching config: DataId=application.yml, Group=DEFAULT_GROUP
[DEBUG] Config received: {"server.port":8080}
[DEBUG] Config saved to local cache: /data/nacos/config/application.yml
[DEBUG] Long polling started: DataId=application.yml, Group=DEFAULT_GROUP
[DEBUG] Config changed detected: application.yml
[DEBUG] Config updated: {"server.port":8081}
```

### 服务发现日志

```
[DEBUG] Getting service info: user-service
[DEBUG] Service info from cache: 3 instances
[DEBUG] Service info updated: 4 instances
[DEBUG] Instances changed: [192.168.1.101:8080]
```

---

## 总结

1. **注册核心**
   - HTTP API 注册实例
   - 心跳保持连接（5 秒间隔）
   - 服务列表缓存（客户端）

2. **配置核心**
   - 长轮询减少请求（30 秒超时）
   - 本地缓存提高性能（快照机制）
   - 推送机制实时更新（配置变更推送）

3. **一致性核心**
   - 服务列表最终一致（定时更新 + 推送）
   - 配置版本号保证（MD5 校验）
   - 客户端缓存兜底（本地快照）

4. **扩展点**
   - `ManagerListener`：配置变更监听
   - `ServiceInfoUpdateCallback`：服务列表更新回调
   - `NamingService`：自定义注册逻辑
