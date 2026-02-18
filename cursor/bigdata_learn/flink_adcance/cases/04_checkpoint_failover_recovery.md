# 案例4：Checkpoint（开启检查点 + 人为故障 + 重启恢复状态）

## 案例描述
这个案例的目标不是“把生产所有细节一次讲完”，而是跑通最小闭环：
- 开启 checkpoint
- 算子里维护一个 **ValueState**（running sum）
- 运行中**故意失败一次**
- 作业重启后，状态从 checkpoint 恢复（而不是从 0 开始）

> 注意：用 `print()` 这类 sink 做实验时，故障重启可能导致“重复打印”。我们关注的是 **状态恢复是否生效**（比如最终 sum 是否符合预期），而不是“日志不重复”。

## 数据准备

### 数据文件（`flink_adcance/data/checkpoint_numbers.txt`）
内容：1~20（每行一个数字）

## Java 实现

### 完整代码（CheckpointFailoverDemo.java）
```java
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.restartstrategy.RestartStrategies;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.time.Time;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.CheckpointConfig;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

import java.time.Duration;

public class CheckpointFailoverDemo {
    public static void main(String[] args) throws Exception {
        final String input = args != null && args.length > 0
                ? args[0]
                : "flink_adcance/data/checkpoint_numbers.txt";

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);

        // 1) 开启 checkpoint（尽量让它在故障前至少成功一次）
        env.enableCheckpointing(1000); // 1s
        CheckpointConfig cfg = env.getCheckpointConfig();
        cfg.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
        cfg.setCheckpointTimeout(60_000);
        cfg.setMinPauseBetweenCheckpoints(500);
        cfg.setMaxConcurrentCheckpoints(1);
        cfg.enableExternalizedCheckpoints(CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);

        // 2) 配置自动重启（演示 failover）
        env.setRestartStrategy(RestartStrategies.fixedDelayRestart(
                3, // 最多重启 3 次
                Time.seconds(2)
        ));

        // 3) 输入流：读取数字
        DataStream<Integer> nums = env
                .readTextFile(input)
                .filter(line -> line != null && !line.trim().isEmpty())
                .map(s -> Integer.parseInt(s.trim()));

        // 4) 故障注入 + 有状态累加
        nums
                // 对于这个 demo，不依赖事件时间，但给一个 watermark 防止某些环境 warning
                .assignTimestampsAndWatermarks(
                        WatermarkStrategy.<Integer>forBoundedOutOfOrderness(Duration.ZERO)
                                .withTimestampAssigner((v, ts) -> 0L)
                )
                .keyBy(v -> "all")
                .process(new SumAndFailOnce(8)) // 处理到 8 时故意失败一次
                .print("SUM");

        env.execute("Checkpoint Failover Recovery Demo");
    }

    /**
     * 逻辑：
     * - 用 ValueState 保存 runningSum
     * - 用 ValueState 保存 hasFailed（保证只失败一次）
     * - 为了让 checkpoint 有机会成功，我们每条数据 sleep 一点点（demo 用）
     */
    public static class SumAndFailOnce extends KeyedProcessFunction<String, Integer, String> {
        private final int failOn;

        private transient ValueState<Integer> sum;
        private transient ValueState<Boolean> hasFailed;

        public SumAndFailOnce(int failOn) {
            this.failOn = failOn;
        }

        @Override
        public void open(Configuration parameters) {
            sum = getRuntimeContext().getState(new ValueStateDescriptor<>("sum", Integer.class));
            hasFailed = getRuntimeContext().getState(new ValueStateDescriptor<>("hasFailed", Boolean.class));
        }

        @Override
        public void processElement(Integer value, Context ctx, Collector<String> out) throws Exception {
            // demo：让 checkpoint 更容易“来得及成功一次”
            Thread.sleep(200);

            Integer s = sum.value();
            if (s == null) s = 0;

            int next = s + value;
            sum.update(next);

            Boolean failed = hasFailed.value();
            if (failed == null) failed = false;

            // 故意失败一次：触发 failover
            if (!failed && value == failOn) {
                hasFailed.update(true);
                throw new RuntimeException("Injected failure at value=" + value);
            }

            out.collect("value=" + value + ", runningSum=" + next);
        }
    }
}
```

## Scala 实现

