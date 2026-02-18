# Spring 源码学习案例（深入版）

## 案例概述

本案例深入 Spring 核心源码，包括 IOC 容器、AOP、事务等关键机制的源码追踪与验证。**重点：断点位置、数据结构、线程模型、常见坑定位、基于源码的扩展实验。**

---

## 📍 断点清单（建议按顺序打断点）

### IOC 容器断点
1. **`AbstractApplicationContext.refresh()`** (L516) - 容器刷新入口
2. **`DefaultListableBeanFactory.getBean(String name)`** (L230) - Bean 获取入口
3. **`AbstractAutowireCapableBeanFactory.doCreateBean()`** (L564) - Bean 创建核心
4. **`AbstractAutowireCapableBeanFactory.createBeanInstance()`** (L1178) - 实例化
5. **`AbstractAutowireCapableBeanFactory.populateBean()`** (L1344) - 属性填充
6. **`AbstractAutowireCapableBeanFactory.initializeBean()`** (L1703) - 初始化

### AOP 断点
1. **`AbstractAutoProxyCreator.postProcessAfterInitialization()`** (L319) - 代理创建入口
2. **`AbstractAutoProxyCreator.wrapIfNecessary()`** (L378) - 判断是否需要代理
3. **`DefaultAopProxyFactory.createAopProxy()`** (L58) - 代理工厂选择
4. **`JdkDynamicAopProxy.invoke()`** (L185) - JDK 代理执行
5. **`CglibAopProxy.intercept()`** (L652) - CGLIB 代理执行

### 事务断点
1. **`TransactionInterceptor.invoke()`** (L118) - 事务拦截入口
2. **`TransactionAspectSupport.invokeWithinTransaction()`** (L366) - 事务执行
3. **`AbstractPlatformTransactionManager.getTransaction()`** (L370) - 获取事务
4. **`AbstractPlatformTransactionManager.handleExistingTransaction()`** (L475) - 处理已有事务

---

## 🔍 关键数据结构

### IOC 容器核心数据结构

```java
// DefaultListableBeanFactory.java
// 1. BeanDefinition 注册表（核心）
private final Map<String, BeanDefinition> beanDefinitionMap = new ConcurrentHashMap<>(256);

// 2. 单例 Bean 缓存（三级缓存）
private final Map<String, Object> singletonObjects = new ConcurrentHashMap<>(256);  // 一级：完整 Bean
private final Map<String, Object> earlySingletonObjects = new HashMap<>(16);          // 二级：早期引用
private final Map<String, ObjectFactory<?>> singletonFactories = new HashMap<>(16);   // 三级：工厂

// 3. BeanPostProcessor 列表（有序）
private final List<BeanPostProcessor> beanPostProcessors = new CopyOnWriteArrayList<>();

// 4. 依赖关系映射（用于循环依赖检测）
private final Map<String, Set<String>> dependentBeanMap = new ConcurrentHashMap<>(64);
private final Map<String, Set<String>> dependenciesForBeanMap = new ConcurrentHashMap<>(64);
```

### AOP 核心数据结构

```java
// AbstractAdvisorAutoProxyCreator.java
// 1. Advisor 缓存（避免重复计算）
private final Map<Object, Boolean> advisedBeans = new ConcurrentHashMap<>(256);

// 2. 代理工厂缓存
private final Map<Object, ProxyFactory> proxyFactoryCache = new ConcurrentHashMap<>(256);

// ProxyFactory.java
// 3. Advisor 链（有序）
private List<Advisor> advisors = new ArrayList<>();

// 4. 目标源
private TargetSource targetSource;
```

### 事务核心数据结构

```java
// AbstractPlatformTransactionManager.java
// 1. 事务同步器（ThreadLocal）
private static final ThreadLocal<Map<Object, Object>> resources = new NamedThreadLocal<>("transactional resources");

// TransactionAspectSupport.java
// 2. 事务属性缓存
private final Map<Object, TransactionAttribute> attributeCache = new ConcurrentHashMap<>(1024);

// DataSourceTransactionManager.java
// 3. 连接持有者（ThreadLocal）
private static final ThreadLocal<Map<DataSource, ConnectionHolder>> connectionHolders = new NamedThreadLocal<>("Connection holders");
```

