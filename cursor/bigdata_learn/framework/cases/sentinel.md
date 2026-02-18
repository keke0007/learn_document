# Sentinel 源码学习案例（深入版）

## 案例概述

本案例深入 Sentinel SlotChain、规则管理、流控熔断等核心源码。**重点：断点位置、数据结构、滑动窗口统计、规则匹配机制、基于源码的扩展实验。**

---

## 📍 断点清单（建议按顺序打断点）

### SlotChain 断点
1. **`SphU.entry(String name)`** (L89) - 资源入口
2. **`CtSph.entry()`** (L124) - 上下文管理器入口
3. **`Entry.new()`** (L89) - Entry 创建
4. **`SlotChain.entry()`** (L89) - Slot 链执行
5. **`FlowSlot.entry()`** (L89) - 流控 Slot
6. **`DegradeSlot.entry()`** (L89) - 熔断 Slot

### 规则匹配断点
1. **`FlowRuleChecker.checkFlow()`** (L124) - 流控规则检查
2. **`DegradeRuleChecker.isPass()`** (L89) - 熔断规则检查
3. **`ParamFlowChecker.passCheck()`** (L124) - 热点参数检查

### 统计断点
1. **`StatisticSlot.entry()`** (L89) - 统计 Slot
2. **`ArrayMetric.addPass()`** (L89) - 通过统计
3. **`LeapArray.currentWindow()`** (L124) - 滑动窗口获取

---

## 🔍 关键数据结构

### SlotChain 核心数据结构

```java
// CtSph.java
// 1. 资源入口映射
private static final Map<String, ResourceWrapper> resourceWrapperMap = new ConcurrentHashMap<>();

// 2. Slot 链构建器
private static final SlotChainBuilder slotChainBuilder = new DefaultSlotChainBuilder();

// 3. ProcessorSlot 链
private ProcessorSlot<Object> chain;

// ProcessorSlotChain.java
// 4. Slot 列表（有序）
private AbstractLinkedProcessorSlot<?> first = new AbstractLinkedProcessorSlot<Object>() {
    @Override
    public void entry(Context context, ResourceWrapper resourceWrapper, Object param, int count, boolean prioritized, Object... args) throws Throwable {
        super.fireEntry(context, resourceWrapper, param, count, prioritized, args);
    }
};
```

### 规则管理核心数据结构

```java
// FlowRuleManager.java
// 1. 流控规则映射
private static final Map<String, List<FlowRule>> flowRules = new ConcurrentHashMap<>();

// DegradeRuleManager.java
// 2. 熔断规则映射
private static final Map<String, List<DegradeRule>> degradeRules = new ConcurrentHashMap<>();

// ParamFlowRuleManager.java
// 3. 热点规则映射
private static final Map<String, ParamFlowRule> paramFlowRules = new ConcurrentHashMap<>();

// SystemRuleManager.java
// 4. 系统规则
private static SystemRule systemRule = new SystemRule();
```

### 统计核心数据结构

```java
// StatisticNode.java
// 1. 通过 QPS 统计
private transient Metric rollingCounterInSecond;

// 2. 通过线程数统计
private transient LongAdder curThreadNum = new LongAdder();

// 3. 阻塞 QPS 统计
private transient Metric rollingCounterInSecondForBlock;

// ArrayMetric.java
// 4. 滑动窗口数组
private final LeapArray<MetricBucket> data;

// LeapArray.java
// 5. 窗口数组
protected final AtomicReferenceArray<WindowWrap<T>> array;

// 6. 窗口长度（毫秒）
protected int windowLengthInMs;

// 7. 样本数量
protected int sampleCount;
```

---

## 🧵 线程模型

### SlotChain 线程模型
- **Entry 创建**：多线程并发创建，线程安全
- **Slot 执行**：同步执行，线程安全
- **规则检查**：同步检查，线程安全

### 统计线程模型
- **滑动窗口**：使用 `AtomicReferenceArray`，线程安全
- **QPS 统计**：使用 `LongAdder`，高性能并发统计
- **规则更新**：使用 `ConcurrentHashMap`，线程安全

### 规则管理线程模型
- **规则加载**：单线程加载，线程安全
- **规则匹配**：多线程并发匹配，线程安全
- **规则更新**：使用 `ConcurrentHashMap`，线程安全

---

## 📚 源码追踪（深入版）

### 案例1：SlotChain 执行（完整流程）

