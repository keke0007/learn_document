# 案例2：窗口操作

## 案例描述
学习 Flink 窗口操作，包括滚动窗口、滑动窗口和会话窗口。

## 数据准备

### 订单数据流 (模拟实时数据)
```
order_id,product_id,amount,timestamp
1001,P001,299.00,2024-01-15 09:00:00
1002,P002,599.00,2024-01-15 09:01:00
1003,P001,299.00,2024-01-15 09:02:00
1004,P003,199.00,2024-01-15 09:03:00
1005,P002,599.00,2024-01-15 09:04:00
1006,P001,299.00,2024-01-15 09:10:00
1007,P003,199.00,2024-01-15 09:11:00
1008,P002,599.00,2024-01-15 09:12:00
```

## Java 实现

### 完整代码 (WindowOperations.java)
```java
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.common.functions.ReduceFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class WindowOperations {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // 设置事件时间
        env.setStreamTimeCharacteristic(org.apache.flink.streaming.api.TimeCharacteristic.EventTime);
        
        // ============================================
        // 1. 创建测试数据流
        // ============================================
        
        DataStream<Order> orders = env.fromElements(
            new Order("1001", "P001", 299.0, "2024-01-15 09:00:00"),
            new Order("1002", "P002", 599.0, "2024-01-15 09:01:00"),
            new Order("1003", "P001", 299.0, "2024-01-15 09:02:00"),
            new Order("1004", "P003", 199.0, "2024-01-15 09:03:00"),
            new Order("1005", "P002", 599.0, "2024-01-15 09:04:00"),
            new Order("1006", "P001", 299.0, "2024-01-15 09:10:00"),
            new Order("1007", "P003", 199.0, "2024-01-15 09:11:00"),
            new Order("1008", "P002", 599.0, "2024-01-15 09:12:00")
        );
        
        // 分配时间戳和水位线
        DataStream<Order> ordersWithTime = orders
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<Order>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withTimestampAssigner((order, timestamp) -> 
                        order.getTimestamp()
                    )
            );
        
        // ============================================
        // 2. 滚动窗口（Tumbling Window）
        // ============================================
        
        // 每5秒统计一次销售额
        DataStream<Tuple2<String, Double>> tumblingWindow = ordersWithTime
            .keyBy(Order::getProductId)
            .window(TumblingEventTimeWindows.of(Time.seconds(5)))
            .aggregate(new AggregateFunction<Order, Tuple2<String, Double>, Tuple2<String, Double>>() {
                @Override
                public Tuple2<String, Double> createAccumulator() {
                    return new Tuple2<>("", 0.0);
                }
                
                @Override
                public Tuple2<String, Double> add(Order value, Tuple2<String, Double> accumulator) {
                    return new Tuple2<>(value.getProductId(), accumulator.f1 + value.getAmount());
                }
                
                @Override
                public Tuple2<String, Double> getResult(Tuple2<String, Double> accumulator) {
                    return accumulator;
                }
                
                @Override
                public Tuple2<String, Double> merge(Tuple2<String, Double> a, Tuple2<String, Double> b) {
                    return new Tuple2<>(a.f0, a.f1 + b.f1);
                }
            });
        
        System.out.println("滚动窗口结果（每5秒）:");
        tumblingWindow.print("TumblingWindow");
        
        // ============================================
        // 3. 滑动窗口（Sliding Window）
        // ============================================
        
        // 每5秒统计一次，窗口大小10秒
        DataStream<Tuple2<String, Double>> slidingWindow = ordersWithTime
            .keyBy(Order::getProductId)
            .window(SlidingEventTimeWindows.of(Time.seconds(10), Time.seconds(5)))
            .reduce(new ReduceFunction<Order>() {
                @Override
                public Order reduce(Order value1, Order value2) throws Exception {
                    return new Order(
                        value1.getOrderId(),
                        value1.getProductId(),
                        value1.getAmount() + value2.getAmount(),
                        value1.getTimestamp()
                    );
                }
            })
            .map(order -> new Tuple2<>(order.getProductId(), order.getAmount()));
        
        System.out.println("\n滑动窗口结果（窗口10秒，滑动5秒）:");
        slidingWindow.print("SlidingWindow");
        
        // ============================================
        // 4. 会话窗口（Session Window）
        // ============================================
        
        // 5秒无活动则关闭窗口
        DataStream<Tuple2<String, Double>> sessionWindow = ordersWithTime
            .keyBy(Order::getProductId)
            .window(EventTimeSessionWindows.withGap(Time.seconds(5)))
            .aggregate(new AggregateFunction<Order, Tuple2<String, Double>, Tuple2<String, Double>>() {
                @Override
                public Tuple2<String, Double> createAccumulator() {
                    return new Tuple2<>("", 0.0);
                }
                
                @Override
                public Tuple2<String, Double> add(Order value, Tuple2<String, Double> accumulator) {
                    return new Tuple2<>(value.getProductId(), accumulator.f1 + value.getAmount());
                }
                
                @Override
                public Tuple2<String, Double> getResult(Tuple2<String, Double> accumulator) {
                    return accumulator;
                }
                
                @Override
                public Tuple2<String, Double> merge(Tuple2<String, Double> a, Tuple2<String, Double> b) {
                    return new Tuple2<>(a.f0, a.f1 + b.f1);
                }
            });
        
        System.out.println("\n会话窗口结果（间隔5秒）:");
        sessionWindow.print("SessionWindow");
        
        env.execute("Window Operations");
    }
    
    // 订单类
    public static class Order {
        private String orderId;
        private String productId;
        private double amount;
        private long timestamp;
        
        public Order(String orderId, String productId, double amount, String timeStr) {
            this.orderId = orderId;
            this.productId = productId;
            this.amount = amount;
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
            this.timestamp = LocalDateTime.parse(timeStr, formatter).atZone(java.time.ZoneId.systemDefault()).toInstant().toEpochMilli();
        }
        
        public String getOrderId() { return orderId; }
        public String getProductId() { return productId; }
        public double getAmount() { return amount; }
        public long getTimestamp() { return timestamp; }
    }
}
```

