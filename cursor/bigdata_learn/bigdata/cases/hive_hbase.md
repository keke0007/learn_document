# Hive 和 HBase 案例

## 案例概述

本案例通过实际 SQL 和配置演示 Hive 和 HBase 的使用。

## 知识点

1. **Hive**
   - 数据仓库
   - HQL 查询
   - 分区和分桶

2. **HBase**
   - NoSQL 数据库
   - 列族设计
   - 读写优化

## 案例代码

### 案例1：Hive 表操作

```sql
-- hive_tables.hql
-- 创建内部表
CREATE TABLE IF NOT EXISTS users (
    id BIGINT,
    name STRING,
    age INT,
    email STRING,
    salary DECIMAL(10,2)
)
STORED AS PARQUET
LOCATION '/user/hive/warehouse/users';

-- 创建外部表
CREATE EXTERNAL TABLE IF NOT EXISTS logs (
    timestamp STRING,
    level STRING,
    message STRING
)
PARTITIONED BY (dt STRING, hour STRING)
STORED AS TEXTFILE
LOCATION '/data/logs';

-- 添加分区
ALTER TABLE logs ADD PARTITION (dt='2024-01-26', hour='10')
LOCATION '/data/logs/2024-01-26/10';

-- 加载数据
LOAD DATA INPATH 'hdfs://namenode:9000/data/users.csv'
INTO TABLE users;

-- 插入数据
INSERT INTO TABLE users
SELECT id, name, age, email, salary
FROM temp_users;

-- 查询
SELECT department, 
       COUNT(*) as count,
       AVG(salary) as avg_salary
FROM users
WHERE age > 25
GROUP BY department
ORDER BY avg_salary DESC;
```

### 案例2：HBase 操作

```java
// HBaseOperations.java
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.util.Bytes;

Configuration config = HBaseConfiguration.create();
config.set("hbase.zookeeper.quorum", "localhost");

Connection connection = ConnectionFactory.createConnection(config);
Table table = connection.getTable(TableName.valueOf("users"));

// 插入数据
Put put = new Put(Bytes.toBytes("user001"));
put.addColumn(Bytes.toBytes("info"), Bytes.toBytes("name"), Bytes.toBytes("Alice"));
put.addColumn(Bytes.toBytes("info"), Bytes.toBytes("age"), Bytes.toBytes("25"));
put.addColumn(Bytes.toBytes("contact"), Bytes.toBytes("email"), Bytes.toBytes("alice@example.com"));
table.put(put);

// 查询数据
Get get = new Get(Bytes.toBytes("user001"));
Result result = table.get(get);
byte[] name = result.getValue(Bytes.toBytes("info"), Bytes.toBytes("name"));
System.out.println("Name: " + Bytes.toString(name));

// 扫描数据
Scan scan = new Scan();
scan.addColumn(Bytes.toBytes("info"), Bytes.toBytes("name"));
ResultScanner scanner = table.getScanner(scan);
for (Result res : scanner) {
    System.out.println(Bytes.toString(res.getValue(Bytes.toBytes("info"), Bytes.toBytes("name"))));
}

table.close();
connection.close();
```

## 验证数据

### Hive 性能

| 数据量 | 查询时间 | 说明 |
|--------|---------|------|
| 10GB | 30s | 全表扫描 |
| 100GB | 5min | 全表扫描 |
| 100GB（分区） | 30s | 单分区查询 |

### HBase 性能

| 操作 | 延迟 | 吞吐量 |
|-----|------|--------|
| 单行读取 | <10ms | 10000 ops/s |
| 批量读取 | <50ms | 50000 ops/s |
| 写入 | <20ms | 50000 ops/s |

## 总结

1. **Hive**
   - 适合分析查询
   - 使用分区优化
   - 选择合适的存储格式

2. **HBase**
   - 适合随机读写
   - 合理设计行键
   - 列族设计优化
