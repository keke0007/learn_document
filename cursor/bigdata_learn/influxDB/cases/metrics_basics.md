# 案例1：基础时序写入与查询（CPU 指标）

## 一、案例目标

- 使用 InfluxDB 存储简单 CPU 指标。
- 掌握 measurement/tag/field/time 模型与基础查询方式。

---

## 二、数据模型设计

- measurement：`cpu`
- tags：`host`、`region`
- fields：`usage_user`（用户态）、`usage_system`（内核态）

Line Protocol 示例（见 `data/cpu_metrics.lp`）：

```text
cpu,host=server1,region=beijing usage_user=12.3,usage_system=5.6 1710391200000000000
cpu,host=server1,region=beijing usage_user=15.0,usage_system=7.2 1710391260000000000
```

---

## 三、写入与查询示例

1. 创建数据库并选择：

```sql
CREATE DATABASE metrics;
USE metrics;
```

2. 导入示例数据：

```bash
influx -database 'metrics' -import -path=./data/cpu_metrics.lp
```

3. 基础查询：

```sql
-- 最近 10 条 CPU 记录
SELECT * FROM cpu ORDER BY time DESC LIMIT 10;

-- 按 host 聚合最近 1h 的平均 usage_user
SELECT MEAN(usage_user)
FROM cpu
WHERE time > now() - 1h
GROUP BY host;
```