---

## 🧵 线程模型

### IOC 容器线程模型
- **单线程启动**：`refresh()` 在主线程执行，线程安全由 `ConcurrentHashMap` 保证
- **Bean 创建**：单例 Bean 创建是同步的（`synchronized`），原型 Bean 可并发
- **循环依赖检测**：使用 `ThreadLocal` 记录当前创建中的 Bean

### AOP 代理线程模型
- **代理创建**：在 Bean 初始化后单线程创建
- **代理调用**：多线程并发调用，由 `ConcurrentHashMap` 缓存保证线程安全

### 事务线程模型
- **事务上下文**：使用 `ThreadLocal` 存储，每个线程独立
- **连接管理**：每个线程持有独立的数据库连接
- **同步器**：`TransactionSynchronizationManager` 使用 `ThreadLocal`

---

## 📚 源码追踪（深入版）

### 案例1：IOC 容器启动流程（完整 refresh() 12 步）

**完整调用链：**
```
AbstractApplicationContext.refresh() (L516)
  ├─ 1. prepareRefresh()                    // 准备刷新：设置启动时间、激活状态
  ├─ 2. obtainFreshBeanFactory()            // 获取 BeanFactory
  │     └─ refreshBeanFactory()
  │         └─ loadBeanDefinitions()        // 加载 BeanDefinition
  ├─ 3. prepareBeanFactory(beanFactory)     // 准备 BeanFactory：添加后处理器、注册环境 Bean
  ├─ 4. postProcessBeanFactory(beanFactory) // 后处理 BeanFactory（子类扩展点）
  ├─ 5. invokeBeanFactoryPostProcessors()   // 【关键】执行 BeanFactoryPostProcessor
  │     └─ PostProcessorRegistrationDelegate.invokeBeanFactoryPostProcessors()
  │         ├─ 先执行 BeanDefinitionRegistryPostProcessor
  │         │   └─ ConfigurationClassPostProcessor.postProcessBeanDefinitionRegistry()
  │         │       └─ processConfigBeanDefinitions()  // 解析 @Configuration/@Component
  │         └─ 再执行 BeanFactoryPostProcessor
  ├─ 6. registerBeanPostProcessors()         // 【关键】注册 BeanPostProcessor
  │     └─ PostProcessorRegistrationDelegate.registerBeanPostProcessors()
  │         └─ 按优先级排序：PriorityOrdered -> Ordered -> 普通
  ├─ 7. initMessageSource()                 // 初始化消息源
  ├─ 8. initApplicationEventMulticaster()   // 初始化事件广播器
  ├─ 9. onRefresh()                         // 子类扩展点（如启动 Web 容器）
  ├─ 10. registerListeners()                // 注册监听器
  ├─ 11. finishBeanFactoryInitialization()  // 【关键】初始化所有单例 Bean
  │      └─ DefaultListableBeanFactory.preInstantiateSingletons()
  │          └─ getBean(beanName)
  │              └─ doGetBean()
  │                  ├─ getSingleton()       // 从缓存获取
  │                  └─ createBean()        // 创建 Bean
  │                      └─ doCreateBean()
  │                          ├─ createBeanInstance()  // 实例化
  │                          ├─ populateBean()        // 属性填充
  │                          └─ initializeBean()      // 初始化
  └─ 12. finishRefresh()                    // 完成刷新：发布 ContextRefreshedEvent
```

**关键源码位置：**
- `AbstractApplicationContext.refresh()` - `spring-context-5.3.x.jar`
- `DefaultListableBeanFactory.getBean()` - `spring-beans-5.3.x.jar`
- `AbstractAutowireCapableBeanFactory.doCreateBean()` - `spring-beans-5.3.x.jar`

**验证代码：** `scripts/SpringIocTrace.java`

---

### 案例2：循环依赖三级缓存（深入机制）

**三级缓存详细机制：**

```java
// DefaultSingletonBeanRegistry.java
// 一级缓存：完整 Bean（已初始化）
private final Map<String, Object> singletonObjects = new ConcurrentHashMap<>(256);

// 二级缓存：早期引用（已实例化但未初始化）
private final Map<String, Object> earlySingletonObjects = new HashMap<>(16);

// 三级缓存：ObjectFactory（延迟创建代理）
private final Map<String, ObjectFactory<?>> singletonFactories = new HashMap<>(16);
```

