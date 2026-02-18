# 案例1：Flink SQL 基础（DDL / DML / 聚合）

## 案例目标
用最小闭环理解 Flink SQL 的“表 → 查询 → 输出”：
- DDL：`CREATE TABLE`
- DML：`INSERT INTO ... SELECT ...`
- 基础聚合：`GROUP BY`
- Changelog 直觉：为什么聚合结果会“更新输出”

## 验证数据
- `flink_sql/data/orders.csv`

## SQL（可直接复制到 SQL Client）

> 把 `path` 改成你本机的绝对路径（见 `flink_sql/scripts/sql_client_run.md`）。

### 1) Source 表：读取订单 CSV（批/流统一视角）
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

> 说明：这里先把 `event_time` 当字符串，先把 DDL/DML 跑通；事件时间/水位线在案例2做。

### 2) Sink 表：控制台输出
```sql
CREATE TABLE print_sink (
  user_id STRING,
  cnt BIGINT,
  total_amount DOUBLE
) WITH (
  'connector' = 'print'
);
```

### 3) 聚合查询：每个用户的订单数与总金额
```sql
INSERT INTO print_sink
SELECT
  user_id,
  COUNT(*) AS cnt,
  SUM(amount) AS total_amount
FROM orders_src
GROUP BY user_id;
```

## 期望结果（对照验证）

从 `orders.csv` 口算：
- U001：订单 3 笔（1001/1003/1007），总额 \(10+15+5=30\)
- U002：订单 3 笔（1002/1005/1006），总额 \(20+7+3=30\)
- U003：订单 1 笔（1004），总额 \(8\)

因此最终你应看到“每个 user_id 一行”且满足：
```
U001, cnt=3, total_amount=30
U002, cnt=3, total_amount=30
U003, cnt=1, total_amount=8
```

> 注意：`print` connector 输出格式可能包含 `+I/+U` 等 changelog 标记；你只需要验证最终统计值正确。

## 费曼式讲解（把它讲给初中生）
- **表是什么**：就是“有列名的结构化数据”
- **SQL 做什么**：把表当成输入，做过滤/聚合/连接，得到新表
- **INSERT INTO 是什么**：把查询结果写到一个“输出表”（sink）
- **为什么会有更新**：流处理里结果会随着数据到来不断变更，Flink 会输出“新增/更新/撤回”的变更记录（changelog）

