-- Doris 建表示例：离线 + 实时

CREATE DATABASE IF NOT EXISTS bigdata_demo;
USE bigdata_demo;

-- 离线订单明细表（DUPLICATE KEY）
CREATE TABLE IF NOT EXISTS orders_offline (
    order_id    BIGINT,
    user_id     BIGINT,
    order_date  DATE,
    city        VARCHAR(32),
    amount      DECIMAL(16, 2),
    status      VARCHAR(16)
)
DUPLICATE KEY(order_id, user_id)
PARTITION BY RANGE (order_date) (
    PARTITION p202401 VALUES LESS THAN ('2024-02-01'),
    PARTITION p202402 VALUES LESS THAN ('2024-03-01'),
    PARTITION p202403 VALUES LESS THAN ('2024-04-01')
)
DISTRIBUTED BY HASH(user_id) BUCKETS 8
PROPERTIES (
    "replication_num" = "1"
);

-- 离线用户基础信息表
CREATE TABLE IF NOT EXISTS users_offline (
    user_id       BIGINT,
    user_name     VARCHAR(32),
    gender        VARCHAR(8),
    age           TINYINT,
    city          VARCHAR(32),
    register_date DATE
)
DUPLICATE KEY(user_id)
DISTRIBUTED BY HASH(user_id) BUCKETS 8
PROPERTIES (
    "replication_num" = "1"
);

-- 离线用户画像宽表（PRIMARY KEY）
CREATE TABLE IF NOT EXISTS user_profile_offline (
    user_id          BIGINT,
    user_name        VARCHAR(32),
    gender           VARCHAR(8),
    age              TINYINT,
    city             VARCHAR(32),
    register_date    DATE,
    total_orders     BIGINT,
    total_amount     DECIMAL(16, 2),
    first_order_date DATE,
    last_order_date  DATE,
    active_days      BIGINT,
    avg_order_amount DECIMAL(16, 2)
)
PRIMARY KEY(user_id)
DISTRIBUTED BY HASH(user_id) BUCKETS 8
PROPERTIES (
    "replication_num" = "1"
);

-- 实时埋点明细表
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

-- 分钟级 PV/UV 物化视图
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_page_view_1min
AS
SELECT
    DATE_TRUNC('minute', event_time) AS ts_min,
    page,
    COUNT(*)                         AS pv,
    NDV(user_id)                     AS uv
FROM events_realtime
GROUP BY ts_min, page;

