# 案例3：State（Keyed State + 定时器：60 秒内 3 次 FAIL 告警）

## 案例描述
实现一个最常见的“有状态规则”：
- 以 `device_id` 为 key
- **60 秒内连续 3 次 FAIL** → 输出告警
- 收到 `OK` → 清空状态（重置连续失败）
- 60 秒内凑不够 3 次 → 超时清理（避免状态无限增长）

这个案例的核心是：你必须能说清楚 **State 存什么**、**什么时候更新**、**什么时候清理**。

## 数据准备

### 数据文件（`flink_adcance/data/state_device_events.csv`）
字段：`arrival,device_id,event_time,status`

（该文件已按 `event_time` 递增排列，便于 Event Time 定时器稳定触发）

## Java 实现

### 完整代码（Fail3TimesAlert.java）
```java
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

public class Fail3TimesAlert {

    private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public static void main(String[] args) throws Exception {
        final String input = args != null && args.length > 0
                ? args[0]
                : "flink_adcance/data/state_device_events.csv";

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        env.getConfig().setAutoWatermarkInterval(200L);

        DataStream<DeviceEvent> events = env
                .readTextFile(input)
                .filter(line -> line != null && !line.trim().isEmpty() && !line.startsWith("arrival,"))
                .map(Fail3TimesAlert::parse);

        // 这里数据已按 event_time 递增，所以用 monotonic watermark 即可
        WatermarkStrategy<DeviceEvent> wm = WatermarkStrategy
                .<DeviceEvent>forMonotonousTimestamps()
                .withTimestampAssigner((e, ts) -> e.eventTimeMillis);

        events
                .assignTimestampsAndWatermarks(wm)
                .keyBy(e -> e.deviceId)
                .process(new AlertFn())
                .print("ALERT");

        env.execute("State - Fail 3 times in 60s");
    }

    private static DeviceEvent parse(String line) {
        // arrival,device_id,event_time,status
        String[] arr = line.split(",");
        int arrival = Integer.parseInt(arr[0].trim());
        String deviceId = arr[1].trim();
        String eventTimeStr = arr[2].trim();
        String status = arr[3].trim();
        long ts = LocalDateTime.parse(eventTimeStr, FMT)
                .atZone(ZoneId.systemDefault())
                .toInstant()
                .toEpochMilli();
        return new DeviceEvent(arrival, deviceId, ts, eventTimeStr, status);
    }

    public static class DeviceEvent {
        public int arrival;
        public String deviceId;
        public long eventTimeMillis;
        public String eventTimeStr;
        public String status;

        public DeviceEvent() {}

        public DeviceEvent(int arrival, String deviceId, long eventTimeMillis, String eventTimeStr, String status) {
            this.arrival = arrival;
            this.deviceId = deviceId;
            this.eventTimeMillis = eventTimeMillis;
            this.eventTimeStr = eventTimeStr;
            this.status = status;
        }
    }

    /**
     * 每个 device_id 维护一组状态：
     * - failCount：当前连续 FAIL 次数
     * - firstFailTs：这轮连续 FAIL 的起始事件时间
     * - cleanupTimerTs：注册的清理定时器时间戳（用于 deleteTimer）
     */
    public static class AlertFn extends KeyedProcessFunction<String, DeviceEvent, String> {
        private transient ValueState<Integer> failCount;
        private transient ValueState<Long> firstFailTs;
        private transient ValueState<Long> cleanupTimerTs;

        @Override
        public void open(Configuration parameters) {
            failCount = getRuntimeContext().getState(new ValueStateDescriptor<>("failCount", Integer.class));
            firstFailTs = getRuntimeContext().getState(new ValueStateDescriptor<>("firstFailTs", Long.class));
            cleanupTimerTs = getRuntimeContext().getState(new ValueStateDescriptor<>("cleanupTimerTs", Long.class));
        }

        @Override
        public void processElement(DeviceEvent e, Context ctx, Collector<String> out) throws Exception {
            if ("OK".equalsIgnoreCase(e.status)) {
                clear(ctx);
                return;
            }

            long ts = e.eventTimeMillis;
            Integer c = failCount.value();
            Long first = firstFailTs.value();

            // 1) 第一次 FAIL 或者超出 60 秒：开启新一轮
            if (c == null || first == null || ts - first > 60_000L) {
                // 开新轮前，清掉旧 timer（如果有）
                deleteTimerIfExists(ctx);

                failCount.update(1);
                firstFailTs.update(ts);

                long timerTs = ts + 60_000L;
                ctx.timerService().registerEventTimeTimer(timerTs);
                cleanupTimerTs.update(timerTs);
                return;
            }

            // 2) 仍在 60 秒窗口内：累计
            int next = c + 1;
            failCount.update(next);

            if (next >= 3) {
                out.collect("device=" + ctx.getCurrentKey()
                        + ", eventTime=" + e.eventTimeStr
                        + ", reason=FAIL_3_TIMES_IN_60S");
                clear(ctx);
            }
        }

        @Override
        public void onTimer(long timestamp, OnTimerContext ctx, Collector<String> out) throws Exception {
            // 60 秒到了还没凑够 3 次，清理状态
            clear(ctx);
        }

        private void clear(Context ctx) throws Exception {
            deleteTimerIfExists(ctx);
            failCount.clear();
            firstFailTs.clear();
            cleanupTimerTs.clear();
        }

        private void deleteTimerIfExists(Context ctx) throws Exception {
            Long t = cleanupTimerTs.value();
            if (t != null) {
                ctx.timerService().deleteEventTimeTimer(t);
            }
        }
    }
}
```

