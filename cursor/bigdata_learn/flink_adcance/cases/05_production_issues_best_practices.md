# Flink 生产环境常见问题与最佳实践清单（含案例 Runbook）

> 适用版本：以 Flink **1.17.x** 的概念与配置为主（你项目里也在用 1.17.0）。
>
> 使用方式：当作“值班手册/排障 Runbook”。每个问题都按 **现象 → 快速确认 → 常见根因 → 处理步骤 → 验证 → 预防（最佳实践）** 给出。

---

## 0. 生产排障总原则（先看什么）

- **先看 Web UI**
  - **JobGraph / ExecutionGraph**：哪个算子变慢？是否存在明显的“红色背压”？
  - **Checkpoint**：最近一次 checkpoint 是否成功？耗时多少？对齐时间（alignment）是否异常？
  - **Task Metrics（如果接了监控）**：`busyTimeMsPerSecond / backPressuredTimeMsPerSecond / idleTimeMsPerSecond`，以及吞吐、延迟等。
- **再看日志（JobManager/TaskManager）**
  - 是否有 `CheckpointException`、`OutOfMemoryError`、`RocksDB` 相关、`TimeoutException`、`ClassNotFoundException` 等关键字。
- **最后看外部系统**
  - Kafka：lag、事务超时、producer error
  - HDFS/S3：checkpoint 目录是否可写、是否慢、是否 403/permission
  - DB：连接池耗尽、写入慢、锁冲突、幂等/唯一键冲突

---

## 1. Checkpoint / 容错类问题（最常见）

### 案例 1.1：Checkpoint 一直失败 / 超时

- **现象**
  - Web UI 的 checkpoint 面板持续失败（FAILED / TIMEOUT）
  - 失败后 job 频繁重启（取决于 restart strategy）
- **快速确认**
  - 看 checkpoint 的 **duration** 是否接近 `checkpoint.timeout`
  - 看 **alignment time** 是否很高（通常意味着背压或网络拥塞）
  - 看失败原因是否为：
    - checkpoint barrier 无法对齐 / 超时
    - state backend 写入慢（HDFS/S3/Fs）
- **常见根因**
  - **下游背压**导致 barrier 对齐卡住（sink 慢、外部系统慢、写入阻塞）
  - checkpoint 存储慢/不可用（HDFS 负载高、S3 限速、权限问题）
  - 状态过大（state size 增长过快，快照写不完）
- **处理步骤**
  - 先**止血**：
    - 临时增大 `checkpoint.timeout`
    - 临时增大 `checkpoint.interval`（降低频率）
  - 再**定位**：
    - 找到背压算子（通常是 sink / join / keyBy 后的重算子）
    - 检查 checkpoint 目录权限与吞吐
  - 最后**根治**：
    - 优化 sink：批量、异步、并行度、幂等写
    - 热 key 拆分/加盐（见 2.2）
    - 控制状态增长（TTL/清理，见 3.2）
- **验证**
  - 连续 N 次 checkpoint 成功（例如 5 次）
  - checkpoint duration 明显下降，且 alignment time 不再飙高
- **预防（最佳实践）**
  - **不要盲目追求超短 checkpoint interval**：先跑稳再调小
  - 重要作业建议开启并审视：
    - `setMinPauseBetweenCheckpoints`
    - `setMaxConcurrentCheckpoints(1)`（先稳后快）
  - checkpoint 存储要选“稳定且吞吐可靠”的位置（HDFS/S3 目录规范化、权限固定）

---

### 案例 1.2：Checkpoint 变得越来越大（状态膨胀）

- **现象**
  - checkpoint size 逐步增长（几十 MB → 几百 MB → GB）
  - duration 变长，最终超时或导致频繁背压
- **快速确认**
  - Web UI 看 checkpoint size/duration 的趋势
  - 观察 RocksDB 本地目录是否膨胀、磁盘是否接近满
- **常见根因**
  - 状态没有清理：ListState/MapState 无上限、窗口没有清理、维表缓存不回收
  - key 空间巨大且业务逻辑“把所有 key 都留住”
