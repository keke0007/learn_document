# Spark 学习指南

## 📚 项目概述

本指南提供了完整的 Spark 学习资源，包括基础知识、实战案例和验证数据，帮助你系统掌握 Apache Spark 大数据处理技术。所有案例都提供了 **Scala** 和 **PySpark** 两种实现方式。

---

## 📁 项目结构

```
spark/
├── README.md                    # Spark 知识点总览（详细文档）
├── GUIDE.md                     # 本指南文档（快速入门）
├── cases/                       # 实战案例目录
│   ├── rdd_basics.md           # 案例1：RDD 基础操作
│   ├── dataframe_operations.md  # 案例2：DataFrame 操作
│   ├── data_analysis.md        # 案例3：数据分析实战
│   └── spark_sql.md            # 案例4：Spark SQL 应用
├── data/                        # 验证数据目录
│   ├── words.txt               # 文本数据
│   ├── numbers.txt             # 数字数据
│   ├── employees.csv           # 员工数据
│   ├── departments.csv         # 部门数据
│   ├── orders.csv              # 订单数据
│   ├── products.csv            # 产品数据
│   └── customers.csv           # 客户数据
└── scripts/                    # 脚本和配置文件
    ├── build.sbt               # Scala 项目配置
    └── requirements.txt        # Python 依赖配置
```

---

## 🎯 学习路径

### 阶段一：Spark 基础（2-3天）
1. **Spark 基础概念**
   - 了解 Spark 架构和核心组件
   - 理解 Spark 与 Hadoop 的关系
   - 掌握 SparkContext 和 SparkSession

2. **RDD 基础**
   - 理解 RDD 的概念和特性
   - 学习 RDD 的创建方式
   - 掌握 Transformation 和 Action

### 阶段二：DataFrame 和 SQL（3-4天）
1. **DataFrame 操作**
   - 创建 DataFrame
   - 列操作、过滤、聚合
   - 连接操作

2. **Spark SQL**
   - SQL 查询
   - 视图创建
   - UDF 自定义函数

### 阶段三：实战应用（3-5天）
1. **数据分析实战**
   - 多表关联分析
   - 时间序列分析
   - 窗口函数应用

2. **性能优化**
   - 缓存和持久化
   - 分区优化
   - 广播变量和累加器

### 阶段四：高级特性（可选，5-7天）
1. **Spark Streaming**：流数据处理
2. **MLlib**：机器学习
3. **GraphX**：图计算

---

## 🚀 快速开始

### 前置要求

#### Scala 环境
- Java 8 或更高版本
- Scala 2.12
- sbt（Scala 构建工具）

#### Python 环境
- Python 3.7+
- PySpark 3.3.0

#### Spark 安装
- 下载 Spark 3.3.0
- 解压并配置环境变量

### 步骤1：环境准备

#### Scala 项目
```bash
# 使用 sbt 构建项目
cd spark/scripts
sbt compile
sbt package
```

#### Python 项目
```bash
# 安装依赖
pip install -r scripts/requirements.txt
```

### 步骤2：运行示例

#### Scala 示例
```bash
# 运行 RDD 基础示例
spark-submit --class RDDBasics \
  --master local[*] \
  target/scala-2.12/spark-learning_2.12-1.0.jar
```

#### PySpark 示例
```bash
# 运行 RDD 基础示例
spark-submit cases/rdd_basics.py
```

### 步骤3：验证结果
检查输出目录中的结果文件，验证程序是否正常运行。

---

## 📖 核心知识点速查

### 1. RDD 操作

| 操作类型 | 方法 | 说明 |
|---------|------|------|
| **创建** | `parallelize()` | 从集合创建 |
| | `textFile()` | 从文件创建 |
| **转换** | `map()` | 一对一转换 |
| | `filter()` | 过滤 |
| | `flatMap()` | 一对多转换 |
| | `reduceByKey()` | 按键聚合 |
| **行动** | `collect()` | 收集结果 |
| | `count()` | 计数 |
| | `saveAsTextFile()` | 保存文件 |

