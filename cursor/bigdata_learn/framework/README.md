# 框架源码学习知识点总览（深入版）

## 📚 快速导航

- **Spring**：`cases/spring.md` - IOC/AOP/事务（断点+数据结构+扩展实验）
- **Spring Boot**：`cases/springboot.md` - 启动/自动配置（断点+条件评估+扩展实验）
- **MyBatis**：`cases/mybatis.md` - Mapper/执行链/插件（断点+执行链+扩展实验）
- **Spring Cloud Gateway**：`cases/springcloud_gateway.md` - 路由/过滤器/Netty（断点+线程模型+扩展实验）
- **OpenFeign**：`cases/openfeign.md` - 代理/请求构建/调用链（断点+负载均衡+扩展实验）
- **Nacos**：`cases/nacos.md` - 注册发现/配置中心（断点+长轮询+扩展实验）
- **Sentinel**：`cases/sentinel.md` - SlotChain/规则/统计（断点+滑动窗口+扩展实验）
- **Seata**：`cases/seata.md` - AT 模式/全局事务（断点+undo_log+扩展实验）
- **XXL-JOB**：`cases/xxl-job.md` - 调度/执行器/路由（断点+路由策略+扩展实验）

---

## 1) Spring（IOC / AOP / Tx）

### 📍 关键断点
1. `AbstractApplicationContext.refresh()` (L516) - 容器刷新入口
2. `DefaultListableBeanFactory.getBean()` (L230) - Bean 获取
3. `AbstractAutowireCapableBeanFactory.doCreateBean()` (L564) - Bean 创建核心
4. `AbstractAutoProxyCreator.postProcessAfterInitialization()` (L319) - AOP 代理创建
5. `TransactionInterceptor.invoke()` (L118) - 事务拦截

### 🔍 关键数据结构
- **三级缓存**：`singletonObjects`（一级）、`earlySingletonObjects`（二级）、`singletonFactories`（三级）
- **BeanDefinition 映射**：`beanDefinitionMap`（ConcurrentHashMap）
- **BeanPostProcessor 列表**：`beanPostProcessors`（CopyOnWriteArrayList）

### 🧵 线程模型
- **单线程启动**：`refresh()` 在主线程执行
- **Bean 创建**：单例 Bean 创建是同步的（`synchronized`）
- **循环依赖检测**：使用 `ThreadLocal` 记录当前创建中的 Bean

### 📚 IOC 主链路
- **BeanDefinition**：解析来源（XML/注解/扫描）-> 注册表
- **实例化**：构造器选择、循环依赖三级缓存
- **属性填充**：`populateBean`、`AutowiredAnnotationBeanPostProcessor`
- **初始化**：`Aware`、`@PostConstruct`、`InitializingBean`、init-method
- **销毁**：`DisposableBean`、destroy-method、`@PreDestroy`

### 📚 扩展点优先级
- `BeanFactoryPostProcessor` / `BeanDefinitionRegistryPostProcessor`（修改 BeanDefinition）
- `BeanPostProcessor`（AOP/事务/Autowired 都在这里发生）
- `ApplicationListener` / 事件发布 `ApplicationEventMulticaster`

### 📚 AOP
- **代理选择**：JDK vs CGLIB（`DefaultAopProxyFactory.createAopProxy()`）
- **代理链构造**：`ProxyFactory`、`AdvisedSupport`
- **拦截器执行**：`JdkDynamicAopProxy.invoke()` / `CglibAopProxy.intercept()`

### 📚 事务
- **注解解析**：`AnnotationTransactionAttributeSource`
- **拦截器**：`TransactionInterceptor` -> `PlatformTransactionManager`
- **核心语义**：传播（REQUIRED/REQUIRES_NEW/...）、隔离、只读、回滚规则

### 🧪 扩展实验
- **自定义 BeanPostProcessor**：修改 Bean 属性（见 `scripts/SpringIocTrace.java`）
- **自定义 Condition**：条件装配（见 `cases/spring.md`）
- **自定义 AOP Advisor**：方法拦截（见 `scripts/SpringAopTxTrace.java`）

### 🐛 常见坑
- **循环依赖**：构造器循环依赖无法解决
- **@Transactional 失效**：同类方法调用、方法不是 public、异常被捕获
- **AOP 代理不生效**：Bean 未被 Spring 管理、切点表达式错误

