USE bigdata_demo;

-- =========================
-- 离线订单统计常用查询
-- =========================

-- 每日订单量与金额
SELECT
    order_date,
    count() AS order_cnt,
    sum(amount) AS total_amount
FROM orders_offline
GROUP BY order_date
ORDER BY order_date;

-- 按城市统计订单量与金额
SELECT
    city,
    count() AS order_cnt,
    sum(amount) AS total_amount
FROM orders_offline
GROUP BY city
ORDER BY total_amount DESC;

-- 用户维度累计订单数与金额
SELECT
    u.user_id,
    u.user_name,
    u.city,
    count(o.order_id) AS order_cnt,
    sum(o.amount) AS total_amount
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

-- 按城市划分用户消费层级
SELECT
    city,
    count() AS user_cnt,
    avg(total_amount) AS avg_city_amount,
    max(total_amount) AS max_city_amount
FROM user_profile_offline
GROUP BY city
ORDER BY avg_city_amount DESC;

-- =========================
-- 实时埋点 & 聚合查询
-- =========================

-- 最近 30 分钟 PV/UV（按页面）
SELECT
    ts_min,
    page,
    pv,
    uv
FROM page_view_1min
WHERE ts_min >= now() - INTERVAL 30 MINUTE
ORDER BY ts_min, page;

-- 各页面总 PV/UV
SELECT
    page,
    sum(pv) AS total_pv,
    sum(uv) AS total_uv
FROM page_view_1min
GROUP BY page
ORDER BY total_pv DESC;

-- 最近 10 分钟内，按设备统计 PV
SELECT
    device,
    count() AS pv
FROM events_realtime
WHERE event_time >= now() - INTERVAL 10 MINUTE
  AND event_type = 'page_view'
GROUP BY device
ORDER BY pv DESC;

