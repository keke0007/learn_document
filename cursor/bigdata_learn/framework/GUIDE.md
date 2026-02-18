# Java 微服务框架与中间件源码学习指南（深入版）

## 📚 项目概述

本指南面向**源码级**学习与面试准备，覆盖：

- Spring、Spring Boot、MyBatis
- Spring Cloud Gateway、OpenFeign
- Nacos、Sentinel、Seata
- XXL-JOB

每个主题都提供：**学习知识点 + 源码阅读路线 + 断点清单 + 可运行/可验证案例 + 验证数据**，最终形成可复盘的面试材料。

---

## 📁 项目结构

```
framework/
├── GUIDE.md                      # 本指南（学习路径 + 全局方法论 + 断点清单）
├── README.md                     # 知识点总览（更细的目录/清单）
├── cases/                        # 源码学习案例（每个组件一个，深入版）
│   ├── spring.md                # Spring IOC/AOP/事务（断点+数据结构+扩展实验）
│   ├── springboot.md            # Spring Boot 启动/自动配置（断点+条件评估+扩展实验）
│   ├── mybatis.md               # MyBatis Mapper/执行链/插件（断点+执行链+扩展实验）
│   ├── springcloud_gateway.md   # Gateway 路由/过滤器/Netty（断点+线程模型+扩展实验）
│   ├── openfeign.md             # OpenFeign 代理/请求构建/调用链（断点+负载均衡+扩展实验）
│   ├── nacos.md                 # Nacos 注册发现/配置中心（断点+长轮询+扩展实验）
│   ├── sentinel.md              # Sentinel SlotChain/规则/统计（断点+滑动窗口+扩展实验）
│   ├── seata.md                 # Seata AT 模式/全局事务（断点+undo_log+扩展实验）
│   └── xxl-job.md               # XXL-JOB 调度/执行器/路由（断点+路由策略+扩展实验）
├── data/                         # 验证数据（配置/规则/日志/SQL/追踪样例）
│   ├── application-sample.yml    # Spring Boot 配置示例
│   ├── sentinel-rules.json       # Sentinel 规则示例
│   ├── seata-undo_log.sql       # Seata undo_log 表结构
│   ├── gateway-trace-sample.log # Gateway 追踪日志（详细版）
│   ├── xxl-job-sample.log       # XXL-JOB 执行日志（详细版）
│   ├── spring-refresh-trace.log  # Spring refresh 追踪日志
│   ├── sentinel-slotchain-trace.log # Sentinel SlotChain 追踪日志
│   └── seata-transaction-trace.log  # Seata 事务追踪日志
└── scripts/                      # 示例代码（可直接粘贴到项目验证，含扩展实验）
    ├── SpringIocTrace.java       # Spring IOC 追踪（含 BeanPostProcessor 扩展）
    ├── SpringAopTxTrace.java    # Spring AOP/事务追踪（含自定义切面）
    ├── MyBatisMapperProxyTrace.java # MyBatis 代理追踪（含自定义插件）
    ├── GatewayFilterTrace.java  # Gateway 过滤器追踪（含自定义过滤器工厂）
    ├── OpenFeignTrace.java      # OpenFeign 追踪（含自定义拦截器/错误解码器）
    ├── NacosConfigTrace.java    # Nacos 追踪（含自定义监听器）
    ├── SentinelResourceTrace.java # Sentinel 追踪（含自定义 Slot）
    ├── SeataATTrace.java        # Seata AT 追踪（含自定义 UndoLogParser）
    └── XxlJobHandlerTrace.java  # XXL-JOB 追踪（含自定义路由策略）
```

---

## 🎯 学习路径（建议 14~28 天）

### 阶段一：Spring 核心（3~5 天）
- **IOC 容器**：BeanDefinition -> 实例化 -> 属性填充 -> 初始化 -> 销毁
  - **断点**：`AbstractApplicationContext.refresh()`、`doCreateBean()`、`createBeanInstance()`、`populateBean()`、`initializeBean()`
  - **数据结构**：三级缓存、BeanDefinitionMap、BeanPostProcessor 列表
  - **扩展实验**：自定义 BeanPostProcessor、自定义 Condition
