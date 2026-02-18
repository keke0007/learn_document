# 案例3：实时埋点明细与聚合分析（Doris）

## 一、案例目标

- **场景**：实时收集用户行为埋点（PV、点击等），在分钟级完成多维度聚合分析。
- **目标**：
  - 设计实时明细表 `events_realtime`。
  - 基于物化视图构建分钟级 PV/UV 聚合视图。
  - 完成“最近 30 分钟 PV/UV”、“按页面/设备聚合”等实时查询。

对应的数据与脚本：

- 数据文件：`data/events_realtime.csv`
- 建表脚本：`scripts/setup_tables.sql`
- 导入 & 查询脚本：`scripts/load_realtime_demo.sql`、`scripts/common_queries.sql`

---

## 二、埋点数据说明（events_realtime.csv）

字段设计：

- `event_time`：事件时间（`DATETIME`）
- `user_id`：用户 ID
- `event_type`：事件类型（如 `page_view`、`click`）
- `page`：页面路径（如 `/home`、`/product`）
- `device`：设备类型（如 `ios`、`android`、`pc`）
- `os`：操作系统
- `network`：网络类型（如 `wifi`、`4g`）
- `duration`：停留时长（秒）

示例数据（20 行）：

```text
event_time,user_id,event_type,page,device,os,network,duration
2024-03-14 10:00:01,1,page_view,/home,ios,iOS,wifi,12
2024-03-14 10:00:05,2,page_view,/home,android,Android,4g,8
2024-03-14 10:00:10,1,click,/product,ios,iOS,wifi,5
2024-03-14 10:01:02,3,page_view,/home,pc,Windows,wifi,20
2024-03-14 10:01:15,1,page_view,/product,ios,iOS,wifi,15
2024-03-14 10:01:40,2,click,/cart,android,Android,4g,3
2024-03-14 10:02:05,4,page_view,/home,android,Android,4g,9
2024-03-14 10:02:18,2,page_view,/product,android,Android,4g,11
2024-03-14 10:02:33,3,click,/product,pc,Windows,wifi,4
2024-03-14 10:03:01,1,page_view,/home,ios,iOS,wifi,13
2024-03-14 10:03:22,4,click,/product,android,Android,4g,6
2024-03-14 10:03:45,2,page_view,/home,android,Android,4g,7
2024-03-14 10:04:10,3,page_view,/cart,pc,Windows,wifi,10
2024-03-14 10:04:25,1,page_view,/product,ios,iOS,wifi,18
2024-03-14 10:04:40,2,page_view,/product,android,Android,4g,14
2024-03-14 10:05:05,4,page_view,/home,android,Android,4g,9
2024-03-14 10:05:20,3,click,/order,pc,Windows,wifi,2
2024-03-14 10:05:35,1,page_view,/order,ios,iOS,wifi,16
2024-03-14 10:05:50,2,page_view,/home,android,Android,4g,10
2024-03-14 10:06:05,4,page_view,/product,android,Android,4g,12
```

---

## 三、表结构设计

### 1. 实时明细表：events_realtime

```sql
CREATE TABLE IF NOT EXISTS events_realtime (
    event_time DATETIME,
    user_id    BIGINT,
    event_type VARCHAR(32),
    page       VARCHAR(128),
    device     VARCHAR(32),
    os         VARCHAR(32),
    network    VARCHAR(16),
    duration   INT
)
DUPLICATE KEY(event_time, user_id, page)
PARTITION BY RANGE (event_time) (
    PARTITION p20240314 VALUES LESS THAN ('2024-03-15')
)
DISTRIBUTED BY HASH(user_id) BUCKETS 8
PROPERTIES (
    "replication_num" = "1"
);
```

### 2. 分钟级 PV/UV 物化视图：mv_page_view_1min

```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_page_view_1min
AS
SELECT
    DATE_TRUNC('minute', event_time) AS ts_min,
    page,
    COUNT(*)                        AS pv,
    NDV(user_id)                    AS uv
FROM events_realtime
GROUP BY ts_min, page;
```

> 当查询与 MV 匹配时，Doris 会自动改写使用该物化视图，从而显著减少扫描与聚合成本。

---

## 四、数据导入与模拟实时写入

### 1. 一次性导入 CSV（Stream Load）

```bash
curl --location-trusted -u user:password \
  -H "label:events_realtime_1" \
  -H "column_separator:," \
  -T /absolute/path/to/doris/data/events_realtime.csv \
  http://fe_host:8030/api/bigdata_demo/events_realtime/_stream_load
```

### 2. Routine Load 思路（生产场景）

生产中更推荐通过 Routine Load 从 Kafka 消费埋点数据，此处仅给出思路，不展开脚本：

- Kafka Topic：`user_events`
- Routine Load：持续从该 Topic 拉取数据，映射到 `events_realtime` 字段

---

## 五、实时查询示例

### 1. 查询最近 30 分钟 PV/UV（按页面）

```sql
SELECT
    DATE_TRUNC('minute', event_time) AS ts_min,
    page,
    COUNT(*)                        AS pv,
    NDV(user_id)                    AS uv
FROM events_realtime
WHERE event_time >= NOW() - INTERVAL 30 MINUTE
GROUP BY ts_min, page
ORDER BY ts_min, page;
```

如果 MV 已建立且条件匹配，可直接查询 `mv_page_view_1min`：

```sql
SELECT
    ts_min,
    page,
    pv,
    uv
FROM mv_page_view_1min
WHERE ts_min >= NOW() - INTERVAL 30 MINUTE
ORDER BY ts_min, page;
```

### 2. 各页面总 PV/UV

```sql
SELECT
    page,
    SUM(pv) AS total_pv,
    SUM(uv) AS total_uv
FROM mv_page_view_1min
GROUP BY page
ORDER BY total_pv DESC;
```

### 3. 最近 10 分钟按设备统计 PV

```sql
SELECT
    device,
    COUNT(*) AS pv
FROM events_realtime
WHERE event_time >= NOW() - INTERVAL 10 MINUTE
  AND event_type = 'page_view'
GROUP BY device
ORDER BY pv DESC;
```

---

## 六、练习建议

1. 为 `events_realtime` 增加 `country` 字段，扩展物化视图维度，统计“国家 + 页面”的 PV/UV。
2. 设计一个小时级别的物化视图 `mv_page_view_1h`，对比分钟级和小时级物化视图在查询延迟和存储占用上的差异。
3. 结合 `clickhouse/cases/realtime_event_agg.md`，思考 Doris 与 ClickHouse 在实时分析路径上的异同点。

