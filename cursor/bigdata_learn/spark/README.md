# Spark 学习知识点

## 目录
1. [Spark 基础概念](#1-spark-基础概念)
2. [RDD 操作](#2-rdd-操作)
3. [DataFrame 和 Dataset](#3-dataframe-和-dataset)
4. [Spark SQL](#4-spark-sql)
5. [Spark Streaming](#5-spark-streaming)
6. [Spark MLlib](#6-spark-mllib)
7. [性能优化](#7-性能优化)
8. [案例与验证数据](#8-案例与验证数据)

---

## 1. Spark 基础概念

### 1.1 什么是 Spark
- Apache Spark 是一个快速、通用的大数据处理引擎
- 支持批处理、流处理、机器学习、图计算
- 基于内存计算，比 MapReduce 快 10-100 倍
- 支持 Scala、Java、Python、R 等多种语言

### 1.2 Spark 架构
- **Driver**：主程序，负责任务调度
- **Executor**：工作节点，执行任务
- **Cluster Manager**：集群管理器（Standalone、YARN、Mesos、Kubernetes）
- **SparkContext**：Spark 应用的入口点
- **SparkSession**：Spark SQL 的入口点（Spark 2.0+）

### 1.3 Spark 核心组件
- **Spark Core**：核心引擎，提供 RDD API
- **Spark SQL**：结构化数据处理
- **Spark Streaming**：流数据处理
- **MLlib**：机器学习库
- **GraphX**：图计算库

---

## 2. RDD 操作

### 2.1 RDD 基础
**RDD（Resilient Distributed Dataset）**：弹性分布式数据集
- 不可变的分布式数据集合
- 支持容错（通过 Lineage 恢复）
- 可并行操作

### 2.2 RDD 创建
```scala
// 从集合创建
val rdd = sc.parallelize(Seq(1, 2, 3, 4, 5))

// 从文件创建
val rdd = sc.textFile("path/to/file.txt")

// 从其他 RDD 转换
val rdd2 = rdd.map(x => x * 2)
```

```python
# PySpark
rdd = sc.parallelize([1, 2, 3, 4, 5])
rdd = sc.textFile("path/to/file.txt")
rdd2 = rdd.map(lambda x: x * 2)
```

### 2.3 Transformation（转换操作）
- **map**：一对一转换
- **filter**：过滤
- **flatMap**：一对多转换
- **mapPartitions**：按分区转换
- **union**：合并
- **intersection**：交集
- **distinct**：去重
- **groupByKey**：按键分组
- **reduceByKey**：按键聚合
- **sortBy**：排序
- **join**：连接

### 2.4 Action（行动操作）
- **collect**：收集所有数据到 Driver
- **count**：计数
- **first**：取第一个元素
- **take**：取前 n 个元素
- **reduce**：归约
- **foreach**：遍历
- **saveAsTextFile**：保存为文本文件

---

## 3. DataFrame 和 Dataset

### 3.1 DataFrame
- 基于 RDD 的分布式数据集合
- 具有 Schema（结构信息）
- 支持 SQL 查询
- 类型安全（Dataset）

### 3.2 创建 DataFrame
```scala
// 从 RDD 创建
val df = spark.createDataFrame(rdd, schema)

// 从文件创建
val df = spark.read.json("path/to/file.json")
val df = spark.read.csv("path/to/file.csv")

// 从集合创建
val df = spark.createDataFrame(data, schema)
```

```python
# PySpark
df = spark.createDataFrame(data, schema)
df = spark.read.json("path/to/file.json")
df = spark.read.csv("path/to/file.csv")
```

### 3.3 DataFrame 操作
- **select**：选择列
- **filter/where**：过滤
- **groupBy**：分组
- **agg**：聚合
- **join**：连接
- **orderBy**：排序
- **withColumn**：添加列
- **drop**：删除列

---

## 4. Spark SQL

### 4.1 Spark SQL 基础
- 支持标准 SQL 查询
- 支持 Hive 兼容
- 支持多种数据源（JSON、Parquet、JDBC 等）

### 4.2 创建临时视图
```scala
df.createOrReplaceTempView("table_name")
spark.sql("SELECT * FROM table_name")
```

```python
df.createOrReplaceTempView("table_name")
spark.sql("SELECT * FROM table_name")
```

### 4.3 常用 SQL 函数
- **聚合函数**：COUNT、SUM、AVG、MAX、MIN
- **字符串函数**：CONCAT、SUBSTRING、UPPER、LOWER
- **日期函数**：CURRENT_DATE、YEAR、MONTH、DAY
- **窗口函数**：ROW_NUMBER、RANK、DENSE_RANK

---

## 5. Spark Streaming

### 5.1 流处理基础
- 微批处理（Micro-batch）
- 支持 Kafka、Flume、TCP Socket 等数据源
- 支持有状态处理

### 5.2 DStream 操作
```scala
val stream = ssc.socketTextStream("localhost", 9999)
val words = stream.flatMap(_.split(" "))
val wordCounts = words.map(x => (x, 1)).reduceByKey(_ + _)
wordCounts.print()
```

```python
stream = ssc.socketTextStream("localhost", 9999)
words = stream.flatMap(lambda line: line.split(" "))
wordCounts = words.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b)
wordCounts.print()
```

---

## 6. Spark MLlib

### 6.1 机器学习流程
1. **数据准备**：特征提取、转换
2. **模型训练**：选择算法、训练模型
3. **模型评估**：评估指标
4. **模型预测**：使用模型预测

### 6.2 常用算法
- **分类**：逻辑回归、决策树、随机森林
- **回归**：线性回归、岭回归
- **聚类**：K-means
- **推荐**：协同过滤

---

## 7. 性能优化

### 7.1 缓存和持久化
```scala
rdd.cache()        // 内存缓存
rdd.persist()      // 持久化
rdd.unpersist()    // 取消持久化
```

### 7.2 分区优化
- **repartition**：重新分区（会 shuffle）
- **coalesce**：合并分区（不 shuffle）
- **partitionBy**：按列分区

### 7.3 广播变量和累加器
```scala
// 广播变量（只读）
val broadcastVar = sc.broadcast(Array(1, 2, 3))

// 累加器（只写）
val accum = sc.longAccumulator("My Accumulator")
```

---

## 8. 案例与验证数据

详见以下文件：
- [案例1：RDD 基础操作](cases/rdd_basics.md)
- [案例2：DataFrame 操作](cases/dataframe_operations.md)
- [案例3：数据分析实战](cases/data_analysis.md)
- [案例4：Spark SQL 应用](cases/spark_sql.md)
- [验证数据文件](data/)
