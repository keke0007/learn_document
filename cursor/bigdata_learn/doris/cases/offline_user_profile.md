# 案例2：离线用户画像宽表（Doris）

## 一、案例目标

- **场景**：基于离线订单与用户基础信息，构建用户画像宽表，为运营与推荐提供支撑。
- **目标指标示例**：
  - 累计订单数、累计消费金额
  - 首单日期、最近一次下单日期
  - 平均客单价
  - 活跃天数（有订单记录的天数）

对应的数据与脚本：

- 数据文件：`data/orders_offline.csv`、`data/users_offline.csv`
- 建表脚本：`scripts/setup_tables.sql`（画像宽表）
- 查询脚本：`scripts/common_queries.sql`

---

## 二、数据来源

复用 **案例1：离线订单统计分析** 中的数据：

- `orders_offline.csv`：订单明细
- `users_offline.csv`：用户基础信息

字段含义与示例详见 `offline_order_analysis.md`，此处不再重复。

---

## 三、用户画像宽表建模（示例）

### 1. 目标宽表结构

表名：`user_profile_offline`

```sql
CREATE TABLE IF NOT EXISTS user_profile_offline (
    user_id          BIGINT,
    user_name        VARCHAR(32),
    gender           VARCHAR(8),
    age              TINYINT,
    city             VARCHAR(32),
    register_date    DATE,
    total_orders     BIGINT,       -- 累计订单数
    total_amount     DECIMAL(16,2),-- 累计消费金额
    first_order_date DATE,         -- 首单日期
    last_order_date  DATE,         -- 最近一次下单日期
    active_days      BIGINT,       -- 有订单记录的天数
    avg_order_amount DECIMAL(16,2) -- 平均客单价
)
PRIMARY KEY(user_id)
DISTRIBUTED BY HASH(user_id) BUCKETS 8
PROPERTIES (
    "replication_num" = "1"
);
```

> 提示：这里使用 `PRIMARY KEY`，方便后续按天增量重算/更新画像记录。

---

## 四、画像指标计算 SQL 示例

### 1. 基础聚合查询（不写表）

```sql
USE bigdata_demo;

WITH user_order_agg AS (
    SELECT
        user_id,
        COUNT(*)            AS total_orders,
        SUM(amount)         AS total_amount,
        MIN(order_date)     AS first_order_date,
        MAX(order_date)     AS last_order_date,
        NDV(order_date)     AS active_days
    FROM orders_offline
    WHERE status = 'paid'
    GROUP BY user_id
)
SELECT
    u.user_id,
    u.user_name,
    u.gender,
    u.age,
    u.city,
    u.register_date,
    IFNULL(o.total_orders, 0)                       AS total_orders,
    IFNULL(o.total_amount, 0)                       AS total_amount,
    o.first_order_date,
    o.last_order_date,
    IFNULL(o.active_days, 0)                        AS active_days,
    IF(o.total_orders = 0, 0, o.total_amount / o.total_orders) AS avg_order_amount
FROM users_offline AS u
LEFT JOIN user_order_agg AS o
    ON u.user_id = o.user_id;
```

### 2. 将画像写入宽表

```sql
INSERT INTO user_profile_offline
SELECT
    u.user_id,
    u.user_name,
    u.gender,
    u.age,
    u.city,
    u.register_date,
    IFNULL(o.total_orders, 0)                       AS total_orders,
    IFNULL(o.total_amount, 0)                       AS total_amount,
    o.first_order_date,
    o.last_order_date,
    IFNULL(o.active_days, 0)                        AS active_days,
    IF(o.total_orders = 0, 0, o.total_amount / o.total_orders) AS avg_order_amount
FROM users_offline AS u
LEFT JOIN (
    SELECT
        user_id,
        COUNT(*)        AS total_orders,
        SUM(amount)     AS total_amount,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date,
        NDV(order_date) AS active_days
    FROM orders_offline
    WHERE status = 'paid'
    GROUP BY user_id
) AS o
    ON u.user_id = o.user_id;
```

> 如需每天重算，可以先 `TRUNCATE TABLE user_profile_offline;` 再执行上述 INSERT。

---

## 五、典型画像分析查询

### 1. 高价值用户（总金额排序）

```sql
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
```

### 2. 按城市划分用户消费水平

```sql
SELECT
    city,
    COUNT(*)          AS user_cnt,
    AVG(total_amount) AS avg_city_amount,
    MAX(total_amount) AS max_city_amount
FROM user_profile_offline
GROUP BY city
ORDER BY avg_city_amount DESC;
```

### 3. 根据消费能力打标签

```sql
SELECT
    user_id,
    user_name,
    total_amount,
    CASE
        WHEN total_amount >= 3000 THEN '高价值用户'
        WHEN total_amount >= 1000 THEN '中价值用户'
        WHEN total_amount > 0     THEN '低价值用户'
        ELSE '未消费用户'
    END AS value_level
FROM user_profile_offline
ORDER BY total_amount DESC;
```

---

## 六、练习建议

1. 增加字段 `order_span_days`：用 `DATEDIFF(last_order_date, first_order_date)` 计算时间跨度，并更新建表与写入逻辑。
2. 为画像表增加最近 30 天是否活跃的标记字段 `is_active_30d`（如基于最大下单日期与当前日期判断）。
3. 对比在 Hive / ClickHouse 中的离线画像实现方式，思考 Doris 使用 PRIMARY KEY + 导入的优劣与适用场景。

