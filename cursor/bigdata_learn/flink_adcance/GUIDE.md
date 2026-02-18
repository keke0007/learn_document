# Flink 进阶指南：Time / Window / State / Checkpoint（费曼学习法）

> 目标：把 Flink 的“进阶四件套”讲到你能 **用自己的话**解释清楚，并能用 **小数据集**做出“对/错可验证”的实验结果。

本指南围绕一个核心闭环：
- **Time** 决定“这条数据属于哪个时刻”
- **Window** 决定“按时间怎么切块统计”
- **State** 决定“跨元素/跨时间记住什么”
- **Checkpoint** 决定“挂了还能不能把记住的东西恢复回来（Exactly-Once）”

本目录自带验证数据在 `flink_adcance/data/`：
- `data/time_events.csv`
- `data/window_orders.csv`
- `data/state_device_events.csv`
- `data/checkpoint_numbers.txt`

本目录自带可验证案例在 `flink_adcance/cases/`：
- `cases/README.md`：案例索引
- `cases/01_time_watermark_lateness.md`：Time（Event Time / Watermark / Lateness / Side Output）
- `cases/02_window_sliding_overlap.md`：Window（滑动窗口重叠的可验证实验）
- `cases/03_state_keyed_fail_alert.md`：State（Keyed State + 定时器：60 秒内 3 次 FAIL 告警）
- `cases/04_checkpoint_failover_recovery.md`：Checkpoint（开启检查点 + 人为故障 + 重启恢复状态）
- `cases/05_production_issues_best_practices.md`：生产常见问题与最佳实践清单（含案例 Runbook）

---

## 0. 学习方法（费曼法的落地模板）

每个知识点都按同一套模板学习：
- **一句话讲明白**：像讲给初中生
- **再讲一遍（稍微严谨）**：补上术语/边界条件
- **你必须能回答的自测题**：答不上来就回到“一句话”
- **小实验（案例 + 验证数据 + 期望输出）**：能跑/能算/能对照
- **常见坑**：真实开发最容易踩的地方

---

## 1. Time（时间）

### 1.1 一句话讲明白
Flink 处理每条数据时，**到底用“数据发生的时间（事件时间）”还是“机器处理它的时间（处理时间）”来做统计**，这决定了你的窗口结果是否“符合业务现实”。

### 1.2 你需要掌握的知识点清单
- **三种时间语义**
  - **Event Time**：事件发生时间（最常用，最贴近业务）
  - **Processing Time**：算子处理时间（最快，但遇到延迟/乱序会偏）
  - **Ingestion Time**：进入 Flink 的时间（介于两者之间，较少用）
- **Timestamp Assigning（时间戳抽取）**：从事件里取出 eventTime
- **Watermark（水位线）**：对“乱序程度”的一种承诺，用来推动 Event Time 前进
- **Out-of-Order（乱序）与 Lateness（迟到）**
  - **乱序**：事件时间小于当前已看到的最大事件时间
  - **迟到**：事件时间已经落后于当前 watermark（窗口可能已触发/关闭）
- **Allowed Lateness（允许迟到）**：窗口触发后仍允许“补数据并更新结果”
- **Late Data Side Output（侧输出）**：迟到到“窗口清理之后”的数据要去哪
- **Idleness（空闲分区）**：某些分区断流导致 watermark 卡住（需要 idle 处理）

### 1.3 用更严谨的话讲一遍
Event Time 下，Flink 用 watermark 来判断“我大概可以认为时间推进到哪了”。当 watermark \(\ge\) 某个窗口的 endTime 时，该窗口会触发计算并输出；如果允许迟到，后续落入该窗口的事件仍可能更新窗口结果；超出允许迟到范围的数据通常会进入侧输出（或被丢弃）。

### 1.4 小实验：乱序 + 迟到 + 侧输出（可验证）

#### 实验目标
同一份数据，用 Event Time + watermark 处理后，你能看见：
- **第一次触发的窗口结果**
- **迟到数据到来后窗口结果更新**
- **过晚数据进入侧输出**

#### 验证数据
文件：`flink_adcance/data/time_events.csv`

我们做 **10 秒滚动窗口**（Tumbling），按 `user_id` 统计 `CLICK` 数量：
- window：`TumblingEventTimeWindows.of(Time.seconds(10))`
- watermark：乱序容忍 **2 秒**
- allowed lateness：**8 秒**
- late side output：输出到 `OutputTag`

#### 你应该得到的“期望输出”（按窗口解释，不依赖具体打印格式）
窗口以 `09:00:00` 为起点（示意）：

