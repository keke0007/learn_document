 # Doris 学习总览

 本文是 `doris/` 模块的总览文档，系统罗列在大数据 **离线批处理** 与 **实时/近实时分析** 场景下需要掌握的 Doris 核心知识点，并与 `cases/` + `data/` + `scripts/` 中的实践案例和验证数据对齐。

 相比 `GUIDE.md` 的“学习路线 + 快速上手”，本文件更偏向“知识点清单 + 案例索引”。

 ---

 ## 一、基础环境与组件

 ### 1. Doris 架构

 - **FE (Frontend)**：
   - 存储元数据（库、表、分区、物化视图等）
   - 负责 SQL 解析、优化、计划生成
 - **BE (Backend)**：
   - 存储数据，负责执行查询计划
 - **Broker（可选）**：
   - 用于访问 HDFS / 对象存储等外部数据源

 ### 2. 客户端与连接

 - 使用 MySQL 协议连接 Doris：
   - `mysql -h fe_host -P9030 -uroot`
 - Web UI（如有开启）：查看集群状态、导入任务、表信息等

 ---

 ## 二、核心概念与表模型

 ### 1. 表模型（Key Type）

 - **DUPLICATE KEY**
   - 不做聚合，原样存储
   - 适用于：日志明细、订单明细等追加写入场景
 - **AGGREGATE KEY**
   - 同 Key 的记录根据聚合函数（SUM、MAX 等）进行合并
   - 适用于：按 Key 聚合的指标表（如日统计表）
 - **UNIQUE KEY**
   - 按 Key 做覆盖更新（旧行被新行覆盖）
   - 适用于：有限规模的维度表或简单更新场景
 - **PRIMARY KEY**
   - 推荐的新模型，支持主键更新，语义更清晰
   - 适用于：对更新有要求的明细/维度表

 **对应案例：**
 - `cases/offline_order_analysis.md`：订单明细用 `DUPLICATE KEY`  
 - `cases/offline_user_profile.md`：画像宽表可考虑 `PRIMARY KEY`/`UNIQUE KEY`

 ### 2. 分区与分桶

 - **分区 (PARTITION BY RANGE)**
   - 常按日期（天/月）或业务主维度进行范围分区
   - 便于冷热数据分层管理、快速删除历史分区
 - **分桶 (DISTRIBUTED BY HASH)**
   - 指定 HASH 列（如 `user_id`），并设置 BUCKETS 个数
   - 决定数据在各 BE 节点上的分布，影响并行度

 ---

 ## 三、数据类型与函数（简要）

 ### 1. 常用数据类型

 - 数值：`TINYINT`、`INT`、`BIGINT`、`LARGEINT`、`FLOAT`、`DOUBLE`、`DECIMAL`
 - 字符串：`CHAR`、`VARCHAR`
 - 日期时间：`DATE`、`DATETIME`

 ### 2. 常用函数（与 MySQL 类似）

 - 聚合：`COUNT()`、`SUM()`、`AVG()`、`MIN()`、`MAX()`、`NDV()` 等
 - 日期：`DATE_TRUNC()`、`DATE_ADD()`、`DATEDIFF()` 等
 - 字符串：`CONCAT()`、`SUBSTRING()`、`LOWER()`、`UPPER()` 等

 **对应案例：**
 - 所有案例 SQL 中都会用到聚合和日期函数，重点在于理解它们在 Doris 向量化执行上的高效性。

 ---

 ## 四、离线开发知识点（批处理）

 ### 1. 订单明细建模（DUPLICATE KEY）

 表：`orders_offline`

 - 列：订单 ID、用户 ID、下单日期、城市、金额、状态
 - 分区：按 `order_date` 范围分区（如按月）
 - 分桶：按 `user_id` HASH 分桶，提高并行度

 示例（简化版）：

 ```sql
 CREATE TABLE orders_offline (
     order_id    BIGINT,
     user_id     BIGINT,
     order_date  DATE,
     city        VARCHAR(32),
     amount      DECIMAL(16,2),
     status      VARCHAR(16)
 )
 DUPLICATE KEY(order_id, user_id)
 PARTITION BY RANGE (order_date) (
     PARTITION p202401 VALUES LESS THAN ('2024-02-01'),
     PARTITION p202402 VALUES LESS THAN ('2024-03-01'),
     PARTITION p202403 VALUES LESS THAN ('2024-04-01')
 )
 DISTRIBUTED BY HASH(user_id) BUCKETS 8
 PROPERTIES (
     "replication_num" = "1"
 );
 ```

 ### 2. 用户画像宽表建模

 表：`user_profile_offline`

 - 基于用户基础信息 + 订单事实聚合得到
 - 画像指标：累计订单数、累计金额、首单/末单日期、活跃天数、平均客单价等
 - 可选用：
   - `PRIMARY KEY(user_id)`：支持更新
   - 或 `UNIQUE KEY(user_id)`：简单覆盖

 **对应案例：**
 - `cases/offline_order_analysis.md`：离线订单统计  
 - `cases/offline_user_profile.md`：离线画像计算与写入

 ---

 ## 五、实时/近实时开发知识点

 ### 1. 实时明细表设计（DUPLICATE KEY）

 表：`events_realtime`

 - 字段：`event_time,user_id,event_type,page,device,os,network,duration`
 - 分区：按 `event_time` 范围分区（按天）
 - 分桶：按 `user_id` 或 `page` HASH

 ### 2. 导入方式

 - **Stream Load**
   - 通过 HTTP 接口直接上传本地文件或应用输出
   - 适合小批量实时/准实时导入
 - **Routine Load**
   - 持续从 Kafka 等 MQ 消费数据
   - 适合在线埋点流水场景

 ### 3. 物化视图实时聚合

 - 基于明细表创建物化视图，实现分钟级 PV/UV 聚合：

   ```sql
   CREATE MATERIALIZED VIEW mv_page_view_1min
   AS
   SELECT
       DATE_TRUNC('minute', event_time) AS ts_min,
       page,
       COUNT(*) AS pv,
       NDV(user_id) AS uv
   FROM events_realtime
   GROUP BY ts_min, page;
   ```

 **对应案例：**
 - `cases/realtime_event_agg.md` + `scripts/load_realtime_demo.sql`

 ---

 ## 六、性能优化与实践经验（概要）

 ### 1. 建模层面

 - 合理选择 Key 类型：明细用 DUPLICATE / 主键可变用 PRIMARY KEY
 - 合理设计分区粒度：按月/按天，结合数据量与保留周期
 - BUCKETS 数量与 BE 数量、并发需求匹配

 ### 2. 查询层面

 - 尽量命中物化视图，减少原表扫描
 - 避免 `SELECT *`，只查需要的字段
 - 利用分区裁剪：where 条件尽量包含分区字段

 ---

 ## 七、知识点与案例/数据对照表

 | 知识点模块      | 关键点                                      | 案例文档                    | 验证数据文件                         | 相关脚本                    |
 |-----------------|---------------------------------------------|-----------------------------|--------------------------------------|-----------------------------|
 | Doris 基础架构  | FE/BE 架构、MySQL 协议                    | `GUIDE.md`                  | -                                    | -                           |
 | DUPLICATE KEY   | 明细建模、分区/分桶                        | `offline_order_analysis.md` | `orders_offline.csv`                 | `setup_tables.sql`          |
 | 离线订单统计    | 日/城市维度聚合                            | `offline_order_analysis.md` | `orders_offline.csv`                 | `common_queries.sql`        |
 | 离线用户画像    | 画像宽表、聚合指标、主键模型              | `offline_user_profile.md`   | `orders_offline.csv`,`users_offline.csv` | `setup_tables.sql`          |
 | 实时埋点明细    | 日志表建模、Stream/Routine Load 思路       | `realtime_event_agg.md`     | `events_realtime.csv`                | `load_realtime_demo.sql`    |
 | 实时聚合 & MV   | 分钟级 PV/UV 物化视图、自动重写            | `realtime_event_agg.md`     | `events_realtime.csv`                | `setup_tables.sql`,`common_queries.sql` |

 ---

 ## 八、如何使用本模块学习

 1. 按 `GUIDE.md` 步骤搭建好 Doris 环境，创建数据库与表结构。
 2. 使用 `data/` 中的 CSV 数据，配合 `scripts/` 中的导入脚本将离线订单和实时埋点导入 Doris。
 3. 打开 `cases/` 下的三个案例文档，对照 `common_queries.sql` 实际执行查询并观察结果。
 4. 在理解示例的基础上，尝试：
    - 根据自身业务增加字段与索引设计；
    - 新建一个基于 AGGREGATE KEY 的日指标表；
    - 新增一个物化视图并观察查询是否自动命中。

 当你能够：

 - 为不同业务选择合适的 Doris 表模型；
 - 为离线和实时场景分别设计合理的分区/分桶策略；
 - 搭建一个从埋点明细 → 物化视图 → 实时分析的简单链路；

 基本就具备了在实际项目中使用 Doris 搭建离线 + 实时一体化数仓的能力。

