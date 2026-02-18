# 案例4：实时数据分析

## 案例描述
使用 Flink 进行实时数据分析，包括实时统计、实时聚合等场景。

## 数据准备

### 用户行为数据流 (模拟实时数据)
```
user_id,action,product_id,timestamp
U001,view,P001,2024-01-15 09:00:00
U002,click,P002,2024-01-15 09:01:00
U001,buy,P001,2024-01-15 09:02:00
U003,view,P003,2024-01-15 09:03:00
U002,click,P001,2024-01-15 09:04:00
U001,view,P002,2024-01-15 09:05:00
```

## Java 实现

### 完整代码 (RealtimeAnalysis.java)
```java
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.time.Duration;

public class RealtimeAnalysis {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setStreamTimeCharacteristic(org.apache.flink.streaming.api.TimeCharacteristic.EventTime);
        
        // ============================================
        // 1. 创建用户行为数据流
        // ============================================
        
        DataStream<UserAction> actions = env.fromElements(
            new UserAction("U001", "view", "P001", 1705280400000L),
            new UserAction("U002", "click", "P002", 1705280460000L),
            new UserAction("U001", "buy", "P001", 1705280520000L),
            new UserAction("U003", "view", "P003", 1705280580000L),
            new UserAction("U002", "click", "P001", 1705280640000L),
            new UserAction("U001", "view", "P002", 1705280700000L)
        );
        
        // 分配时间戳和水位线
        DataStream<UserAction> actionsWithTime = actions
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<UserAction>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withTimestampAssigner((action, timestamp) -> action.getTimestamp())
            );
        
        // ============================================
        // 2. 实时用户行为统计
        // ============================================
        
        // 按用户统计行为数
        DataStream<Tuple2<String, Long>> userActionCount = actionsWithTime
            .keyBy(UserAction::getUserId)
            .window(TumblingEventTimeWindows.of(Time.seconds(10)))
            .aggregate(new AggregateFunction<UserAction, Long, Long>() {
                @Override
                public Long createAccumulator() {
                    return 0L;
                }
                
                @Override
                public Long add(UserAction value, Long accumulator) {
                    return accumulator + 1;
                }
                
                @Override
                public Long getResult(Long accumulator) {
                    return accumulator;
                }
                
                @Override
                public Long merge(Long a, Long b) {
                    return a + b;
                }
            })
            .map(count -> new Tuple2<>("user_actions", count));
        
        System.out.println("用户行为统计:");
        userActionCount.print("UserActionCount");
        
        // ============================================
        // 3. 实时产品热度统计
        // ============================================
        
        // 按产品统计浏览量
        DataStream<Tuple2<String, Long>> productViews = actionsWithTime
            .filter(action -> "view".equals(action.getAction()))
            .keyBy(UserAction::getProductId)
            .window(TumblingEventTimeWindows.of(Time.seconds(10)))
            .aggregate(new AggregateFunction<UserAction, Long, Long>() {
                @Override
                public Long createAccumulator() {
                    return 0L;
                }
                
                @Override
                public Long add(UserAction value, Long accumulator) {
                    return accumulator + 1;
                }
                
                @Override
                public Long getResult(Long accumulator) {
                    return accumulator;
                }
                
                @Override
                public Long merge(Long a, Long b) {
                    return a + b;
                }
            })
            .map(count -> new Tuple2<>("product_views", count));
        
        System.out.println("\n产品浏览量统计:");
        productViews.print("ProductViews");
        
        env.execute("Realtime Analysis");
    }
    
    public static class UserAction {
        private String userId;
        private String action;
        private String productId;
        private long timestamp;
        
        public UserAction(String userId, String action, String productId, long timestamp) {
            this.userId = userId;
            this.action = action;
            this.productId = productId;
            this.timestamp = timestamp;
        }
        
        public String getUserId() { return userId; }
        public String getAction() { return action; }
        public String getProductId() { return productId; }
        public long getTimestamp() { return timestamp; }
    }
}
```

## Scala 实现

### 完整代码 (RealtimeAnalysis.scala)
```scala
import org.apache.flink.api.common.eventtime.{WatermarkStrategy, TimestampAssigner}
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows
import org.apache.flink.streaming.api.windowing.time.Time

import java.time.Duration

case class UserAction(userId: String, action: String, productId: String, timestamp: Long)

object RealtimeAnalysis {
  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setStreamTimeCharacteristic(org.apache.flink.streaming.api.TimeCharacteristic.EventTime)
    
    // ============================================
    // 1. 创建用户行为数据流
    // ============================================
    
    val actions = env.fromElements(
      UserAction("U001", "view", "P001", 1705280400000L),
      UserAction("U002", "click", "P002", 1705280460000L),
      UserAction("U001", "buy", "P001", 1705280520000L),
      UserAction("U003", "view", "P003", 1705280580000L),
      UserAction("U002", "click", "P001", 1705280640000L),
      UserAction("U001", "view", "P002", 1705280700000L)
    )
    
    // 分配时间戳和水位线
    val actionsWithTime = actions
      .assignTimestampsAndWatermarks(
        WatermarkStrategy
          .forBoundedOutOfOrderness[UserAction](Duration.ofSeconds(5))
          .withTimestampAssigner(new TimestampAssigner[UserAction] {
            override def extractTimestamp(element: UserAction, recordTimestamp: Long): Long = {
              element.timestamp
            }
          })
      )
    
    // ============================================
    // 2. 实时用户行为统计
    // ============================================
    
    val userActionCount = actionsWithTime
      .keyBy(_.userId)
      .window(TumblingEventTimeWindows.of(Time.seconds(10)))
      .aggregate(new AggregateFunction[UserAction, Long, Long] {
        override def createAccumulator(): Long = 0L
        
        override def add(value: UserAction, accumulator: Long): Long = accumulator + 1
        
        override def getResult(accumulator: Long): Long = accumulator
        
        override def merge(a: Long, b: Long): Long = a + b
      })
      .map(count => ("user_actions", count))
    
    println("用户行为统计:")
    userActionCount.print("UserActionCount")
    
    // ============================================
    // 3. 实时产品热度统计
    // ============================================
    
    val productViews = actionsWithTime
      .filter(_.action == "view")
      .keyBy(_.productId)
      .window(TumblingEventTimeWindows.of(Time.seconds(10)))
      .aggregate(new AggregateFunction[UserAction, Long, Long] {
        override def createAccumulator(): Long = 0L
        
        override def add(value: UserAction, accumulator: Long): Long = accumulator + 1
        
        override def getResult(accumulator: Long): Long = accumulator
        
        override def merge(a: Long, b: Long): Long = a + b
      })
      .map(count => ("product_views", count))
    
    println("\n产品浏览量统计:")
    productViews.print("ProductViews")
    
    env.execute("Realtime Analysis")
  }
}
```

## 学习要点

1. **实时处理**：事件时间处理
2. **窗口聚合**：实时统计
3. **多维度分析**：用户、产品、转化率
4. **水位线**：处理乱序数据
5. **状态管理**：窗口状态