- **窗口 A**：\[09:00:00, 09:00:10)
  - 第一次触发时（看到 09:00:12 后 watermark 到 09:00:10），窗口内已到达的事件：
    - u1：09:00:01 / 09:00:04 / 09:00:03 → **3**
    - u2：09:00:07 → **1**
  - 后续迟到但仍被接受的事件更新窗口：
    - arrival=6：u1 09:00:05 → u1 变为 **4**
    - arrival=7：u2 09:00:09 → u2 变为 **2**
  - **过晚**（进入侧输出）：
    - arrival=11：u1 09:00:06（此时 watermark 已推进很靠后）→ **进入 side output**

- **窗口 B**：\[09:00:10, 09:00:20)
  - 最终结果（流结束后会关闭窗口）：
    - u1：09:00:12 → **1**
    - u2：09:00:19 → **1**（它在 arrival=9 才到，但仍应被计入）

- **窗口 C**：\[09:00:20, 09:00:30)
  - 最终结果：
    - u1：09:00:22 → **1**
    - u2：09:00:21 → **1**

#### 核心代码骨架（Java，便于对照理解）
> 仅展示关键点：时间戳、watermark、allowed lateness、侧输出。

```java
final OutputTag<Event> lateTag = new OutputTag<Event>("late-events") {};

WatermarkStrategy<Event> wm = WatermarkStrategy
    .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(2))
    .withTimestampAssigner((e, ts) -> e.eventTimeMillis);

events
  .assignTimestampsAndWatermarks(wm)
  .keyBy(e -> e.userId)
  .window(TumblingEventTimeWindows.of(Time.seconds(10)))
  .allowedLateness(Time.seconds(8))
  .sideOutputLateData(lateTag)
  .process(new ProcessWindowFunction<Event, String, String, TimeWindow>() { /* count */ });
```

### 1.5 常见坑（Time）
- **把 Processing Time 当成 Event Time 用**：业务统计会被机器抖动/延迟严重影响。
- **watermark 过小**：乱序稍微大一点就大量迟到，窗口反复更新/侧输出爆炸。
- **watermark 过大**：窗口迟迟不触发，看起来像“没数据/卡住了”。
- **分区空闲导致 watermark 不前进**：需要 `.withIdleness(...)`。

---

## 2. Window（窗口）

### 2.1 一句话讲明白
窗口就是把“无限的数据流”切成一个个“可结算的小账本”，你要先决定 **怎么切**（窗口类型），再决定 **怎么结算**（聚合函数/窗口函数/触发器）。

### 2.2 你需要掌握的知识点清单
- **窗口类型**
  - **滚动窗口（Tumbling）**：不重叠，适合“每分钟/每小时结算一次”
  - **滑动窗口（Sliding）**：重叠，适合“最近 10 分钟，每 1 分钟刷新”
  - **会话窗口（Session）**：按“间隔”切，适合“用户连续访问”
  - **全局窗口（Global）**：不建议直接用，通常配 Trigger
- **Keyed vs Non-Keyed**
  - `keyBy(...).window(...)`：每个 key 一组窗口（最常见）
  - `windowAll(...)`：全局窗口（单并行度/易成为瓶颈）
- **窗口函数**
  - **增量聚合**：`ReduceFunction / AggregateFunction`（更省内存）
  - **全量窗口**：`ProcessWindowFunction`（拿到窗口信息，但会缓存元素或依赖增量结果）
- **Trigger / Evictor（进阶）**
  - Trigger 决定“何时触发”
  - Evictor 决定“触发前/后剔除哪些元素”

### 2.3 小实验：滑动窗口的“重叠计数”为什么会变大？

#### 实验目标
用同一份订单数据，做 **窗口大小 10 秒、滑动步长 5 秒** 的滑动窗口聚合，理解“同一条数据会进入多个窗口”。

#### 验证数据
文件：`flink_adcance/data/window_orders.csv`

按 `product_id` 聚合 `amount`：
- window：`SlidingEventTimeWindows.of(Time.seconds(10), Time.seconds(5))`

#### 期望输出（按窗口解释，关键是“每个窗口各算各的”）
以 `09:00:00` 对齐（示意）：

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

#### 你必须能回答的自测题
- 为什么同一条 `09:00:06` 的事件会同时出现在窗口 A 和窗口 B？
- 如果把 slide 从 5s 改成 1s，会发生什么（计算量/输出频率/成本）？

### 2.4 常见坑（Window）
- **没有 `keyBy` 直接 `windowAll`**：吞吐很快被打爆。
- **窗口函数选错**：全量窗口容易内存压力；能增量就尽量增量。
- **窗口边界对齐误解**：Flink 窗口通常按 epoch 对齐，不一定按你“人类直觉的整点”。

