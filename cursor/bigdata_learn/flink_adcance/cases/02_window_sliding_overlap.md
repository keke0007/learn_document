# 案例2：Window（Sliding Window 重叠的可验证实验）

## 案例描述
用滑动窗口演示一个事实：**同一条事件会进入多个窗口**（窗口重叠），因此你会看到“窗口数量变多、计算量变大、输出更频繁”。

## 数据准备

### 数据文件（`flink_adcance/data/window_orders.csv`）
字段：`order_id,product_id,amount,event_time`

```
order_id,product_id,amount,event_time
1001,P001,10.0,2024-01-15 09:00:01
1002,P001,20.0,2024-01-15 09:00:04
1003,P002,7.0,2024-01-15 09:00:06
...
1007,P002,4.0,2024-01-15 09:00:21
```

## 实验设置
- **窗口大小**：10 秒
- **滑动步长**：5 秒
- **时间语义**：Event Time（配 timestamp + watermark）

## Java 实现

### 完整代码（SlidingWindowOverlap.java）
```java
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

public class SlidingWindowOverlap {
    private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public static void main(String[] args) throws Exception {
        final String input = args != null && args.length > 0
                ? args[0]
                : "flink_adcance/data/window_orders.csv";

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        env.getConfig().setAutoWatermarkInterval(200L);

        DataStream<Order> orders = env
                .readTextFile(input)
                .filter(line -> line != null && !line.trim().isEmpty() && !line.startsWith("order_id,"))
                .map(SlidingWindowOverlap::parse);

        WatermarkStrategy<Order> wm = WatermarkStrategy
                .<Order>forBoundedOutOfOrderness(Duration.ofSeconds(1))
                .withTimestampAssigner((o, ts) -> o.eventTimeMillis);

        orders
                .assignTimestampsAndWatermarks(wm)
                .keyBy(o -> o.productId)
                .window(SlidingEventTimeWindows.of(Time.seconds(10), Time.seconds(5)))
                .aggregate(new SumAgg(), new FormatResult())
                .print("SlidingWindow");

        env.execute("Window - Sliding Overlap");
    }

    private static Order parse(String line) {
        // order_id,product_id,amount,event_time
        String[] arr = line.split(",");
        String orderId = arr[0].trim();
        String productId = arr[1].trim();
        double amount = Double.parseDouble(arr[2].trim());
        String eventTimeStr = arr[3].trim();
        long ts = LocalDateTime.parse(eventTimeStr, FMT)
                .atZone(ZoneId.systemDefault())
                .toInstant()
                .toEpochMilli();
        return new Order(orderId, productId, amount, ts, eventTimeStr);
    }

    public static class Order {
        public String orderId;
        public String productId;
        public double amount;
        public long eventTimeMillis;
        public String eventTimeStr;

        public Order() {}

        public Order(String orderId, String productId, double amount, long eventTimeMillis, String eventTimeStr) {
            this.orderId = orderId;
            this.productId = productId;
            this.amount = amount;
            this.eventTimeMillis = eventTimeMillis;
            this.eventTimeStr = eventTimeStr;
        }
    }

    public static class SumAgg implements AggregateFunction<Order, Double, Double> {
        @Override
        public Double createAccumulator() { return 0.0; }

        @Override
        public Double add(Order value, Double accumulator) { return accumulator + value.amount; }

        @Override
        public Double getResult(Double accumulator) { return accumulator; }

        @Override
        public Double merge(Double a, Double b) { return a + b; }
    }

    public static class FormatResult extends ProcessWindowFunction<Double, String, String, TimeWindow> {
        @Override
        public void process(String key, Context ctx, Iterable<Double> elements, Collector<String> out) {
            double sum = elements.iterator().next();
            String ws = fmt(ctx.window().getStart());
            String we = fmt(ctx.window().getEnd());
            out.collect("product=" + key + ", window=[" + ws + "," + we + "), sum=" + sum);
        }

        private String fmt(long millis) {
            return LocalDateTime.ofInstant(java.time.Instant.ofEpochMilli(millis), ZoneId.systemDefault()).format(FMT);
        }
    }
}
```

## Scala 实现

