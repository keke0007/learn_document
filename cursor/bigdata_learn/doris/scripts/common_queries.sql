USE bigdata_demo;

-- =========================
-- 离线订单统计常用查询
-- =========================

-- 每日订单量与金额
SELECT
    order_date,
    COUNT(*)    AS order_cnt,
    SUM(amount) AS total_amount
FROM orders_offline
GROUP BY order_date
ORDER BY order_date;

-- 按城市统计订单量与金额
SELECT
    city,
    COUNT(*)    AS order_cnt,
    SUM(amount) AS total_amount
FROM orders_offline
GROUP BY city
ORDER BY total_amount DESC;

-- 用户维度累计订单数与金额
SELECT
    u.user_id,
    u.user_name,
    u.city,
    COUNT(o.order_id) AS order_cnt,
    SUM(o.amount)     AS total_amount
FROM orders_offline AS o
LEFT JOIN users_offline AS u
    ON o.user_id = u.user_id
GROUP BY
    u.user_id, u.user_name, u.city
ORDER BY total_amount DESC;

-- =========================
-- 离线用户画像查询
-- =========================

-- 高价值用户
SELECT
    user_id,
    user_name,
    city,
    total_orders,
    total_amount,
    avg_order_amount
FROM user_profile_offline
ORDER BY total_amount DESC
LIMIT 10;

-- 按城市划分用户消费水平
SELECT
    city,
    COUNT(*)          AS user_cnt,
    AVG(total_amount) AS avg_city_amount,
    MAX(total_amount) AS max_city_amount
FROM user_profile_offline
GROUP BY city
ORDER BY avg_city_amount DESC;

-- =========================
-- 实时埋点 & 聚合查询
-- =========================

-- 最近 30 分钟 PV/UV（基于明细）
SELECT
    DATE_TRUNC('minute', event_time) AS ts_min,
    page,
    COUNT(*)                         AS pv,
    NDV(user_id)                     AS uv
FROM events_realtime
WHERE event_time >= NOW() - INTERVAL 30 MINUTE
GROUP BY ts_min, page
ORDER BY ts_min, page;

-- 使用物化视图的分钟级 PV/UV
SELECT
    ts_min,
    page,
    pv,
    uv
FROM mv_page_view_1min
WHERE ts_min >= NOW() - INTERVAL 30 MINUTE
ORDER BY ts_min, page;

-- 最近 10 分钟按设备统计 PV
SELECT
    device,
    COUNT(*) AS pv
FROM events_realtime
WHERE event_time >= NOW() - INTERVAL 10 MINUTE
  AND event_type = 'page_view'
GROUP BY device
ORDER BY pv DESC;

