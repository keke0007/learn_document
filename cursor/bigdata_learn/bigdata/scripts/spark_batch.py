"""
Spark 批处理示例
演示 Spark 离线批处理的各种操作
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum, count, max, min
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# 创建 SparkSession
spark = SparkSession.builder \
    .appName("SparkBatchProcessing") \
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
    .enableHiveSupport() \
    .getOrCreate()

# 示例1：读取 CSV 文件
print("=== 示例1：读取 CSV 文件 ===")
df = spark.read.csv(
    "hdfs://namenode:9000/data/users.csv",
    header=True,
    inferSchema=True
)
df.show(5)
df.printSchema()

# 示例2：DataFrame 操作
print("\n=== 示例2：DataFrame 操作 ===")
result = df \
    .filter(col("age") > 25) \
    .groupBy("department") \
    .agg(
        count("*").alias("count"),
        avg("salary").alias("avg_salary"),
        sum("salary").alias("total_salary"),
        max("salary").alias("max_salary"),
        min("salary").alias("min_salary")
    ) \
    .orderBy(col("avg_salary").desc())

result.show()

# 示例3：SQL 查询
print("\n=== 示例3：SQL 查询 ===")
df.createOrReplaceTempView("users")

result_sql = spark.sql("""
    SELECT 
        department,
        COUNT(*) as count,
        AVG(salary) as avg_salary,
        MAX(salary) as max_salary,
        MIN(salary) as min_salary,
        SUM(salary) as total_salary
    FROM users
    WHERE age > 25
    GROUP BY department
    HAVING count > 5
    ORDER BY avg_salary DESC
""")

result_sql.show()

# 示例4：数据写入
print("\n=== 示例4：数据写入 ===")
result.write \
    .mode("overwrite") \
    .format("parquet") \
    .option("compression", "snappy") \
    .save("hdfs://namenode:9000/data/output/department_stats")

# 示例5：读取 Parquet
print("\n=== 示例5：读取 Parquet ===")
parquet_df = spark.read.parquet("hdfs://namenode:9000/data/output/department_stats")
parquet_df.show()

# 示例6：数据转换
print("\n=== 示例6：数据转换 ===")
transformed_df = df \
    .withColumn("salary_level", 
        when(col("salary") < 10000, "Low")
        .when(col("salary") < 20000, "Medium")
        .otherwise("High")) \
    .withColumn("age_group",
        when(col("age") < 30, "Young")
        .when(col("age") < 50, "Middle")
        .otherwise("Senior"))

transformed_df.show(10)

# 示例7：连接操作
print("\n=== 示例7：连接操作 ===")
# 假设有部门表
departments = spark.createDataFrame([
    ("IT", "Information Technology"),
    ("HR", "Human Resources"),
    ("Finance", "Finance Department")
], ["dept_code", "dept_name"])

joined_df = df.join(departments, df.department == departments.dept_code, "left")
joined_df.select("name", "department", "dept_name", "salary").show()

# 示例8：窗口函数
print("\n=== 示例8：窗口函数 ===")
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank

window_spec = Window.partitionBy("department").orderBy(col("salary").desc())

ranked_df = df.withColumn("rank", rank().over(window_spec)) \
              .withColumn("dense_rank", dense_rank().over(window_spec)) \
              .withColumn("row_number", row_number().over(window_spec))

ranked_df.filter(col("rank") <= 3).show()

spark.stop()