### 2. DataFrame 操作

| 操作 | Scala | PySpark |
|------|-------|---------|
| **创建** | `spark.read.csv()` | `spark.read.csv()` |
| **选择列** | `df.select()` | `df.select()` |
| **过滤** | `df.filter()` | `df.filter()` |
| **分组** | `df.groupBy().agg()` | `df.groupBy().agg()` |
| **连接** | `df1.join(df2)` | `df1.join(df2)` |

### 3. Spark SQL

```sql
-- 创建视图
df.createOrReplaceTempView("table_name")

-- SQL 查询
spark.sql("SELECT * FROM table_name")
```

### 4. 窗口函数

```scala
// Scala
import org.apache.spark.sql.expressions.Window
val windowSpec = Window.partitionBy("dept").orderBy($"salary".desc)
df.withColumn("rank", row_number().over(windowSpec))
```

```python
# PySpark
from pyspark.sql.window import Window
window_spec = Window.partitionBy("dept").orderBy(col("salary").desc())
df.withColumn("rank", row_number().over(window_spec))
```

---

## 💡 实战案例概览

### 案例1：RDD 基础操作
**学习目标**：掌握 RDD 的基本操作

**涉及知识点**：
- RDD 创建（从集合、文件）
- Transformation（map、filter、flatMap）
- Action（collect、count、reduce）
- 键值对操作（reduceByKey）
- 分区操作（mapPartitions）

**数据规模**：
- 文本文件：6 行
- 数字文件：3 行

**典型操作**：
- 单词计数
- 数据过滤和转换
- 键值对聚合

### 案例2：DataFrame 操作
**学习目标**：掌握 DataFrame 的基本操作

**涉及知识点**：
- DataFrame 创建
- 列操作（select、withColumn）
- 过滤和聚合
- 连接操作
- 窗口函数

**数据规模**：
- 员工表：10 条记录
- 部门表：3 条记录

**典型操作**：
- 各部门统计
- 薪资排名
- 多表关联

### 案例3：数据分析实战
**学习目标**：进行实际的数据分析

**涉及知识点**：
- 多表关联分析
- 时间序列分析
- 复购分析
- 窗口函数应用

**数据规模**：
- 订单表：15 条记录
- 产品表：5 条记录
- 客户表：4 条记录

**典型分析**：
- 每月销售额统计
- 产品销量排行
- 客户消费分析
- 复购客户识别

### 案例4：Spark SQL 应用
**学习目标**：使用 SQL 进行数据查询

**涉及知识点**：
- SQL 查询
- 视图创建
- UDF 注册
- 复杂查询（子查询、窗口函数）

**数据规模**：
- 使用案例3的数据

**典型查询**：
- SQL 聚合查询
- 多表 JOIN
- 窗口函数查询
- 复购分析 SQL

---

## 📊 数据说明

### 数据文件格式

| 文件名 | 格式 | 记录数 | 用途 | 案例 |
|--------|------|--------|------|------|
| words.txt | 文本 | 6 行 | 文本处理 | 案例1 |
| numbers.txt | CSV | 3 行 | 数字处理 | 案例1 |
| employees.csv | CSV | 10 | 员工信息 | 案例2 |
| departments.csv | CSV | 3 | 部门信息 | 案例2 |
| orders.csv | CSV | 15 | 订单数据 | 案例3,4 |
| products.csv | CSV | 5 | 产品信息 | 案例3,4 |
| customers.csv | CSV | 4 | 客户信息 | 案例3,4 |

### 数据字段说明

**employees.csv** 字段：
- id, name, age, salary, department

**departments.csv** 字段：
- dept_id, dept_name, location

**orders.csv** 字段：
- order_id, order_date, customer_id, product_id, quantity, total_amount

**products.csv** 字段：
- product_id, product_name, price, category

**customers.csv** 字段：
- customer_id, customer_name, city, age, register_date

---

## 🔧 使用技巧

### 1. Scala vs PySpark