示例代码：`scripts/SpringIocTrace.java`、`scripts/SpringAopTxTrace.java`
验证日志：`data/spring-refresh-trace.log`

---

## 2) Spring Boot（启动/自动配置/配置绑定）

### 📍 关键断点
1. `SpringApplication.run()` (L297) - 启动入口
2. `AutoConfigurationImportSelector.selectImports()` (L108) - 自动配置选择
3. `OnClassCondition.getMatchOutcome()` (L64) - 类路径条件评估
4. `ConfigurationPropertiesBindingPostProcessor.postProcessBeforeInitialization()` (L89) - 配置绑定

### 🔍 关键数据结构
- **自动配置类缓存**：`cache`（ConcurrentReferenceHashMap）
- **条件评估结果缓存**：`conditionOutcomesCache`（HashMap）
- **配置源列表**：`sources`（List<ConfigurationPropertySource>）

### 🧵 线程模型
- **单线程启动**：`run()` 在主线程执行
- **条件评估**：启动时单线程评估，结果缓存
- **配置绑定**：Bean 初始化时单线程绑定

### 📚 启动
- `SpringApplication.run`：推断 `WebApplicationType`、创建/刷新 `ApplicationContext`
- `SpringFactoriesLoader`：读取自动配置/监听器（`META-INF/spring.factories`）

### 📚 自动装配
- `@EnableAutoConfiguration` / `AutoConfigurationImportSelector`
- **条件装配**：`@ConditionalOnClass/@ConditionalOnMissingBean/@ConditionalOnProperty`
- **条件评估流程**：`OnClassCondition` -> `OnBeanCondition` -> `OnPropertyCondition`

### 📚 配置体系
- `Environment` / `PropertySource`
- `@ConfigurationProperties` 绑定与校验（`Binder.bind()`）

### 📚 Starter 设计
- `xxx-spring-boot-starter`（依赖聚合）
- `xxx-spring-boot-autoconfigure`（自动配置与属性）

### 🧪 扩展实验
- **自定义 Starter**：完整实现（见 `cases/springboot.md`）
- **自定义 Condition**：环境条件（见 `cases/springboot.md`）
- **自定义 ApplicationListener**：启动监听（见 `cases/springboot.md`）

### 🐛 常见坑
- **自动配置不生效**：spring.factories 路径错误、条件不满足
- **配置绑定失败**：前缀不匹配、属性名不匹配、类型转换失败

验证配置：`data/application-sample.yml`

---

## 3) MyBatis（Mapper 代理 / 执行链 / 插件）

### 📍 关键断点
1. `SqlSession.getMapper()` (L56) - Mapper 获取入口
2. `MapperProxy.invoke()` (L59) - 代理方法调用
3. `Executor.query()` (L82) - SQL 执行入口
4. `Plugin.wrap()` (L60) - 插件包装

### 🔍 关键数据结构
- **Mapper 代理工厂映射**：`knownMappers`（HashMap）
- **方法缓存**：`methodCache`（ConcurrentHashMap）
- **MappedStatement 映射**：`mappedStatements`（StrictMap）
- **一级缓存**：`localCache`（PerpetualCache）
- **二级缓存**：`tcm`（TransactionalCacheManager）

### 🧵 线程模型
- **代理创建**：单例模式，线程安全
- **SQL 执行**：每个 `SqlSession` 一个 `Executor`，线程隔离
- **插件执行**：多线程并发执行，需要线程安全

### 📚 Mapper 动态代理
- `SqlSession.getMapper` -> `MapperProxyFactory` -> `MapperProxy`
- `MapperMethod`：方法解析（SQL 语句、返回类型、参数映射）

### 📚 执行链
- `Executor`（Simple/Reuse/Batch + CachingExecutor）
- `StatementHandler`、`ParameterHandler`、`ResultSetHandler`

### 📚 插件
- `Interceptor` + `Plugin.wrap`：如何织入执行链（责任链模式）

### 📚 缓存
- **一级缓存**：Session 级（`PerpetualCache`）
- **二级缓存**：Mapper 级（`TransactionalCacheManager`）

### 🧪 扩展实验
- **自定义 Interceptor**：SQL 执行时间统计（见 `scripts/MyBatisMapperProxyTrace.java`）
- **自定义 TypeHandler**：自定义类型转换（见 `cases/mybatis.md`）
- **自定义 ResultHandler**：结果集处理（见 `cases/mybatis.md`）

