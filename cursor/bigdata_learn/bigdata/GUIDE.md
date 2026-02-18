# 大数据离线与实时开发学习指南

## 📚 项目概述

本指南提供了完整的大数据离线与实时开发学习资源，包括 Hadoop、Spark、Flink、Kafka 等核心技术，涵盖离线批处理和实时流处理，帮助你系统掌握大数据开发技术。

---

## 📁 项目结构

```
bigdata/
├── GUIDE.md                     # 本指南文档（快速入门）
├── README.md                    # 大数据开发知识点总览（详细文档）
├── cases/                       # 实战案例目录
│   ├── hadoop_ecosystem.md     # 案例1：Hadoop 生态系统
│   ├── spark_batch.md          # 案例2：Spark 离线批处理
│   ├── flink_streaming.md      # 案例3：Flink 实时流处理
│   ├── kafka_streaming.md      # 案例4：Kafka 流式数据
│   ├── hive_hbase.md           # 案例5：Hive 和 HBase
│   └── data_pipeline.md        # 案例6：数据管道
├── data/                        # 验证数据目录
│   ├── sample_data.csv          # 示例数据
│   ├── streaming_data.json      # 流式数据
│   └── performance_test.txt     # 性能测试数据
└── scripts/                     # 代码示例目录
    ├── spark_batch.py           # Spark 批处理示例
    ├── flink_streaming.java     # Flink 流处理示例
    ├── kafka_producer.py        # Kafka 生产者示例
    └── hive_query.hql           # Hive 查询示例
```

---

## 🎯 学习路径

### 阶段一：Hadoop 生态系统（10-14天）
1. **HDFS**
   - 分布式文件系统
   - 数据存储和读取
   - 副本机制

2. **MapReduce**
   - MapReduce 编程模型
   - 作业调度
   - 性能优化

3. **YARN**
   - 资源管理
   - 任务调度
   - 集群管理

### 阶段二：Spark 离线批处理（10-14天）
1. **Spark Core**
   - RDD 编程
   - 转换和行动操作
   - 持久化机制

2. **Spark SQL**
   - DataFrame 和 Dataset
   - SQL 查询
   - 数据源集成

3. **Spark 优化**
   - 分区优化
   - 广播变量
   - 数据倾斜处理

### 阶段三：Flink 实时流处理（10-14天）
1. **Flink 基础**
   - DataStream API
   - 窗口操作
   - 时间语义

2. **流处理**
   - 事件时间处理
   - 状态管理
   - 容错机制

3. **Flink SQL**
   - 流式 SQL
   - 表连接
   - 动态表

### 阶段四：Kafka 流式数据（7-10天）
1. **Kafka 基础**
   - Topic 和 Partition
   - Producer 和 Consumer
   - 消息存储

2. **Kafka Streams**
   - 流处理应用
   - 状态存储
   - 窗口操作

### 阶段五：数据存储（7-10天）
1. **Hive**
   - 数据仓库
   - HQL 查询
   - 分区和分桶

2. **HBase**
   - NoSQL 数据库
   - 列族设计
   - 读写优化

### 阶段六：数据管道（7-10天）
1. **数据采集**
   - Flume
   - Sqoop
   - DataX

2. **数据管道**
   - ETL 流程
   - 数据质量
   - 监控告警

---

## 📖 核心知识点详解

### 1. Hadoop 生态系统

#### 知识点概述
Hadoop 是大数据的基础框架，包括 HDFS、MapReduce、YARN 等核心组件。

#### HDFS

**核心概念**
- NameNode：元数据管理
- DataNode：数据存储
- 副本机制：默认3副本
- 块大小：128MB（Hadoop 2.x）

**常用命令**
```bash
# 文件操作
hdfs dfs -ls /
hdfs dfs -put local.txt /data/
hdfs dfs -get /data/remote.txt
hdfs dfs -mkdir -p /data/input
hdfs dfs -rm /data/old.txt

# 查看文件系统
hdfs dfs -df -h
hdfs dfsadmin -report
```

#### MapReduce

**编程模型**
- Map 阶段：数据映射
- Shuffle 阶段：数据排序和分组
- Reduce 阶段：数据聚合

**案例代码**

```java
// WordCount.java
public class WordCount {
    public static class TokenizerMapper 
        extends Mapper<Object, Text, Text, IntWritable> {
        
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();
        
        public void map(Object key, Text value, Context context) 
            throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }
    
    public static class IntSumReducer 
        extends Reducer<Text, IntWritable, Text, IntWritable> {
        
        private IntWritable result = new IntWritable();
        
        public void reduce(Text key, Iterable<IntWritable> values, 
                          Context context) 
            throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }
}
```

---

### 2. Spark 离线批处理

#### 知识点概述
Spark 是基于内存计算的分布式计算框架，适合离线批处理和交互式查询。

#### Spark Core

**RDD 操作**
```python
# spark_batch.py
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("WordCount")
sc = SparkContext(conf=conf)

# 读取数据
lines = sc.textFile("hdfs://namenode:9000/data/input.txt")

# 转换操作
words = lines.flatMap(lambda line: line.split(" "))
wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# 行动操作
result = wordCounts.collect()
for word, count in result:
    print(f"{word}: {count}")

sc.stop()
```