**Scala 优势**：
- 性能更好（JVM 原生）
- 类型安全
- 适合生产环境

**PySpark 优势**：
- 语法简洁
- 易于学习
- 丰富的 Python 生态

**选择建议**：
- 初学者：推荐 PySpark
- 生产环境：推荐 Scala
- 数据分析：PySpark + Pandas

### 2. 性能优化

```scala
// 缓存重复使用的 RDD/DataFrame
df.cache()
df.persist()

// 合理设置分区数
rdd.repartition(200)
df.coalesce(10)

// 使用广播变量
val broadcastVar = sc.broadcast(largeData)
```

### 3. 常见问题

**问题1：内存不足**
```scala
// 增加 executor 内存
spark-submit --executor-memory 4g ...
```

**问题2：任务执行慢**
```scala
// 检查分区数
println(rdd.partitions.length)

// 使用缓存
rdd.cache()
```

**问题3：数据倾斜**
```scala
// 使用 salting 技术
val salted = rdd.map(x => (x + random, value))
```

---

## 📝 学习建议

### 初学者
1. 先学习 PySpark（语法更简单）
2. 从案例1开始，逐步练习
3. 理解 Transformation 和 Action 的区别
4. 掌握 DataFrame API 的基本操作

### 进阶学习
1. 学习 Scala 实现（性能更好）
2. 完成所有四个案例
3. 学习性能优化技巧
4. 尝试处理更大的数据集

### 实践建议
1. **动手实践**：不要只看代码，要实际运行
2. **理解原理**：了解 Spark 的执行机制
3. **性能调优**：学习如何优化 Spark 作业
4. **混合使用**：结合 RDD、DataFrame、SQL

---

## 🔗 相关资源

### 官方文档
- [Apache Spark 官方文档](https://spark.apache.org/docs/latest/)
- [Spark SQL 指南](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [PySpark API 文档](https://spark.apache.org/docs/latest/api/python/)

### 推荐阅读
- `README.md` - 详细的知识点文档
- `cases/` - 四个实战案例的详细说明
- Spark 官方示例代码

### 扩展学习
- Spark Streaming：流数据处理
- MLlib：机器学习应用
- GraphX：图计算
- Spark 性能调优

---

## ✅ 学习检查清单

完成以下任务，确保掌握 Spark 核心技能：

### 基础操作
- [ ] 能够创建 RDD 和 DataFrame
- [ ] 能够执行基本的 Transformation 和 Action
- [ ] 能够使用 DataFrame API 进行查询
- [ ] 能够使用 Spark SQL 进行查询

### 进阶操作
- [ ] 能够进行多表关联
- [ ] 能够使用窗口函数
- [ ] 能够注册和使用 UDF
- [ ] 能够进行性能优化

### 实战能力
- [ ] 完成案例1的所有操作
- [ ] 完成案例2的所有操作
- [ ] 完成案例3的所有分析
- [ ] 完成案例4的所有查询
- [ ] 能够独立设计 Spark 应用

---

## 🎓 学习成果

完成本指南的学习后，你将能够：
- ✅ 熟练使用 Spark 进行大数据处理
- ✅ 掌握 RDD 和 DataFrame 的操作
- ✅ 能够使用 Spark SQL 进行数据查询
- ✅ 理解 Spark 的性能优化方法
- ✅ 具备独立开发 Spark 应用的能力
- ✅ 掌握 Scala 和 PySpark 两种实现方式

**祝你学习愉快！** 🚀

---

## 📌 快速参考

### 启动 Spark Shell

**Scala**：
```bash
spark-shell
```

**PySpark**：
```bash
pyspark
```

### 提交作业

**Scala**：
```bash
spark-submit --class MainClass \
  --master local[*] \
  app.jar
```

**PySpark**：
```bash
spark-submit app.py
```

### 常用配置

```bash
# 设置 executor 内存
--executor-memory 4g

# 设置 executor 核心数
--executor-cores 2

# 设置 driver 内存
--driver-memory 2g
```
