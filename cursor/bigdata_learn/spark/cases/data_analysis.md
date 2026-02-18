# 案例3：数据分析实战

## 案例描述
使用 Spark 进行实际数据分析，包括销售数据分析、用户行为分析等。

## 数据准备

### 订单数据 (orders.csv)
```csv
order_id,order_date,customer_id,product_id,quantity,total_amount
1001,2024-01-15,C001,P001,2,299.00
1002,2024-01-16,C002,P002,1,599.00
1003,2024-01-17,C001,P003,3,899.00
1004,2024-01-18,C003,P001,1,299.00
1005,2024-01-19,C002,P004,2,199.00
1006,2024-02-01,C001,P002,1,599.00
1007,2024-02-02,C004,P003,2,599.00
1008,2024-02-03,C003,P001,3,897.00
1009,2024-02-04,C002,P004,1,199.00
1010,2024-02-05,C001,P005,2,399.00
1011,2024-03-10,C004,P001,1,299.00
1012,2024-03-11,C003,P002,2,1198.00
1013,2024-03-12,C001,P003,1,299.00
1014,2024-03-13,C002,P004,3,597.00
1015,2024-03-14,C004,P005,1,199.00
```

### 产品数据 (products.csv)
```csv
product_id,product_name,price,category
P001,手机,299.00,电子产品
P002,笔记本电脑,599.00,电子产品
P003,耳机,299.00,电子产品
P004,鼠标,199.00,电子产品
P005,键盘,199.00,电子产品
```

### 客户数据 (customers.csv)
```csv
customer_id,customer_name,city,age,register_date
C001,张三,北京,25,2023-01-01
C002,李四,上海,30,2023-02-15
C003,王五,广州,28,2023-03-20
C004,赵六,深圳,35,2023-04-10
```

## Scala 实现