### 🐛 常见坑
- **一级缓存导致数据不一致**：同一 SqlSession 中查询结果不一致
- **二级缓存导致数据不一致**：不同 SqlSession 查询结果不一致
- **插件拦截失效**：拦截方法签名不匹配、目标对象未被代理

示例代码：`scripts/MyBatisMapperProxyTrace.java`

---

## 4) Spring Cloud Gateway（路由/过滤器链/Netty）

### 📍 关键断点
1. `DispatcherHandler.handle()` (L124) - 请求处理入口
2. `RoutePredicateHandlerMapping.getHandler()` (L89) - 路由匹配
3. `FilteringWebHandler.handle()` (L89) - 过滤器处理入口
4. `NettyRoutingFilter.filter()` (L200) - Netty 路由过滤

### 🔍 关键数据结构
- **路由定义列表**：`Flux<RouteDefinition>`
- **全局过滤器列表**：`globalFilters`（有序 List）
- **过滤器列表**：`filters`（有序 List）
- **HTTP 客户端**：`httpClient`（Reactor Netty）

### 🧵 线程模型
- **请求处理**：Netty EventLoop 线程（非阻塞）
- **过滤器执行**：响应式流处理，支持异步
- **背压处理**：通过 `onBackpressureBuffer` 自动处理

### 📚 路由匹配
- `RouteDefinitionLocator` -> `RouteLocator`
- `Predicate` 匹配（Path/Host/Header/Method/Query）

### 📚 过滤器链
- `GlobalFilter` + `GatewayFilterFactory` 组合
- 有序执行：`Ordered` / `@Order`（数值越小越先执行）

### 📚 响应式模型
- Reactor + Netty：线程模型、背压、超时、熔断/限流接入点

### 🧪 扩展实验
- **自定义 GlobalFilter**：请求日志记录（见 `scripts/GatewayFilterTrace.java`）
- **自定义 GatewayFilterFactory**：请求头添加（见 `cases/springcloud_gateway.md`）
- **自定义 RoutePredicateFactory**：自定义断言（见 `cases/springcloud_gateway.md`）

### 🐛 常见坑
- **路由不匹配**：路径不匹配、断言条件不满足、路由顺序问题
- **过滤器不执行**：过滤器顺序错误、过滤器未注册、过滤器短路返回
- **响应式流阻塞**：同步阻塞操作、背压未处理、超时未设置

验证日志：`data/gateway-trace-sample.log`
示例代码：`scripts/GatewayFilterTrace.java`

---

## 5) OpenFeign（代理/编解码/拦截器/容错）

### 📍 关键断点
1. `FeignClientFactoryBean.getObject()` (L124) - Feign 客户端创建入口
2. `SynchronousMethodHandler.invoke()` (L89) - 同步方法处理
3. `LoadBalancerFeignClient.execute()` (L124) - 负载均衡执行
4. `Retryer.continueOrPropagate()` (L45) - 重试判断

### 🔍 关键数据结构
- **方法处理器映射**：`methodToHandler`（Map<Method, MethodHandler>）
- **请求拦截器列表**：`requestInterceptors`（List<RequestInterceptor>）
- **重试配置**：`maxAttempts`、`period`、`attempt`

### 🧵 线程模型
- **代理创建**：启动时单线程创建，线程安全
- **请求构建**：每次调用创建新模板，线程隔离
- **HTTP 请求**：异步执行（如果配置），支持超时

### 📚 代理生成
- `FeignClientFactoryBean` -> `Feign.Builder` -> 动态代理
- `ReflectiveFeign.newInstance()` -> `Proxy.newProxyInstance()`

### 📚 请求构建
- `Contract`（SpringMVC 注解解析）
- `RequestInterceptor`、`Encoder/Decoder`

### 📚 调用链
- 负载均衡：Ribbon/Spring Cloud LoadBalancer
- 超时：Feign Client 配置（`Request.Options`）
- 重试：Retryer
- 熔断：Sentinel/Resilience4j

### 🧪 扩展实验
- **自定义 RequestInterceptor**：请求头添加（见 `scripts/OpenFeignTrace.java`）
- **自定义 ErrorDecoder**：错误处理（见 `scripts/OpenFeignTrace.java`）
- **自定义 Retryer**：重试策略（见 `scripts/OpenFeignTrace.java`）