---

## 3. State（状态）

### 3.1 一句话讲明白
State 就是 Flink 帮你“记住过去”，让你能做 **跨事件** 的业务逻辑：比如计数、去重、检测连续异常、维表规则等。

### 3.2 你需要掌握的知识点清单
- **Managed State vs Raw State**
  - Managed State：由 Flink 管、能参与 checkpoint、能做容错（推荐）
  - Raw State：自己管序列化/快照（除非你很确定）
- **Keyed State（键控状态）**：最常用（必须在 `keyBy` 之后）
  - `ValueState / ListState / MapState / ReducingState / AggregatingState`
- **Operator State（算子状态）**：与并行子任务绑定（例如 source 的 offset）
- **Broadcast State（广播状态）**：一份规则广播到所有并行实例
- **State Backend / 存储**
  - 大状态通常需要落盘（如 RocksDB），小状态可内存
  - 关注：状态大小、序列化、TTL、清理策略
- **TTL（状态过期）**：避免状态无限增长

### 3.3 小实验：60 秒内连续 3 次 FAIL 触发告警（Keyed State）

#### 实验目标
你能用 `ValueState`（或组合状态）实现：
- 每个 `device_id` 独立计数
- 连续 FAIL 计数达到 3 次且发生在 60 秒内 → 输出告警
- OK 到来 → 清空状态（重置）
- 超过 60 秒还没凑够 3 次 → 自动清空（避免老状态堆积）

#### 验证数据
文件：`flink_adcance/data/state_device_events.csv`

#### 期望输出（告警）
- d1：在 `09:00:20` 触发一次告警（前三次 FAIL 在 60 秒内）
- d2：在 `09:01:30` 触发一次告警（09:01:10/20/30 三次 FAIL）

#### 核心实现思路（用费曼法解释）
把每个设备当成一个小抽屉，抽屉里放两样东西：
- `failCount`：连续失败次数
- `firstFailTs`：这轮连续失败的“起始时间”

规则很像生活里“30 分钟内累计 3 次违章就扣分”：
- 第一次 FAIL：记下起始时间并开始计数
- 后续 FAIL：如果还在 60 秒内，计数 +1；否则“重新开一轮”
- 遇到 OK：清空抽屉
- 计数到 3：告警并清空（避免重复告警）

#### 代码骨架（Java，KeyedProcessFunction）
```java
public class Fail3TimesAlert extends KeyedProcessFunction<String, DeviceEvent, String> {
  private transient ValueState<Integer> failCount;
  private transient ValueState<Long> firstFailTs;

  @Override
  public void open(Configuration parameters) {
    failCount = getRuntimeContext().getState(new ValueStateDescriptor<>("failCount", Integer.class));
    firstFailTs = getRuntimeContext().getState(new ValueStateDescriptor<>("firstFailTs", Long.class));
  }

  @Override
  public void processElement(DeviceEvent e, Context ctx, Collector<String> out) throws Exception {
    if ("OK".equals(e.status)) {
      clear();
      return;
    }

    long ts = e.eventTimeMillis;
    Integer c = failCount.value();
    Long first = firstFailTs.value();

    if (c == null || first == null || ts - first > 60_000L) {
      failCount.update(1);
      firstFailTs.update(ts);
      // 可选：注册一个 event-time timer，在 first+60s 清理状态
      ctx.timerService().registerEventTimeTimer(ts + 60_000L);
      return;
    }

    int next = c + 1;
    failCount.update(next);
    if (next >= 3) {
      out.collect("ALERT device=" + ctx.getCurrentKey() + " ts=" + ts + " reason=FAIL_3_TIMES_IN_60S");
      clear();
    }
  }

  @Override
  public void onTimer(long timestamp, OnTimerContext ctx, Collector<String> out) throws Exception {
    // 超时清理（避免状态无限增长）
    clear();
  }

  private void clear() throws Exception {
    failCount.clear();
    firstFailTs.clear();
  }
}
```

### 3.4 常见坑（State）
- **忘了 `keyBy` 就用 Keyed State**：运行期直接报错或逻辑不生效。
- **状态不清理**：状态会无限增长，最终 OOM/磁盘爆。
- **用 ListState 但从不做去重/压缩**：状态膨胀很快。
- **TTL 以为能“立刻删除”**：TTL 通常是“惰性清理”，需要结合访问/compact 才释放。

---

## 4. Checkpoint（检查点）

