# 案例2：DataFrame 操作

## 案例描述
学习 Spark DataFrame 的基本操作，包括创建、查询、聚合和连接操作。

## 数据准备

### 员工数据 (employees.csv)
```csv
id,name,age,salary,department
1,张三,25,5000.0,IT
2,李四,30,8000.0,HR
3,王五,28,6000.0,IT
4,赵六,35,12000.0,Sales
5,孙七,27,5500.0,IT
6,周八,32,9000.0,HR
7,吴九,29,7000.0,Sales
8,郑十,26,4800.0,IT
9,钱一,31,8500.0,HR
10,陈二,33,11000.0,Sales
```

### 部门数据 (departments.csv)
```csv
dept_id,dept_name,location
IT,技术部,北京
HR,人力资源部,上海
Sales,销售部,广州
```

## Scala 实现

### 完整代码 (DataFrameOperations.scala)
```scala
import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._

object DataFrameOperations {
  def main(args: Array[String]): Unit = {
    // 创建 SparkSession
    val spark = SparkSession.builder()
      .appName("DataFrame Operations")
      .master("local[*]")
      .getOrCreate()
    
    import spark.implicits._
    
    try {
      // ============================================
      // 1. 创建 DataFrame
      // ============================================
      
      // 从 CSV 文件创建
      val employees = spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("data/employees.csv")
      
      val departments = spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("data/departments.csv")
      
      println("员工表:")
      employees.show()
      
      println("部门表:")
      departments.show()
      
      // ============================================
      // 2. 基本查询操作
      // ============================================
      
      // select: 选择列
      val names = employees.select("name", "salary")
      println("\n姓名和薪资:")
      names.show()
      
      // filter/where: 过滤
      val highSalary = employees.filter($"salary" > 7000)
      println("\n高薪员工 (薪资 > 7000):")
      highSalary.show()
      
      // 多条件过滤
      val itEmployees = employees.filter($"department" === "IT" && $"age" < 30)
      println("\nIT部门30岁以下员工:")
      itEmployees.show()
      
      // ============================================
      // 3. 聚合操作
      // ============================================
      
      // groupBy: 分组聚合
      val deptStats = employees.groupBy("department")
        .agg(
          count("*").alias("count"),
          avg("salary").alias("avg_salary"),
          max("salary").alias("max_salary"),
          min("salary").alias("min_salary"),
          sum("salary").alias("total_salary")
        )
      println("\n各部门统计:")
      deptStats.show()
      
      // ============================================
      // 4. 排序操作
      // ============================================
      
      // orderBy: 排序
      val sortedBySalary = employees.orderBy($"salary".desc)
      println("\n按薪资降序排序:")
      sortedBySalary.show()
      
      // 多列排序
      val sortedMulti = employees.orderBy($"department".asc, $"salary".desc)
      println("\n按部门升序、薪资降序排序:")
      sortedMulti.show()
      
      // ============================================
      // 5. 添加和修改列
      // ============================================
      
      // withColumn: 添加新列
      val withBonus = employees.withColumn("bonus", $"salary" * 0.1)
      println("\n添加奖金列 (薪资的10%):")
      withBonus.select("name", "salary", "bonus").show()
      
      // withColumnRenamed: 重命名列
      val renamed = employees.withColumnRenamed("department", "dept")
      println("\n重命名列:")
      renamed.show()
      
      // ============================================
      // 6. 连接操作
      // ============================================
      
      // join: 内连接
      val joined = employees.join(
        departments,
        employees("department") === departments("dept_id"),
        "inner"
      )
      println("\n员工和部门信息连接:")
      joined.select("name", "salary", "dept_name", "location").show()
      
      // 左连接
      val leftJoined = employees.join(
        departments,
        employees("department") === departments("dept_id"),
        "left"
      )
      println("\n左连接结果:")
      leftJoined.select("name", "dept_name").show()
      
      // ============================================
      // 7. 窗口函数
      // ============================================
      
      import org.apache.spark.sql.expressions.Window
      
      val windowSpec = Window.partitionBy("department").orderBy($"salary".desc)
      
      val withRank = employees.withColumn("rank", row_number().over(windowSpec))
      println("\n各部门薪资排名:")
      withRank.select("name", "department", "salary", "rank").show()
      
      val withAvg = employees.withColumn(
        "dept_avg_salary",
        avg("salary").over(Window.partitionBy("department"))
      )
      println("\n添加部门平均薪资:")
      withAvg.select("name", "department", "salary", "dept_avg_salary").show()
      
      // ============================================
      // 8. 保存结果
      // ============================================
      
      // 保存为 CSV
      deptStats.write
        .option("header", "true")
        .csv("output/dept_stats")
      
      // 保存为 Parquet
      joined.write.parquet("output/employees_departments")
      
      println("\n结果已保存")
      
    } finally {
      spark.stop()
    }
  }
}
```

## PySpark 实现

### 完整代码 (dataframe_operations.py)
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window