## Scala 实现

### 完整代码（Fail3TimesAlert.scala）
```scala
import org.apache.flink.api.common.eventtime.{SerializableTimestampAssigner, WatermarkStrategy}
import org.apache.flink.api.common.state.{ValueState, ValueStateDescriptor}
import org.apache.flink.configuration.Configuration
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.functions.KeyedProcessFunction
import org.apache.flink.util.Collector

import java.time.format.DateTimeFormatter
import java.time.{Duration, LocalDateTime, ZoneId}

case class DeviceEvent(arrival: Int, deviceId: String, eventTimeMillis: Long, eventTimeStr: String, status: String)

object Fail3TimesAlert {
  private val fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")

  def main(args: Array[String]): Unit = {
    val input = if (args != null && args.nonEmpty) args(0) else "flink_adcance/data/state_device_events.csv"

    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(1)
    env.getConfig.setAutoWatermarkInterval(200L)

    val events = env
      .readTextFile(input)
      .filter(line => line != null && line.trim.nonEmpty && !line.startsWith("arrival,"))
      .map(parse)

    val wm = WatermarkStrategy
      .forMonotonousTimestamps[DeviceEvent]()
      .withTimestampAssigner(new SerializableTimestampAssigner[DeviceEvent] {
        override def extractTimestamp(element: DeviceEvent, recordTimestamp: Long): Long = element.eventTimeMillis
      })

    events
      .assignTimestampsAndWatermarks(wm)
      .keyBy(_.deviceId)
      .process(new AlertFn)
      .print("ALERT")

    env.execute("State - Fail 3 times in 60s")
  }

  def parse(line: String): DeviceEvent = {
    val arr = line.split(",")
    val arrival = arr(0).trim.toInt
    val deviceId = arr(1).trim
    val eventTimeStr = arr(2).trim
    val status = arr(3).trim
    val ts = LocalDateTime.parse(eventTimeStr, fmt)
      .atZone(ZoneId.systemDefault())
      .toInstant
      .toEpochMilli
    DeviceEvent(arrival, deviceId, ts, eventTimeStr, status)
  }

  class AlertFn extends KeyedProcessFunction[String, DeviceEvent, String] {
    private var failCount: ValueState[Integer] = _
    private var firstFailTs: ValueState[java.lang.Long] = _
    private var cleanupTimerTs: ValueState[java.lang.Long] = _

    override def open(parameters: Configuration): Unit = {
      failCount = getRuntimeContext.getState(new ValueStateDescriptor[Integer]("failCount", classOf[Integer]))
      firstFailTs = getRuntimeContext.getState(new ValueStateDescriptor[java.lang.Long]("firstFailTs", classOf[java.lang.Long]))
      cleanupTimerTs = getRuntimeContext.getState(new ValueStateDescriptor[java.lang.Long]("cleanupTimerTs", classOf[java.lang.Long]))
    }

    override def processElement(e: DeviceEvent, ctx: KeyedProcessFunction[String, DeviceEvent, String]#Context, out: Collector[String]): Unit = {
      if ("OK".equalsIgnoreCase(e.status)) {
        clear(ctx)
        return
      }

      val ts = e.eventTimeMillis
      val c = Option(failCount.value()).map(_.intValue()).getOrElse(0)
      val firstOpt = Option(firstFailTs.value()).map(_.longValue())

      if (c == 0 || firstOpt.isEmpty || ts - firstOpt.get > 60000L) {
        deleteTimerIfExists(ctx)
        failCount.update(1)
        firstFailTs.update(ts)
        val timerTs = ts + 60000L
        ctx.timerService().registerEventTimeTimer(timerTs)
        cleanupTimerTs.update(timerTs)
        return
      }

      val next = c + 1
      failCount.update(next)

      if (next >= 3) {
        out.collect(s"device=${ctx.getCurrentKey}, eventTime=${e.eventTimeStr}, reason=FAIL_3_TIMES_IN_60S")
        clear(ctx)
      }
    }

    override def onTimer(timestamp: Long, ctx: KeyedProcessFunction[String, DeviceEvent, String]#OnTimerContext, out: Collector[String]): Unit = {
      clear(ctx)
    }

    private def clear(ctx: KeyedProcessFunction[String, DeviceEvent, String]#Context): Unit = {
      deleteTimerIfExists(ctx)
      failCount.clear()
      firstFailTs.clear()
      cleanupTimerTs.clear()
    }

    private def deleteTimerIfExists(ctx: KeyedProcessFunction[String, DeviceEvent, String]#Context): Unit = {
      val t = cleanupTimerTs.value()
      if (t != null) ctx.timerService().deleteEventTimeTimer(t)
    }
  }
}
```

### 运行方式（参考）
```bash
flink run -c Fail3TimesAlert your.jar flink_adcance/data/state_device_events.csv
```

## 预期结果（告警验证）
你应能看到 **两条告警**（顺序可能不同）：
- d1：在 `2024-01-15 09:00:20` 触发（09:00:01 / 09:00:10 / 09:00:20）
- d2：在 `2024-01-15 09:01:30` 触发（09:01:10 / 09:01:20 / 09:01:30）

## 学习要点
1. **Keyed State 一定在 `keyBy` 后使用**：每个 key 都有自己的一套“抽屉”
2. **状态必须可清理**：timer/TTL/规则清理，否则无限增长
3. **定时器靠 watermark 推动**：Event Time timer 什么时候触发取决于 watermark 什么时候走到那

