# Flink SQL 学习指南（费曼学习法）：知识点 + 案例 + 验证数据

> 目标：把 Flink SQL 学到“能解释清楚、能写出能跑的 DDL/DML、能用小数据对照结果”的程度。

本目录自带：
- **验证数据**：`flink_sql/data/`
  - `orders.csv`、`user_events.csv`、`dim_products.csv`
- **案例**：`flink_sql/cases/`
  - `cases/README.md`（索引页）
  - 4 个可复制执行的 SQL 案例
- **运行说明**：`flink_sql/scripts/sql_client_run.md`

---

## 0. 费曼学习法（在 Flink SQL 上怎么用）

每个知识点都按这 5 句话来学：
- **一句话讲明白**：不用术语也能讲通
- **关键术语补齐**：把“模糊”变“可操作”
- **会写的最小 SQL**：能 CREATE / INSERT / SELECT 跑通
- **能对照的小数据**：用 10 行数据算出期望结果
- **能解释的坑**：为什么生产会错/慢/不一致

---

## 1. Flink SQL 学习知识点清单（生产视角）

### 1.1 表与动态表（Dynamic Table）
- **一句话**：Flink SQL 里“表”不一定是静态结果，它可能会随着流数据不断变化。
- **你必须知道**
  - **Append-only**：只插入不更新（最简单）
  - **Changelog**：会更新/撤回（聚合、去重、TopN 常见）
  - sink 是否能消费 changelog（能不能 upsert）

### 1.2 DDL：Connector / Format / Schema
- **一句话**：DDL 决定“数据从哪来、长什么样、到哪去”。
- **你必须会写**
  - `CREATE TABLE ... WITH (...)`
  - `filesystem` + `csv/json`（学习最友好）
  - `print` sink（验证最方便）
- **生产关注**
  - Kafka / Upsert-Kafka / JDBC / Iceberg 等 connector 的语义与容错能力

### 1.3 DML：INSERT / CTAS / 视图
- **一句话**：DML 把查询结果写入 sink。
- **你必须知道**
  - `INSERT INTO sink SELECT ...`
  - `CREATE VIEW` 组织复杂 SQL（可读性/复用）

### 1.4 时间语义：Event Time / Watermark / Lateness
- **一句话**：窗口统计要用“事件发生时间”，Watermark 决定什么时候可以结算。
- **你必须会写**
  - 计算列：`ts AS TO_TIMESTAMP(time_str)`
  - watermark：`WATERMARK FOR ts AS ts - INTERVAL 'x' SECOND`
- **生产关注**
  - watermark 太小 → 迟到多、结果反复更新
  - watermark 太大 → 窗口迟迟不出结果

### 1.5 窗口：Window TVF（TUMBLE / HOP / SESSION）
- **一句话**：把无限流切成一段段小账本结算。
- **你必须知道**
  - `TUMBLE(TABLE t, DESCRIPTOR(ts), INTERVAL '10' SECOND)`
  - 输出里常见 `window_start/window_end`

### 1.6 Join：事实表 / 维表 / Temporal（进阶）
- **一句话**：Join 让你把“发生了什么”拼上“它是什么/规则是什么”。
- **你必须知道**
  - 普通 `JOIN`（维表静态）
  - 生产常见：Lookup Join（外部维表）、Temporal Join（随时间变化）

### 1.7 去重、TopN 与 Over Window
- **一句话**：很多“只要最新一条/TopN”都可以用窗口函数解决。
- **你必须会写**
  - `ROW_NUMBER() OVER (PARTITION BY k ORDER BY ts DESC)`

### 1.8 主键与 Upsert（结果正确性关键）
- **一句话**：如果结果会更新，就需要主键来“覆盖旧值”，否则外部系统会重复/脏写。
- **你必须知道**
  - `PRIMARY KEY (...) NOT ENFORCED`
  - append-only sink vs upsert sink 的差别

### 1.9 状态与调优（SQL 也会用 state）
- **一句话**：SQL 的聚合/去重/Join 都在用状态，状态不控就会慢/大/不稳。
- **你必须知道**
  - 状态 TTL：`SET 'table.exec.state.ttl' = '1 h';`
  - mini-batch：`SET 'table.exec.mini-batch.enabled' = 'true';`

---

## 2. 案例与验证数据（建议按顺序跑）

### 案例1：DDL / DML / 聚合（入门闭环）
- 文档：`flink_sql/cases/01_flink_sql_ddl_dml_basics.md`
- 数据：`flink_sql/data/orders.csv`
- 你要验证的结果：
  - U001：cnt=3 total=30
  - U002：cnt=3 total=30
  - U003：cnt=1 total=8

### 案例2：Event Time / Watermark / 窗口（TUMBLE）
- 文档：`flink_sql/cases/02_flink_sql_event_time_watermark_windows.md`
- 数据：`flink_sql/data/orders.csv`
- 你要验证的结果：按 10 秒滚动窗口、按 product 聚合金额

### 案例3：Join 维表（按维度聚合）
- 文档：`flink_sql/cases/03_flink_sql_joins_lookup_dim.md`
- 数据：`flink_sql/data/orders.csv` + `flink_sql/data/dim_products.csv`
- 你要验证的结果：
  - cat_a：cnt=5 total=55
  - cat_b：cnt=2 total=13

### 案例4：Changelog + 去重（ROW_NUMBER）+ Upsert
- 文档：`flink_sql/cases/04_flink_sql_changelog_dedup_upsert.md`
- 数据：`flink_sql/data/user_events.csv`
- 你要验证的结果（最终最新事件）：
  - U001 → 09:00:18 view P003
  - U002 → 09:00:12 buy  P002
  - U003 → 09:00:22 buy  P003

---

## 3. 最终总结：一页速查（Checklist）

### 3.1 你能用一句话讲清楚
- **动态表**：结果会变，所以会有 changelog
- **主键/Upsert**：更新型结果必须能覆盖旧值
- **Event Time / Watermark**：窗口何时触发取决于 watermark
- **Window TVF**：按时间切块结算（TUMBLE/HOP/SESSION）
- **SQL 也有状态**：聚合/Join/去重都在用 state，TTL/mini-batch 是常用开关

### 3.2 上线前必查
- [ ] sink 语义是否匹配（append-only 还是 upsert/changelog）
- [ ] watermark 是否符合真实乱序（避免迟到爆炸或窗口不出数）
- [ ] 状态是否可控（TTL/清理策略）
- [ ] checkpoint 是否稳定（否则一致性无法保证）

