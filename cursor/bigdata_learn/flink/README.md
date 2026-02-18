# Flink 学习知识点

## 目录
1. [Flink 基础概念](#1-flink-基础概念)
2. [DataStream API](#2-datastream-api)
3. [Table API & SQL](#3-table-api--sql)
4. [窗口操作](#4-窗口操作)
5. [时间语义](#5-时间语义)
6. [状态管理](#6-状态管理)
7. [容错机制](#7-容错机制)
8. [连接器](#8-连接器)
9. [案例与验证数据](#9-案例与验证数据)

---

## 1. Flink 基础概念

### 1.1 什么是 Flink
- Apache Flink 是一个分布式流处理框架
- 支持批处理和流处理（批流一体）
- 低延迟、高吞吐、精确一次（Exactly-Once）语义
- 支持事件时间（Event Time）处理

### 1.2 Flink 架构
- **JobManager**：作业管理器，负责任务调度和协调
- **TaskManager**：任务管理器，执行实际的数据处理任务
- **Client**：客户端，提交作业到集群
- **DataStream**：数据流抽象
- **Operator**：算子，数据转换操作

### 1.3 Flink 核心特性
- **流处理**：真正的流处理引擎
- **批流一体**：同一套 API 处理批和流
- **状态管理**：内置状态管理
- **容错机制**：Checkpoint 和 Savepoint
- **时间语义**：Event Time、Processing Time、Ingestion Time

---

## 2. DataStream API

### 2.1 创建执行环境
```java
// Java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
```

```scala
// Scala
val env = StreamExecutionEnvironment.getExecutionEnvironment
```

### 2.2 数据源（Source）
- **集合数据源**：`fromCollection()`
- **文件数据源**：`readTextFile()`
- **Socket 数据源**：`socketTextStream()`
- **Kafka 数据源**：`FlinkKafkaConsumer`
- **自定义数据源**：实现 `SourceFunction`

### 2.3 数据转换（Transformation）
- **map**：一对一转换
- **flatMap**：一对多转换
- **filter**：过滤
- **keyBy**：按键分组
- **reduce**：归约
- **aggregate**：聚合
- **union**：合并流
- **connect**：连接流
- **split/select**：分流

### 2.4 数据汇（Sink）
- **文件输出**：`writeAsText()`
- **打印输出**：`print()`
- **Kafka 输出**：`FlinkKafkaProducer`
- **数据库输出**：JDBC Sink
- **自定义 Sink**：实现 `SinkFunction`

---

## 3. Table API & SQL

### 3.1 Table API 基础
```java
// 创建 TableEnvironment
StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);

// 将 DataStream 转换为 Table
Table table = tableEnv.fromDataStream(dataStream);

// 执行 Table API 查询
Table result = table.select("name, age").where("age > 18");
```

### 3.2 SQL 查询
```sql
-- 注册表
tableEnv.createTemporaryView("users", dataStream);

-- SQL 查询
Table result = tableEnv.sqlQuery("SELECT name, age FROM users WHERE age > 18");
```

### 3.3 窗口表函数
- **TUMBLE**：滚动窗口
- **HOP**：滑动窗口
- **SESSION**：会话窗口

---

## 4. 窗口操作

### 4.1 窗口类型
- **滚动窗口（Tumbling Window）**：固定大小，不重叠
- **滑动窗口（Sliding Window）**：固定大小，有重叠
- **会话窗口（Session Window）**：基于活动间隔
- **全局窗口（Global Window）**：所有数据一个窗口

### 4.2 窗口分配器
```java
// 滚动时间窗口
.window(TumblingEventTimeWindows.of(Time.seconds(5)))

// 滑动时间窗口
.window(SlidingEventTimeWindows.of(Time.seconds(10), Time.seconds(5)))

// 滚动计数窗口
.countWindow(100)

// 会话窗口
.window(EventTimeSessionWindows.withGap(Time.minutes(5)))
```

### 4.3 窗口函数
- **增量聚合函数**：ReduceFunction、AggregateFunction
- **全量窗口函数**：WindowFunction、ProcessWindowFunction

---

## 5. 时间语义

### 5.1 时间类型
- **Event Time**：事件时间（数据产生的时间）
- **Processing Time**：处理时间（系统处理时间）
- **Ingestion Time**：摄入时间（进入 Flink 的时间）

### 5.2 设置时间语义
```java
env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
```

### 5.3 水位线（Watermark）
```java
// 周期性水位线
.assignTimestampsAndWatermarks(
    WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(5))
        .withTimestampAssigner((event, timestamp) -> event.getTimestamp())
);
```

---

## 6. 状态管理

### 6.1 状态类型
- **Keyed State**：键控状态
  - ValueState
  - ListState
  - MapState
  - ReducingState
  - AggregatingState
- **Operator State**：算子状态
- **Broadcast State**：广播状态

### 6.2 状态使用
```java
// 定义状态描述符
ValueStateDescriptor<Long> stateDescriptor = 
    new ValueStateDescriptor<>("count", Long.class);

// 获取状态
ValueState<Long> countState = getRuntimeContext().getState(stateDescriptor);
```

---

## 7. 容错机制

### 7.1 Checkpoint
```java
// 启用 Checkpoint
env.enableCheckpointing(60000); // 60秒

// 配置 Checkpoint
CheckpointConfig checkpointConfig = env.getCheckpointConfig();
checkpointConfig.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
checkpointConfig.setMinPauseBetweenCheckpoints(500);
checkpointConfig.setCheckpointTimeout(600000);
```

### 7.2 Savepoint
```bash
# 创建 Savepoint
flink savepoint <jobId> <savepointPath>

# 从 Savepoint 恢复
flink run -s <savepointPath> <jarFile>
```

---

## 8. 连接器

### 8.1 常用连接器
- **Kafka**：`flink-connector-kafka`
- **文件系统**：`flink-connector-filesystem`
- **Elasticsearch**：`flink-connector-elasticsearch`
- **JDBC**：`flink-connector-jdbc`
- **Redis**：`flink-connector-redis`

### 8.2 Kafka 连接器示例
```java
// Kafka Source
FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
    "topic",
    new SimpleStringSchema(),
    properties
);

// Kafka Sink
FlinkKafkaProducer<String> producer = new FlinkKafkaProducer<>(
    "topic",
    new SimpleStringSchema(),
    properties
);
```

---

## 9. 案例与验证数据

详见以下文件：
- [案例1：DataStream 基础操作](cases/datastream_basics.md)
- [案例2：窗口操作](cases/window_operations.md)
- [案例3：Table API 应用](cases/table_api.md)
- [案例4：实时数据分析](cases/realtime_analysis.md)
- [验证数据文件](data/)