**完整解决流程（带源码位置）：**

1. **A 实例化** (`doCreateBean()` L564)
   ```java
   // AbstractAutowireCapableBeanFactory.doCreateBean()
   instanceWrapper = createBeanInstance(beanName, mbd, args);  // 实例化
   ```

2. **放入三级缓存** (`doCreateBean()` L584)
   ```java
   // 如果允许早期暴露（单例 + 允许循环依赖）
   if (earlySingletonExposure) {
       addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
       // 这里放入的是 ObjectFactory，延迟执行 getEarlyBeanReference
   }
   ```

3. **A 属性填充** (`populateBean()` L1344)
   ```java
   // 需要注入 B，触发 B 的创建
   applyPropertyValues(beanName, mbd, bw, pvs);
   ```

4. **B 实例化** -> **B 属性填充需要 A**
   ```java
   // B 在 populateBean 时发现需要 A
   // 调用 getBean("serviceA")
   ```

5. **从三级缓存获取 A 的早期引用** (`getSingleton()` L181)
   ```java
   // DefaultSingletonBeanRegistry.getSingleton()
   ObjectFactory<?> singletonFactory = this.singletonFactories.get(beanName);
   if (singletonFactory != null) {
       singletonObject = singletonFactory.getObject();  // 调用 getEarlyBeanReference
       this.earlySingletonObjects.put(beanName, singletonObject);
       this.singletonFactories.remove(beanName);
   }
   ```

6. **B 初始化完成** -> **放入一级缓存**
   ```java
   // addSingleton() 放入一级缓存，清除二级缓存
   this.singletonObjects.put(beanName, singletonObject);
   this.earlySingletonObjects.remove(beanName);
   ```

7. **A 继续属性填充** -> **从一级缓存获取 B**
8. **A 初始化完成** -> **放入一级缓存**

**为什么需要三级缓存？**
- **一级缓存**：完整 Bean，可直接使用
- **二级缓存**：早期引用，避免重复创建代理
- **三级缓存**：ObjectFactory，延迟创建代理（如果 A 需要 AOP，此时创建代理）

**常见坑：**
- **构造器循环依赖无法解决**：因为实例化前无法放入三级缓存
- **原型 Bean 循环依赖会报错**：原型 Bean 不支持循环依赖

**验证数据：**
```java
// 循环依赖示例
@Service
public class ServiceA {
    @Autowired
    private ServiceB serviceB;
}

@Service
public class ServiceB {
    @Autowired
    private ServiceA serviceA;
}
```

---

### 案例3：AOP 代理创建（深入机制）

**完整调用链：**
```
AbstractAutoProxyCreator.postProcessAfterInitialization() (L319)
  -> wrapIfNecessary() (L378)
    -> getAdvicesAndAdvisorsForBean() (L95)  // 获取 Advisor
    -> createProxy() (L483)
      -> ProxyFactory.getProxy() (L187)
        -> DefaultAopProxyFactory.createAopProxy() (L58)
          -> 判断是否需要接口
            ├─ 有接口 -> JdkDynamicAopProxy
            └─ 无接口 -> CglibAopProxy
```

**代理选择逻辑：**
```java
// DefaultAopProxyFactory.createAopProxy()
if (config.isOptimize() || config.isProxyTargetClass() || hasNoUserSuppliedProxyInterfaces(config)) {
    Class<?> targetClass = config.getTargetClass();
    if (targetClass.isInterface() || Proxy.isProxyClass(targetClass)) {
        return new JdkDynamicAopProxy(config);
    }
    return new ObjenesisCglibAopProxy(config);
} else {
    return new JdkDynamicAopProxy(config);
}
```

**JDK 动态代理执行链：**
```java
// JdkDynamicAopProxy.invoke() (L185)
public Object invoke(Object proxy, Method method, Object[] args) {
    // 1. 获取拦截器链
    List<Object> chain = this.advised.getInterceptorsAndDynamicInterceptionAdvice(method, targetClass);
    
    // 2. 如果没有拦截器，直接调用目标方法
    if (chain.isEmpty()) {
        return method.invoke(target, args);
    }
    
    // 3. 创建 MethodInvocation，执行拦截器链
    MethodInvocation invocation = new ReflectiveMethodInvocation(proxy, target, method, args, targetClass, chain);
    return invocation.proceed();
}
```

