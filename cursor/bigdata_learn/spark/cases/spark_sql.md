# 案例4：Spark SQL 应用

## 案例描述
学习使用 Spark SQL 进行数据查询和分析，包括 SQL 查询、UDF、视图等。

## 数据准备

使用案例3的数据文件（orders.csv, products.csv, customers.csv）

## Scala 实现

### 完整代码 (SparkSQLApp.scala)
```scala
import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._

object SparkSQLApp {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("Spark SQL Application")
      .master("local[*]")
      .getOrCreate()
    
    import spark.implicits._
    
    try {
      // ============================================
      // 1. 加载数据并创建视图
      // ============================================
      
      val orders = spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("data/orders.csv")
        .withColumn("order_date", to_date($"order_date", "yyyy-MM-dd"))
      
      val products = spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("data/products.csv")
      
      val customers = spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("data/customers.csv")
      
      // 创建临时视图
      orders.createOrReplaceTempView("orders")
      products.createOrReplaceTempView("products")
      customers.createOrReplaceTempView("customers")
      
      // ============================================
      // 2. 基本 SQL 查询
      // ============================================
      
      // 查询所有订单
      val allOrders = spark.sql("SELECT * FROM orders LIMIT 10")
      println("所有订单:")
      allOrders.show()
      
      // 条件查询
      val highValueOrders = spark.sql("""
        SELECT * FROM orders 
        WHERE total_amount > 500 
        ORDER BY total_amount DESC
      """)
      println("\n高价值订单:")
      highValueOrders.show()
      
      // ============================================
      // 3. 聚合查询
      // ============================================
      
      // 每月销售额
      val monthlySales = spark.sql("""
        SELECT 
          YEAR(order_date) as year,
          MONTH(order_date) as month,
          COUNT(*) as order_count,
          SUM(total_amount) as monthly_sales,
          AVG(total_amount) as avg_order_amount
        FROM orders
        GROUP BY YEAR(order_date), MONTH(order_date)
        ORDER BY year, month
      """)
      println("\n每月销售额:")
      monthlySales.show()
      
      // ============================================
      // 4. JOIN 查询
      // ============================================
      
      // 订单详情（三表关联）
      val orderDetails = spark.sql("""
        SELECT 
          o.order_id,
          o.order_date,
          c.customer_name,
          c.city,
          p.product_name,
          p.category,
          o.quantity,
          o.total_amount
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
        ORDER BY o.order_date DESC
      """)
      println("\n订单详情:")
      orderDetails.show()
      
      // ============================================
      // 5. 窗口函数
      // ============================================
      
      // 客户订单排名
      val customerRanking = spark.sql("""
        SELECT 
          customer_name,
          order_date,
          total_amount,
          ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
          ) as order_sequence,
          SUM(total_amount) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
          ) as cumulative_spent
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        ORDER BY customer_name, order_date
      """)
      println("\n客户订单排名:")
      customerRanking.show()
      
      // ============================================
      // 6. 子查询
      // ============================================
      
      // 高于平均订单金额的订单
      val aboveAvgOrders = spark.sql("""
        SELECT * FROM orders
        WHERE total_amount > (
          SELECT AVG(total_amount) FROM orders
        )
        ORDER BY total_amount DESC
      """)
      println("\n高于平均金额的订单:")
      aboveAvgOrders.show()
      
      // ============================================
      // 7. 注册 UDF（用户定义函数）
      // ============================================
      
      // 注册简单的 UDF
      spark.udf.register("double_amount", (amount: Double) => amount * 2)
      
      val withDouble = spark.sql("""
        SELECT 
          order_id,
          total_amount,
          double_amount(total_amount) as doubled_amount
        FROM orders
        LIMIT 5
      """)
      println("\n使用 UDF 计算双倍金额:")
      withDouble.show()
      
      // ============================================
      // 8. 创建全局临时视图
      // ============================================
      
      orderDetails.createOrReplaceGlobalTempView("order_details_global")
      
      // 在另一个 SparkSession 中也可以访问
      val globalView = spark.sql("SELECT * FROM global_temp.order_details_global LIMIT 5")
      println("\n全局临时视图:")
      globalView.show()
      
      // ============================================
      // 9. 复杂查询：复购分析
      // ============================================
      
      val repeatCustomers = spark.sql("""
        SELECT 
          c.customer_name,
          COUNT(DISTINCT o.order_id) as order_count,
          SUM(o.total_amount) as total_spent,
          MIN(o.order_date) as first_order_date,
          MAX(o.order_date) as last_order_date,
          DATEDIFF(MAX(o.order_date), MIN(o.order_date)) as days_between
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.customer_name
        HAVING COUNT(DISTINCT o.order_id) >= 2
        ORDER BY order_count DESC
      """)
      println("\n复购客户分析:")
      repeatCustomers.show()
      
      // ============================================
      // 10. 保存查询结果
      // ============================================
      
      monthlySales.write
        .option("header", "true")
        .csv("output/monthly_sales_sql")
      
      println("\n查询结果已保存")
      
    } finally {
      spark.stop()
    }
  }
}
```

## PySpark 实现