## Scala 实现

### 完整代码 (WindowOperations.scala)
```scala
import org.apache.flink.api.common.eventtime.{WatermarkStrategy, TimestampAssigner}
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.assigners.{TumblingEventTimeWindows, SlidingEventTimeWindows, EventTimeSessionWindows}
import org.apache.flink.streaming.api.windowing.time.Time

import java.time.{Duration, LocalDateTime, ZoneId}
import java.time.format.DateTimeFormatter

case class Order(orderId: String, productId: String, amount: Double, timestamp: Long)

object WindowOperations {
  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    
    // 设置事件时间
    env.setStreamTimeCharacteristic(org.apache.flink.streaming.api.TimeCharacteristic.EventTime)
    
    // ============================================
    // 1. 创建测试数据流
    // ============================================
    
    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
    
    val orders = env.fromElements(
      Order("1001", "P001", 299.0, parseTime("2024-01-15 09:00:00", formatter)),
      Order("1002", "P002", 599.0, parseTime("2024-01-15 09:01:00", formatter)),
      Order("1003", "P001", 299.0, parseTime("2024-01-15 09:02:00", formatter)),
      Order("1004", "P003", 199.0, parseTime("2024-01-15 09:03:00", formatter)),
      Order("1005", "P002", 599.0, parseTime("2024-01-15 09:04:00", formatter)),
      Order("1006", "P001", 299.0, parseTime("2024-01-15 09:10:00", formatter)),
      Order("1007", "P003", 199.0, parseTime("2024-01-15 09:11:00", formatter)),
      Order("1008", "P002", 599.0, parseTime("2024-01-15 09:12:00", formatter))
    )
    
    // 分配时间戳和水位线
    val ordersWithTime = orders
      .assignTimestampsAndWatermarks(
        WatermarkStrategy
          .forBoundedOutOfOrderness[Order](Duration.ofSeconds(5))
          .withTimestampAssigner(new TimestampAssigner[Order] {
            override def extractTimestamp(element: Order, recordTimestamp: Long): Long = {
              element.timestamp
            }
          })
      )
    
    // ============================================
    // 2. 滚动窗口（Tumbling Window）
    // ============================================
    
    val tumblingWindow = ordersWithTime
      .keyBy(_.productId)
      .window(TumblingEventTimeWindows.of(Time.seconds(5)))
      .aggregate(new AggregateFunction[Order, (String, Double), (String, Double)] {
        override def createAccumulator(): (String, Double) = ("", 0.0)
        
        override def add(value: Order, accumulator: (String, Double)): (String, Double) = {
          (value.productId, accumulator._2 + value.amount)
        }
        
        override def getResult(accumulator: (String, Double)): (String, Double) = accumulator
        
        override def merge(a: (String, Double), b: (String, Double)): (String, Double) = {
          (a._1, a._2 + b._2)
        }
      })
    
    println("滚动窗口结果（每5秒）:")
    tumblingWindow.print("TumblingWindow")
    
    // ============================================
    // 3. 滑动窗口（Sliding Window）
    // ============================================
    
    val slidingWindow = ordersWithTime
      .keyBy(_.productId)
      .window(SlidingEventTimeWindows.of(Time.seconds(10), Time.seconds(5)))
      .reduce((a, b) => Order(a.orderId, a.productId, a.amount + b.amount, a.timestamp))
      .map(order => (order.productId, order.amount))
    
    println("\n滑动窗口结果（窗口10秒，滑动5秒）:")
    slidingWindow.print("SlidingWindow")
    
    // ============================================
    // 4. 会话窗口（Session Window）
    // ============================================
    
    val sessionWindow = ordersWithTime
      .keyBy(_.productId)
      .window(EventTimeSessionWindows.withGap(Time.seconds(5)))
      .aggregate(new AggregateFunction[Order, (String, Double), (String, Double)] {
        override def createAccumulator(): (String, Double) = ("", 0.0)
        
        override def add(value: Order, accumulator: (String, Double)): (String, Double) = {
          (value.productId, accumulator._2 + value.amount)
        }
        
        override def getResult(accumulator: (String, Double)): (String, Double) = accumulator
        
        override def merge(a: (String, Double), b: (String, Double)): (String, Double) = {
          (a._1, a._2 + b._2)
        }
      })
    
    println("\n会话窗口结果（间隔5秒）:")
    sessionWindow.print("SessionWindow")
    
    env.execute("Window Operations")
  }
  
  def parseTime(timeStr: String, formatter: DateTimeFormatter): Long = {
    LocalDateTime.parse(timeStr, formatter)
      .atZone(ZoneId.systemDefault())
      .toInstant
      .toEpochMilli
  }
}
```

## 学习要点

1. **窗口类型**：滚动、滑动、会话、计数窗口
2. **时间语义**：Event Time、Processing Time
3. **水位线**：处理乱序数据
4. **窗口函数**：ReduceFunction、AggregateFunction
5. **窗口分配器**：TumblingEventTimeWindows、SlidingEventTimeWindows
