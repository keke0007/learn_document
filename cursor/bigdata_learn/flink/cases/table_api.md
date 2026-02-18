# 案例3：Table API 应用

## 案例描述
学习使用 Flink Table API 和 SQL 进行数据处理。

## 数据准备

使用案例2的订单数据

## Java 实现

### 完整代码 (TableAPIApp.java)
```java
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
import org.apache.flink.types.Row;

import static org.apache.flink.table.api.Expressions.$;

public class TableAPIApp {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
        
        // ============================================
        // 1. 创建数据流
        // ============================================
        
        DataStream<Order> orders = env.fromElements(
            new Order("1001", "P001", 299.0),
            new Order("1002", "P002", 599.0),
            new Order("1003", "P001", 299.0),
            new Order("1004", "P003", 199.0),
            new Order("1005", "P002", 599.0)
        );
        
        // ============================================
        // 2. 将 DataStream 转换为 Table
        // ============================================
        
        Table orderTable = tableEnv.fromDataStream(orders);
        
        // ============================================
        // 3. Table API 操作
        // ============================================
        
        // 选择列
        Table selected = orderTable.select($("productId"), $("amount"));
        System.out.println("选择列:");
        tableEnv.toDataStream(selected, Row.class).print();
        
        // 过滤
        Table filtered = orderTable.filter($("amount").isGreater(300.0));
        System.out.println("\n过滤（金额>300）:");
        tableEnv.toDataStream(filtered, Row.class).print();
        
        // 分组聚合
        Table aggregated = orderTable
            .groupBy($("productId"))
            .select($("productId"), $("amount").sum().as("totalAmount"));
        System.out.println("\n分组聚合:");
        tableEnv.toDataStream(aggregated, Row.class).print();
        
        // ============================================
        // 4. SQL 查询
        // ============================================
        
        // 注册表
        tableEnv.createTemporaryView("orders", orders);
        
        // SQL 查询
        Table sqlResult = tableEnv.sqlQuery(
            "SELECT productId, SUM(amount) as totalAmount " +
            "FROM orders " +
            "GROUP BY productId"
        );
        System.out.println("\nSQL 查询结果:");
        tableEnv.toDataStream(sqlResult, Row.class).print();
        
        env.execute("Table API Application");
    }
    
    public static class Order {
        public String orderId;
        public String productId;
        public Double amount;
        
        public Order() {}
        
        public Order(String orderId, String productId, Double amount) {
            this.orderId = orderId;
            this.productId = productId;
            this.amount = amount;
        }
    }
}
```

## Scala 实现

### 完整代码 (TableAPIApp.scala)
```scala
import org.apache.flink.streaming.api.scala._
import org.apache.flink.table.api._
import org.apache.flink.table.api.bridge.scala.StreamTableEnvironment

case class Order(orderId: String, productId: String, amount: Double)

object TableAPIApp {
  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    val tableEnv = StreamTableEnvironment.create(env)
    
    // ============================================
    // 1. 创建数据流
    // ============================================
    
    val orders = env.fromElements(
      Order("1001", "P001", 299.0),
      Order("1002", "P002", 599.0),
      Order("1003", "P001", 299.0),
      Order("1004", "P003", 199.0),
      Order("1005", "P002", 599.0)
    )
    
    // ============================================
    // 2. 将 DataStream 转换为 Table
    // ============================================
    
    val orderTable = tableEnv.fromDataStream(orders)
    
    // ============================================
    // 3. Table API 操作
    // ============================================
    
    // 选择列
    val selected = orderTable.select($"productId", $"amount")
    println("选择列:")
    tableEnv.toDataStream(selected).print()
    
    // 过滤
    val filtered = orderTable.filter($"amount" > 300.0)
    println("\n过滤（金额>300）:")
    tableEnv.toDataStream(filtered).print()
    
    // 分组聚合
    val aggregated = orderTable
      .groupBy($"productId")
      .select($"productId", $"amount".sum().as("totalAmount"))
    println("\n分组聚合:")
    tableEnv.toDataStream(aggregated).print()
    
    // ============================================
    // 4. SQL 查询
    // ============================================
    
    // 注册表
    tableEnv.createTemporaryView("orders", orders)
    
    // SQL 查询
    val sqlResult = tableEnv.sqlQuery(
      """
        |SELECT productId, SUM(amount) as totalAmount
        |FROM orders
        |GROUP BY productId
      """.stripMargin
    )
    println("\nSQL 查询结果:")
    tableEnv.toDataStream(sqlResult).print()
    
    env.execute("Table API Application")
  }
}
```

## 学习要点

1. **TableEnvironment**：Table API 的入口
2. **DataStream 转换**：fromDataStream、toDataStream
3. **Table API**：链式调用风格
4. **SQL 查询**：标准 SQL 语法
5. **窗口表函数**：TUMBLE、HOP、SESSION