- **扩展点**：`BeanFactoryPostProcessor` / `BeanPostProcessor` / `Aware` / `ApplicationListener`
- **AOP**：代理创建、`Advisor`、`MethodInterceptor`、`@Aspect` 编织
  - **断点**：`AbstractAutoProxyCreator.postProcessAfterInitialization()`、`wrapIfNecessary()`、`JdkDynamicAopProxy.invoke()`
  - **扩展实验**：自定义 AOP Advisor
- **事务**：`@Transactional` 解析、拦截器链、传播/隔离级别
  - **断点**：`TransactionInterceptor.invoke()`、`invokeWithinTransaction()`、`handleExistingTransaction()`

对应案例：`cases/spring.md`，示例：`scripts/SpringIocTrace.java`、`scripts/SpringAopTxTrace.java`

### 阶段二：Spring Boot 自动装配（3~4 天）
- **启动链路**：`SpringApplication.run`、`SpringFactoriesLoader`
  - **断点**：`SpringApplication.run()`、`createApplicationContext()`、`AutoConfigurationImportSelector.selectImports()`
- **自动配置**：`@EnableAutoConfiguration`、条件装配（`@Conditional*`）
  - **断点**：`OnClassCondition.getMatchOutcome()`、`OnBeanCondition.getMatchOutcome()`、`OnPropertyCondition.getMatchOutcome()`
  - **扩展实验**：自定义 Starter、自定义 Condition
- **配置绑定**：`@ConfigurationProperties`、`Environment`、`PropertySource`
  - **断点**：`ConfigurationPropertiesBindingPostProcessor.postProcessBeforeInitialization()`、`Binder.bind()`

对应案例：`cases/springboot.md`

### 阶段三：MyBatis（2~3 天）
- **Mapper 动态代理**：`MapperProxy`、`MapperMethod`
  - **断点**：`SqlSession.getMapper()`、`MapperProxy.invoke()`、`MapperMethod.execute()`
- **SQL 执行**：`Executor`/`StatementHandler`/`ResultSetHandler`
  - **断点**：`Executor.query()`、`PreparedStatementHandler.query()`、`DefaultResultSetHandler.handleResultSets()`
- **插件机制**：`Interceptor` + `Plugin.wrap`
  - **断点**：`InterceptorChain.pluginAll()`、`Plugin.wrap()`、`Plugin.invoke()`
  - **扩展实验**：自定义 Interceptor、自定义 TypeHandler

对应案例：`cases/mybatis.md`，示例：`scripts/MyBatisMapperProxyTrace.java`

### 阶段四：Gateway + OpenFeign（3~5 天）
- **Gateway**：路由匹配、过滤器链、全局过滤器、Netty 线程模型、背压与超时
  - **断点**：`DispatcherHandler.handle()`、`RoutePredicateHandlerMapping.getHandler()`、`FilteringWebHandler.handle()`、`NettyRoutingFilter.filter()`
  - **扩展实验**：自定义 GlobalFilter、自定义 GatewayFilterFactory、自定义 RoutePredicateFactory
- **OpenFeign**：接口代理、编码/解码、拦截器、负载均衡、超时重试
  - **断点**：`FeignClientFactoryBean.getObject()`、`SynchronousMethodHandler.invoke()`、`LoadBalancerFeignClient.execute()`
  - **扩展实验**：自定义 RequestInterceptor、自定义 ErrorDecoder、自定义 Retryer

对应案例：`cases/springcloud_gateway.md`、`cases/openfeign.md`，示例：`scripts/GatewayFilterTrace.java`、`scripts/OpenFeignTrace.java`

### 阶段五：Nacos + Sentinel（3~5 天）
- **Nacos**：注册发现、配置中心、长轮询/推送、客户端缓存、健康检查
  - **断点**：`NacosServiceRegistry.register()`、`NacosConfigService.getConfig()`、`LongPollingRunnable.run()`
  - **扩展实验**：自定义 NamingService、自定义 ConfigListener、自定义 ServiceInfoUpdateCallback
