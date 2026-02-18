# 案例3：Spark SQL Join（事实表 Join 维表 + 按维度聚合）

## 案例目标
用 Spark SQL 跑通最常见的数仓模式之一：
- 事实表（订单） + 维表（产品）
- 按品类统计订单数与销售额

## 验证数据
- `spark_sql/data/orders.csv`
- `spark_sql/data/dim_products.csv`

## Scala 代码示例（可在 `spark-shell` 中执行）

```scala
import org.apache.spark.sql.functions._

val spark = spark
val base = "C:/Users/ke/Desktop/bigdata_learn/spark_sql"  // 修改为你的路径

val orders = spark.read
  .option("header", "true")
  .option("inferSchema", "true")
  .csv(s"$base/data/orders.csv")

val products = spark.read
  .option("header", "true")
  .option("inferSchema", "true")
  .csv(s"$base/data/dim_products.csv")

orders.createOrReplaceTempView("orders")
products.createOrReplaceTempView("dim_products")

// 事实表 Join 维表，再按 category 聚合
val catAgg = spark.sql(
  """
    |SELECT
    |  p.category,
    |  COUNT(*) AS cnt,
    |  SUM(o.amount) AS total_amount
    |FROM orders o
    |JOIN dim_products p
    |  ON o.product_id = p.product_id
    |GROUP BY p.category
    |ORDER BY p.category
    |""".stripMargin)

catAgg.show(false)
```

## 期望结果（手算对照）

维表：
- P001、P002 → cat_a
- P003 → cat_b

订单金额按品类汇总：
- cat_a：
  - P001：10 + 15 + 7 = 32
  - P002：20 + 3 = 23
  - 合计：32 + 23 = **55**，条数 **5**
- cat_b：
  - P003：8 + 5 = **13**，条数 **2**

所以期望输出：
```text
category cnt total_amount
cat_a    5   55.0
cat_b    2   13.0
```

## 费曼式讲解
- **事实表**：记录“发生了多少笔订单、金额是多少”。
- **维表**：告诉你“每个 product 属于哪个 category”。
- **Join**：把这两类信息拼起来，才能按品类统计销售额。

