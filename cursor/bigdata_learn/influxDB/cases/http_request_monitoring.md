# 案例2：HTTP 请求监控与聚合分析（InfluxDB）

## 一、案例目标

- 使用 InfluxDB 存储 HTTP 请求指标（QPS/延迟）。
- 通过时间窗口和标签聚合分析请求量与延迟。

---

## 二、数据模型设计

- measurement：`http_requests`
- tags：`service`（服务名）、`status`（状态码）、`method`（GET/POST）
- fields：`count`（请求数）、`latency_ms`（平均延迟）

Line Protocol 示例（见 `data/http_requests.lp`）：

```text
http_requests,service=api,status=200,method=GET count=120,latency_ms=35.5 1710391200000000000
http_requests,service=api,status=500,method=GET count=5,latency_ms=120.0 1710391200000000000
```

---

## 三、聚合查询示例（InfluxQL）

```sql
USE metrics;

-- 最近 15 分钟各服务每分钟请求数
SELECT SUM(count)
FROM http_requests
WHERE time > now() - 15m
GROUP BY time(1m), service fill(0);

-- 最近 15 分钟按状态码统计请求数
SELECT SUM(count)
FROM http_requests
WHERE time > now() - 15m
GROUP BY status fill(0);

-- 最近 1 小时各服务 95 分位延迟（示意，实际可在写入或外部计算）
SELECT MEAN(latency_ms)
FROM http_requests
WHERE time > now() - 1h
GROUP BY time(5m), service fill(null);
```

