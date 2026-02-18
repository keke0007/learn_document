# 案例1：Spark SQL 基础（DataFrame / 临时视图 / 基础聚合）

## 案例目标
理解 Spark SQL 中最小可用闭环：
- 用 DataFrame 读取 CSV
- 注册成临时视图
- 用 SQL 做过滤 / 聚合
- 用小数据手算结果、对照 `show()`

## 验证数据
- `spark_sql/data/orders.csv`

## Scala 代码示例（可在 `spark-shell` 中执行）

> 注意：把 `base` 路径改成你本机的绝对路径。

```scala
import org.apache.spark.sql.functions._

val spark = spark
spark.conf.set("spark.sql.shuffle.partitions", 4)

val base = "C:/Users/ke/Desktop/bigdata_learn/spark_sql"  // 修改成你的路径

val orders = spark.read
  .option("header", "true")
  .option("inferSchema", "true")
  .csv(s"$base/data/orders.csv")

orders.printSchema()
orders.show(false)

orders.createOrReplaceTempView("orders")

// 每个用户的订单数和总金额
val userAgg = spark.sql(
  """
    |SELECT
    |  user_id,
    |  COUNT(*) AS cnt,
    |  SUM(amount) AS total_amount
    |FROM orders
    |GROUP BY user_id
    |ORDER BY user_id
    |""".stripMargin)

userAgg.show(false)
```

## 期望结果（手算对照）

从 `orders.csv`：
- U001：1001(10.0)、1003(15.0)、1007(5.0) → cnt=3, sum=30.0
- U002：1002(20.0)、1005(7.0)、1006(3.0) → cnt=3, sum=30.0
- U003：1004(8.0) → cnt=1, sum=8.0

所以应看到：
```text
user_id cnt total_amount
U001    3   30.0
U002    3   30.0
U003    1   8.0
```

## 费曼式讲解（用自己的话重述）
- **DataFrame**：像一张带列名的表，只不过在内存里，按列优化存储（Catalyst/列式）。
- **临时视图**：给 DataFrame 起个“表名”，方便用 SQL 写查询。
- **SQL**：本质上是针对 DataFrame 的声明式查询，Spark 会自动做优化和执行计划。

