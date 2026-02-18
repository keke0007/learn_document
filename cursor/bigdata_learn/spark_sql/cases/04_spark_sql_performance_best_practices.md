# 案例4：Spark SQL 性能与最佳实践（小实验版）

## 案例目标
用一个小实验理解几条最重要的 Spark SQL 性能实践：
- 控制 `spark.sql.shuffle.partitions`
- 理解宽依赖（聚合、Join）会触发 shuffle
- 观察缓存（cache）对重复查询的影响

## 验证数据
- 仍使用 `spark_sql/data/orders.csv`，重点是理解行为而非大数据量。

## Scala 代码示例（可在 `spark-shell` 中执行）

```scala
import org.apache.spark.sql.functions._

val spark = spark
val base = "C:/Users/ke/Desktop/bigdata_learn/spark_sql"  // 修改为你的路径

// 1) 基础设置：观察 shuffle 分区数
spark.conf.get("spark.sql.shuffle.partitions")
spark.conf.set("spark.sql.shuffle.partitions", 4)

val orders = spark.read
  .option("header", "true")
  .option("inferSchema", "true")
  .csv(s"$base/data/orders.csv")

orders.createOrReplaceTempView("orders")

// 2) 简单聚合 —— 会触发一次 shuffle
val userAgg = spark.sql(
  """
    |SELECT user_id, COUNT(*) AS cnt, SUM(amount) AS total_amount
    |FROM orders
    |GROUP BY user_id
    |""".stripMargin)

userAgg.explain(true)
userAgg.show(false)

// 3) 多次使用相同中间结果时，cache 的差异
val cachedOrders = orders.cache()

val agg1 = cachedOrders.groupBy("user_id").agg(sum("amount").as("total_amount"))
val agg2 = cachedOrders.groupBy("product_id").agg(sum("amount").as("total_amount"))

agg1.explain(true)
agg2.explain(true)

agg1.show(false)
agg2.show(false)
```

## 观察要点（如何用这个小实验理解性能）

1. `explain(true)` 能看见：
   - 哪些算子触发 shuffle（通常带 `Exchange`）
   - shuffle 使用的分区数（受 `spark.sql.shuffle.partitions` 影响）
2. `cache()` 后再次使用同一个 DataFrame：
   - 有机会避免重复扫描源数据
   - 在大数据场景下显著减少 I/O

## 费曼式讲解
- **宽依赖**（比如 `groupBy`、`join`）意味着“需要跨分区重新分布数据”，就会触发 shuffle。
- `spark.sql.shuffle.partitions` 决定 shuffle 之后有多少分区：
  - 太小：单个分区压力大、并行度不够。
  - 太大：任务数量爆炸、调度和小文件问题。
- **cache**：就像把中间结果放在内存/磁盘里，下次再用时不用从头算。

