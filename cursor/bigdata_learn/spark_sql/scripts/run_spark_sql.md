# Spark SQL 运行说明（本目录案例）

> 目标：在本地用 Spark 的 `spark-shell` / `spark-sql` 直接跑 `spark_sql/cases/` 里的示例。

## 1) 准备 Spark 环境

- 安装 Spark（例如 3.4.x），确保本地有：
  - `spark-shell`
  - `spark-sql`

## 2) 用 `spark-shell`（Scala）运行案例

在 Spark 安装目录下：
```bash
./bin/spark-shell \
  --master local[*] \
  --conf spark.sql.shuffle.partitions=4
```

进入 REPL 后：

```scala
import org.apache.spark.sql.functions._

val spark = spark // 已自动创建
spark.conf.set("spark.sql.shuffle.partitions", 4)

// 把路径改成你本机的绝对路径
val base = "C:/Users/ke/Desktop/bigdata_learn/spark_sql"

val orders = spark.read
  .option("header", "true")
  .option("inferSchema", "true")
  .csv(s"$base/data/orders.csv")

orders.createOrReplaceTempView("orders")
```

然后可以复制 `cases/` 中的 SQL 到：

```scala
spark.sql(\"\"\"SELECT ... FROM orders ...\"\"\").show(false)
```

## 3) 用 `spark-sql` 运行纯 SQL

```bash
./bin/spark-sql \
  --master local[*] \
  -S   # 简化输出格式（可选）
```

进入后先创建临时视图：

```sql
CREATE TEMPORARY VIEW orders
USING csv
OPTIONS (
  path 'C:/Users/ke/Desktop/bigdata_learn/spark_sql/data/orders.csv',
  header 'true',
  inferSchema 'true'
);
```

之后可直接执行本目录 `cases/` 中的 SQL 片段。