- **Sentinel**：SlotChain、规则（流控/熔断/热点）、统计、降级策略
  - **断点**：`SphU.entry()`、`FlowSlot.entry()`、`DegradeSlot.entry()`、`StatisticSlot.entry()`
  - **扩展实验**：自定义 Slot、自定义 FlowRule、自定义 StatisticSlot

对应案例：`cases/nacos.md`、`cases/sentinel.md`，验证：`data/sentinel-rules.json`

### 阶段六：Seata + XXL-JOB（3~6 天）
- **Seata**：AT 模式（undo_log）、全局事务、RM/TM/TC 交互、隔离与回滚
  - **断点**：`GlobalTransactionalInterceptor.invoke()`、`UndoLogManager.insertUndoLog()`、`UndoLogManager.undo()`
  - **扩展实验**：自定义 UndoLogParser、自定义 LockManager、自定义 ResourceManager
- **XXL-JOB**：调度中心、执行器注册、心跳、路由策略、失败重试、任务一致性
  - **断点**：`JobScheduleHelper.run()`、`XxlJobTrigger.trigger()`、`ExecutorBiz.run()`
  - **扩展实验**：自定义路由策略、自定义 JobHandler、自定义回调

对应案例：`cases/seata.md`、`cases/xxl-job.md`，验证：`data/seata-undo_log.sql`、`data/xxl-job-sample.log`

---

## 🧠 源码学习方法论（强烈建议照做）

### 1) 先画“概念图”，再看代码
- **对象/模块**：谁负责配置？谁负责运行时？谁负责扩展？
- **边界**：哪些是框架内核？哪些是可插拔 SPI？
- **数据流**：数据如何流转？状态如何变化？

### 2) 只追关键路径（Happy Path）
建议顺序：入口 -> 核心接口 -> 默认实现 -> 扩展点 -> 异常分支。

**每个组件至少追踪 3 条关键调用链：**
- **主流程**：正常执行路径（5~8 个节点）
- **扩展点**：如何扩展框架功能（3~5 个节点）
- **异常处理**：错误处理和恢复机制（3~5 个节点）

### 3) 用“断点 + 日志 + 指标”闭环验证
- **断点**：入口方法 / 工厂方法 / 关键拦截器（见各案例的“断点清单”）
- **日志**：请求链路、路由选择、事务分支、调度触发（见 `data/` 目录）
- **指标**：QPS、RT、错误率、队列堆积、限流触发次数

### 4) 输出“面试可复述”的产物
每个组件至少沉淀：
- **3 条关键调用链**（用 5~8 个节点描述，带源码位置）
- **3 个常见坑**（以及你会怎么排查，带源码定位）
- **1 个性能优化点**（为什么有效，带数据验证）
- **1 个扩展实验**（基于源码扩展点实现功能）

---

## 📍 全局断点清单（按学习顺序）

### Spring 核心断点（优先级：高）
1. `AbstractApplicationContext.refresh()` - 容器刷新入口
2. `DefaultListableBeanFactory.getBean()` - Bean 获取
3. `AbstractAutowireCapableBeanFactory.doCreateBean()` - Bean 创建核心
4. `AbstractAutoProxyCreator.postProcessAfterInitialization()` - AOP 代理创建
5. `TransactionInterceptor.invoke()` - 事务拦截

### Spring Boot 断点（优先级：高）
1. `SpringApplication.run()` - 启动入口
2. `AutoConfigurationImportSelector.selectImports()` - 自动配置选择
3. `OnClassCondition.getMatchOutcome()` - 条件评估

### MyBatis 断点（优先级：中）
1. `SqlSession.getMapper()` - Mapper 获取
2. `MapperProxy.invoke()` - 代理调用
3. `Executor.query()` - SQL 执行
4. `Plugin.wrap()` - 插件包装

### Gateway 断点（优先级：中）
1. `DispatcherHandler.handle()` - 请求处理
2. `RoutePredicateHandlerMapping.getHandler()` - 路由匹配
3. `FilteringWebHandler.handle()` - 过滤器链
4. `NettyRoutingFilter.filter()` - Netty 路由