**CGLIB 代理执行链：**
```java
// CglibAopProxy.intercept() (L652)
public Object intercept(Object proxy, Method method, Object[] args, MethodProxy methodProxy) {
    // 1. 获取拦截器链
    List<Object> chain = this.advised.getInterceptorsAndDynamicInterceptionAdvice(method, targetClass);
    
    // 2. 创建 CglibMethodInvocation，执行拦截器链
    CglibMethodInvocation invocation = new CglibMethodInvocation(proxy, target, method, args, targetClass, chain, methodProxy);
    return invocation.proceed();
}
```

**验证代码：** `scripts/SpringAopTxTrace.java`

---

### 案例4：事务拦截器（深入传播机制）

**完整调用链：**
```
@Transactional 方法调用
  -> TransactionInterceptor.invoke() (L118)
    -> TransactionAspectSupport.invokeWithinTransaction() (L366)
      -> PlatformTransactionManager.getTransaction() (L370)
        -> AbstractPlatformTransactionManager.getTransaction()
          -> doGetTransaction()              // 获取事务对象
          -> isExistingTransaction()        // 判断是否已有事务
          -> handleExistingTransaction()     // 【关键】处理传播行为
            ├─ PROPAGATION_REQUIRED        // 存在则加入，不存在则新建
            ├─ PROPAGATION_REQUIRES_NEW    // 总是新建事务
            ├─ PROPAGATION_NESTED          // 嵌套事务（保存点）
            └─ PROPAGATION_SUPPORTS        // 存在则加入，不存在则非事务
      -> 执行业务方法
      -> commitTransactionAfterReturning()  // 提交事务
      -> completeTransactionAfterThrowing() // 回滚事务
```

**传播行为源码实现：**
```java
// AbstractPlatformTransactionManager.handleExistingTransaction()
private TransactionStatus handleExistingTransaction(TransactionDefinition definition, Object transaction, boolean debug) {
    if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_NEVER) {
        throw new IllegalTransactionStateException("Existing transaction found for transaction marked with propagation 'never'");
    }
    
    if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_NOT_SUPPORTED) {
        // 挂起当前事务
        Object suspendedResources = suspend(transaction);
        return prepareTransactionStatus(definition, null, false, false, suspendedResources, null);
    }
    
    if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_REQUIRES_NEW) {
        // 挂起当前事务，创建新事务
        Object suspendedResources = suspend(transaction);
        return startTransaction(definition, transaction, true, debug, suspendedResources);
    }
    
    if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_NESTED) {
        // 创建保存点
        if (isNestedTransactionAllowed()) {
            Object savepoint = createSavepoint(transaction);
            return prepareTransactionStatus(definition, transaction, false, false, null, savepoint);
        }
    }
    
    // PROPAGATION_REQUIRED, PROPAGATION_SUPPORTS, PROPAGATION_MANDATORY
    return prepareTransactionStatus(definition, transaction, false, false, null, null);
}
```

**常见坑：**
- **REQUIRES_NEW 会挂起外层事务**：内层事务提交后，外层事务回滚不影响内层
- **NESTED 使用保存点**：内层回滚不影响外层，但需要数据库支持保存点
- **@Transactional 在同类方法调用失效**：因为走的是 this，不是代理

**验证数据：**
```java
@Transactional(propagation = Propagation.REQUIRED)
public void methodA() {
    // 业务逻辑
    methodB();  // 同类调用，@Transactional 失效！
}

@Transactional(propagation = Propagation.REQUIRES_NEW)
public void methodB() {
    // 业务逻辑
}
```

---

## 🧪 基于源码扩展实验

### 实验1：自定义 BeanPostProcessor（修改 Bean 属性）

**目标**：在 Bean 初始化后，自动给所有 String 类型属性添加前缀。