- **处理步骤**
  - 排查状态来源：
    - 哪些算子用了 keyed state / 窗口 state
    - 是否能加 **TTL** 或明确清理时机（timer、窗口清理、业务重置）
  - 若使用 RocksDB：
    - 检查本地盘是否够用、I/O 是否饱和
- **验证**
  - checkpoint size 稳定在可控区间（并能解释其上限）
- **预防（最佳实践）**
  - 所有状态都要问一句：**“它什么时候能被删除？”**
  - 规则/维表类状态，优先用 TTL + 上限控制（例如 LRU/最大条目）

---

### 案例 1.3：作业 Cancel/升级后想回滚，但找不到可恢复点

- **现象**
  - Cancel 后 checkpoint 被清理，无法快速恢复
  - 升级失败后无法从 savepoint 回滚
- **快速确认**
  - 是否开启 Externalized Checkpoint（取消时保留）
  - 是否在升级前做了 savepoint
- **处理步骤**
  - 关键作业建议：
    - **升级前必做 savepoint**
    - 生产策略：保留最近 N 个 savepoint（并有清理策略）
- **预防（最佳实践）**
  - 一条硬规则：**“上线前先 savepoint，回滚靠 savepoint”**

---

## 2. 性能 / 背压 / 吞吐问题

### 案例 2.1：背压（Backpressure）持续为红，吞吐下降

- **现象**
  - Web UI Backpressure 面板显示红色（高 backpressured time）
  - 上游堆积、延迟上升
- **快速确认**
  - 找到最慢的下游算子（通常是 sink 或重计算算子）
  - 看并行度：是否某个算子并行度过低
  - 看外部系统：DB/Kafka/HDFS 是否写入慢
- **常见根因**
  - sink 写入慢（同步写/单线程写/每条写一次）
  - 网络 buffer 不足或下游处理能力不足
  - 反序列化/对象创建过多导致 GC 压力（见 2.3）
- **处理步骤**
  - sink 优化：批量、异步、并行、幂等
  - 提高热点算子并行度（注意 keyBy 后 rescale 的语义）
  - 必要时做算子链调整（避免长链让局部瓶颈放大）
- **验证**
  - backPressuredTime 下降
  - 端到端延迟下降，吞吐恢复
- **预防（最佳实践）**
  - 生产 sink 必须有“写入速率”与“失败重试”设计
  - 关键指标要告警：吞吐、延迟、背压、checkpoint 成功率

---

### 案例 2.2：热 key / 数据倾斜导致某个 subtask 打满

- **现象**
  - 同一个算子的某个 subtask CPU/忙碌时间明显高于其他
  - 吞吐受单点限制
- **快速确认**
  - Web UI / metrics 对比每个 subtask 的 `numRecordsIn/Out`、busy time
- **常见根因**
  - 业务 key 分布极不均匀（例如某个 userId 占 80%）
- **处理步骤**
  - 方案 A（常用）：**加盐拆分 key**
    - 先在上游把热 key 拆成多个子 key（`key + randomSalt`）
    - 下游再做二次聚合还原
  - 方案 B：局部预聚合（map-side combine）降低 shuffle 压力
- **验证**
  - 各 subtask 的负载趋于均匀
- **预防（最佳实践）**
  - 上线前对 key 分布做压测（哪怕用采样数据）

---

### 案例 2.3：频繁 Full GC / OOM，任务抖动或反复重启

- **现象**
  - 日志出现 `OutOfMemoryError` 或 GC 时间占比异常高
  - 吞吐周期性下降、checkpoint 变慢、延迟拉高
- **快速确认**
  - 看 GC 日志（建议生产开启）
  - 看堆/直接内存/managed memory 的使用趋势
- **常见根因**
  - 对象创建过多（每条数据 new 大量对象、频繁字符串拼接）
  - 大窗口全量缓存元素（用错窗口函数）
  - RocksDB/managed memory 与堆内存分配不合理
- **处理步骤**
  - 先减少对象创建（复用、避免大对象、避免无界集合）
  - 窗口优先用增量聚合（Aggregate/Reduce）
  - 调整 TaskManager 内存模型与 RocksDB 配置（按集群实际资源）
