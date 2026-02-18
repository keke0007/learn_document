# 案例1：离线订单统计分析（ClickHouse）

## 一、案例目标

- **场景**：T+1 离线订单统计，支持按天、城市、用户维度查看订单量与订单金额。
- **目的**：
  - 熟悉在 ClickHouse 中使用 `MergeTree` 建模离线事实表。
  - 学会从 CSV 批量导入离线数据。
  - 完成典型的离线统计查询（按天、按城市、按用户）。

对应的数据与脚本：

- 数据文件：`data/orders_offline.csv`、`data/users_offline.csv`
- 建表脚本：`scripts/setup_tables.sql`
- 加载脚本：`scripts/load_offline_data.sql`

---

## 二、数据说明

### 1. 订单明细数据（orders_offline.csv）

字段含义：

- `order_id`：订单 ID，整型
- `user_id`：用户 ID，整型
- `order_date`：下单日期，`YYYY-MM-DD`
- `city`：下单城市
- `amount`：订单金额
- `status`：订单状态（示例：`paid`、`refund`）

示例数据（与 Hive 案例类似规模，便于对比）：

```text
order_id,user_id,order_date,city,amount,status
1001,1,2024-01-15,北京,299.00,paid
1002,2,2024-01-16,上海,599.00,paid
1003,1,2024-01-17,北京,899.00,paid
1004,3,2024-01-18,广州,299.00,paid
1005,2,2024-01-19,上海,199.00,refund
1006,1,2024-02-01,北京,599.00,paid
1007,4,2024-02-02,深圳,599.00,paid
1008,3,2024-02-03,广州,897.00,paid
1009,2,2024-02-04,上海,199.00,paid
1010,1,2024-02-05,北京,399.00,paid
1011,4,2024-03-10,深圳,299.00,paid
1012,3,2024-03-11,广州,1198.00,paid
1013,1,2024-03-12,北京,299.00,refund
1014,2,2024-03-13,上海,597.00,paid
1015,4,2024-03-14,深圳,199.00,paid
```

### 2. 用户基础信息（users_offline.csv）

字段含义：

- `user_id`：用户 ID
- `user_name`：姓名
- `gender`：性别
- `age`：年龄
- `city`：所在城市
- `register_date`：注册日期

示例数据：

```text
user_id,user_name,gender,age,city,register_date
1,张三,男,25,北京,2023-01-01
2,李四,女,30,上海,2023-02-15
3,王五,男,28,广州,2023-03-20
4,赵六,男,35,深圳,2023-04-10
5,小红,女,22,杭州,2023-05-01
6,小明,男,26,成都,2023-06-01
7,小李,女,29,武汉,2023-07-01
8,小王,男,33,西安,2023-08-01
```

---

## 三、建表 SQL（节选，完整见 scripts/setup_tables.sql）

```sql
CREATE DATABASE IF NOT EXISTS bigdata_demo;
USE bigdata_demo;

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
```

---

## 四、数据加载方式

> 路径请根据你本机的实际路径调整。

### 1. 使用脚本加载（推荐）

```bash
clickhouse-client --multiquery < scripts/load_offline_data.sql
```

### 2. 手工执行示例

```sql
USE bigdata_demo;

-- 导入订单数据
INSERT INTO orders_offline
FORMAT CSV
INFILE '/absolute/path/to/clickhouse/data/orders_offline.csv';

-- 导入用户数据
INSERT INTO users_offline
FORMAT CSV
INFILE '/absolute/path/to/clickhouse/data/users_offline.csv';
```

---

## 五、典型分析查询

### 1. 每日订单量与金额统计

```sql
SELECT
    order_date,
    count() AS order_cnt,
    sum(amount) AS total_amount
FROM orders_offline
GROUP BY order_date
ORDER BY order_date;
```

**预期结果示例（部分）：**

```text
order_date | order_cnt | total_amount
-----------+-----------+-------------
2024-01-15 |    1      |   299.00
2024-01-16 |    1      |   599.00
...
```

### 2. 按城市统计订单量与金额

```sql
SELECT
    city,
    count() AS order_cnt,
    sum(amount) AS total_amount
FROM orders_offline
GROUP BY city
ORDER BY total_amount DESC;
```

### 3. 用户维度的累计订单数与金额

```sql
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
```

### 4. 过滤退款订单后的统计

```sql
SELECT
    order_date,
    count() AS paid_order_cnt,
    sum(amount) AS paid_amount
FROM orders_offline
WHERE status = 'paid'
GROUP BY order_date
ORDER BY order_date;
```

---

## 六、练习建议

1. 在现有字段基础上增加一个 `channel`（渠道）字段，重新设计分区与查询。
2. 新增一个“订单状态统计”需求：分别统计 `paid` 和 `refund` 的订单数量与金额。
3. 对比同样数据在 Hive 中的实现（参考 `hive/cases/sales_analysis.md`），感受 ClickHouse 的查询延迟和写入方式差异。