**完整调用链：**
```
SphU.entry(String name) (L89)
  -> Env.sph.entry() (L124)
    -> CtSph.entry() (L89)
      -> 获取资源包装器
        -> getResourceWrapper(name)
      -> 获取上下文
        -> ContextUtil.getContext()
      -> Entry.new() (L89)
        -> 创建 Entry
          -> new Entry(resourceWrapper, chain, context)
        -> SlotChain.entry() (L89)
          -> NodeSelectorSlot.entry()      // 选择节点
            -> 选择 DefaultNode
          -> ClusterBuilderSlot.entry()    // 集群构建
            -> 构建 ClusterNode
          -> LogSlot.entry()               // 日志
            -> 记录日志
          -> StatisticSlot.entry()         // 统计
            -> 统计通过/阻塞
          -> SystemSlot.entry()            // 系统规则
            -> 检查系统负载
          -> AuthoritySlot.entry()         // 授权
            -> 检查授权规则
          -> FlowSlot.entry()              // 流控
            -> FlowRuleChecker.checkFlow()
              -> 检查流控规则
          -> DegradeSlot.entry()           // 熔断
            -> DegradeRuleChecker.isPass()
              -> 检查熔断规则
```

**Slot 执行顺序：**
1. **NodeSelectorSlot**：选择统计节点
2. **ClusterBuilderSlot**：构建集群节点
3. **LogSlot**：记录日志
4. **StatisticSlot**：统计指标
5. **SystemSlot**：系统规则检查
6. **AuthoritySlot**：授权规则检查
7. **FlowSlot**：流控规则检查
8. **DegradeSlot**：熔断规则检查

**关键类：**
- `SphU`：入口工具类
- `CtSph`：上下文管理器
- `SlotChain`：Slot 链
- `Entry`：入口对象

**验证代码：** `scripts/SentinelResourceTrace.java`
**验证数据：** `data/sentinel-rules.json`

---

### 案例2：流控规则（深入算法）

**流控算法详细机制：**

**1. QPS 流控**
```java
// FlowRuleChecker.checkFlow()
public static boolean checkFlow(ResourceWrapper resource, Context context, DefaultNode node, int count, boolean prioritized) {
    // 1. 获取流控规则
    List<FlowRule> rules = FlowRuleManager.getFlowRule(resource.getName());
    
    // 2. 遍历规则
    for (FlowRule rule : rules) {
        // 3. 检查规则
        if (!canPassCheck(rule, context, node, count, prioritized)) {
            return false;
        }
    }
    return true;
}

// canPassCheck()
private static boolean canPassCheck(FlowRule rule, Context context, DefaultNode node, int count, boolean prioritized) {
    // 1. 获取统计节点
    Node selectedNode = selectNodeByRequesterAndStrategy(rule, context, node);
    
    // 2. 获取当前 QPS
    int curCount = avgUsedTokens(selectedNode, rule);
    
    // 3. 检查是否超过阈值
    if (curCount + count > rule.getCount()) {
        return false;
    }
    return true;
}
```

**2. 并发线程数流控**
```java
// FlowRuleChecker.checkFlow()
if (rule.getGrade() == FlowRuleConstant.FLOW_GRADE_THREAD) {
    // 1. 获取当前线程数
    int curThreadNum = node.curThreadNum();
    
    // 2. 检查是否超过阈值
    if (curThreadNum + count > rule.getCount()) {
        return false;
    }
}
```

**3. 关联流控**
```java
// FlowRuleChecker.checkFlow()
if (rule.getStrategy() == FlowRuleConstant.STRATEGY_RELATE) {
    // 1. 获取关联资源
    String refResource = rule.getRefResource();
    
    // 2. 获取关联资源节点
    Node refNode = ClusterBuilderSlot.getClusterNode(refResource);
    
    // 3. 检查关联资源 QPS
    int refQps = avgUsedTokens(refNode, rule);
    if (refQps > rule.getCount()) {
        return false;
    }
}
```

**4. 链路流控**
```java
// FlowRuleChecker.checkFlow()
if (rule.getStrategy() == FlowRuleConstant.STRATEGY_CHAIN) {
    // 1. 获取入口资源
    String entranceResource = rule.getRefResource();
    
    // 2. 获取入口节点
    DefaultNode entranceNode = (DefaultNode) context.getEntranceNode();
    
    // 3. 检查入口链路 QPS
    int entranceQps = avgUsedTokens(entranceNode, rule);
    if (entranceQps > rule.getCount()) {
        return false;
    }
}
```

