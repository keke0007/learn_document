# 案例3：实时埋点明细与聚合分析（ClickHouse）

## 一、案例目标

- **场景**：实时收集用户行为埋点（PV、点击、曝光等），并在秒/分钟级完成多维度聚合分析。
- **目标**：
  - 设计实时明细表 `events_realtime`。
  - 基于物化视图构建分钟级 PV/UV 聚合表 `page_view_1min`。
  - 完成“最近 30 分钟 PV/UV”、“按页面/事件类型聚合”等实时查询。

对应的数据与脚本：

- 数据文件：`data/events_realtime.csv`（模拟实时事件）
- 建表脚本：`scripts/setup_tables.sql`
- 加载 & 演示脚本：`scripts/load_realtime_demo.sql`、`scripts/common_queries.sql`

---

## 二、埋点数据说明（events_realtime.csv）

字段设计：

- `event_time`：事件发生时间（`DateTime`）
- `user_id`：用户 ID
- `event_type`：事件类型（如：`page_view`、`click`、`expose`）
- `page`：页面标识（如：`/home`、`/product`）
- `device`：设备类型（如：`ios`、`android`、`pc`）
- `os`：操作系统（如：`iOS`、`Android`、`Windows`）
- `network`：网络类型（如：`wifi`、`4g`）
- `duration`：本次会话/页面停留时长（秒）

示例数据（约 20 行，覆盖多种页面/用户/设备）：

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
    event_time DateTime,
    user_id    UInt32,
    event_type String,
    page       String,
    device     String,
    os         String,
    network    String,
    duration   UInt32
)
ENGINE = MergeTree
PARTITION BY toYYYYMMDD(event_time)
ORDER BY (event_time, user_id);
```

> 说明：
> - 分区：按天分区，方便按日期范围清理与查询。
> - 排序键：`(event_time, user_id)` 兼顾时间维度和用户维度。

### 2. 分钟级 PV/UV 聚合表：page_view_1min

```sql
CREATE TABLE IF NOT EXISTS page_view_1min (
    ts_min DateTime,
    page   String,
    pv     UInt64,
    uv     UInt64
)
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMMDD(ts_min)
ORDER BY (ts_min, page);
```

### 3. 物化视图：mv_page_view_1min

```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_page_view_1min
TO page_view_1min
AS
SELECT
    toStartOfMinute(event_time) AS ts_min,
    page,
    count() AS pv,
    uniqExact(user_id) AS uv
FROM events_realtime
GROUP BY ts_min, page;
```

> 说明：每当 `events_realtime` 有新写入数据，物化视图会自动将增量数据聚合写入 `page_view_1min`。

---

## 四、数据加载与模拟实时写入

### 1. 一次性加载 CSV（演示用）

```sql
USE bigdata_demo;

INSERT INTO events_realtime
FORMAT CSV
INFILE '/absolute/path/to/clickhouse/data/events_realtime.csv';
```

### 2. 脚本模拟“实时”写入

在 `scripts/load_realtime_demo.sql` 中可以写成多段 `INSERT`，逐批执行模拟实时流入（你也可以用 shell / Python 循环发送）。

示例（简化版）：

```sql
INSERT INTO events_realtime
FORMAT CSV
INFILE '/absolute/path/to/clickhouse/data/events_realtime.csv';
```

> 如果要更贴近实时，可以将 CSV 拆分成多份或按行逐条写入。

---

## 五、实时查询示例

### 1. 查询最近 30 分钟 PV/UV（按页面）

```sql
SELECT
    ts_min,
    page,
    pv,
    uv
FROM page_view_1min
WHERE ts_min >= now() - INTERVAL 30 MINUTE
ORDER BY ts_min, page;
```

### 2. 统计各页面的总 PV/UV

```sql
SELECT
    page,
    sum(pv) AS total_pv,
    sum(uv) AS total_uv
FROM page_view_1min
GROUP BY page
ORDER BY total_pv DESC;
```

### 3. 按设备类型统计实时 PV

可以直接基于明细表做近一段时间的聚合：

```sql
SELECT
    device,
    count() AS pv
FROM events_realtime
WHERE event_time >= now() - INTERVAL 10 MINUTE
  AND event_type = 'page_view'
GROUP BY device
ORDER BY pv DESC;
```

### 4. 分钟级 PV 趋势（单页面）

```sql
SELECT
    ts_min,
    pv
FROM page_view_1min
WHERE page = '/home'
ORDER BY ts_min;
```

---

## 六、练习建议

1. 增加一个按 `event_type` 维度聚合的物化视图（例如 `event_agg_1min`），统计每分钟的点击量、曝光量等。
2. 将 `duration` 聚合进来，计算每分钟平均停留时长。
3. 思考真实生产环境中：
   - 如何使用 Kafka 引擎表 + 物化视图替代“CSV + INSERT”的写入方式？
   - 如何做多分片部署，并在前面增加 `Distributed` 表统一查询？