### 完整代码（SlidingWindowOverlap.scala）
```scala
import org.apache.flink.api.common.eventtime.{SerializableTimestampAssigner, WatermarkStrategy}
import org.apache.flink.api.common.functions.AggregateFunction
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows
import org.apache.flink.streaming.api.windowing.time.Time
import org.apache.flink.streaming.api.windowing.windows.TimeWindow
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction
import org.apache.flink.util.Collector

import java.time.format.DateTimeFormatter
import java.time.{Duration, LocalDateTime, ZoneId}

case class Order(orderId: String, productId: String, amount: Double, eventTimeMillis: Long, eventTimeStr: String)

object SlidingWindowOverlap {
  private val fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")

  def main(args: Array[String]): Unit = {
    val input = if (args != null && args.nonEmpty) args(0) else "flink_adcance/data/window_orders.csv"

    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(1)
    env.getConfig.setAutoWatermarkInterval(200L)

    val orders = env
      .readTextFile(input)
      .filter(line => line != null && line.trim.nonEmpty && !line.startsWith("order_id,"))
      .map(parse)

    val wm = WatermarkStrategy
      .forBoundedOutOfOrderness[Order](Duration.ofSeconds(1))
      .withTimestampAssigner(new SerializableTimestampAssigner[Order] {
        override def extractTimestamp(element: Order, recordTimestamp: Long): Long = element.eventTimeMillis
      })

    orders
      .assignTimestampsAndWatermarks(wm)
      .keyBy(_.productId)
      .window(SlidingEventTimeWindows.of(Time.seconds(10), Time.seconds(5)))
      .aggregate(new SumAgg, new FormatResult)
      .print("SlidingWindow")

    env.execute("Window - Sliding Overlap")
  }

  def parse(line: String): Order = {
    val arr = line.split(",")
    val orderId = arr(0).trim
    val productId = arr(1).trim
    val amount = arr(2).trim.toDouble
    val eventTimeStr = arr(3).trim
    val ts = LocalDateTime.parse(eventTimeStr, fmt)
      .atZone(ZoneId.systemDefault())
      .toInstant
      .toEpochMilli
    Order(orderId, productId, amount, ts, eventTimeStr)
  }

  class SumAgg extends AggregateFunction[Order, Double, Double] {
    override def createAccumulator(): Double = 0.0
    override def add(value: Order, accumulator: Double): Double = accumulator + value.amount
    override def getResult(accumulator: Double): Double = accumulator
    override def merge(a: Double, b: Double): Double = a + b
  }

  class FormatResult extends ProcessWindowFunction[Double, String, String, TimeWindow] {
    override def process(key: String, ctx: Context, elements: Iterable[Double], out: Collector[String]): Unit = {
      val sum = elements.iterator.next()
      val ws = formatMillis(ctx.window.getStart)
      val we = formatMillis(ctx.window.getEnd)
      out.collect(s"product=$key, window=[$ws,$we), sum=$sum")
    }

    private def formatMillis(millis: Long): String =
      LocalDateTime.ofInstant(java.time.Instant.ofEpochMilli(millis), ZoneId.systemDefault()).format(fmt)
  }
}
```

### 运行方式（参考）
```bash
flink run -c SlidingWindowOverlap your.jar flink_adcance/data/window_orders.csv
```

## 预期结果（窗口对照表）

以 09:00:00 对齐的 10s/5s 滑动窗口，最终应满足（不要求打印顺序一致）：

- **窗口 A**：\[09:00:00, 09:00:10)
  - P001：10 + 20 = **30**
  - P002：7 = **7**
- **窗口 B**：\[09:00:05, 09:00:15)
  - P001：5 = **5**
  - P002：7 + 3 = **10**
- **窗口 C**：\[09:00:10, 09:00:20)
  - P001：5 + 8 = **13**
  - P002：3 = **3**
- **窗口 D**：\[09:00:15, 09:00:25)
  - P001：8 = **8**
  - P002：4 = **4**
- **窗口 E**：\[09:00:20, 09:00:30)
  - P002：4 = **4**

## 学习要点
1. **滑动窗口会重叠**：一条数据可能会被统计多次（分别落在多个窗口里）
2. **窗口步长越小**：输出越频繁、计算越贵
3. **能增量聚合就别全量窗口**：`AggregateFunction` 更省内存

