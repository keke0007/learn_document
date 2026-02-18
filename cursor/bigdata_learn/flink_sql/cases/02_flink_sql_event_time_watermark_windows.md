# 案例2：Flink SQL 时间与窗口（Event Time / Watermark / Window TVF）

## 案例目标
用 Flink SQL 跑通“事件时间 + 水位线 + 窗口聚合”的最小闭环，理解：
- 事件时间列（time attribute）
- Watermark 的作用（推动窗口触发）
- Window TVF：`TUMBLE/HOP/SESSION`

## 验证数据
- `flink_sql/data/orders.csv`

## SQL（可直接复制到 SQL Client）

> 把 `path` 改成你本机的绝对路径（见 `flink_sql/scripts/sql_client_run.md`）。

### 1) Source 表：声明事件时间与 Watermark
```sql
CREATE TABLE orders_wm (
  order_id STRING,
  user_id STRING,
  product_id STRING,
  amount DOUBLE,
  event_time_str STRING,
  -- 把字符串转成时间戳（TIMESTAMP(3)）
  ts AS TO_TIMESTAMP(event_time_str),
  -- 声明 watermark：允许 2 秒乱序
  WATERMARK FOR ts AS ts - INTERVAL '2' SECOND
) WITH (
  'connector' = 'filesystem',
  'path' = 'file:///C:/REPLACE_ME/bigdata_learn/flink_sql/data/orders.csv',
  'format' = 'csv',
  'csv.ignore-parse-errors' = 'true'
);
```

### 2) Sink 表：控制台输出
```sql
CREATE TABLE window_sink (
  window_start TIMESTAMP(3),
  window_end TIMESTAMP(3),
  product_id STRING,
  sum_amount DOUBLE
) WITH (
  'connector' = 'print'
);
```

### 3) 10 秒滚动窗口（TUMBLE）按产品聚合金额
```sql
INSERT INTO window_sink
SELECT
  window_start,
  window_end,
  product_id,
  SUM(amount) AS sum_amount
FROM TABLE(
  TUMBLE(TABLE orders_wm, DESCRIPTOR(ts), INTERVAL '10' SECOND)
)
GROUP BY window_start, window_end, product_id;
```

## 期望结果（对照验证）

`orders.csv` 的事件时间分布：
- 09:00:01,04,07 → 在窗口 \[09:00:00,09:00:10)
  - P001：10 + 15 = **25**
  - P002：20 = **20**
- 09:00:12,16,19 → 在窗口 \[09:00:10,09:00:20)
  - P003：8 = **8**
  - P001：7 = **7**
  - P002：3 = **3**
- 09:00:21 → 在窗口 \[09:00:20,09:00:30)
  - P003：5 = **5**

因此你应能看到以上 3 个窗口对应的聚合输出（顺序不要求一致）。

## 费曼式讲解（把它讲给初中生）
- **事件时间**：用“这件事发生的时间”来做统计，不用“电脑处理它的时间”
- **水位线**：相当于告诉系统“我大概等到这个时间点了，之前那段时间可以结算了”
- **窗口**：把时间切成小段（例如每 10 秒一段），每段算一次总和