### 🐛 常见坑
- **Feign 客户端未创建**：未启用 Feign、包扫描路径错误
- **请求超时**：超时配置过短、服务响应慢
- **负载均衡不生效**：未配置负载均衡客户端、服务实例未注册

示例代码：`scripts/OpenFeignTrace.java`

---

## 6) Nacos（注册发现/配置中心/一致性）

### 📍 关键断点
1. `NacosServiceRegistry.register()` (L65) - 服务注册入口
2. `NacosConfigService.getConfig()` (L124) - 配置获取入口
3. `LongPollingRunnable.run()` (L124) - 长轮询任务
4. `HostReactor.getServiceInfo()` (L89) - 服务发现

### 🔍 关键数据结构
- **服务实例映射**：`instanceMap`（ConcurrentHashMap）
- **服务信息缓存**：`serviceInfoMap`（ConcurrentHashMap）
- **配置缓存**：`cacheMap`（ConcurrentHashMap）
- **长轮询任务列表**：`longPollingTasks`（List<LongPollingRunnable>）

### 🧵 线程模型
- **注册线程**：主线程同步注册，HTTP 请求阻塞
- **心跳线程**：`BeatReactor` 使用 `ScheduledExecutorService` 定时发送心跳（5 秒间隔）
- **长轮询线程**：`LongPollingRunnable` 使用线程池执行长轮询任务（30 秒超时）

### 📚 注册发现
- 实例注册/心跳/摘除
- 客户端缓存与服务列表更新（推/拉）
- **健康检查**：客户端心跳（5 秒）、服务端超时（15 秒）、自动摘除（30 秒）

### 📚 配置中心
- DataId/Group/Namespace
- **长轮询机制**：30 秒超时、配置变更推送、本地缓存
- **灰度发布策略**：版本号、分组策略

### 🧪 扩展实验
- **自定义 NamingService**：扩展注册逻辑（见 `cases/nacos.md`）
- **自定义 ConfigListener**：配置变更监听（见 `scripts/NacosConfigTrace.java`）
- **自定义 ServiceInfoUpdateCallback**：服务列表更新回调（见 `cases/nacos.md`）

### 🐛 常见坑
- **服务注册失败**：Nacos 服务器不可用、网络问题、命名空间/分组不匹配
- **配置拉取失败**：DataId/Group 不匹配、长轮询超时、本地缓存损坏
- **服务发现不及时**：缓存更新间隔过长、心跳失败、服务端健康检查延迟

示例代码：`scripts/NacosConfigTrace.java`

---

## 7) Sentinel（SlotChain/规则/熔断降级）

### 📍 关键断点
1. `SphU.entry()` (L89) - 资源入口
2. `FlowSlot.entry()` (L89) - 流控 Slot
3. `DegradeSlot.entry()` (L89) - 熔断 Slot
4. `StatisticSlot.entry()` (L89) - 统计 Slot

### 🔍 关键数据结构
- **资源入口映射**：`resourceWrapperMap`（ConcurrentHashMap）
- **流控规则映射**：`flowRules`（ConcurrentHashMap）
- **滑动窗口数组**：`array`（AtomicReferenceArray）
- **通过 QPS 统计**：`rollingCounterInSecond`（Metric）

### 🧵 线程模型
- **Entry 创建**：多线程并发创建，线程安全
- **Slot 执行**：同步执行，线程安全
- **滑动窗口统计**：使用 `AtomicReferenceArray`，线程安全

### 📚 核心链路
- `SphU.entry` -> SlotChain -> pass/block
- **Slot 执行顺序**：NodeSelectorSlot -> ClusterBuilderSlot -> LogSlot -> StatisticSlot -> SystemSlot -> AuthoritySlot -> FlowSlot -> DegradeSlot

### 📚 规则类型
- **流控**：QPS/并发、关联流控、链路流控
- **熔断**：慢调用比例、异常比例、异常数
- **热点参数**：参数索引、QPS 阈值、统计窗口

### 📚 统计
- **滑动窗口**：`LeapArray`、`WindowWrap`、`MetricBucket`
- **指标上报**：QPS、RT、异常数、线程数
- **规则动态加载**：`FlowRuleManager.loadRules()`