**实现：**
```java
@Component
public class CustomBeanPostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        // 使用反射修改 String 属性
        Field[] fields = bean.getClass().getDeclaredFields();
        for (Field field : fields) {
            if (field.getType() == String.class) {
                field.setAccessible(true);
                try {
                    String value = (String) field.get(bean);
                    if (value != null && !value.startsWith("[CUSTOM]")) {
                        field.set(bean, "[CUSTOM]" + value);
                    }
                } catch (IllegalAccessException e) {
                    // 忽略
                }
            }
        }
        return bean;
    }
}
```

**验证**：创建测试 Bean，观察属性值是否被修改。

---

### 实验2：自定义 Condition（条件装配）

**目标**：根据环境变量决定是否创建某个 Bean。

**实现：**
```java
// 自定义 Condition
public class CustomCondition implements Condition {
    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        Environment env = context.getEnvironment();
        String feature = env.getProperty("feature.enabled");
        return "true".equals(feature);
    }
}

// 使用 Condition
@Configuration
public class CustomConfiguration {
    @Bean
    @Conditional(CustomCondition.class)
    public MyService myService() {
        return new MyService();
    }
}
```

**验证**：设置 `feature.enabled=true`，观察 Bean 是否创建。

---

### 实验3：自定义 AOP Advisor（方法拦截）

**目标**：拦截所有 Controller 方法，记录执行时间。

**实现：**
```java
@Component
@Aspect
public class PerformanceAspect {
    @Around("@within(org.springframework.web.bind.annotation.RestController)")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long duration = System.currentTimeMillis() - start;
        System.out.println(joinPoint.getSignature() + " executed in " + duration + "ms");
        return result;
    }
}
```

**验证**：调用 Controller 方法，观察日志输出。

---

## 🐛 常见坑与排查

### 坑1：循环依赖报错
**现象**：`BeanCurrentlyInCreationException`
**原因**：构造器循环依赖或原型 Bean 循环依赖
**排查**：
1. 检查是否有构造器注入的循环依赖
2. 检查是否有原型 Bean 的循环依赖
3. 使用 `@Lazy` 延迟注入

### 坑2：@Transactional 失效
**现象**：事务不生效
**原因**：
1. 同类方法调用（走 this，不是代理）
2. 方法不是 public
3. 异常被捕获
**排查**：
1. 检查是否同类调用
2. 检查方法可见性
3. 检查异常处理

### 坑3：AOP 代理不生效
**现象**：切面不执行
**原因**：
1. Bean 没有被 Spring 管理
2. 切点表达式错误
3. 代理类型选择错误
**排查**：
1. 检查 Bean 是否被扫描
2. 检查切点表达式
3. 检查是否需要强制 CGLIB

---

## 验证数据

### Bean 生命周期日志

```
[DEBUG] Creating instance of bean 'userService'
[DEBUG] Eagerly caching bean 'userService' to allow for resolving potential circular references
[DEBUG] Finished creating instance of bean 'userService'
[DEBUG] Invoking afterPropertiesSet() on bean 'userService'
[DEBUG] Initialized bean 'userService'
```

### AOP 代理日志

```
[DEBUG] Creating JDK dynamic proxy for [com.example.UserService]
[DEBUG] JDK dynamic proxy created for [com.example.UserService]
[DEBUG] Invoking method: getUserById with args: [1]
[DEBUG] Before advice executed
[DEBUG] After advice executed
```

---

## 总结

1. **IOC 核心**
   - BeanDefinition 是元数据，Bean 是实例
   - 三级缓存解决循环依赖（单例 + 属性注入）
   - BeanPostProcessor 是扩展点（初始化前后）

2. **AOP 核心**
   - 代理在初始化后创建（`postProcessAfterInitialization`）
   - JDK/CGLIB 选择策略（接口 vs 类）
   - 拦截器链执行（责任链模式）

3. **事务核心**
   - 拦截器链中的一环（AOP 实现）
   - 传播行为决定事务边界（`handleExistingTransaction`）
   - 回滚规则决定异常处理（`completeTransactionAfterThrowing`）

4. **扩展点**
   - `BeanPostProcessor`：修改 Bean
   - `BeanFactoryPostProcessor`：修改 BeanDefinition
   - `@Conditional`：条件装配
   - `@Aspect`：AOP 切面