### 完整代码（CheckpointFailoverDemo.scala）
```scala
import org.apache.flink.api.common.eventtime.{SerializableTimestampAssigner, WatermarkStrategy}
import org.apache.flink.api.common.restartstrategy.RestartStrategies
import org.apache.flink.api.common.state.{ValueState, ValueStateDescriptor}
import org.apache.flink.api.common.time.{Time => FlinkTime}
import org.apache.flink.configuration.Configuration
import org.apache.flink.streaming.api.CheckpointingMode
import org.apache.flink.streaming.api.environment.{CheckpointConfig, StreamExecutionEnvironment}
import org.apache.flink.streaming.api.functions.KeyedProcessFunction
import org.apache.flink.streaming.api.scala._
import org.apache.flink.util.Collector

import java.time.Duration

object CheckpointFailoverDemo {
  def main(args: Array[String]): Unit = {
    val input = if (args != null && args.nonEmpty) args(0) else "flink_adcance/data/checkpoint_numbers.txt"

    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(1)

    // 1) checkpoint
    env.enableCheckpointing(1000)
    val cfg: CheckpointConfig = env.getCheckpointConfig
    cfg.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE)
    cfg.setCheckpointTimeout(60000)
    cfg.setMinPauseBetweenCheckpoints(500)
    cfg.setMaxConcurrentCheckpoints(1)
    cfg.enableExternalizedCheckpoints(CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION)

    // 2) restart strategy
    env.setRestartStrategy(RestartStrategies.fixedDelayRestart(3, FlinkTime.seconds(2)))

    val nums = env
      .readTextFile(input)
      .filter(line => line != null && line.trim.nonEmpty)
      .map(_.trim.toInt)

    nums
      .assignTimestampsAndWatermarks(
        WatermarkStrategy
          .forBoundedOutOfOrderness[Int](Duration.ZERO)
          .withTimestampAssigner(new SerializableTimestampAssigner[Int] {
            override def extractTimestamp(element: Int, recordTimestamp: Long): Long = 0L
          })
      )
      .keyBy(_ => "all")
      .process(new SumAndFailOnce(8))
      .print("SUM")

    env.execute("Checkpoint Failover Recovery Demo")
  }

  class SumAndFailOnce(failOn: Int) extends KeyedProcessFunction[String, Int, String] {
    private var sum: ValueState[Integer] = _
    private var hasFailed: ValueState[java.lang.Boolean] = _

    override def open(parameters: Configuration): Unit = {
      sum = getRuntimeContext.getState(new ValueStateDescriptor[Integer]("sum", classOf[Integer]))
      hasFailed = getRuntimeContext.getState(new ValueStateDescriptor[java.lang.Boolean]("hasFailed", classOf[java.lang.Boolean]))
    }

    override def processElement(value: Int, ctx: KeyedProcessFunction[String, Int, String]#Context, out: Collector[String]): Unit = {
      Thread.sleep(200)

      val current = Option(sum.value()).map(_.intValue()).getOrElse(0)
      val next = current + value
      sum.update(next)

      val failed = Option(hasFailed.value()).exists(_.booleanValue())
      if (!failed && value == failOn) {
        hasFailed.update(true)
        throw new RuntimeException(s"Injected failure at value=$value")
      }

      out.collect(s"value=$value, runningSum=$next")
    }
  }
}
```

## 运行方式（参考）
```bash
flink run -c CheckpointFailoverDemo your.jar flink_adcance/data/checkpoint_numbers.txt
```

## 预期结果（如何验证恢复生效）
- 你应该能观察到：作业在处理到 value=8 时失败一次，然后自动重启继续跑（最多重启 3 次）。
- 最终（流结束时）你应该能看到某一行输出包含：
  - `runningSum=210`（1~20 的和）
- 你可能会看到中间某些 `runningSum` 行“重复出现”（print sink 的典型现象），这不影响你验证 **状态从 checkpoint 恢复并继续累加**。

## 学习要点
1. **Checkpoint 存的是状态**（以及必要时的在途数据），不是“控制台输出”
2. **Exactly-Once 不是白送的**：最终是否严格一次，还取决于 source/sink 语义
3. **没 checkpoint 成功就故障**：重启后可能从头来（不是 Flink 不行，是没存档成功）

