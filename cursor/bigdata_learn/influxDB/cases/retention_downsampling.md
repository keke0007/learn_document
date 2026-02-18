# 案例3：保留策略与下采样（InfluxDB）

## 一、案例目标

- 为高频时序数据配置合理的保留策略（Retention Policy）。
- 使用下采样（Continuous Query/Task）将高频数据汇总为低频数据。

---

## 二、保留策略示例

假设数据库为 `metrics`：

```sql
-- 默认保留策略：数据保留 24 小时
CREATE RETENTION POLICY "rp_24h" ON "metrics" DURATION 24h REPLICATION 1 DEFAULT;

-- 下采样保留策略：下采样结果保留 30 天
CREATE RETENTION POLICY "rp_30d" ON "metrics" DURATION 30d REPLICATION 1;
```

---

## 三、Continuous Query 下采样示例（InfluxQL）

按 5 分钟粒度对 `cpu` 数据做平均值聚合，并写入新的 measurement `cpu_5m`：

```sql
CREATE CONTINUOUS QUERY "cq_cpu_5m" ON "metrics"
BEGIN
  SELECT
    MEAN(usage_user)   AS mean_usage_user,
    MEAN(usage_system) AS mean_usage_system
  INTO "metrics"."rp_30d"."cpu_5m"
  FROM "cpu"
  GROUP BY time(5m), host, region
END;
```

查询下采样结果：

```sql
SELECT * FROM "cpu_5m" WHERE time > now() - 7d LIMIT 10;
```

---

## 四、练习建议

1. 为 `http_requests` 数据设计类似的 Continuous Query，将每秒/每分钟数据下采样为 5 分钟粒度的统计。  
2. 结合实际场景思考 “原始数据 + 下采样数据” 的保留时间，例如原始数据保留 7 天、下采样数据保留 90 天。  

