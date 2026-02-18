-- ClickHouse 建表示例：离线 + 实时

CREATE DATABASE IF NOT EXISTS bigdata_demo;
USE bigdata_demo;

-- 离线订单明细表
CREATE TABLE IF NOT EXISTS orders_offline (
    order_id    UInt32,
    user_id     UInt32,
    order_date  Date,
    city        String,
    amount      Float64,
    status      String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(order_date)
ORDER BY (order_date, user_id)
SETTINGS index_granularity = 8192;

-- 离线用户基础信息表
CREATE TABLE IF NOT EXISTS users_offline (
    user_id       UInt32,
    user_name     String,
    gender        String,
    age           UInt8,
    city          String,
    register_date Date
)
ENGINE = MergeTree
ORDER BY (user_id);

-- 离线用户画像宽表
CREATE TABLE IF NOT EXISTS user_profile_offline (
    user_id          UInt32,
    user_name        String,
    gender           String,
    age              UInt8,
    city             String,
    register_date    Date,
    total_orders     UInt32,
    total_amount     Float64,
    first_order_date Date,
    last_order_date  Date,
    active_days      UInt32,
    avg_order_amount Float64
)
ENGINE = MergeTree
ORDER BY (user_id);

-- 实时埋点明细表
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

-- 分钟级 PV/UV 聚合表
CREATE TABLE IF NOT EXISTS page_view_1min (
    ts_min DateTime,
    page   String,
    pv     UInt64,
    uv     UInt64
)
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMMDD(ts_min)
ORDER BY (ts_min, page);

-- 物化视图：从明细表自动写入聚合表
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

