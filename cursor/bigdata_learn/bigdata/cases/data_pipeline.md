# 数据管道案例

## 案例概述

本案例通过实际配置演示数据管道的构建，包括数据采集、ETL、数据质量等。

## 知识点

1. **数据采集**
   - Flume
   - Sqoop
   - DataX

2. **ETL 流程**
   - 数据提取
   - 数据转换
   - 数据加载

3. **数据质量**
   - 数据校验
   - 数据清洗
   - 监控告警

## 案例代码

### 案例1：Flume 配置

```properties
# flume.conf
# Agent 名称
agent.sources = r1
agent.sinks = k1
agent.channels = c1

# Source 配置
agent.sources.r1.type = spooldir
agent.sources.r1.spoolDir = /data/flume/spool
agent.sources.r1.channels = c1

# Channel 配置
agent.channels.c1.type = memory
agent.channels.c1.capacity = 10000
agent.channels.c1.transactionCapacity = 1000

# Sink 配置
agent.sinks.k1.type = hdfs
agent.sinks.k1.hdfs.path = hdfs://namenode:9000/data/flume/%Y-%m-%d
agent.sinks.k1.hdfs.fileType = DataStream
agent.sinks.k1.hdfs.writeFormat = Text
agent.sinks.k1.channel = c1
```

### 案例2：Sqoop 数据导入

```bash
#!/bin/bash
# sqoop_import.sh

# 从 MySQL 导入到 HDFS
sqoop import \
  --connect jdbc:mysql://mysql-server:3306/mydb \
  --username user \
  --password pass \
  --table users \
  --target-dir /data/sqoop/users \
  --fields-terminated-by ',' \
  --num-mappers 4

# 从 MySQL 导入到 Hive
sqoop import \
  --connect jdbc:mysql://mysql-server:3306/mydb \
  --username user \
  --password pass \
  --table users \
  --hive-import \
  --hive-table users \
  --create-hive-table \
  --hive-overwrite

# 增量导入
sqoop import \
  --connect jdbc:mysql://mysql-server:3306/mydb \
  --username user \
  --password pass \
  --table users \
  --target-dir /data/sqoop/users \
  --incremental append \
  --check-column id \
  --last-value 1000
```

### 案例3：数据质量检查

```python
# data_quality.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, isnan, isnull

spark = SparkSession.builder.appName("DataQuality").getOrCreate()

df = spark.read.parquet("hdfs://namenode:9000/data/input")

# 数据质量检查
quality_report = {
    "total_rows": df.count(),
    "null_counts": {},
    "duplicate_rows": df.count() - df.dropDuplicates().count(),
    "data_types": {}
}

# 检查空值
for column in df.columns:
    null_count = df.filter(col(column).isNull()).count()
    quality_report["null_counts"][column] = null_count

# 数据范围检查
df_stats = df.describe()
print(df_stats.show())

# 数据清洗
df_cleaned = df \
    .filter(col("age").isNotNull()) \
    .filter(col("age") > 0) \
    .filter(col("age") < 150) \
    .dropDuplicates()

# 保存清洗后的数据
df_cleaned.write.parquet("hdfs://namenode:9000/data/cleaned")
```

## 验证数据

### 数据管道性能

| 阶段 | 数据量 | 耗时 | 说明 |
|-----|--------|------|------|
| 采集 | 10GB | 5min | Flume |
| ETL | 10GB | 10min | Spark |
| 加载 | 10GB | 2min | Hive |

## 总结

1. **数据采集**
   - 选择合适的工具
   - 配置合理的批次大小
   - 监控采集进度

2. **ETL 流程**
   - 数据清洗
   - 数据转换
   - 数据验证

3. **数据质量**
   - 建立质量规则
   - 定期检查
   - 告警机制
