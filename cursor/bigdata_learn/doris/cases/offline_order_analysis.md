# 案例1：离线订单统计分析（Doris）

## 一、案例目标

- **场景**：T+1 离线订单统计，按天、城市、用户维度查看订单量与订单金额。
- **目的**：
  - 熟悉在 Doris 中使用 `DUPLICATE KEY` + 分区/分桶建模离线事实表。
  - 学会通过 Stream Load/Broker Load 从 CSV 导入离线数据。
  - 完成典型的离线统计查询（按天、按城市、按用户）。

对应的数据与脚本：

- 数据文件：`data/orders_offline.csv`、`data/users_offline.csv`
- 建表脚本：`scripts/setup_tables.sql`
- 导入脚本思路：`scripts/load_offline_data.sql`

---

## 二、数据说明

### 1. 订单明细数据（orders_offline.csv）

字段含义：

- `order_id`：订单 ID
- `user_id`：用户 ID
- `order_date`：下单日期，`YYYY-MM-DD`
- `city`：下单城市
- `amount`：订单金额
- `status`：订单状态（如 `paid`、`refund`）

示例数据（与 ClickHouse 模块保持一致，便于对比）：

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
```

---

## 四、数据导入方式（示例）

> 实际导入时请根据你的 Doris 版本、账号和集群地址调整 URL 与认证信息。

### 1. 使用 Stream Load 从本地 CSV 导入

```bash
# 导入订单数据
curl --location-trusted -u user:password \
  -H "label:orders_offline_1" \
  -H "column_separator:," \
  -T /absolute/path/to/doris/data/orders_offline.csv \
  http://fe_host:8030/api/bigdata_demo/orders_offline/_stream_load

# 导入用户数据
curl --location-trusted -u user:password \
  -H "label:users_offline_1" \
  -H "column_separator:," \
  -T /absolute/path/to/doris/data/users_offline.csv \
  http://fe_host:8030/api/bigdata_demo/users_offline/_stream_load
```

### 2. 使用 Broker Load（如果数据在 HDFS/对象存储）

可以在 `scripts/load_offline_data.sql` 中编写 Broker Load 语句，这里略。

---

## 五、典型分析查询

### 1. 每日订单量与金额统计

```sql
SELECT
    order_date,
    COUNT(*)        AS order_cnt,
    SUM(amount)     AS total_amount
FROM orders_offline
GROUP BY order_date
ORDER BY order_date;
```

### 2. 按城市统计订单量与金额

```sql
SELECT
    city,
    COUNT(*)    AS order_cnt,
    SUM(amount) AS total_amount
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
    COUNT(o.order_id) AS order_cnt,
    SUM(o.amount)     AS total_amount
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
    COUNT(*)    AS paid_order_cnt,
    SUM(amount) AS paid_amount
FROM orders_offline
WHERE status = 'paid'
GROUP BY order_date
ORDER BY order_date;
```

---

## 六、练习建议

1. 调整分区策略（例如按日分区），并观察分区裁剪对查询性能的影响。
2. 尝试基于 `orders_offline` 创建一个物化视图，预聚合每日城市订单指标，并验证查询是否命中 MV。
3. 对照 `clickhouse/cases/offline_order_analysis.md`，对比 Doris 与 ClickHouse 在建模与导入方式上的差异。