### 4.1 一句话讲明白
Checkpoint 是 Flink 的“自动存档”：它定期把 **状态**（以及必要时的“在路上的数据”）做快照；作业挂了重启后，从最近一次快照恢复，做到 **（尽可能）Exactly-Once**。

### 4.2 你需要掌握的知识点清单
- **Checkpoint vs Savepoint**
  - **Checkpoint**：系统自动、频繁、用于容错恢复
  - **Savepoint**：人为触发、用于升级/迁移/回滚（更像“版本存档”）
- **Exactly-Once 的前提**
  - 作业本身 checkpoint 成功
  - source/sink 支持或配合 exactly-once（例如 2PC sink、Kafka 事务等）
- **Barrier（屏障）与对齐**
  - aligned checkpoint：需要等待 barrier 对齐（可能增加延迟）
  - unaligned checkpoint：背压时更稳，但会更大（进阶）
- **常用配置项（必须知道“为什么要改”）**
  - interval：checkpoint 间隔
  - timeout：超时
  - minPause：最小间隔（防止太频繁）
  - maxConcurrent：并发 checkpoint 数
  - externalized：作业取消时是否保留 checkpoint

### 4.3 小实验：有状态计数 + 人为故障 + 恢复后不丢不重（验证思路）

> 说明：Checkpoint 的“真正验证”需要 **作业能自动重启**（本地或集群均可），这里给你一个最小验证套路。你不需要先把所有生产细节学完，先把“闭环”跑通。

#### 验证数据
文件：`flink_adcance/data/checkpoint_numbers.txt`（1~20）

#### 实验目标
做一个 keyed count（状态里存计数），运行过程中人为抛异常触发重启：
- 恢复后计数 **从最近 checkpoint 的状态继续**（不会从 0 重新计）
- 最终输出 **count=20**（或至少能解释为什么不是 0/不是随机）

#### 参考配置（代码层面）
```java
env.enableCheckpointing(2000); // 2s
CheckpointConfig cfg = env.getCheckpointConfig();
cfg.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
cfg.setCheckpointTimeout(60_000);
cfg.setMinPauseBetweenCheckpoints(500);
cfg.setMaxConcurrentCheckpoints(1);
cfg.enableExternalizedCheckpoints(CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);
```

#### 关键验证步骤（你要能“口算/解释”）
- 在输出里找两类信息：
  - **checkpoint 成功**的日志/提示（表示有可恢复点）
  - **重启后继续输出**（表示恢复生效）
- 观察 count：
  - 如果没有 checkpoint 成功就挂了 → 重启后可能从头再来（这不是 Flink “不行”，是你没存档成功）
  - 如果 checkpoint 成功了 → 重启后 count 应该从上次快照继续

### 4.4 常见坑（Checkpoint）
- **只开 checkpoint 不看 sink 语义**：最终结果仍可能重复（尤其是外部系统写入）。
- **checkpoint 太频繁**：反而拖慢吞吐、造成更大背压。
- **checkpoint 太稀疏**：一挂就回退很多，恢复成本和数据回放压力大。
- **不理解“对齐”**：背压时 aligned checkpoint 可能让延迟变大，误以为是“Flink 卡了”。

---

## 5. 最终总结：一页指南（可当速查表）

### 5.1 你学会了什么（用一句话复述）
- **Time**：我知道 Flink 用哪种时间做业务统计，能用 watermark 解释乱序/迟到。
- **Window**：我知道如何把流切块结算，能解释滚动/滑动/会话窗口的差异与代价。
- **State**：我知道如何在 `keyBy` 后“记住过去”，并且会清理状态避免无限增长。
- **Checkpoint**：我知道怎么让状态可恢复，能说清 exactly-once 依赖哪些条件。

### 5.2 最小闭环检查清单（建议你逐条打勾）
- **Time**
  - [ ] 能说清 Event Time vs Processing Time 的差异
  - [ ] 能解释 watermark 为什么决定窗口何时触发
  - [ ] 能解释 allowed lateness 与 side output 的区别
- **Window**
  - [ ] 能区分 tumbling/sliding/session
  - [ ] 能解释滑动窗口为何会“重复计入”
  - [ ] 能说明增量聚合 vs 全量窗口的内存差异
- **State**
  - [ ] 会用 ValueState 做最小的“跨事件逻辑”
  - [ ] 会做状态清理（timer/TTL/规则）
  - [ ] 了解 keyed/operator/broadcast 的适用场景
- **Checkpoint**
  - [ ] 会开启 checkpoint 并解释关键参数
  - [ ] 知道 savepoint 适合做升级/迁移
  - [ ] 知道 sink 语义决定最终是否 exactly-once

