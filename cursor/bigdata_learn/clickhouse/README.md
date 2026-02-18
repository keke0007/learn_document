 # ClickHouse 学习总览

 本文是 `clickhouse/` 模块的总览文档，详细罗列大数据 **离线批处理** 与 **实时分析** 场景下需要掌握的 ClickHouse 知识点，并与 `cases/` + `data/` + `scripts/` 中的实践案例和验证数据对应起来。

 更偏向“全量知识清单 + 对照案例索引”，而 `GUIDE.md` 更像“学习路线 + 快速上手指南”。

 ---

 ## 一、基础环境与工具

 ### 1. 安装与部署

 - **单机安装**
   - 二进制安装 `clickhouse-server`、`clickhouse-client`
   - 基本配置文件位置：`/etc/clickhouse-server/config.xml`, `users.xml`
 - **集群环境（了解）**
   - ZooKeeper/ClickHouse Keeper
   - 分片（Shard）与副本（Replica）规划

 ### 2. 客户端使用

 - `clickhouse-client` 基本参数：
   - `--host`、`--port`、`--user`、`--password`  
   - `--multiquery` 一次执行多个 SQL
 - HTTP 接口（了解）：`POST /?query=...`

 ---

 ## 二、核心概念与存储引擎

 ### 1. 数据库与表

 - 数据库：逻辑隔离命名空间  
 - 表：存储实体，绑定具体 **表引擎（Engine）**

 ### 2. 表引擎体系（重点）

 - **MergeTree 系列（核心）**
   - `MergeTree`：基础列式引擎，支持分区、排序、索引
   - `ReplacingMergeTree`：带“版本列”的去重/覆盖场景
   - `SummingMergeTree`：后台合并时自动累计数值列
   - `AggregatingMergeTree`：存储聚合状态
 - **日志系列（轻量）**
   - `Log` / `StripeLog` / `TinyLog`
 - **分布式路由**
   - `Distributed`：路由到多个 shard 上的同构表

 **对应案例：**
 - `cases/offline_order_analysis.md`：使用 `MergeTree` 进行离线统计  
 - `cases/realtime_event_agg.md`：使用 `MergeTree` + 物化视图做实时聚合

 ---

 ## 三、数据类型与函数

 ### 1. 数据类型

 - 数值：`Int8/16/32/64`, `UInt8/16/32/64`, `Float32/64`
 - 字符串：`String`, `FixedString(N)`
 - 日期时间：`Date`, `DateTime`, `DateTime64`
 - 复合类型：`Array(T)`, `Tuple(T1, T2, ...)`, `Map(K,V)`（新版本）

 ### 2. 常用函数

 - **聚合函数**
   - `count()`, `sum()`, `avg()`, `min()`, `max()`  
   - `uniqExact()/uniqCombined()`（去重计数）
 - **日期函数**
   - `today()`, `now()`, `toDate()`, `toStartOfDay()`, `toStartOfMinute()`  
   - `dateDiff()`, `dateAdd()`
 - **字符串函数**
   - `lower()`, `upper()`, `substring()`, `replaceAll()` 等
 - **窗口函数（新版本支持）**
   - `row_number() over (...)`, `rank()`, `lag()`, `lead()` 等

 **对应案例：**
 - 在所有案例 SQL 中广泛使用，尤其是：
   - 订单金额统计（聚合函数）  
   - 实时 PV/UV 统计（`uniqExact` + 时间函数）

 ---

 ## 四、离线开发知识点（批处理）

 ### 1. 模型设计

 - **事实表**：订单明细（`orders_offline`）
   - 列：订单 ID、用户 ID、下单时间、城市、金额、状态等  
   - 分区：按月或按天分区（`PARTITION BY toYYYYMM(order_date)` 等）  
   - 排序键：`ORDER BY (order_date, user_id)`，兼顾查询与写入
 - **维度表**：用户表（`users_offline`）
   - 相对小表，可用 `MergeTree` 或 `ReplacingMergeTree`

 ### 2. 批量导入

 - `INSERT INTO table FORMAT CSV`  
 - `clickhouse-client --query="INSERT INTO ... FORMAT CSV" < file.csv`

 ### 3. 常用分析模式

 - 按天/周/月统计：

   ```sql
   SELECT
       order_date,
       count() AS order_cnt,
       sum(amount) AS total_amount
   FROM orders_offline
   GROUP BY order_date
   ORDER BY order_date;
   ```

 - 用户维度画像：
   - 累计订单数/金额  
   - 最近一次下单时间  

 **对应案例：**
 - `cases/offline_order_analysis.md`  
 - `cases/offline_user_profile.md`

 ---

 ## 五、实时开发知识点（实时/近实时）

 ### 1. 实时明细表设计

 - 表：`events_realtime`（行为日志/埋点数据）
   - 字段：事件时间、用户 ID、事件类型、页面、设备、网络、停留时长等  
   - 分区键：按天或按月（`PARTITION BY toYYYYMMDD(event_time)`）  
   - 排序键：`ORDER BY (event_time, user_id)` 或 `(user_id, event_time)`

 ### 2. 写入方式

 - 简单模拟：周期性 `INSERT` CSV 行  
 - 生产级：通过 Kafka / Flink / 自研服务写入 ClickHouse
   - 表引擎可以使用 `Kafka` + 物化视图，或外部流计算写入 MergeTree

 ### 3. 实时聚合与物化视图

 - 明细表 + 物化视图 + 聚合表 的经典模式：  
   - 明细表：高写入吞吐  
   - 物化视图：对新写入数据做增量聚合  
   - 聚合表：高性能查询

 **对应案例：**
 - `cases/realtime_event_agg.md` + `scripts/load_realtime_demo.sql`

 ---

 ## 六、性能优化与开发实践

 ### 1. 建模层面

 - 合理选择分区字段（时间/业务主维度）  
 - 选择合适的排序键，避免“全表扫描”  
 - 适当控制单分区大小（避免过多/过少）

 ### 2. 查询层面

 - 避免 `SELECT *`，只查需要的列  
 - 优先使用过滤条件匹配分区与排序键  
 - 善用 `LIMIT`（尤其在调试时）  
 - 使用 `EXPLAIN` 查看查询计划（新版本）

 ### 3. 资源与配置层面（了解）

 - 并发设置、内存限制、最大查询时间等  
 - 合并线程数量与后台任务压力

 ---

 ## 七、知识点与案例/数据对照表

 | 知识点模块 | 关键点 | 案例文档 | 验证数据文件 | 相关脚本 |
 |------------|--------|----------|--------------|----------|
 | 基础安装与客户端 | 单机安装、client 使用 | `GUIDE.md` | - | - |
 | MergeTree 表建模 | PARTITION / ORDER BY | `offline_order_analysis.md` | `orders_offline.csv` | `setup_tables.sql` |
 | 离线订单统计 | 每日/城市维度统计 | `offline_order_analysis.md` | `orders_offline.csv` | `load_offline_data.sql` |
 | 离线用户画像 | 用户累计指标、最近下单 | `offline_user_profile.md` | `orders_offline.csv`, `users_offline.csv` | `load_offline_data.sql` |
 | 实时事件明细 | 行为日志表设计 | `realtime_event_agg.md` | `events_realtime.csv` | `load_realtime_demo.sql` |
 | 实时聚合 & 物化视图 | PV/UV 聚合表 | `realtime_event_agg.md` | `events_realtime.csv` | `setup_tables.sql`, `common_queries.sql` |

 > 提示：你可以先不关心集群/分布式细节，在单机上把以上三个案例都跑通，再逐步理解分布式部署与高可用。

 ---

 ## 八、如何使用本模块学习

 1. 阅读 `GUIDE.md`，按照学习路径安装环境并执行一个完整流转（建表 → 导入离线数据 → 查询 → 模拟实时数据 → 实时聚合查询）。
 2. 打开 `cases/` 中的三个案例文档，对照 `data/` 中的 CSV 数据与 `scripts/` 中的 SQL 动手实践。
 3. 在掌握示例的基础上，尝试：  
    - 按自己的业务设计新的字段与表结构  
    - 新增一个离线宽表 + 一个实时聚合表  
    - 对比 Hive/Spark 的实现方式与性能差异。

 当你能：

 - 自己设计 ClickHouse 表结构（包含分区 & 排序键）  
 - 完成离线批量导入并做多维统计  
 - 搭建一个简单的实时埋点 → 实时聚合指标链路  

 基本就具备了 ClickHouse 在“大数据离线 + 实时开发”中的实战能力。

