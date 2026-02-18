# 案例2：Spark SQL 窗口函数（按时间分组 / 排名）

## 案例目标
学习 Spark SQL 中的“分析窗口函数”：
- 按时间分组统计（简单版）
- `ROW_NUMBER` / `RANK` 排名
- 理解“分区（PARTITION BY）+ 排序（ORDER BY）”的含义

> 注意：这里用的是 SQL 的 **窗口函数（Window Function）**，不是流式引擎里的“时间窗口”。Spark SQL 是批/微批模式，重点是“分析函数”的使用。

## 验证数据
- `spark_sql/data/user_events.csv`

## Scala 代码示例（可在 `spark-shell` 中执行）

```scala
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions.Window

val spark = spark
val base = "C:/Users/ke/Desktop/bigdata_learn/spark_sql"  // 修改为你的路径

val events = spark.read
  .option("header", "true")
  .option("inferSchema", "true")
  .csv(s"$base/data/user_events.csv")

events.createOrReplaceTempView("user_events")

// 1) 每个用户的事件时间线（按时间排序）
val ordered = spark.sql(
  """
    |SELECT
    |  user_id,
    |  action,
    |  product_id,
    |  event_time,
    |  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time) AS rn_asc,
    |  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time DESC) AS rn_desc
    |FROM user_events
    |ORDER BY user_id, event_time
    |""".stripMargin)

ordered.show(false)

// 2) 每个用户的“最新一次行为”
val latestAction = ordered
  .filter(col("rn_desc") === 1)
  .select("user_id", "action", "product_id", "event_time")
  .orderBy("user_id")

latestAction.show(false)
```

## 期望结果（手算对照）

从 `user_events.csv` 可知：
- U001：最晚是 09:00:18 → `view P003`
- U002：最晚是 09:00:12 → `buy P002`
- U003：最晚是 09:00:22 → `buy P003`

因此 `latestAction` 的结果应为：
```text
U001, view, P003, 2024-01-15 09:00:18
U002, buy,  P002, 2024-01-15 09:00:12
U003, buy,  P003, 2024-01-15 09:00:22
```

## 费曼式讲解
- **PARTITION BY**：就像把大表按 user_id 分成很多小表，每个用户一小块。
- **ORDER BY**：在每一小块里按时间排队。
- **ROW_NUMBER()**：给排好序的每一行一个编号，从 1 开始。
- **取 rn_desc=1**：就是“每个用户时间上最新的一条记录”。