- **验证**
  - GC 时间占比下降、OOM 不再出现，吞吐更平稳
- **预防（最佳实践）**
  - 关键作业保留 GC 日志与 JVM 参数基线
  - 大状态作业优先用 RocksDB（并确保本地盘与 IOPS）

---

## 3. State / RocksDB / 存储问题

### 案例 3.1：RocksDB 本地盘爆满 / compaction 造成卡顿

- **现象**
  - TaskManager 本地目录膨胀，磁盘接近满
  - 日志出现 RocksDB compaction/IO 相关告警
  - checkpoint duration 变长、背压加剧
- **快速确认**
  - 检查 TM 本地磁盘剩余空间与 I/O
  - 看 checkpoint size 是否同步增大
- **常见根因**
  - 状态增长过快（没 TTL/没清理）
  - 本地盘太小或 IOPS 不足
- **处理步骤**
  - 立即扩容磁盘/迁移 TM 到更好的盘（止血）
  - 加 TTL/清理状态（根治）
- **验证**
  - 磁盘使用曲线变缓并趋稳，checkpoint 恢复正常
- **预防（最佳实践）**
  - RocksDB 作业：本地盘容量与 IOPS 必须按“状态上限 + buffer + compaction”评估

---

### 案例 3.2：状态逻辑正确但“越来越慢”（状态访问变重）

- **现象**
  - 业务逻辑没变，但延迟逐渐升高
  - state 相关算子 busy time 上升
- **常见根因**
  - MapState/ListState 过大，单次访问成本不断上升
  - 序列化/反序列化成本高（复杂对象、嵌套结构）
- **处理步骤**
  - 改为更紧凑的状态结构（例如只存聚合值，不存全量明细）
  - 对大 Map 做分片/分桶
- **预防（最佳实践）**
  - 状态设计优先选择“可汇总、可裁剪”的结构

---

## 4. 时间语义 / 窗口正确性问题（结果不对最难排）

### 案例 4.1：Watermark 不推进，窗口迟迟不触发

- **现象**
  - 你明明有数据，但窗口结果不输出
  - watermark 停在某个时间不动
- **快速确认**
  - 是否是多分区 source，其中某些分区长时间无数据
- **常见根因**
  - **空闲分区**导致 watermark 被最慢分区拖住
- **处理步骤**
  - 事件时间 + 多分区场景建议启用：
    - `.withIdleness(Duration.ofMinutes(x))`
- **验证**
  - watermark 能持续推进，窗口按预期触发
- **预防（最佳实践）**
  - 所有“可能断流的分区化 source”都要考虑 idleness

---

### 案例 4.2：迟到数据太多，窗口疯狂更新，输出爆炸

- **现象**
  - allowed lateness 开了很大，窗口频繁“更新输出”
  - 下游被更新流量打爆
- **常见根因**
  - watermark 设得过激进（乱序容忍太小）
  - allowed lateness 设得过大且没做侧输出治理
- **处理步骤**
  - 调整 watermark 策略（更贴合真实乱序）
  - 将“极晚数据”导入 side output，单独补偿
- **验证**
  - 主链路稳定，迟到数据进入可控通道
- **预防（最佳实践）**
  - 迟到数据处理一定要有“业务策略”：丢弃/补偿/重算/离线修正

---

## 5. Connector / Exactly-Once / 数据一致性问题

### 案例 5.1：Kafka sink / 事务超时导致写入失败或重复

- **现象**
  - 日志出现 Kafka transaction timeout / producer fenced
  - 重启后出现重复数据（视业务实现）
- **快速确认**
  - Kafka 端配置与 Flink 端事务超时是否匹配
  - checkpoint 间隔/超时是否导致事务长时间不提交
- **处理步骤**
  - 保证 checkpoint 能稳定成功（事务提交通常与 checkpoint 绑定）
  - 调整 Kafka 事务相关超时（按实际平台）
- **预防（最佳实践）**
  - Exactly-once 要求“端到端协同”：source、state、sink 都要匹配

