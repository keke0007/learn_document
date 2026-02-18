# Java 高级开发面试知识点总览

## 📚 目录

1. [JVM 核心知识](#1-jvm-核心知识)
2. [并发编程](#2-并发编程)
3. [集合框架](#3-集合框架)
4. [设计模式](#4-设计模式)
5. [Spring 框架](#5-spring-框架)
6. [数据库优化](#6-数据库优化)
7. [分布式系统](#7-分布式系统)
8. [微服务架构](#8-微服务架构)

---

## 1. JVM 核心知识

### 1.1 内存模型

#### 运行时数据区

**程序计数器（PC Register）**
- 线程私有
- 记录当前线程执行的字节码行号
- 唯一不会 OOM 的区域

**Java 虚拟机栈（JVM Stack）**
- 线程私有
- 存储局部变量表、操作数栈、动态链接、方法出口
- StackOverflowError：栈深度超过限制
- OutOfMemoryError：无法申请足够内存

**本地方法栈（Native Method Stack）**
- 线程私有
- 为 Native 方法服务

**堆（Heap）**
- 线程共享
- 存储对象实例
- 分为新生代和老年代
- OutOfMemoryError：堆内存溢出

**方法区（Method Area）**
- 线程共享
- JDK 1.8 后改为元空间（Metaspace）
- 存储类信息、常量、静态变量
- OutOfMemoryError：方法区溢出

#### 堆内存结构

**新生代（Young Generation）**
- Eden 区：新对象分配区域
- Survivor 区（S0/S1）：存活对象暂存区
- 默认比例：Eden:S0:S1 = 8:1:1

**老年代（Old Generation）**
- 长期存活的对象
- 大对象直接进入老年代

### 1.2 垃圾回收

#### GC 算法

**标记-清除算法（Mark-Sweep）**
- 标记需要回收的对象
- 清除被标记的对象
- 缺点：产生内存碎片

**复制算法（Copying）**
- 将内存分为两块，每次使用一块
- 存活对象复制到另一块
- 优点：无碎片
- 缺点：内存利用率低

**标记-整理算法（Mark-Compact）**
- 标记需要回收的对象
- 存活对象向一端移动
- 优点：无碎片，内存利用率高

**分代收集算法**
- 新生代：复制算法
- 老年代：标记-清除或标记-整理

#### GC 收集器

**Serial 收集器**
- 单线程
- 适合客户端应用

**Parallel 收集器**
- 多线程
- 适合吞吐量优先的场景

**CMS 收集器**
- 并发标记清除
- 低停顿时间
- 适合响应时间优先的场景

**G1 收集器**
- 分代收集
- 可预测的停顿时间
- 适合大堆内存

**ZGC 收集器**
- 超低延迟
- 适合超大堆内存

### 1.3 类加载机制

**加载（Loading）**
- 通过类的全限定名获取字节流
- 将字节流转换为方法区的运行时数据结构
- 在内存中生成 Class 对象

**验证（Verification）**
- 文件格式验证
- 元数据验证
- 字节码验证
- 符号引用验证

**准备（Preparation）**
- 为类变量分配内存并设置初始值

**解析（Resolution）**
- 将符号引用转换为直接引用

**初始化（Initialization）**
- 执行类构造器 `<clinit>()` 方法

**类加载器**
- 启动类加载器（Bootstrap ClassLoader）
- 扩展类加载器（Extension ClassLoader）
- 应用程序类加载器（Application ClassLoader）

---

## 2. 并发编程

### 2.1 线程基础

**线程创建方式**
1. 继承 Thread 类
2. 实现 Runnable 接口
3. 实现 Callable 接口
4. 使用线程池

**线程生命周期**
- NEW：新建
- RUNNABLE：可运行
- BLOCKED：阻塞
- WAITING：等待
- TIMED_WAITING：超时等待
- TERMINATED：终止

### 2.2 线程同步

**synchronized**
- 对象锁：锁定对象实例
- 类锁：锁定类对象
- 可重入性：同一线程可重复获取锁
- 锁升级：偏向锁 → 轻量级锁 → 重量级锁

**volatile**
- 保证可见性：修改立即刷新到主内存
- 禁止指令重排序：通过内存屏障实现
- 不保证原子性：复合操作仍需同步

**Lock 接口**
- ReentrantLock：可重入锁
- ReadWriteLock：读写锁
- StampedLock：乐观读锁

### 2.3 并发工具类

**CountDownLatch**
- 等待多个线程完成
- 计数器不能重置

**CyclicBarrier**
- 多个线程相互等待
- 计数器可以重置

**Semaphore**
- 控制并发访问数量
- 信号量机制

**CompletableFuture**
- 异步编程
- 链式调用
- 组合多个异步操作

### 2.4 线程池

**ThreadPoolExecutor 参数**
- corePoolSize：核心线程数
- maximumPoolSize：最大线程数
- keepAliveTime：空闲线程存活时间
- workQueue：工作队列
- threadFactory：线程工厂
- handler：拒绝策略

**拒绝策略**
- AbortPolicy：抛出异常
- CallerRunsPolicy：调用者运行
- DiscardPolicy：丢弃任务
- DiscardOldestPolicy：丢弃最老任务

**线程池类型**
- FixedThreadPool：固定线程数
- CachedThreadPool：缓存线程池
- ScheduledThreadPool：定时任务线程池
- ForkJoinPool：分治线程池

### 2.5 原子类

**基本类型**
- AtomicInteger
- AtomicLong
- AtomicBoolean

**引用类型**
- AtomicReference
- AtomicStampedReference（解决 ABA 问题）
- AtomicMarkableReference

**数组类型**
- AtomicIntegerArray
- AtomicLongArray
- AtomicReferenceArray

---

## 3. 集合框架

### 3.1 HashMap

**JDK 1.7 实现**
- 数组 + 链表
- 头插法
- 多线程下可能形成环形链表

**JDK 1.8 实现**
- 数组 + 链表 + 红黑树
- 尾插法
- 链表长度 >= 8 且数组长度 >= 64 时转为红黑树

**关键参数**
- 初始容量：16
- 负载因子：0.75
- 扩容阈值：容量 × 负载因子

**put 方法流程**
1. 计算 key 的 hash 值
2. 确定数组索引：(n - 1) & hash
3. 如果该位置为空，直接插入
4. 如果该位置有节点，遍历链表/红黑树
5. 如果 key 已存在，更新 value
6. 如果不存在，插入新节点
7. 判断是否需要扩容

**扩容机制**
- 容量变为原来的 2 倍
- 重新计算 hash 值
- JDK 1.8 优化：元素位置要么不变，要么移动 2 的幂次方位置

### 3.2 ConcurrentHashMap

**JDK 1.7 实现**
- 分段锁（Segment）
- 每个 Segment 独立加锁
- 并发度 = Segment 数量

**JDK 1.8 实现**
- CAS + synchronized
- 锁粒度更细（锁住链表头节点）
- 并发度更高

### 3.3 ArrayList vs LinkedList

**ArrayList**
- 基于数组
- 随机访问：O(1)
- 插入删除：O(n)
- 扩容：1.5 倍

**LinkedList**
- 基于双向链表
- 随机访问：O(n)
- 插入删除：O(1)
- 不需要扩容

### 3.4 其他集合

**Vector**
- 线程安全
- 使用 synchronized 同步
- 性能较差

**CopyOnWriteArrayList**
- 写时复制
- 读操作无锁
- 适合读多写少的场景

**TreeMap**
- 基于红黑树
- 有序
- 插入删除：O(log n)

**LinkedHashMap**
- 继承 HashMap
- 维护插入顺序或访问顺序

---

## 4. 设计模式

### 4.1 创建型模式

**单例模式**
- 饿汉式
- 懒汉式（双重检查锁定）
- 静态内部类
- 枚举

**工厂模式**
- 简单工厂
- 工厂方法
- 抽象工厂

**建造者模式**
- 分离复杂对象的构建和表示
- 链式调用

### 4.2 结构型模式

**代理模式**
- 静态代理
- JDK 动态代理
- CGLIB 代理

**适配器模式**
- 类适配器
- 对象适配器
- 接口适配器

**装饰器模式**
- 动态添加功能
- 比继承更灵活

### 4.3 行为型模式

**观察者模式**
- 一对多依赖
- 主题和观察者

**策略模式**
- 定义算法族
- 运行时选择算法

**责任链模式**
- 请求沿着链传递
- 直到有对象处理它

---

## 5. Spring 框架

### 5.1 IOC 容器

**Bean 生命周期**
1. 实例化（Instantiation）
2. 属性赋值（Population）
3. 初始化（Initialization）
   - BeanPostProcessor.postProcessBeforeInitialization
   - @PostConstruct / InitializingBean.afterPropertiesSet
   - BeanPostProcessor.postProcessAfterInitialization
4. 使用（In Use）
5. 销毁（Destruction）
   - @PreDestroy / DisposableBean.destroy

**Bean 作用域**
- singleton：单例（默认）
- prototype：原型
- request：请求
- session：会话
- application：应用

### 5.2 AOP

**AOP 原理**
- JDK 动态代理：基于接口
- CGLIB 代理：基于继承

**AOP 术语**
- 切面（Aspect）
- 连接点（Join Point）
- 切点（Pointcut）
- 通知（Advice）
- 目标对象（Target）
- 代理对象（Proxy）

### 5.3 事务管理

**事务传播行为**
- REQUIRED：默认，如果存在事务则加入，否则创建新事务
- REQUIRES_NEW：创建新事务
- SUPPORTS：如果存在事务则加入，否则非事务执行
- NOT_SUPPORTED：非事务执行
- MANDATORY：必须在事务中执行
- NEVER：不能在事务中执行
- NESTED：嵌套事务

**事务隔离级别**
- READ_UNCOMMITTED：读未提交
- READ_COMMITTED：读已提交
- REPEATABLE_READ：可重复读
- SERIALIZABLE：串行化

### 5.4 Spring Boot

**自动配置原理**
- @SpringBootApplication
- @EnableAutoConfiguration
- spring.factories
- 条件注解（@ConditionalOnClass 等）

**Starter 机制**
- 依赖管理
- 自动配置
- 约定优于配置

---

## 6. 数据库优化

### 6.1 索引优化

**B+ 树索引**
- 聚簇索引：数据和索引存储在一起（InnoDB）
- 非聚簇索引：数据和索引分离（MyISAM）

**索引类型**
- 主键索引（PRIMARY KEY）
- 唯一索引（UNIQUE）
- 普通索引（INDEX）
- 联合索引（复合索引）

**索引优化原则**
1. 最左前缀原则
2. 避免在 WHERE 子句中使用函数
3. 避免使用 SELECT *
4. 合理使用覆盖索引

### 6.2 SQL 优化

**查询优化**
- 避免全表扫描
- 使用索引
- 避免使用 OR
- 使用 UNION 代替 OR
- 避免在 WHERE 子句中使用 != 或 <>
- 避免在 WHERE 子句中使用函数

**分页优化**
- 避免深度分页
- 使用子查询优化
- 使用游标分页

### 6.3 MySQL 原理

**InnoDB 存储引擎**
- 支持事务
- 行级锁
- 外键约束
- 聚簇索引

**事务隔离级别**
- READ UNCOMMITTED：读未提交
- READ COMMITTED：读已提交
- REPEATABLE READ：可重复读（默认）
- SERIALIZABLE：串行化

**锁机制**
- 表锁：MyISAM
- 行锁：InnoDB
- 间隙锁：防止幻读
- 临键锁：行锁 + 间隙锁

---

## 7. 分布式系统

### 7.1 分布式锁

**实现方式**
- 数据库锁
- Redis 锁
- Zookeeper 锁

**Redis 分布式锁**
- SETNX + EXPIRE
- Redisson
- 锁续期

### 7.2 分布式事务

**CAP 理论**
- Consistency：一致性
- Availability：可用性
- Partition tolerance：分区容错性

**BASE 理论**
- Basically Available：基本可用
- Soft state：软状态
- Eventually consistent：最终一致性

**分布式事务解决方案**
- 2PC（两阶段提交）
- 3PC（三阶段提交）
- TCC（Try-Confirm-Cancel）
- 消息事务
- Saga 模式

### 7.3 分布式 ID

**生成方式**
- UUID
- 数据库自增 ID
- Redis 自增 ID
- 雪花算法（Snowflake）
- 美团 Leaf

---

## 8. 微服务架构

### 8.1 服务注册与发现

**Eureka**
- 服务注册
- 服务发现
- 心跳检测

**Consul**
- 服务发现
- 健康检查
- Key/Value 存储

**Nacos**
- 服务注册与发现
- 配置管理
- 动态 DNS

### 8.2 服务网关

**Spring Cloud Gateway**
- 路由转发
- 过滤器
- 限流

**Zuul**
- 动态路由
- 监控
- 弹性

### 8.3 服务调用

**Ribbon**
- 客户端负载均衡
- 轮询、随机、加权轮询

**Feign**
- 声明式 HTTP 客户端
- 集成 Ribbon
- 集成 Hystrix

**OpenFeign**
- Feign 的增强版
- 支持 Spring MVC 注解

### 8.4 服务容错

**Hystrix**
- 熔断器
- 降级
- 限流

**Sentinel**
- 流量控制
- 熔断降级
- 系统负载保护

---

## 📊 面试重点总结

### 高频面试题

1. **JVM 相关**
   - 内存模型和 GC 机制
   - 类加载机制
   - 内存溢出排查

2. **并发编程**
   - synchronized 和 volatile 的区别
   - CAS 原理和 ABA 问题
   - 线程池参数和拒绝策略
   - AQS 原理

3. **集合框架**
   - HashMap 实现原理
   - ConcurrentHashMap 实现原理
   - ArrayList 和 LinkedList 的区别

4. **设计模式**
   - 单例模式的多种实现
   - 工厂模式和抽象工厂模式
   - 代理模式和动态代理

5. **Spring 框架**
   - IOC 和 AOP 原理
   - Bean 生命周期
   - 事务传播机制
   - Spring Boot 自动配置原理

6. **数据库**
   - MySQL 索引原理
   - 事务隔离级别
   - 锁机制
   - SQL 优化

---

**最后更新：2026-01-26**