### 完整代码 (DataAnalysis.scala)
```scala
import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object DataAnalysis {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("Data Analysis")
      .master("local[*]")
      .getOrCreate()
    
    import spark.implicits._
    
    try {
      // ============================================
      // 1. 加载数据
      // ============================================
      
      val orders = spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("data/orders.csv")
      
      val products = spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("data/products.csv")
      
      val customers = spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("data/customers.csv")
      
      // 转换日期类型
      val ordersWithDate = orders.withColumn(
        "order_date",
        to_date($"order_date", "yyyy-MM-dd")
      )
      
      // ============================================
      // 2. 销售统计
      // ============================================
      
      // 总销售额
      val totalSales = ordersWithDate.agg(sum("total_amount").alias("total_sales"))
      println("总销售额:")
      totalSales.show()
      
      // 每月销售额
      val monthlySales = ordersWithDate
        .groupBy(
          year($"order_date").alias("year"),
          month($"order_date").alias("month")
        )
        .agg(
          count("*").alias("order_count"),
          sum("total_amount").alias("monthly_sales"),
          avg("total_amount").alias("avg_order_amount")
        )
        .orderBy("year", "month")
      
      println("\n每月销售额:")
      monthlySales.show()
      
      // ============================================
      // 3. 产品分析
      // ============================================
      
      // 产品销量排行
      val productSales = ordersWithDate
        .join(products, ordersWithDate("product_id") === products("product_id"))
        .groupBy("product_name", "category")
        .agg(
          sum("quantity").alias("total_quantity"),
          sum("total_amount").alias("total_sales"),
          countDistinct("order_id").alias("order_count")
        )
        .orderBy($"total_sales".desc)
      
      println("\n产品销量排行:")
      productSales.show()
      
      // ============================================
      // 4. 客户分析
      // ============================================
      
      // 客户消费排行
      val customerSpending = ordersWithDate
        .join(customers, ordersWithDate("customer_id") === customers("customer_id"))
        .groupBy("customer_name", "city")
        .agg(
          countDistinct("order_id").alias("order_count"),
          sum("total_amount").alias("total_spent"),
          avg("total_amount").alias("avg_order_amount")
        )
        .orderBy($"total_spent".desc)
      
      println("\n客户消费排行:")
      customerSpending.show()
      
      // 城市销售分析
      val citySales = ordersWithDate
        .join(customers, ordersWithDate("customer_id") === customers("customer_id"))
        .groupBy("city")
        .agg(
          countDistinct("customer_id").alias("customer_count"),
          countDistinct("order_id").alias("order_count"),
          sum("total_amount").alias("city_sales")
        )
        .orderBy($"city_sales".desc)
      
      println("\n城市销售分析:")
      citySales.show()
      
      // ============================================
      // 5. 时间序列分析
      // ============================================
      
      import org.apache.spark.sql.expressions.Window
      
      // 每月销售额及累计销售额
      val windowSpec = Window.orderBy("year", "month")
      
      val salesWithCumulative = monthlySales
        .withColumn(
          "cumulative_sales",
          sum("monthly_sales").over(windowSpec)
        )
      
      println("\n每月销售额及累计:")
      salesWithCumulative.show()
      
      // ============================================
      // 6. 复购分析
      // ============================================
      
      // 复购客户（购买次数>=2）
      val repeatCustomers = ordersWithDate
        .join(customers, ordersWithDate("customer_id") === customers("customer_id"))
        .groupBy("customer_name")
        .agg(
          countDistinct("order_id").alias("order_count"),
          sum("total_amount").alias("total_spent"),
          min("order_date").alias("first_order_date"),
          max("order_date").alias("last_order_date")
        )
        .filter($"order_count" >= 2)
        .withColumn(
          "days_between",
          datediff($"last_order_date", $"first_order_date")
        )
        .orderBy($"order_count".desc)
      
      println("\n复购客户分析:")
      repeatCustomers.show()
      
      // ============================================
      // 7. 保存结果
      // ============================================
      
      monthlySales.write
        .option("header", "true")
        .csv("output/monthly_sales")
      
      productSales.write
        .option("header", "true")
        .csv("output/product_sales")
      
      println("\n分析结果已保存")
      
    } finally {
      spark.stop()
    }
  }
}
```

## PySpark 实现

### 完整代码 (data_analysis.py)
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window