### 🧪 扩展实验
- **自定义 Slot**：自定义限流逻辑（见 `scripts/SentinelResourceTrace.java`）
- **自定义 FlowRule**：动态规则（见 `cases/sentinel.md`）
- **自定义 StatisticSlot**：自定义统计（见 `cases/sentinel.md`）

### 🐛 常见坑
- **限流不生效**：资源名不匹配、规则未加载、Slot 链未正确构建
- **熔断不恢复**：重试时间未设置、探测请求失败、状态机转换错误
- **统计不准确**：滑动窗口配置错误、时间窗口未对齐、并发统计问题

验证规则：`data/sentinel-rules.json`
验证日志：`data/sentinel-slotchain-trace.log`
示例代码：`scripts/SentinelResourceTrace.java`

---

## 8) Seata（AT/TCC/事务一致性）

### 📍 关键断点
1. `GlobalTransactionalInterceptor.invoke()` (L89) - 全局事务拦截入口
2. `UndoLogManager.insertUndoLog()` (L89) - undo_log 插入
3. `UndoLogManager.undo()` (L124) - undo_log 回滚
4. `DefaultCoordinator.doGlobalRollback()` (L124) - TC 全局回滚

### 🔍 关键数据结构
- **全局事务映射**：`globalSessions`（ConcurrentHashMap）
- **分支会话列表**：`branchSessions`（List<BranchSession>）
- **undo_log 对象**：`branchId`、`xid`、`rollbackInfo`、`logStatus`

### 🧵 线程模型
- **事务拦截**：业务线程同步执行
- **undo_log 生成**：业务线程同步生成
- **TC 通信**：Netty 异步通信，同步等待响应

### 📚 角色
- **TM**：事务管理器（开启全局事务）
- **RM**：资源管理器（注册分支事务、执行回滚）
- **TC**：事务协调器（协调提交/回滚）

### 📚 AT 模式
- **一阶段**：业务 SQL + undo_log（前后镜像）
- **二阶段**：提交/回滚（undo_log 反向补偿）
- **undo_log 结构**：branch_id、xid、rollback_info、log_status

### 📚 关键问题
- **幂等**：XID 唯一性保证
- **悬挂**：TCC 模式问题（Try 超时、Cancel 先执行）
- **空回滚**：TCC 模式问题（Try 未执行、Cancel 执行）
- **隔离**：全局锁保证（`LockManager.acquireLock()`）

### 🧪 扩展实验
- **自定义 UndoLogParser**：自定义序列化（见 `scripts/SeataATTrace.java`）
- **自定义 LockManager**：自定义锁管理（见 `cases/seata.md`）
- **自定义 ResourceManager**：自定义资源管理（见 `cases/seata.md`）

### 🐛 常见坑
- **undo_log 表不存在**：未创建 undo_log 表
- **全局锁冲突**：多个事务同时修改同一行数据
- **回滚失败**：undo_log 数据损坏、反向 SQL 生成错误

验证 SQL：`data/seata-undo_log.sql`
验证日志：`data/seata-transaction-trace.log`
示例代码：`scripts/SeataATTrace.java`

---

## 9) XXL-JOB（调度中心/执行器/可靠性）

### 📍 关键断点
1. `JobScheduleHelper.run()` (L89) - 调度线程运行
2. `XxlJobTrigger.trigger()` (L89) - 任务触发
3. `ExecutorBiz.run()` (L89) - 任务执行
4. `JobThread.run()` (L124) - 任务线程运行

### 🔍 关键数据结构
- **任务触发线程池**：`triggerPool`（ThreadPoolExecutor）
- **任务队列**：`triggerQueue`（LinkedBlockingQueue）
- **任务处理器映射**：`jobHandlerRepository`（ConcurrentHashMap）

### 🧵 线程模型
- **调度线程**：单线程扫描任务，每 1 秒扫描一次
- **触发线程池**：多线程并发触发任务，线程池大小可配置
- **任务线程**：每个任务一个线程，从队列取任务执行

### 📚 调度中心
- **任务触发**：定时扫描任务（`JobScheduleHelper.run()`）
- **路由策略**：10 种策略（FIRST/LAST/ROUND/RANDOM/CONSISTENT_HASH/FAILOVER/BUSYOVER/SHARDING_BROADCAST 等）
- **失败重试**：重试次数配置、重试间隔配置