#### Spark SQL

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkSQL") \
    .getOrCreate()

# 读取数据
df = spark.read.csv("hdfs://namenode:9000/data/users.csv", 
                   header=True, inferSchema=True)

# SQL 查询
df.createOrReplaceTempView("users")
result = spark.sql("""
    SELECT department, COUNT(*) as count, AVG(salary) as avg_salary
    FROM users
    GROUP BY department
    ORDER BY count DESC
""")

result.show()
```

---

### 3. Flink 实时流处理

#### 知识点概述
Flink 是流式处理框架，支持低延迟、高吞吐的实时数据处理。

#### Flink DataStream

```java
// flink_streaming.java
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.time.Time;

public class FlinkStreaming {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // 读取 Kafka 数据源
        DataStream<String> stream = env
            .addSource(new FlinkKafkaConsumer<>("topic", 
                new SimpleStringSchema(), kafkaProps));
        
        // 数据处理
        stream
            .map(new MapFunction<String, Tuple2<String, Integer>>() {
                @Override
                public Tuple2<String, Integer> map(String value) {
                    String[] parts = value.split(",");
                    return new Tuple2<>(parts[0], Integer.parseInt(parts[1]));
                }
            })
            .keyBy(0)
            .timeWindow(Time.minutes(5))
            .sum(1)
            .print();
        
        env.execute("Flink Streaming Job");
    }
}
```

---

### 4. Kafka 流式数据

#### 知识点概述
Kafka 是分布式消息队列，用于构建实时数据管道和流式应用。

#### Kafka Producer

```python
# kafka_producer.py
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 发送消息
for i in range(100):
    message = {
        'id': i,
        'timestamp': '2024-01-26 10:00:00',
        'value': i * 10
    }
    producer.send('test-topic', message)

producer.flush()
producer.close()
```

#### Kafka Consumer

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

for message in consumer:
    print(f"Received: {message.value}")
```

---

### 5. Hive 数据仓库

#### 知识点概述
Hive 是基于 Hadoop 的数据仓库工具，提供 SQL 查询能力。

#### Hive 查询

```sql
-- hive_query.hql
-- 创建表
CREATE TABLE IF NOT EXISTS users (
    id BIGINT,
    name STRING,
    age INT,
    department STRING,
    salary DECIMAL(10,2)
)
PARTITIONED BY (dt STRING)
STORED AS PARQUET;

-- 加载数据
LOAD DATA INPATH 'hdfs://namenode:9000/data/users/' 
INTO TABLE users PARTITION (dt='2024-01-26');

-- 查询
SELECT department, 
       COUNT(*) as count,
       AVG(salary) as avg_salary,
       MAX(salary) as max_salary
FROM users
WHERE dt = '2024-01-26'
GROUP BY department
ORDER BY avg_salary DESC;
```

---

## 📊 面试重点总结

### 高频面试题

1. **Hadoop 生态系统**
   - HDFS 原理和架构
   - MapReduce 编程模型
   - YARN 资源管理

2. **Spark**
   - RDD 和 DataFrame
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
   - 消息存储机制
   - 消费者组
   - 消息顺序保证

5. **数据存储**
   - Hive 分区和分桶
   - HBase 行键设计
   - 数据模型选择

### 学习建议

1. **理论与实践结合**
   - 理解原理后，通过代码验证
   - 搭建实验环境练习

2. **循序渐进**
   - 先掌握基础，再深入高级特性
   - 每个知识点都要有代码示例

3. **持续练习**
   - 定期回顾知识点
   - 参与实际项目实践
   - 关注大数据技术更新

4. **面试准备**
   - 准备项目经验描述
   - 准备技术难点和解决方案
   - 准备性能优化案例

---

## 🔧 工具推荐

### 开发工具
- **IDE**：IntelliJ IDEA、VS Code
- **构建工具**：Maven、SBT
- **版本控制**：Git

### 大数据工具
- **Hadoop**：分布式存储和计算
- **Spark**：内存计算框架
- **Flink**：流处理框架
- **Kafka**：消息队列
- **Hive**：数据仓库
- **HBase**：NoSQL 数据库

---

## 📚 参考资源

### 官方文档
1. **Hadoop 官方文档**：https://hadoop.apache.org/docs/
2. **Spark 官方文档**：https://spark.apache.org/docs/
3. **Flink 官方文档**：https://flink.apache.org/docs/
4. **Kafka 官方文档**：https://kafka.apache.org/documentation/

### 在线资源
1. **大数据技术博客**：各种技术博客
2. **GitHub**：搜索相关开源项目源码

---

## ✅ 学习检查清单

- [ ] 理解 Hadoop 生态系统
- [ ] 掌握 Spark 批处理
- [ ] 熟悉 Flink 流处理
- [ ] 理解 Kafka 消息队列
- [ ] 掌握 Hive 数据仓库
- [ ] 熟悉 HBase NoSQL
- [ ] 能够设计数据管道
- [ ] 了解性能优化方法

---

**最后更新：2026-01-26**