**滑动窗口统计：**
```java
// ArrayMetric.addPass()
public void addPass(int count) {
    // 1. 获取当前窗口
    WindowWrap<MetricBucket> wrap = data.currentWindow();
    
    // 2. 增加通过数
    wrap.value().addPass(count);
}

// LeapArray.currentWindow()
public WindowWrap<T> currentWindow() {
    // 1. 计算当前时间戳
    long time = TimeUtil.currentTimeMillis();
    
    // 2. 计算窗口索引
    int idx = calculateTimeIdx(time);
    
    // 3. 计算窗口开始时间
    long windowStart = calculateWindowStart(time);
    
    // 4. 获取或创建窗口
    while (true) {
        WindowWrap<T> old = array.get(idx);
        if (old == null) {
            WindowWrap<T> window = new WindowWrap<T>(windowLengthInMs, windowStart, newEmptyBucket(time));
            if (array.compareAndSet(idx, null, window)) {
                return window;
            }
        } else if (windowStart == old.windowStart()) {
            return old;
        } else if (windowStart > old.windowStart()) {
            if (updateLock.tryLock()) {
                try {
                    return resetWindowTo(old, windowStart);
                } finally {
                    updateLock.unlock();
                }
            }
        } else if (windowStart < old.windowStart()) {
            return new WindowWrap<T>(windowLengthInMs, windowStart, newEmptyBucket(time));
        }
    }
}
```

---

### 案例3：熔断规则（深入状态机）

**熔断策略详细机制：**

**1. 慢调用比例**
```java
// DegradeRuleChecker.isPass()
if (rule.getGrade() == RuleConstant.DEGRADE_GRADE_RT) {
    // 1. 获取平均响应时间
    double rt = clusterNode.avgRt();
    
    // 2. 检查是否超过阈值
    if (rt < rule.getCount()) {
        // 3. 重置熔断状态
        pass.set(true);
        return pass.get();
    }
    
    // 4. 检查慢调用比例
    double slowRequestRatio = clusterNode.getSlowRequestQps() / clusterNode.totalQps();
    if (slowRequestRatio > rule.getSlowRatioThreshold()) {
        // 5. 触发熔断
        return false;
    }
}
```

**2. 异常比例**
```java
// DegradeRuleChecker.isPass()
if (rule.getGrade() == RuleConstant.DEGRADE_GRADE_EXCEPTION_RATIO) {
    // 1. 获取异常比例
    double exceptionRatio = clusterNode.exceptionQps() / clusterNode.totalQps();
    
    // 2. 检查是否超过阈值
    if (exceptionRatio > rule.getCount()) {
        // 3. 触发熔断
        return false;
    }
}
```

**3. 异常数**
```java
// DegradeRuleChecker.isPass()
if (rule.getGrade() == RuleConstant.DEGRADE_GRADE_EXCEPTION_COUNT) {
    // 1. 获取异常数
    double exceptionCount = clusterNode.totalException();
    
    // 2. 检查是否超过阈值
    if (exceptionCount > rule.getCount()) {
        // 3. 触发熔断
        return false;
    }
}
```

**熔断状态机：**
```java
// CircuitBreaker.java
public enum State {
    CLOSED,    // 关闭状态（正常）
    OPEN,      // 开启状态（熔断）
    HALF_OPEN  // 半开状态（探测）
}

// DegradeRule.java
private volatile State currentState = State.CLOSED;
private volatile long nextRetryTimestamp;

// 状态转换
// CLOSED -> OPEN: 触发熔断条件
// OPEN -> HALF_OPEN: 达到重试时间
// HALF_OPEN -> CLOSED: 探测成功
// HALF_OPEN -> OPEN: 探测失败
```

---

## 🧪 基于源码扩展实验

### 实验1：自定义 Slot（自定义限流逻辑）

**目标**：创建自定义 Slot，实现自定义限流逻辑。

**实现：**
```java
@Component
public class CustomSlot extends AbstractLinkedProcessorSlot<DefaultNode> {
    @Override
    public void entry(Context context, ResourceWrapper resourceWrapper, DefaultNode node, int count, boolean prioritized, Object... args) throws Throwable {
        // 1. 自定义限流逻辑
        String resourceName = resourceWrapper.getName();
        if (shouldBlock(resourceName)) {
            throw new BlockException("Custom block");
        }
        
        // 2. 调用下一个 Slot
        fireEntry(context, resourceWrapper, node, count, prioritized, args);
    }
    
    @Override
    public void exit(Context context, ResourceWrapper resourceWrapper, int count, Object... args) {
        // 退出处理
        fireExit(context, resourceWrapper, count, args);
    }
    
    private boolean shouldBlock(String resourceName) {
        // 自定义限流逻辑
        return false;
    }
}

// 注册自定义 Slot
@Configuration
public class SentinelConfig {
    @PostConstruct
    public void init() {
        SlotChainBuilder builder = new DefaultSlotChainBuilder();
        // 添加自定义 Slot（需要在 FlowSlot 之前）
        builder.addLast(new CustomSlot());
    }
}
```