### 完整代码 (spark_sql_app.py)
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

def main():
    spark = SparkSession.builder \
        .appName("Spark SQL Application") \
        .master("local[*]") \
        .getOrCreate()
    
    try:
        # ============================================
        # 1. 加载数据并创建视图
        # ============================================
        
        orders = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv("data/orders.csv") \
            .withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd"))
        
        products = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv("data/products.csv")
        
        customers = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv("data/customers.csv")
        
        # 创建临时视图
        orders.createOrReplaceTempView("orders")
        products.createOrReplaceTempView("products")
        customers.createOrReplaceTempView("customers")
        
        # ============================================
        # 2. 基本 SQL 查询
        # ============================================
        
        # 查询所有订单
        all_orders = spark.sql("SELECT * FROM orders LIMIT 10")
        print("所有订单:")
        all_orders.show()
        
        # 条件查询
        high_value_orders = spark.sql("""
            SELECT * FROM orders 
            WHERE total_amount > 500 
            ORDER BY total_amount DESC
        """)
        print("\n高价值订单:")
        high_value_orders.show()
        
        # ============================================
        # 3. 聚合查询
        # ============================================
        
        # 每月销售额
        monthly_sales = spark.sql("""
            SELECT 
                YEAR(order_date) as year,
                MONTH(order_date) as month,
                COUNT(*) as order_count,
                SUM(total_amount) as monthly_sales,
                AVG(total_amount) as avg_order_amount
            FROM orders
            GROUP BY YEAR(order_date), MONTH(order_date)
            ORDER BY year, month
        """)
        print("\n每月销售额:")
        monthly_sales.show()
        
        # ============================================
        # 4. JOIN 查询
        # ============================================
        
        # 订单详情（三表关联）
        order_details = spark.sql("""
            SELECT 
                o.order_id,
                o.order_date,
                c.customer_name,
                c.city,
                p.product_name,
                p.category,
                o.quantity,
                o.total_amount
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN products p ON o.product_id = p.product_id
            ORDER BY o.order_date DESC
        """)
        print("\n订单详情:")
        order_details.show()
        
        # ============================================
        # 5. 窗口函数
        # ============================================
        
        # 客户订单排名
        customer_ranking = spark.sql("""
            SELECT 
                customer_name,
                order_date,
                total_amount,
                ROW_NUMBER() OVER (
                    PARTITION BY customer_id 
                    ORDER BY order_date
                ) as order_sequence,
                SUM(total_amount) OVER (
                    PARTITION BY customer_id 
                    ORDER BY order_date
                ) as cumulative_spent
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            ORDER BY customer_name, order_date
        """)
        print("\n客户订单排名:")
        customer_ranking.show()
        
        # ============================================
        # 6. 子查询
        # ============================================
        
        # 高于平均订单金额的订单
        above_avg_orders = spark.sql("""
            SELECT * FROM orders
            WHERE total_amount > (
                SELECT AVG(total_amount) FROM orders
            )
            ORDER BY total_amount DESC
        """)
        print("\n高于平均金额的订单:")
        above_avg_orders.show()
        
        # ============================================
        # 7. 注册 UDF（用户定义函数）
        # ============================================
        
        # 注册简单的 UDF
        def double_amount(amount):
            return amount * 2
        
        spark.udf.register("double_amount", double_amount, DoubleType())
        
        with_double = spark.sql("""
            SELECT 
                order_id,
                total_amount,
                double_amount(total_amount) as doubled_amount
            FROM orders
            LIMIT 5
        """)
        print("\n使用 UDF 计算双倍金额:")
        with_double.show()
        
        # ============================================
        # 8. 创建全局临时视图
        # ============================================
        
        order_details.createOrReplaceGlobalTempView("order_details_global")
        
        # 在另一个 SparkSession 中也可以访问
        global_view = spark.sql("SELECT * FROM global_temp.order_details_global LIMIT 5")
        print("\n全局临时视图:")
        global_view.show()
        
        # ============================================
        # 9. 复杂查询：复购分析
        # ============================================
        
        repeat_customers = spark.sql("""
            SELECT 
                c.customer_name,
                COUNT(DISTINCT o.order_id) as order_count,
                SUM(o.total_amount) as total_spent,
                MIN(o.order_date) as first_order_date,
                MAX(o.order_date) as last_order_date,
                DATEDIFF(MAX(o.order_date), MIN(o.order_date)) as days_between
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.customer_name
            HAVING COUNT(DISTINCT o.order_id) >= 2
            ORDER BY order_count DESC
        """)
        print("\n复购客户分析:")
        repeat_customers.show()
        
        # ============================================
        # 10. 保存查询结果
        # ============================================
        
        monthly_sales.write \
            .option("header", "true") \
            .csv("output/monthly_sales_sql")
        
        print("\n查询结果已保存")
        
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
```

## 学习要点

1. **SQL 查询**：使用标准 SQL 进行数据查询
2. **视图创建**：临时视图和全局临时视图
3. **UDF 注册**：自定义函数扩展功能
4. **复杂查询**：子查询、窗口函数、多表关联
5. **SQL 与 DataFrame API**：两种方式可以混合使用
