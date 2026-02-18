# 案例2：离线用户画像指标（ClickHouse）

## 一、案例目标

- **场景**：基于离线订单与用户基础信息，构建简单的用户画像指标表，为推荐/运营提供支撑。
- **目标指标示例**：
  - 累计订单数、累计消费金额
  - 首单日期、最近一次下单日期
  - 平均客单价
  - 活跃天数（有下单记录的天数）

对应的数据与脚本：

- 数据文件：`data/orders_offline.csv`、`data/users_offline.csv`
- 建表脚本：`scripts/setup_tables.sql`（用户画像宽表建表）
- 加载 & 计算脚本：`scripts/load_offline_data.sql`、`scripts/common_queries.sql`

---

## 二、数据来源

直接复用 **案例1：离线订单统计分析** 中的数据：

- `orders_offline.csv`：订单明细
- `users_offline.csv`：用户基础信息

字段说明参见 `offline_order_analysis.md`，此处不再赘述。

---

## 三、用户画像宽表建模（示例）

### 1. 目标宽表结构

表名：`user_profile_offline`

```sql
CREATE TABLE IF NOT EXISTS user_profile_offline (
    user_id          UInt32,
    user_name        String,
    gender           String,
    age              UInt8,
    city             String,
    register_date    Date,
    total_orders     UInt32,       -- 累计订单数
    total_amount     Float64,      -- 累计消费金额
    first_order_date Date,         -- 首单日期
    last_order_date  Date,         -- 最近一次下单日期
    active_days      UInt32,       -- 有下单记录的天数
    avg_order_amount Float64       -- 平均客单价
)
ENGINE = MergeTree
ORDER BY (user_id);
```

> 提示：这里选择 `MergeTree` + `ORDER BY (user_id)`，方便按用户维度查询与更新（如果后续改为 `ReplacingMergeTree`，可以支持“重算覆盖”场景）。

---

## 四、离线画像计算 SQL 示例

### 1. 基础聚合查询

```sql
USE bigdata_demo;

-- 1) 统计每个用户的订单数、消费金额、首单/末单日期、活跃天数
WITH
user_order_agg AS (
    SELECT
        user_id,
        count() AS total_orders,
        sum(amount) AS total_amount,
        min(order_date) AS first_order_date,
        max(order_date) AS last_order_date,
        uniqExact(order_date) AS active_days
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
    coalesce(o.total_orders, 0) AS total_orders,
    coalesce(o.total_amount, 0) AS total_amount,
    o.first_order_date,
    o.last_order_date,
    coalesce(o.active_days, 0) AS active_days,
    if(o.total_orders = 0, 0, o.total_amount / o.total_orders) AS avg_order_amount
FROM users_offline AS u
LEFT JOIN user_order_agg AS o
    ON u.user_id = o.user_id;
```

### 2. 写入画像宽表

```sql
INSERT INTO user_profile_offline
SELECT
    u.user_id,
    u.user_name,
    u.gender,
    u.age,
    u.city,
    u.register_date,
    coalesce(o.total_orders, 0) AS total_orders,
    coalesce(o.total_amount, 0) AS total_amount,
    o.first_order_date,
    o.last_order_date,
    coalesce(o.active_days, 0) AS active_days,
    if(o.total_orders = 0, 0, o.total_amount / o.total_orders) AS avg_order_amount
FROM users_offline AS u
LEFT JOIN (
    SELECT
        user_id,
        count() AS total_orders,
        sum(amount) AS total_amount,
        min(order_date) AS first_order_date,
        max(order_date) AS last_order_date,
        uniqExact(order_date) AS active_days
    FROM orders_offline
    WHERE status = 'paid'
    GROUP BY user_id
) AS o
    ON u.user_id = o.user_id;
```

> 如果你倾向于每天重算整表，可以在插入前 `TRUNCATE TABLE user_profile_offline;`。

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

### 2. 按城市划分用户消费层级

```sql
SELECT
    city,
    count() AS user_cnt,
    avg(total_amount) AS avg_city_amount,
    max(total_amount) AS max_city_amount
FROM user_profile_offline
GROUP BY city
ORDER BY avg_city_amount DESC;
```

### 3. 根据消费能力打标签（CASE）

```sql
SELECT
    user_id,
    user_name,
    total_amount,
    CASE
        WHEN total_amount >= 3000 THEN '高价值用户'
        WHEN total_amount >= 1000 THEN '中价值用户'
        WHEN total_amount > 0 THEN '低价值用户'
        ELSE '未消费用户'
    END AS value_level
FROM user_profile_offline
ORDER BY total_amount DESC;
```

---

## 六、练习建议

1. 在画像表中增加一个字段 `order_span_days`：最近一次订单日期与首单日期的时间跨度（天数）。
2. 增加“最近 30 天内是否有订单”的标记字段 `is_active_30d`，基于 `last_order_date` 计算。
3. 对比 Hive 中的离线画像计算方式（如 `INSERT OVERWRITE` + 分区表），思考：
   - ClickHouse 更适合如何组织离线画像表？
   - 是每天重算全表，还是做增量更新（结合 `ReplacingMergeTree`）？