**验证**：发送请求，观察自定义限流逻辑是否生效。

---

### 实验2：自定义 FlowRule（动态规则）

**目标**：动态添加/删除流控规则。

**实现：**
```java
@Component
public class DynamicRuleManager {
    public void addFlowRule(String resource, int qps) {
        // 1. 创建流控规则
        FlowRule rule = new FlowRule();
        rule.setResource(resource);
        rule.setGrade(RuleConstant.FLOW_GRADE_QPS);
        rule.setCount(qps);
        
        // 2. 加载规则
        List<FlowRule> rules = new ArrayList<>();
        rules.add(rule);
        FlowRuleManager.loadRules(rules);
    }
    
    public void removeFlowRule(String resource) {
        // 1. 获取现有规则
        List<FlowRule> rules = FlowRuleManager.getFlowRule(resource);
        
        // 2. 移除规则
        rules.clear();
        FlowRuleManager.loadRules(rules);
    }
}
```

**验证**：动态添加/删除规则，观察限流效果。

---

### 实验3：自定义 StatisticSlot（自定义统计）

**目标**：扩展统计 Slot，记录自定义指标。

**实现：**
```java
@Component
public class CustomStatisticSlot extends StatisticSlot {
    @Override
    public void entry(Context context, ResourceWrapper resourceWrapper, DefaultNode node, int count, boolean prioritized, Object... args) throws Throwable {
        // 1. 调用父类统计
        super.entry(context, resourceWrapper, node, count, prioritized, args);
        
        // 2. 自定义统计
        recordCustomMetric(resourceWrapper.getName(), count);
    }
    
    private void recordCustomMetric(String resource, int count) {
        // 记录自定义指标（如：发送到监控系统）
        System.out.println("Custom metric: " + resource + " - " + count);
    }
}
```

**验证**：发送请求，观察自定义统计是否记录。

---

## 🐛 常见坑与排查

### 坑1：限流不生效
**现象**：配置了流控规则，但未限流
**原因**：
1. 资源名不匹配
2. 规则未加载
3. Slot 链未正确构建
**排查**：
1. 检查资源名是否一致
2. 检查规则是否加载：`FlowRuleManager.getFlowRule()`
3. 检查 Slot 链构建

### 坑2：熔断不恢复
**现象**：熔断后一直不恢复
**原因**：
1. 重试时间未设置
2. 探测请求失败
3. 状态机转换错误
**排查**：
1. 检查 `timeWindow` 配置
2. 检查探测请求是否成功
3. 检查状态机转换逻辑

### 坑3：统计不准确
**现象**：统计指标不准确
**原因**：
1. 滑动窗口配置错误
2. 时间窗口未对齐
3. 并发统计问题
**排查**：
1. 检查窗口长度和样本数
2. 检查时间对齐
3. 检查并发统计逻辑

---

## 验证数据

### 流控日志

```
[INFO] Flow rule triggered: resource=userService, qps=100, threshold=50
[WARN] Blocked by flow control: resource=userService
[DEBUG] FlowSlot.checkFlow: resource=userService, currentQps=100, threshold=50
```

### 熔断日志

```
[INFO] Circuit breaker opened: resource=userService, strategy=slow_ratio
[INFO] Circuit breaker half-open: resource=userService
[INFO] Circuit breaker closed: resource=userService
[DEBUG] DegradeSlot.checkDegrade: resource=userService, state=OPEN
```

### 统计日志

```
[DEBUG] StatisticSlot.entry: resource=userService
[DEBUG] ArrayMetric.addPass: resource=userService, count=1
[DEBUG] LeapArray.currentWindow: resource=userService, windowStart=1640000000000
```

---

## 总结

1. **SlotChain 核心**
   - 责任链模式（8 个 Slot 有序执行）
   - 每个 Slot 负责不同功能（统计/流控/熔断）
   - 可扩展 Slot（自定义 Slot）

2. **规则核心**
   - 规则动态加载（`FlowRuleManager.loadRules()`）
   - 规则匹配资源（资源名匹配）
   - 规则实时生效（立即生效）

3. **统计核心**
   - 滑动窗口统计（`LeapArray`）
   - 多维度指标（QPS/线程数/响应时间）
   - 高性能设计（`LongAdder`/`AtomicReferenceArray`）

4. **扩展点**
   - `AbstractLinkedProcessorSlot`：自定义 Slot
   - `FlowRuleManager`：动态规则管理
   - `StatisticSlot`：自定义统计