---

### 案例 5.2：JDBC/数据库 sink 重启后重复写 / 脏写

- **现象**
  - 作业重启后出现重复行/重复累加
- **常见根因**
  - sink 不是幂等（insert-only）
  - 没有唯一键约束或 upsert 语义
- **处理步骤**
  - 改成 upsert（按主键覆盖）或幂等写
  - 或引入 2PC sink（成本更高但一致性更强）
- **预防（最佳实践）**
  - 生产 DB sink：必须明确“幂等策略”与“回放策略”

---

## 6. 发布/升级/依赖问题（常见但容易忽略）

### 案例 6.1：ClassNotFound / NoSuchMethod（依赖冲突）

- **现象**
  - 本地能跑，集群一提交就报类找不到/方法不存在
- **常见根因**
  - jar 没有正确打包（缺依赖）
  - 与集群自带依赖冲突（版本不一致）
- **处理步骤**
  - 使用 shading 打包（把依赖打进 fat jar，并做 relocate）
  - 明确 provided vs shaded 的边界（尤其 connector）
- **预防（最佳实践）**
  - 上线前做一次“与集群环境一致”的集成测试提交

---

### 案例 6.2：从 savepoint 恢复失败（状态 schema 不兼容）

- **现象**
  - 从 savepoint 恢复时报反序列化失败/状态不匹配
- **常见根因**
  - 修改了 state 的序列化结构但没有做兼容
  - 更换了 POJO/序列化器导致不兼容
- **处理步骤**
  - 升级策略：
    - 能保持状态兼容就保持（优先）
    - 不兼容就做“新作业 + 双写/切流 + 回放”的迁移方案
- **预防（最佳实践）**
  - 状态结构一旦上线，就要像“数据库 schema”一样谨慎演进

---

## 7. 上线前最佳实践清单（Checklist）

- **作业语义**
  - [ ] 明确时间语义（event/processing），watermark 策略与乱序假设有数据支撑
  - [ ] 迟到数据策略明确：丢弃/侧输出补偿/离线修正
- **状态**
  - [ ] 每个状态都有清理策略（TTL/timer/窗口清理）
  - [ ] 状态上限可估算（key 数 * 每 key 大小）
- **Checkpoint / 恢复**
  - [ ] checkpoint 目录（HDFS/S3）权限与吞吐确认
  - [ ] checkpoint interval/timeout/minPause/maxConcurrent 有基线
  - [ ] externalized checkpoint / savepoint 策略明确（保留与清理）
- **性能**
  - [ ] 热 key 风险评估（采样/压测）
  - [ ] sink 写入模型（批量/异步/并行）与幂等性确定
- **可观测性**
  - [ ] 关键指标接入监控：吞吐、延迟、背压、checkpoint 成功率、重启次数
  - [ ] 告警阈值与 oncall 处理步骤明确
- **发布**
  - [ ] 上线前做 savepoint（可回滚）
  - [ ] 与集群环境一致的提交验证通过（依赖冲突/权限/连接器）

---

## 8. 运行中巡检清单（Daily/Weekly）

- **稳定性**
  - [ ] 最近 24h checkpoint 成功率、平均耗时是否异常
  - [ ] 重启次数是否上升（是否有隐性异常）
- **资源**
  - [ ] TM/容器 CPU、内存、磁盘、网络是否接近瓶颈
  - [ ] RocksDB 本地目录增长是否异常
- **业务**
  - [ ] 输入 lag（Kafka）是否升高
  - [ ] 输出端（DB/Kafka/ES）错误率是否升高

---

## 9. 故障演练与回滚策略（建议做一次）

- **演练 1：故意 kill TaskManager**
  - 目标：验证 checkpoint 恢复链路可用、恢复时间可接受
- **演练 2：故意让 sink 变慢（限速/停服务）**
  - 目标：观察背压传播、checkpoint 是否能坚持、告警是否触发
- **回滚**
  - 规则：发布前 savepoint，发布后保留一段时间
  - 操作：出现严重问题优先从最近 savepoint 回滚