def main():
    # 创建 SparkSession
    spark = SparkSession.builder \
        .appName("DataFrame Operations") \
        .master("local[*]") \
        .getOrCreate()
    
    try:
        # ============================================
        # 1. 创建 DataFrame
        # ============================================
        
        # 从 CSV 文件创建
        employees = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv("data/employees.csv")
        
        departments = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv("data/departments.csv")
        
        print("员工表:")
        employees.show()
        
        print("部门表:")
        departments.show()
        
        # ============================================
        # 2. 基本查询操作
        # ============================================
        
        # select: 选择列
        names = employees.select("name", "salary")
        print("\n姓名和薪资:")
        names.show()
        
        # filter/where: 过滤
        high_salary = employees.filter(col("salary") > 7000)
        print("\n高薪员工 (薪资 > 7000):")
        high_salary.show()
        
        # 多条件过滤
        it_employees = employees.filter(
            (col("department") == "IT") & (col("age") < 30)
        )
        print("\nIT部门30岁以下员工:")
        it_employees.show()
        
        # ============================================
        # 3. 聚合操作
        # ============================================
        
        # groupBy: 分组聚合
        dept_stats = employees.groupBy("department") \
            .agg(
                count("*").alias("count"),
                avg("salary").alias("avg_salary"),
                max("salary").alias("max_salary"),
                min("salary").alias("min_salary"),
                sum("salary").alias("total_salary")
            )
        print("\n各部门统计:")
        dept_stats.show()
        
        # ============================================
        # 4. 排序操作
        # ============================================
        
        # orderBy: 排序
        sorted_by_salary = employees.orderBy(col("salary").desc())
        print("\n按薪资降序排序:")
        sorted_by_salary.show()
        
        # 多列排序
        sorted_multi = employees.orderBy(
            col("department").asc(),
            col("salary").desc()
        )
        print("\n按部门升序、薪资降序排序:")
        sorted_multi.show()
        
        # ============================================
        # 5. 添加和修改列
        # ============================================
        
        # withColumn: 添加新列
        with_bonus = employees.withColumn("bonus", col("salary") * 0.1)
        print("\n添加奖金列 (薪资的10%):")
        with_bonus.select("name", "salary", "bonus").show()
        
        # withColumnRenamed: 重命名列
        renamed = employees.withColumnRenamed("department", "dept")
        print("\n重命名列:")
        renamed.show()
        
        # ============================================
        # 6. 连接操作
        # ============================================
        
        # join: 内连接
        joined = employees.join(
            departments,
            employees.department == departments.dept_id,
            "inner"
        )
        print("\n员工和部门信息连接:")
        joined.select("name", "salary", "dept_name", "location").show()
        
        # 左连接
        left_joined = employees.join(
            departments,
            employees.department == departments.dept_id,
            "left"
        )
        print("\n左连接结果:")
        left_joined.select("name", "dept_name").show()
        
        # ============================================
        # 7. 窗口函数
        # ============================================
        
        window_spec = Window.partitionBy("department").orderBy(col("salary").desc())
        
        with_rank = employees.withColumn(
            "rank",
            row_number().over(window_spec)
        )
        print("\n各部门薪资排名:")
        with_rank.select("name", "department", "salary", "rank").show()
        
        with_avg = employees.withColumn(
            "dept_avg_salary",
            avg("salary").over(Window.partitionBy("department"))
        )
        print("\n添加部门平均薪资:")
        with_avg.select("name", "department", "salary", "dept_avg_salary").show()
        
        # ============================================
        # 8. 保存结果
        # ============================================
        
        # 保存为 CSV
        dept_stats.write \
            .option("header", "true") \
            .csv("output/dept_stats")
        
        # 保存为 Parquet
        joined.write.parquet("output/employees_departments")
        
        print("\n结果已保存")
        
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
```

## 预期结果

### 各部门统计
```
department | count | avg_salary | max_salary | min_salary | total_salary
-----------|-------|------------|------------|------------|-------------
HR         | 3     | 8500.0     | 9000.0     | 8000.0     | 25500.0
IT         | 4     | 5575.0     | 6000.0     | 4800.0     | 22300.0
Sales      | 3     | 10000.0    | 12000.0    | 7000.0     | 30000.0
```

### 各部门薪资排名
```
name | department | salary | rank
-----|------------|--------|-----
赵六 | Sales      | 12000.0| 1
陈二 | Sales      | 11000.0| 2
吴九 | Sales      | 7000.0 | 3
周八 | HR         | 9000.0 | 1
钱一 | HR         | 8500.0 | 2
李四 | HR         | 8000.0 | 3
王五 | IT         | 6000.0 | 1
孙七 | IT         | 5500.0 | 2
张三 | IT         | 5000.0 | 3
郑十 | IT         | 4800.0 | 4
```

## 学习要点

1. **DataFrame 创建**：从文件、集合创建 DataFrame
2. **列操作**：select、withColumn、drop
3. **过滤**：filter、where 条件过滤
4. **聚合**：groupBy、agg 聚合函数
5. **连接**：join 各种连接类型
6. **窗口函数**：排名、累计等窗口操作
7. **数据保存**：保存为不同格式
