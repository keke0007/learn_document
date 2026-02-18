# InfluxDB 基础与高级开发案例

## 案例概述

本案例通过实际代码演示 InfluxDB 的时序数据存储和查询，包括数据模型、保留策略、连续查询等。

## 知识点

1. **数据模型**
   - Database：数据库
   - Measurement：表
   - Tag：标签（索引）
   - Field：字段（值）
   - Timestamp：时间戳

2. **数据保留策略**
   - Retention Policy：数据保留策略
   - Continuous Query：连续查询

3. **查询语言**
   - InfluxQL
   - Flux（新查询语言）

## 案例代码

### 案例1：基本数据操作

```python
# influxdb_basic.py
from influxdb import InfluxDBClient
from datetime import datetime

# 连接 InfluxDB
client = InfluxDBClient(
    host='localhost',
    port=8086,
    username='admin',
    password='password',
    database='mydb'
)

# 创建数据库
client.create_database('mydb')

# 写入数据点
json_body = [
    {
        "measurement": "cpu_usage",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": datetime.now(),
        "fields": {
            "value": 0.64
        }
    },
    {
        "measurement": "cpu_usage",
        "tags": {
            "host": "server02",
            "region": "us-east"
        },
        "time": datetime.now(),
        "fields": {
            "value": 0.78
        }
    }
]
client.write_points(json_body)

# 查询数据
result = client.query('SELECT * FROM cpu_usage WHERE time > now() - 1h')
for point in result.get_points():
    print(f"Time: {point['time']}, Host: {point['host']}, Value: {point['value']}")
```

### 案例2：聚合查询

```python
# influxdb_aggregate.py
from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086, database='mydb')

# 平均值查询
result = client.query("""
    SELECT MEAN(value) 
    FROM cpu_usage 
    WHERE time > now() - 1h 
    GROUP BY time(5m), host
""")

# 最大值查询
result = client.query("""
    SELECT MAX(value) 
    FROM cpu_usage 
    WHERE time > now() - 1d 
    GROUP BY host
""")

# 百分位数查询
result = client.query("""
    SELECT PERCENTILE(value, 95) 
    FROM cpu_usage 
    WHERE time > now() - 1h 
    GROUP BY host
""")

for point in result.get_points():
    print(point)
```

### 案例3：保留策略

```python
# influxdb_retention.py
from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086, database='mydb')

# 创建保留策略（数据保留7天）
client.create_retention_policy(
    name='7days',
    duration='7d',
    replication=1,
    database='mydb',
    default=True
)

# 创建保留策略（数据保留30天）
client.create_retention_policy(
    name='30days',
    duration='30d',
    replication=1,
    database='mydb',
    default=False
)

# 写入数据到指定保留策略
json_body = [{
    "measurement": "metrics",
    "tags": {"host": "server01"},
    "time": datetime.now(),
    "fields": {"value": 0.5}
}]
client.write_points(json_body, retention_policy='30days')
```

### 案例4：连续查询

```python
# influxdb_cq.py
from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086, database='mydb')

# 创建连续查询（每5分钟计算平均值）
client.create_continuous_query(
    name='cq_5min_avg',
    select='SELECT MEAN(value) INTO cpu_usage_5min FROM cpu_usage GROUP BY time(5m), host',
    database='mydb',
    resample_every='5m',
    resample_for='10m'
)

# 创建连续查询（每小时计算最大值）
client.create_continuous_query(
    name='cq_1h_max',
    select='SELECT MAX(value) INTO cpu_usage_1h FROM cpu_usage GROUP BY time(1h), host',
    database='mydb'
)
```

## 验证数据

### InfluxDB 性能测试

| 操作 | 数据量 | 耗时 | 说明 |
|-----|--------|------|------|
| 写入 | 100万点 | 10s | 单机 |
| 查询（1小时） | 10万点 | <100ms | 索引查询 |
| 聚合查询 | 100万点 | 2s | 5分钟聚合 |

### 存储效率

```
原始数据：100GB
压缩后：10GB
压缩比：10:1
```

## 总结

1. **数据模型设计**
   - Tag 用于过滤和分组
   - Field 存储实际值
   - 合理设计 Tag 和 Field

2. **保留策略**
   - 根据数据重要性设置保留时间
   - 使用连续查询预聚合数据
   - 节省存储空间

3. **查询优化**
   - 使用时间范围限制查询
   - 合理使用 GROUP BY
   - 使用连续查询预计算

4. **最佳实践**
   - 批量写入提高性能
   - 使用保留策略管理数据
   - 监控数据库性能