### 📚 执行器
- **注册心跳**：每 30 秒注册一次（`ExecutorRegistryThread.run()`）
- **任务执行**：任务线程执行（`JobThread.run()`）
- **回调上报**：异步上报结果（`ExecutorBiz.callback()`）

### 📚 一致性与可靠性
- **避免重复执行**：任务状态管理（RUNNING/SUCCESS/FAIL）
- **超时控制**：executorTimeout 配置
- **幂等 Job 设计**：任务参数唯一性、数据库唯一索引

### 🧪 扩展实验
- **自定义路由策略**：自定义路由（见 `scripts/XxlJobHandlerTrace.java`）
- **自定义 JobHandler**：任务处理器（见 `scripts/XxlJobHandlerTrace.java`）
- **自定义回调**：结果处理（见 `cases/xxl-job.md`）

### 🐛 常见坑
- **任务不触发**：Cron 表达式错误、任务状态未启用、调度中心未启动
- **执行器未注册**：执行器配置错误、网络不通、注册线程未启动
- **任务执行失败**：任务处理器未注册、任务参数错误、执行超时

验证日志：`data/xxl-job-sample.log`
示例代码：`scripts/XxlJobHandlerTrace.java`

---

## 📊 面试重点总结

### 高频面试题

1. **Spring**
   - Bean 生命周期完整流程（12 步 refresh）
   - 循环依赖三级缓存机制（为什么需要三级）
   - AOP 代理创建时机和选择策略（JDK vs CGLIB）
   - 事务传播行为源码实现（`handleExistingTransaction`）

2. **Spring Boot**
   - 自动配置发现机制（`SpringFactoriesLoader`）
   - 条件评估流程（`OnClassCondition`、`OnBeanCondition`、`OnPropertyCondition`）
   - Starter 设计模式（自动配置 + 配置属性 + Bean 暴露）

3. **MyBatis**
   - Mapper 动态代理实现（`MapperProxy`、`MapperMethod`）
   - SQL 执行链（`Executor` -> `StatementHandler` -> `ResultSetHandler`）
   - 插件拦截机制（`Plugin.wrap`、责任链模式）

4. **Gateway**
   - 路由匹配机制（`RoutePredicateHandlerMapping`）
   - 过滤器链执行（`DefaultGatewayFilterChain`）
   - Netty 响应式模型（EventLoop、背压处理）

5. **OpenFeign**
   - 代理生成机制（`ReflectiveFeign.newInstance()`）
   - 负载均衡集成（`LoadBalancerFeignClient`）
   - 超时重试机制（`Request.Options`、`Retryer`）

6. **Nacos**
   - 长轮询机制（30 秒超时、配置变更推送）
   - 服务发现缓存机制（客户端缓存、定时更新）
   - 健康检查机制（心跳、超时、摘除）

7. **Sentinel**
   - SlotChain 执行顺序（8 个 Slot）
   - 滑动窗口统计（`LeapArray`、`WindowWrap`）
   - 流控算法实现（QPS、并发线程数、关联流控）

8. **Seata**
   - undo_log 生成机制（前后镜像、序列化）
   - 回滚机制（解析 undo_log、生成反向 SQL）
   - 全局锁机制（`LockManager.acquireLock()`）

9. **XXL-JOB**
   - 调度线程机制（每 1 秒扫描任务）
   - 路由策略实现（10 种策略）
   - 执行器注册心跳机制（每 30 秒注册一次）

### 手写代码题

1. **Spring**
   - 实现自定义 BeanPostProcessor
   - 实现自定义 Condition
   - 实现自定义 AOP Advisor

2. **MyBatis**
   - 实现自定义 Interceptor
   - 实现自定义 TypeHandler
   - 实现自定义 ResultHandler

3. **Gateway**
   - 实现自定义 GlobalFilter
   - 实现自定义 GatewayFilterFactory
   - 实现自定义 RoutePredicateFactory

4. **OpenFeign**
   - 实现自定义 RequestInterceptor
   - 实现自定义 ErrorDecoder
   - 实现自定义 Retryer

5. **Sentinel**
   - 实现自定义 Slot
   - 实现动态规则管理
   - 实现自定义统计

6. **Seata**
   - 实现自定义 UndoLogParser
   - 实现自定义 LockManager
   - 实现自定义 ResourceManager

7. **XXL-JOB**
   - 实现自定义路由策略
   - 实现自定义 JobHandler
   - 实现自定义回调

---

**最后更新：2026-01-26**
