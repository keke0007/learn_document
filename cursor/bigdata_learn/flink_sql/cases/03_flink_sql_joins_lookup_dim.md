# 案例3：Flink SQL Join（事实表 Join 维表：最小可验证）

## 案例目标
理解 Flink SQL 中 Join 的常见落地方式之一：
- 用事实表（orders）Join 维表（products）得到维度字段（category/price）
- 练习：`INNER JOIN`、按维度聚合

> 说明：真正生产里更常见的是 **Lookup Join（外部维表）**、**Temporal Join（随时间变化的维表）**。
> 本案例先用文件维表把 Join 的语义跑通（最易验证）。

## 验证数据
- `flink_sql/data/orders.csv`
- `flink_sql/data/dim_products.csv`

## SQL（可直接复制到 SQL Client）

> 把 `path` 改成你本机的绝对路径（见 `flink_sql/scripts/sql_client_run.md`）。

### 1) Source 表：订单
```sql
CREATE TABLE orders_src (
  order_id STRING,
  user_id STRING,
  product_id STRING,
  amount DOUBLE,
  event_time_str STRING
) WITH (
  'connector' = 'filesystem',
  'path' = 'file:///C:/REPLACE_ME/bigdata_learn/flink_sql/data/orders.csv',
  'format' = 'csv',
  'csv.ignore-parse-errors' = 'true'
);
```

### 2) Source 表：产品维表
```sql
CREATE TABLE dim_products (
  product_id STRING,
  category STRING,
  price BIGINT
) WITH (
  'connector' = 'filesystem',
  'path' = 'file:///C:/REPLACE_ME/bigdata_learn/flink_sql/data/dim_products.csv',
  'format' = 'csv',
  'csv.ignore-parse-errors' = 'true'
);
```

### 3) Sink：控制台输出（按品类聚合）
```sql
CREATE TABLE cat_sink (
  category STRING,
  cnt BIGINT,
  total_amount DOUBLE
) WITH (
  'connector' = 'print'
);
```

### 4) Join + 聚合
```sql
INSERT INTO cat_sink
SELECT
  p.category,
  COUNT(*) AS cnt,
  SUM(o.amount) AS total_amount
FROM orders_src o
JOIN dim_products p
ON o.product_id = p.product_id
GROUP BY p.category;
```

## 期望结果（对照验证）

维表：
- P001、P002 → cat_a
- P003 → cat_b

订单金额按品类汇总：
- cat_a：P001(10+15+7) + P002(20+3) = **55**，条数 **5**
  - P001：3 条（1001=10、1003=15、1005=7）
  - P002：2 条（1002=20、1006=3）
- cat_b：P003(8+5) = **13**，条数 **2**（1004=8、1007=5）

因此期望：
```
cat_a, cnt=5, total_amount=55
cat_b, cnt=2, total_amount=13
```

## 费曼式讲解（把它讲给初中生）
- **事实表**：记录发生了什么（订单）
- **维表**：解释这是什么（产品属于哪个品类）
- **Join**：把“发生了什么”跟“它是什么”拼起来，才能按品类统计

