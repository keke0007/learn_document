# 大数据离线与实时开发知识点总览

## 📚 目录

1. [Hadoop 生态系统](#1-hadoop-生态系统)
2. [Spark 离线批处理](#2-spark-离线批处理)
3. [Flink 实时流处理](#3-flink-实时流处理)
4. [Kafka 流式数据](#4-kafka-流式数据)
5. [数据存储](#5-数据存储)
6. [数据管道](#6-数据管道)
7. [性能优化](#7-性能优化)
8. [架构设计](#8-架构设计)

---

## 1. Hadoop 生态系统

### 1.1 HDFS

**核心概念**
- NameNode：元数据管理
- DataNode：数据存储
- Secondary NameNode：辅助 NameNode
- 副本机制：默认3副本

**特点**
- 适合大文件存储
- 流式访问模式
- 高容错性
- 可扩展性

### 1.2 MapReduce

**编程模型**
- Map 阶段：数据映射
- Shuffle 阶段：数据排序和分组
- Reduce 阶段：数据聚合

**执行流程**
1. Input：数据输入
2. Map：映射处理
3. Shuffle：数据重排
4. Reduce：聚合处理
5. Output：结果输出

### 1.3 YARN

**组件**
- ResourceManager：资源管理
- NodeManager：节点管理
- ApplicationMaster：应用管理

**资源调度**
- FIFO Scheduler
- Capacity Scheduler
- Fair Scheduler

---

## 2. Spark 离线批处理

### 2.1 Spark Core

**RDD（弹性分布式数据集）**
- 不可变
- 分区存储
- 容错机制
- 延迟计算

**操作类型**
- 转换操作（Transformation）：延迟执行
- 行动操作（Action）：触发计算

**宽窄依赖**
- 窄依赖：一对一或一对多
- 宽依赖：多对一（Shuffle）

### 2.2 Spark SQL

**DataFrame**
- 结构化数据
- 列式存储
- 优化执行计划

**Dataset**
- 类型安全
- 编译时检查
- 更好的性能

### 2.3 性能优化

**分区优化**
- 合理设置分区数
- 避免小文件
- 数据倾斜处理

**Shuffle 优化**
- 减少 Shuffle
- 使用广播变量
- 启用 AQE

---

## 3. Flink 实时流处理

### 3.1 DataStream API

**数据源**
- 文件系统
- Kafka
- 自定义 Source

**转换操作**
- Map、FlatMap
- Filter
- KeyBy
- Window

### 3.2 时间语义

**事件时间（Event Time）**
- 事件发生时间
- 准确性高
- 需要 Watermark

**处理时间（Processing Time）**
- 处理时间
- 延迟低
- 简单易用

**摄入时间（Ingestion Time）**
- 摄入时间
- 平衡准确性和延迟

### 3.3 窗口操作

**窗口类型**
- 滚动窗口（Tumbling）
- 滑动窗口（Sliding）
- 会话窗口（Session）

**窗口函数**
- 增量聚合：Reduce、Aggregate
- 全量聚合：ProcessWindowFunction

---

## 4. Kafka 流式数据

### 4.1 核心概念

**Topic 和 Partition**
- Topic：主题
- Partition：分区
- 副本：保证可靠性

**Producer**
- 消息发送
- 分区策略
- 可靠性保证

**Consumer**
- 消息消费
- 消费者组
- 偏移量管理

### 4.2 Kafka Streams

**流处理**
- 状态存储
- 窗口操作
- 表连接

**应用场景**
- 实时数据转换
- 流式聚合
- 事件驱动应用

---

## 5. 数据存储

### 5.1 Hive

**数据仓库**
- 基于 HDFS
- SQL 查询
- 分区和分桶

**存储格式**
- TextFile
- SequenceFile
- Parquet
- ORC

### 5.2 HBase

**NoSQL 数据库**
- 列式存储
- 随机读写
- 实时查询

**数据模型**
- Row Key
- Column Family
- Column Qualifier
- Timestamp

---

## 6. 数据管道

### 6.1 数据采集

**Flume**
- 日志收集
- 实时传输
- 可靠性保证

**Sqoop**
- 关系数据库导入导出
- 批量传输
- 增量导入

### 6.2 ETL 流程

**提取（Extract）**
- 多数据源
- 增量提取
- 数据验证

**转换（Transform）**
- 数据清洗
- 数据转换
- 数据质量

**加载（Load）**
- 目标系统
- 批量加载
- 增量更新

---

## 7. 性能优化

### 7.1 Spark 优化

**资源优化**
- 合理设置 Executor 数量
- 内存分配
- CPU 核心数

**数据优化**
- 分区优化
- 数据倾斜处理
- 缓存策略

### 7.2 Flink 优化

**并行度**
- 合理设置并行度
- 资源利用
- 延迟控制

**状态优化**
- 状态后端选择
- Checkpoint 配置
- 状态清理

---

## 8. 架构设计

### 8.1 Lambda 架构

**批处理层**
- 完整数据
- 高延迟
- 准确性高

**速度层**
- 实时数据
- 低延迟
- 近似结果

**服务层**
- 查询服务
- 结果合并

### 8.2 Kappa 架构

**流处理**
- 统一流处理
- 简化架构
- 实时性高

---

## 📊 面试重点总结

### 高频面试题

1. **Hadoop**
   - HDFS 原理
   - MapReduce 执行流程
   - YARN 资源管理

2. **Spark**
   - RDD vs DataFrame
   - 宽窄依赖
   - 数据倾斜处理
   - Spark SQL 优化

3. **Flink**
   - 流处理和批处理
   - 时间语义
   - 窗口操作
   - 状态管理

4. **Kafka**
   - Topic 和 Partition
   - 消息存储
   - 消费者组
   - 顺序保证

5. **数据存储**
   - Hive 分区和分桶
   - HBase 行键设计
   - 存储格式选择

### 手写代码题

1. **Spark**
   - WordCount
   - 数据聚合
   - 数据倾斜处理

2. **Flink**
   - 窗口聚合
   - 状态处理
   - 流式 SQL

3. **Kafka**
   - Producer
   - Consumer
   - Kafka Streams

---

**最后更新：2026-01-26**