def main():
    spark = SparkSession.builder \
        .appName("Data Analysis") \
        .master("local[*]") \
        .getOrCreate()
    
    try:
        # ============================================
        # 1. 加载数据
        # ============================================
        
        orders = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv("data/orders.csv")
        
        products = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv("data/products.csv")
        
        customers = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv("data/customers.csv")
        
        # 转换日期类型
        orders_with_date = orders.withColumn(
            "order_date",
            to_date(col("order_date"), "yyyy-MM-dd")
        )
        
        # ============================================
        # 2. 销售统计
        # ============================================
        
        # 总销售额
        total_sales = orders_with_date.agg(
            sum("total_amount").alias("total_sales")
        )
        print("总销售额:")
        total_sales.show()
        
        # 每月销售额
        monthly_sales = orders_with_date \
            .groupBy(
                year(col("order_date")).alias("year"),
                month(col("order_date")).alias("month")
            ) \
            .agg(
                count("*").alias("order_count"),
                sum("total_amount").alias("monthly_sales"),
                avg("total_amount").alias("avg_order_amount")
            ) \
            .orderBy("year", "month")
        
        print("\n每月销售额:")
        monthly_sales.show()
        
        # ============================================
        # 3. 产品分析
        # ============================================
        
        # 产品销量排行
        product_sales = orders_with_date \
            .join(products, orders_with_date.product_id == products.product_id) \
            .groupBy("product_name", "category") \
            .agg(
                sum("quantity").alias("total_quantity"),
                sum("total_amount").alias("total_sales"),
                countDistinct("order_id").alias("order_count")
            ) \
            .orderBy(col("total_sales").desc())
        
        print("\n产品销量排行:")
        product_sales.show()
        
        # ============================================
        # 4. 客户分析
        # ============================================
        
        # 客户消费排行
        customer_spending = orders_with_date \
            .join(customers, orders_with_date.customer_id == customers.customer_id) \
            .groupBy("customer_name", "city") \
            .agg(
                countDistinct("order_id").alias("order_count"),
                sum("total_amount").alias("total_spent"),
                avg("total_amount").alias("avg_order_amount")
            ) \
            .orderBy(col("total_spent").desc())
        
        print("\n客户消费排行:")
        customer_spending.show()
        
        # 城市销售分析
        city_sales = orders_with_date \
            .join(customers, orders_with_date.customer_id == customers.customer_id) \
            .groupBy("city") \
            .agg(
                countDistinct("customer_id").alias("customer_count"),
                countDistinct("order_id").alias("order_count"),
                sum("total_amount").alias("city_sales")
            ) \
            .orderBy(col("city_sales").desc())
        
        print("\n城市销售分析:")
        city_sales.show()
        
        # ============================================
        # 5. 时间序列分析
        # ============================================
        
        # 每月销售额及累计销售额
        window_spec = Window.orderBy("year", "month")
        
        sales_with_cumulative = monthly_sales \
            .withColumn(
                "cumulative_sales",
                sum("monthly_sales").over(window_spec)
            )
        
        print("\n每月销售额及累计:")
        sales_with_cumulative.show()
        
        # ============================================
        # 6. 复购分析
        # ============================================
        
        # 复购客户（购买次数>=2）
        repeat_customers = orders_with_date \
            .join(customers, orders_with_date.customer_id == customers.customer_id) \
            .groupBy("customer_name") \
            .agg(
                countDistinct("order_id").alias("order_count"),
                sum("total_amount").alias("total_spent"),
                min("order_date").alias("first_order_date"),
                max("order_date").alias("last_order_date")
            ) \
            .filter(col("order_count") >= 2) \
            .withColumn(
                "days_between",
                datediff(col("last_order_date"), col("first_order_date"))
            ) \
            .orderBy(col("order_count").desc())
        
        print("\n复购客户分析:")
        repeat_customers.show()
        
        # ============================================
        # 7. 保存结果
        # ============================================
        
        monthly_sales.write \
            .option("header", "true") \
            .csv("output/monthly_sales")
        
        product_sales.write \
            .option("header", "true") \
            .csv("output/product_sales")
        
        print("\n分析结果已保存")
        
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
```

## 预期结果

### 每月销售额
```
year | month | order_count | monthly_sales | avg_order_amount
-----|-------|-------------|---------------|-----------------
2024 | 1     | 5           | 2295.00       | 459.00
2024 | 2     | 5           | 2692.00       | 538.40
2024 | 3     | 5           | 2592.00       | 518.40
```

### 产品销量排行
```
product_name | category | total_quantity | total_sales | order_count
-------------|----------|----------------|-------------|-------------
笔记本电脑   | 电子产品 | 4              | 2396.00     | 4
手机         | 电子产品 | 7              | 2093.00     | 7
耳机         | 电子产品 | 6              | 1794.00     | 6
```

### 客户消费排行
```
customer_name | city | order_count | total_spent | avg_order_amount
--------------|------|-------------|-------------|-----------------
张三          | 北京 | 5           | 2095.00     | 419.00
王五          | 广州 | 3           | 2394.00     | 798.00
李四          | 上海 | 4           | 1596.00     | 399.00
赵六          | 深圳 | 3           | 1197.00     | 399.00
```

## 学习要点

1. **多表关联**：join 操作连接多个数据源
2. **时间处理**：日期转换、时间函数
3. **分组聚合**：groupBy、agg 多维度分析
4. **窗口函数**：累计计算、排名
5. **数据保存**：保存分析结果