### OpenFeign 断点（优先级：中）
1. `FeignClientFactoryBean.getObject()` - 客户端创建
2. `SynchronousMethodHandler.invoke()` - 方法调用
3. `LoadBalancerFeignClient.execute()` - 负载均衡

### Nacos 断点（优先级：中）
1. `NacosServiceRegistry.register()` - 服务注册
2. `NacosConfigService.getConfig()` - 配置获取
3. `LongPollingRunnable.run()` - 长轮询

### Sentinel 断点（优先级：中）
1. `SphU.entry()` - 资源入口
2. `FlowSlot.entry()` - 流控检查
3. `StatisticSlot.entry()` - 统计记录

### Seata 断点（优先级：中）
1. `GlobalTransactionalInterceptor.invoke()` - 全局事务拦截
2. `UndoLogManager.insertUndoLog()` - undo_log 插入
3. `UndoLogManager.undo()` - 回滚执行

### XXL-JOB 断点（优先级：低）
1. `JobScheduleHelper.run()` - 调度线程
2. `XxlJobTrigger.trigger()` - 任务触发
3. `ExecutorBiz.run()` - 任务执行

---

## ✅ 最终面试输出（你应该能回答）

### Spring
- Bean 生命周期与 AOP/事务如何串起来？哪些扩展点会“影响全局”？
- **调用链**：`refresh()` -> `finishBeanFactoryInitialization()` -> `getBean()` -> `doCreateBean()` -> `initializeBean()` -> `postProcessAfterInitialization()`（AOP 代理）-> `TransactionInterceptor.invoke()`（事务）
- **扩展点**：`BeanFactoryPostProcessor`（修改 BeanDefinition）、`BeanPostProcessor`（修改 Bean）、`ApplicationListener`（事件监听）

### Boot
- 自动配置是怎么发现/生效/回退的？如何写一个 starter？
- **发现**：`SpringFactoriesLoader.loadFactoryNames()` 读取 `META-INF/spring.factories`
- **生效**：条件评估（`OnClassCondition`、`OnBeanCondition`、`OnPropertyCondition`）
- **回退**：条件不满足时，自动配置类不生效

### MyBatis
- Mapper 如何变成可执行 SQL？插件怎么插到执行链里？
- **调用链**：`getMapper()` -> `MapperProxy.invoke()` -> `MapperMethod.execute()` -> `SqlSession.selectOne()` -> `Executor.query()` -> `StatementHandler.query()`
- **插件**：`InterceptorChain.pluginAll()` -> `Plugin.wrap()` -> 创建代理 -> `Plugin.invoke()` -> `Interceptor.intercept()`

### Gateway
- 路由匹配与过滤器链如何执行？如何定位超时/背压？
- **路由匹配**：`RoutePredicateHandlerMapping.getHandler()` -> `RouteLocator.getRoutes()` -> `Predicate.test()`
- **过滤器链**：`FilteringWebHandler.handle()` -> `DefaultGatewayFilterChain.filter()` -> 有序执行过滤器
- **超时定位**：`NettyRoutingFilter.filter()` -> `HttpClient.request()` -> `timeout()` 操作符

### Feign
- 接口如何变成 HTTP 调用？超时/重试/熔断在链路哪里发生？
- **调用链**：`SynchronousMethodHandler.invoke()` -> `RequestTemplate.create()` -> `LoadBalancerFeignClient.execute()` -> `HttpClient.execute()`
- **超时**：`Request.Options.readTimeout`
- **重试**：`Retryer.continueOrPropagate()`
- **熔断**：与 Sentinel/Resilience4j 集成时，在 `LoadBalancerFeignClient.execute()` 之后

### Nacos
- 注册发现如何保证可用？配置推送如何保证一致性？
- **可用性**：心跳机制（5 秒）、健康检查（15 秒超时、30 秒摘除）
- **一致性**：服务列表最终一致（定时更新 + 推送）、配置版本号保证（MD5 校验）

### Sentinel
- SlotChain 怎么决定放行/限流/熔断？热点规则怎么统计？
- **调用链**：`SphU.entry()` -> `SlotChain.entry()` -> 8 个 Slot 有序执行 -> `FlowSlot.entry()`（流控）-> `DegradeSlot.entry()`（熔断）
- **热点统计**：`ParamFlowChecker.passCheck()` -> `ParamFlowRule` -> 滑动窗口统计

