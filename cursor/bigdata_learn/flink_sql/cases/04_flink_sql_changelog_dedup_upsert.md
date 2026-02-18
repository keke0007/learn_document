# 案例4：Flink SQL Changelog / 去重 / Upsert（用 ROW_NUMBER 做“每个用户最新事件”）

## 案例目标
把 Flink SQL 最核心、也最容易“学了但用错”的点跑通：
- **动态表（Dynamic Table）**：查询结果会随着数据到来而变化
- **Changelog（变更日志）**：输出不只是“插入”，还可能有“更新/撤回”
- **去重（Dedup）**：`ROW_NUMBER()` 是生产里非常常用的 SQL 模式
- **Upsert 语义**：当结果是“更新型”（update/retract）时，sink 需要能处理变更（通常基于主键）

## 验证数据
- `flink_sql/data/user_events.csv`

## SQL（可直接复制到 SQL Client）

> 把 `path` 改成你本机的绝对路径（见 `flink_sql/scripts/sql_client_run.md`）。

### 1) Source 表：用户行为（事件时间 + watermark）
```sql
CREATE TABLE user_events (
  arrival BIGINT,
  user_id STRING,
  action STRING,
  product_id STRING,
  event_time_str STRING,
  ts AS TO_TIMESTAMP(event_time_str),
  WATERMARK FOR ts AS ts - INTERVAL '1' SECOND
) WITH (
  'connector' = 'filesystem',
  'path' = 'file:///C:/REPLACE_ME/bigdata_learn/flink_sql/data/user_events.csv',
  'format' = 'csv',
  'csv.ignore-parse-errors' = 'true'
);
```

### 2) Sink 表：按 user_id upsert 输出“最新事件”
```sql
CREATE TABLE latest_user_action_sink (
  user_id STRING,
  action STRING,
  product_id STRING,
  ts TIMESTAMP(3),
  PRIMARY KEY (user_id) NOT ENFORCED
) WITH (
  'connector' = 'print'
);
```

### 3) 去重查询：每个 user_id 只保留事件时间最新的一条
```sql
INSERT INTO latest_user_action_sink
SELECT user_id, action, product_id, ts
FROM (
  SELECT
    user_id,
    action,
    product_id,
    ts,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts DESC) AS rn
  FROM user_events
)
WHERE rn = 1;
```

## 期望结果（对照验证）

从 `user_events.csv` 按 `user_id` 找最新事件时间：
- U001：最新为 `2024-01-15 09:00:18` → `view P003`
- U002：最新为 `2024-01-15 09:00:12` → `buy P002`
- U003：最新为 `2024-01-15 09:00:22` → `buy P003`

因此最终“逻辑结果表”应等价于：
```
U001, view, P003, 2024-01-15 09:00:18
U002, buy,  P002, 2024-01-15 09:00:12
U003, buy,  P003, 2024-01-15 09:00:22
```

> 注意：你在控制台可能会看到 `+I/+U/-U` 之类的变更输出，这是正常的 —— 它体现了“同一个 user_id 的最新事件会被不断更新”。

## 费曼式讲解（把它讲给初中生）
- 你可以把每个 `user_id` 想成一个“名片夹”
- 新事件来了，如果时间更晚，就把这张人的“最新记录”换掉
- 因为会“换掉”，所以系统必须能表达“更新”，这就是 changelog
- 如果你把结果写到外部系统（MySQL/Kafka），必须能按主键把旧的覆盖掉（Upsert）

## 生产提示（最佳实践）
- 这类去重查询会用到状态（需要保存每个 user 的候选记录），生产建议设置状态 TTL：
  - `SET 'table.exec.state.ttl' = '1 h';`
- 若数据量大，建议打开 mini-batch 降低频繁更新的开销：
  - `SET 'table.exec.mini-batch.enabled' = 'true';`

