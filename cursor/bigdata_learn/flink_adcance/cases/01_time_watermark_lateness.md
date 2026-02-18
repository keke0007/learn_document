# 案例1：Time（Event Time / Watermark / Lateness / Side Output）

## 案例描述
用一份**乱序 + 极晚到**的数据，演示 Event Time 下：
- **Watermark 推进窗口触发**
- **Allowed Lateness 让窗口结果“二次更新”**
- **Side Output 收集“晚到到不能再晚”的数据**

## 数据准备

### 数据文件（`flink_adcance/data/time_events.csv`）
字段：`arrival,user_id,event_time,status`

```
arrival,user_id,event_time,status
1,u1,2024-01-15 09:00:01,CLICK
2,u1,2024-01-15 09:00:04,CLICK
3,u1,2024-01-15 09:00:03,CLICK
...
11,u1,2024-01-15 09:00:06,CLICK  # 极晚到（用于 side output）
```

## 实验设置（你要牢记的 4 个参数）
- **窗口**：10 秒滚动窗口（`TumblingEventTimeWindows.of(Time.seconds(10))`）
- **Watermark 乱序容忍**：2 秒（`forBoundedOutOfOrderness(Duration.ofSeconds(2))`）
- **允许迟到**：8 秒（`allowedLateness(Time.seconds(8))`）
- **迟到侧输出**：`sideOutputLateData(lateTag)`

## Java 实现

### 完整代码（TimeWatermarkLateness.java）
```java
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.util.Collector;
import org.apache.flink.util.OutputTag;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

public class TimeWatermarkLateness {

    // 侧输出：收集“太晚了”的事件
    private static final OutputTag<Event> LATE_TAG = new OutputTag<Event>("late-events") {};

    public static void main(String[] args) throws Exception {
        final String input = args != null && args.length > 0
                ? args[0]
                : "flink_adcance/data/time_events.csv";

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        env.getConfig().setAutoWatermarkInterval(200L);

        DataStream<Event> events = env
                .readTextFile(input)
                .filter(line -> line != null && !line.trim().isEmpty() && !line.startsWith("arrival,"))
                .map(TimeWatermarkLateness::parse);

        WatermarkStrategy<Event> wm = WatermarkStrategy
                .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(2))
                .withTimestampAssigner((e, ts) -> e.eventTimeMillis);

        SingleOutputStreamOperator<String> main = events
                .assignTimestampsAndWatermarks(wm)
                .keyBy(e -> e.userId)
                .window(TumblingEventTimeWindows.of(Time.seconds(10)))
                .allowedLateness(Time.seconds(8))
                .sideOutputLateData(LATE_TAG)
                .aggregate(new CountAgg(), new WindowFormat());

        // 主流：窗口计数（注意：同一窗口可能会输出多次，这是 allowed lateness 的“更新”）
        main.print("WindowResult");

        // 侧输出：过晚数据
        main.getSideOutput(LATE_TAG)
                .map(e -> "arrival=" + e.arrival
                        + ", user=" + e.userId
                        + ", eventTime=" + e.eventTimeStr
                        + ", status=" + e.status)
                .print("TooLate");

        env.execute("Time - Watermark - Lateness");
    }

    // -------------------------
    // 解析与模型
    // -------------------------
    private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    private static Event parse(String line) {
        // arrival,user_id,event_time,status
        String[] arr = line.split(",");
        int arrival = Integer.parseInt(arr[0].trim());
        String userId = arr[1].trim();
        String eventTimeStr = arr[2].trim();
        String status = arr[3].trim();
        long ts = LocalDateTime.parse(eventTimeStr, FMT)
                .atZone(ZoneId.systemDefault())
                .toInstant()
                .toEpochMilli();
        return new Event(arrival, userId, ts, status, eventTimeStr);
    }

    public static class Event {
        public int arrival;
        public String userId;
        public long eventTimeMillis;
        public String status;
        public String eventTimeStr; // 仅用于打印

        public Event() {}

        public Event(int arrival, String userId, long eventTimeMillis, String status, String eventTimeStr) {
            this.arrival = arrival;
            this.userId = userId;
            this.eventTimeMillis = eventTimeMillis;
            this.status = status;
            this.eventTimeStr = eventTimeStr;
        }
    }

    // -------------------------
    // 聚合与窗口格式化输出
    // -------------------------
    public static class CountAgg implements AggregateFunction<Event, Long, Long> {
        @Override
        public Long createAccumulator() { return 0L; }

        @Override
        public Long add(Event value, Long accumulator) {
            return accumulator + 1;
        }

        @Override
        public Long getResult(Long accumulator) { return accumulator; }

        @Override
        public Long merge(Long a, Long b) { return a + b; }
    }

    /**
     * 输出格式：
     * userId, windowStart, windowEnd, count
     */
    public static class WindowFormat extends ProcessWindowFunction<Long, String, String, TimeWindow> {
        @Override
        public void process(String key, Context ctx, Iterable<Long> elements, Collector<String> out) {
            long cnt = elements.iterator().next();
            String ws = fmt(ctx.window().getStart());
            String we = fmt(ctx.window().getEnd());
            out.collect("user=" + key + ", window=[" + ws + "," + we + "), count=" + cnt);
        }

        private String fmt(long millis) {
            return LocalDateTime.ofInstant(java.time.Instant.ofEpochMilli(millis), ZoneId.systemDefault()).format(FMT);
        }
    }
}
```

