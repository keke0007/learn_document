# Spark SQL 学习指南（费曼学习法）：知识点 + 案例 + 验证数据

> 目标：把 Spark SQL 学到“能解释清楚、能在 `spark-shell` 或应用里写出能跑的 SQL/DSL，并能用小数据对照结果”的程度。

本目录自带：
- **验证数据**：`spark_sql/data/`
  - `orders.csv`、`user_events.csv`、`dim_products.csv`
- **案例**：`spark_sql/cases/`
  - `cases/README.md`（索引页）
  - 4 个可执行案例（Scala 代码 + 期望结果）
- **运行说明**：`spark_sql/scripts/run_spark_sql.md`

---

## 0. 费曼学习法在 Spark SQL 上怎么用

每个知识点都按这 5 步来：
- **一句话讲明白**：不用术语也能说得让人点头
- **关键术语补齐**：把“模糊印象”变成“可配置、可查看的东西”
- **能写出的最小示例**：3–10 行代码 / SQL 就能跑
- **能算出来的小例子**：用 10 行 CSV 手算结果
- **能解释的坑**：为什么生产里会慢、会 OOM、会结果不对

---

## 1. 核心知识点清单（Spark SQL 视角）

### 1.1 SparkSession / DataFrame / Dataset
- **一句话**：SparkSession 是“入口”，DataFrame/Dataset 是“表”，SQL 是针对这张表的声明式查询。
- **你必须知道**
  - `SparkSession.builder().getOrCreate()`
  - `spark.read.option("header","true").csv(...)` → DataFrame
  - Dataset = 有类型的 DataFrame（Scala/Java 强类型场景）

### 1.2 DataFrame API vs Spark SQL
- **一句话**：同一件事既可以用链式 API 写，也可以用 SQL 写，底层走的是同一个优化器。
- **你必须会写**
  - DataFrame 形式：`df.groupBy("user_id").agg(sum("amount"))`
  - SQL 形式：注册视图 + `spark.sql("SELECT ...")`

### 1.3 Schema / 类型与读取数据
- **一句话**：Schema 决定每列是什么类型，这决定了你能做什么算子。
- **你必须知道**
  - `inferSchema` 的便利与局限（生产常用显式 schema）
  - 常见类型：`StringType/IntegerType/DoubleType/TimestampType`

### 1.4 SQL 基础：过滤 / 分组聚合 / 排序
- **一句话**：和传统 SQL 一样，但执行在分布式 DataFrame 上。
- **你必须会写**
  - `SELECT ... FROM t WHERE ... GROUP BY ... ORDER BY ...`

### 1.5 分析函数（Window Functions）
- **一句话**：在“每个小分组内部”再按某种顺序打标签、做排名、算累积和等。
- **你必须知道**
  - `ROW_NUMBER() OVER (PARTITION BY k ORDER BY ts)`
  - `RANK()`、`DENSE_RANK()`、`SUM() OVER (...)`（进阶）

### 1.6 Join 与维度建模
- **一句话**：事实表里是“发生了什么”，维表里是“这是什么”，Join 把两者拼起来。
- **你必须会写**
  - `df.join(dim, "product_id")`
  - `SELECT ... FROM facts JOIN dim ON ...`

### 1.7 Catalyst 优化器与物理执行（只需要直觉）
- **一句话**：Spark 会自动改写/重排你的查询，选择合适的 join/聚合/执行计划。
- **你必须知道**
  - `df.explain(true)` 能看见逻辑计划 / 物理计划 / shuffle 位置

### 1.8 Shuffle / 分区 / cache（性能的关键）
- **一句话**：宽依赖（groupBy/join）会 shuffle，shuffle 会影响性能；cache 可以避免重复计算。
- **你必须知道**
  - `spark.sql.shuffle.partitions`（默认 200，通常需要调小）
  - `df.repartition(n)`、`df.coalesce(n)`
  - `df.cache()` / `df.persist()`

---

## 2. 案例与验证数据（建议顺序）

### 案例1：DataFrame / 视图 / 聚合（入门闭环）
- 文档：`cases/01_spark_sql_ddl_dml_basics.md`
- 数据：`data/orders.csv`
- 你要验证的结果：
  - U001：cnt=3 total=30.0
  - U002：cnt=3 total=30.0
  - U003：cnt=1 total=8.0

### 案例2：窗口函数（按时间排序 + 最新事件）
- 文档：`cases/02_spark_sql_window_functions_time.md`
- 数据：`data/user_events.csv`
- 你要验证的结果（最新事件）：
  - U001 → 09:00:18 view P003
  - U002 → 09:00:12 buy  P002
  - U003 → 09:00:22 buy  P003

### 案例3：Join + 维度聚合
- 文档：`cases/03_spark_sql_joins_dim_agg.md`
- 数据：`data/orders.csv` + `data/dim_products.csv`
- 你要验证的结果：
  - cat_a：cnt=5 total_amount=55.0
  - cat_b：cnt=2 total_amount=13.0

### 案例4：性能与最佳实践（小实验）
- 文档：`cases/04_spark_sql_performance_best_practices.md`
- 你要学会：
  - 看 `explain(true)` 识别 shuffle
  - 调整 `spark.sql.shuffle.partitions`
  - 通过 `cache()` 避免重复扫描

---

## 3. 费曼式解释：Spark SQL vs 传统数据库

- **相同点**
  - 都是“表 + SQL”模型，有 SELECT / WHERE / GROUP BY / JOIN 等。
  - 都可以用分析函数做排名/去重/TopN。
- **不同点**
  - Spark SQL 面向分布式大数据集，执行在集群上，有 shuffle / 分区概念。
  - Spark SQL 通常是“离线批处理/大规模分析”，而不是单条事务。
  - Spark 可以方便和其他 Spark 组件联动（MLlib、Streaming 等）。

---

## 4. 最终总结：一页速查 Checklist

### 4.1 能用自己的话说清楚
- **SparkSession**：Spark SQL 的入口，持有 catalog、配置、执行环境。
- **DataFrame**：带 schema 的分布式表，所有 SQL 都跑在它上面。
- **Window Function**：在分区内部按顺序“看前看后”的工具。
- **Join + 维表**：把事实和维度拼在一起才能做多维分析。
- **shuffle / partitions / cache**：性能调优的 3 个关键旋钮。

### 4.2 上手与上线前自查
- [ ] 会用 DataFrame API 和 SQL 两种方式表达同一个需求。
- [ ] 会用 `explain(true)` 看懂大致执行计划（知道哪里会 shuffle）。
- [ ] 知道如何设置 `spark.sql.shuffle.partitions`，避免默认 200 带来的小任务过多。
- [ ] 知道在“反复重用中间结果”的场景下用 `cache()`/`persist()`。