### Seata
- AT 回滚靠什么数据？undo_log 如何生成与消费？一致性怎么保证？
- **回滚数据**：undo_log 中的前后镜像
- **生成**：`UndoLogManager.insertUndoLog()` -> 序列化前后镜像
- **消费**：`UndoLogManager.undo()` -> 解析 undo_log -> 生成反向 SQL -> 执行回滚
- **一致性**：全局锁（防止脏读）、undo_log（保证回滚）、幂等性（保证重试）

### XXL-JOB
- 调度中心如何“可靠触发”？执行器如何上报与重试？
- **可靠触发**：调度线程每 1 秒扫描任务、任务快照机制、失败重试机制
- **上报**：`ExecutorBiz.callback()` -> HTTP 回调 -> 调度中心更新任务状态
- **重试**：任务执行失败后，调度中心根据重试次数重新触发

---

## 🔧 工具推荐

### 源码阅读工具
- **IDE**：IntelliJ IDEA（推荐，断点调试方便）
- **反编译工具**：JD-GUI、Fernflower（查看第三方库源码）
- **代码搜索**：SourceGraph、GitHub Code Search

### 调试工具
- **断点调试**：IDEA Debugger（设置条件断点、日志断点）
- **日志框架**：Logback、Log4j2（配置详细日志级别）
- **性能分析**：JProfiler、Arthas（分析性能瓶颈）

### 验证工具
- **单元测试**：JUnit、TestNG（验证扩展功能）
- **集成测试**：Spring Boot Test、TestContainers（验证完整流程）
- **监控工具**：Prometheus、Grafana（监控指标）

---

## 📚 参考资源

### 官方文档
1. **Spring**：https://docs.spring.io/spring-framework/docs/current/reference/html/
2. **Spring Boot**：https://docs.spring.io/spring-boot/docs/current/reference/html/
3. **MyBatis**：https://mybatis.org/mybatis-3/
4. **Spring Cloud Gateway**：https://docs.spring.io/spring-cloud-gateway/docs/current/reference/html/
5. **OpenFeign**：https://github.com/OpenFeign/feign
6. **Nacos**：https://nacos.io/docs/latest/
7. **Sentinel**：https://sentinelguard.io/zh-cn/docs/
8. **Seata**：https://seata.io/zh-cn/docs/
9. **XXL-JOB**：https://www.xuxueli.com/xxl-job/

### 源码仓库
1. **Spring Framework**：https://github.com/spring-projects/spring-framework
2. **Spring Boot**：https://github.com/spring-projects/spring-boot
3. **MyBatis**：https://github.com/mybatis/mybatis-3
4. **Spring Cloud Gateway**：https://github.com/spring-cloud/spring-cloud-gateway
5. **OpenFeign**：https://github.com/OpenFeign/feign
6. **Nacos**：https://github.com/alibaba/nacos
7. **Sentinel**：https://github.com/alibaba/Sentinel
8. **Seata**：https://github.com/seata/seata
9. **XXL-JOB**：https://github.com/xuxueli/xxl-job

---

## ✅ 学习检查清单

### 基础能力
- [ ] 能够画出每个组件的核心调用链（5~8 个节点）
- [ ] 能够说出关键数据结构的作用（Map/List/ThreadLocal 等）
- [ ] 能够理解线程模型（单线程/多线程/响应式）

### 深入能力
- [ ] 能够在源码中找到常见问题的定位点（循环依赖、事务失效等）
- [ ] 能够基于源码扩展点实现自定义功能（BPP、Condition、Interceptor 等）
- [ ] 能够分析性能瓶颈并提出优化方案

### 面试能力
- [ ] 能够复述 3 条关键调用链（带源码位置）
- [ ] 能够说出 3 个常见坑及排查方法（带源码定位）
- [ ] 能够描述 1 个性能优化点（带数据验证）
- [ ] 能够展示 1 个扩展实验（基于源码实现）

---

**最后更新：2026-01-26**