## Scala 实现

### 完整代码（TimeWatermarkLateness.scala）
```scala
import org.apache.flink.api.common.eventtime.{SerializableTimestampAssigner, WatermarkStrategy}
import org.apache.flink.api.common.functions.AggregateFunction
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows
import org.apache.flink.streaming.api.windowing.time.Time
import org.apache.flink.streaming.api.windowing.windows.TimeWindow
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction
import org.apache.flink.util.{Collector, OutputTag}

import java.time.format.DateTimeFormatter
import java.time.{Duration, LocalDateTime, ZoneId}

case class Event(arrival: Int, userId: String, eventTimeMillis: Long, status: String, eventTimeStr: String)

object TimeWatermarkLateness {
  private val fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
  private val lateTag = new OutputTag[Event]("late-events") {}

  def main(args: Array[String]): Unit = {
    val input = if (args != null && args.nonEmpty) args(0) else "flink_adcance/data/time_events.csv"

    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(1)
    env.getConfig.setAutoWatermarkInterval(200L)

    val events = env
      .readTextFile(input)
      .filter(line => line != null && line.trim.nonEmpty && !line.startsWith("arrival,"))
      .map(parse)

    val wm = WatermarkStrategy
      .forBoundedOutOfOrderness[Event](Duration.ofSeconds(2))
      .withTimestampAssigner(new SerializableTimestampAssigner[Event] {
        override def extractTimestamp(element: Event, recordTimestamp: Long): Long = element.eventTimeMillis
      })

    val main = events
      .assignTimestampsAndWatermarks(wm)
      .keyBy(_.userId)
      .window(TumblingEventTimeWindows.of(Time.seconds(10)))
      .allowedLateness(Time.seconds(8))
      .sideOutputLateData(lateTag)
      .aggregate(new CountAgg, new WindowFormat)

    main.print("WindowResult")
    main.getSideOutput(lateTag)
      .map(e => s"arrival=${e.arrival}, user=${e.userId}, eventTime=${e.eventTimeStr}, status=${e.status}")
      .print("TooLate")

    env.execute("Time - Watermark - Lateness")
  }

  def parse(line: String): Event = {
    val arr = line.split(",")
    val arrival = arr(0).trim.toInt
    val userId = arr(1).trim
    val eventTimeStr = arr(2).trim
    val status = arr(3).trim
    val ts = LocalDateTime.parse(eventTimeStr, fmt)
      .atZone(ZoneId.systemDefault())
      .toInstant
      .toEpochMilli
    Event(arrival, userId, ts, status, eventTimeStr)
  }

  class CountAgg extends AggregateFunction[Event, Long, Long] {
    override def createAccumulator(): Long = 0L
    override def add(value: Event, accumulator: Long): Long = accumulator + 1L
    override def getResult(accumulator: Long): Long = accumulator
    override def merge(a: Long, b: Long): Long = a + b
  }

  class WindowFormat extends ProcessWindowFunction[Long, String, String, TimeWindow] {
    override def process(key: String, ctx: Context, elements: Iterable[Long], out: Collector[String]): Unit = {
      val cnt = elements.iterator.next()
      val ws = formatMillis(ctx.window.getStart)
      val we = formatMillis(ctx.window.getEnd)
      out.collect(s"user=$key, window=[$ws,$we), count=$cnt")
    }

    private def formatMillis(millis: Long): String =
      LocalDateTime.ofInstant(java.time.Instant.ofEpochMilli(millis), ZoneId.systemDefault()).format(fmt)
  }
}
```

### 运行方式（参考）
```bash
# 你可以把 input path 作为 args 传入：
flink run -c TimeWatermarkLateness your.jar flink_adcance/data/time_events.csv
```

## 预期结果（如何验证“对/错”）

你不需要依赖打印顺序，只要对照“窗口 + key 的最终计数”：

### 窗口 [09:00:00, 09:00:10)
- u1：最终应为 **4**（01/03/04/05 秒的 4 条）
- u2：最终应为 **2**（07/09 秒的 2 条）

### 窗口 [09:00:10, 09:00:20)
- u1：**1**（12 秒）
- u2：**1**（19 秒）

### 窗口 [09:00:20, 09:00:30)
- u1：**1**（22 秒）
- u2：**1**（21 秒）

### TooLate（侧输出）
你应能看到 arrival=11 的那条（09:00:06）进入 `TooLate`（因为它“晚过了 allowed lateness 的范围”）。

## 学习要点
1. **Watermark** 决定窗口何时“结算”
2. **Allowed Lateness** 会让同一个窗口结果“更新输出多次”
3. **Side Output** 是你处理“极晚数据”的标准出口（不要默默丢掉）

