 # Doris 学习指南（离线 & 实时）

 ## 📚 项目概述

 本指南在 `doris/` 目录下，参考 `hive/` 与 `clickhouse/` 模块的组织方式，提供 **大数据离线批处理 + 实时分析** 的 Doris 学习路径，包括：

 - **核心知识点**：Doris 架构、FE/BE、存储模型（Duplicate / Aggregate / Unique / Primary Key）、分区 & 分桶、物化视图、导入方式等  
 - **离线场景案例**：T+1 订单宽表统计、用户画像离线计算  
 - **实时场景案例**：实时埋点明细 + 近实时聚合分析（Routine Load / Stream Load 思路）  
 - **验证数据**：小规模 CSV 示例数据，方便本地或测试集群快速演练

 ---

 ## 📁 项目结构

 ```
 doris/
 ├── README.md                     # Doris 知识点总览（详细文档）
 ├── GUIDE.md                      # 本指南文档（快速入门 + 学习路径）
 ├── cases/                        # 实战案例目录
 │   ├── offline_order_analysis.md # 案例1：离线订单统计分析
 │   ├── offline_user_profile.md   # 案例2：离线用户画像宽表
 │   └── realtime_event_agg.md     # 案例3：实时埋点明细与聚合分析
 ├── data/                         # 验证数据目录（CSV）
 │   ├── orders_offline.csv        # 离线订单数据（约15条）
 │   ├── users_offline.csv         # 用户基础信息（约8条）
 │   └── events_realtime.csv       # 模拟实时埋点数据（约20条）
 └── scripts/                      # SQL / 工具脚本目录
     ├── setup_tables.sql          # 建表脚本：一键创建所有表
     ├── load_offline_data.sql     # 离线场景数据导入（Broker/Stream Load 示例）
     ├── load_realtime_demo.sql    # 实时场景模拟导入（Stream Load 示例）
     └── common_queries.sql        # 常用查询示例（批 + 实时）
 ```

 ---

 ## 🎯 学习路径（建议 5~7 天）

 ### 阶段一：基础知识（1 天）

 1. **Doris 基本概念**
    - Doris 是什么，适用场景（MPP OLAP、实时数仓、明细 + 多维分析）
    - 与 Hive/Spark/ClickHouse 的对比：  
      - Hive：离线批处理，延迟分钟级 ~ 小时级  
      - Doris：在线/近实时分析，延迟秒级，支持高并发查询  
    - 行列混合存储架构、向量化执行

 2. **核心组件与架构**
    - FE（Frontend）：元数据管理、查询解析与优化  
    - BE（Backend）：数据存储与执行引擎  
    - Broker（可选）：HDFS/对象存储访问

 3. **基本操作**
    - 使用 MySQL 客户端连接 Doris：`mysql -h fe_host -P9030 -uroot`  
    - 创建/删除数据库与表  
    - 基本查询：`SELECT / WHERE / ORDER BY / GROUP BY / LIMIT`

 ### 阶段二：存储模型与数据建模（2 天）

 1. **表模型（Key 类型）**
    - `DUPLICATE KEY`：明细表（不做聚合，保留原始行）
    - `AGGREGATE KEY`：按 Key 聚合数值列（适合指标汇总表）
    - `UNIQUE KEY`：基于 Key 覆盖更新（早期语义）
    - `PRIMARY KEY`：支持主键更新（新版本推荐）

 2. **分区 & 分桶**
    - 分区：`PARTITION BY RANGE (date_col)`，常用按天/按月  
    - 分桶：`DISTRIBUTED BY HASH (user_id) BUCKETS 10` 等

 3. **物化视图（Materialized View）**
    - 基于明细表自动生成聚合/宽表，提升复杂查询性能  
    - 常见场景：按时间 & 维度聚合 PV/UV、订单指标

 ### 阶段三：离线分析场景（1~2 天）

 1. **离线订单统计（案例1）**
    - 从 `orders_offline.csv` + `users_offline.csv` 导入 Doris  
    - 典型指标：
      - 每日订单量、订单金额  
      - 用户维度的累计订单数、累计金额  
      - 按城市/渠道/设备的订单指标

 2. **离线用户画像（案例2）**
    - 基于订单 + 用户信息构建画像宽表：  
      - 累计订单数、累计消费金额  
      - 首单日期、最近下单日期  
      - 平均客单价、活跃天数

 ### 阶段四：实时分析场景（1~2 天）

 1. **实时埋点明细（案例3）**
    - 以 `events_realtime.csv` 模拟实时行为日志：  
      - `event_time, user_id, event_type, page, device, os, network, duration`
    - 表模型选型：`DUPLICATE KEY` 明细表

 2. **近实时聚合 + 物化视图**
    - 按分钟/小时维度聚合 PV/UV  
    - 按页面/事件类型统计访问量、停留时长  
    - 使用物化视图减少扫描与聚合开销

 ---

 ## 🚀 快速开始

 ### 前置要求

 - 已安装 Doris 集群（本地或测试环境）
   - 至少 1 FE + 1 BE
 - 可通过 MySQL 客户端或 Doris 自带 `mysql-client` 连接

 ### 步骤1：创建数据库

 ```sql
 CREATE DATABASE IF NOT EXISTS bigdata_demo;
 USE bigdata_demo;
 ```

 ### 步骤2：执行建表脚本

 ```sql
 -- 在 MySQL 客户端中执行脚本内容（拷贝粘贴或 source）
 SOURCE /absolute/path/to/doris/scripts/setup_tables.sql;
 ```

 或者手动执行 `scripts/setup_tables.sql` 中的建表 SQL。

 ### 步骤3：加载离线数据

 这里用 **Stream Load 思路** 示例（实际参数请根据你的 Doris 版本与环境调整）：

 ```bash
 # orders_offline
 curl --location-trusted -u user:password \
   -H "label:orders_offline_1" \
   -H "column_separator:," \
   -T /absolute/path/to/doris/data/orders_offline.csv \
   http://fe_host:8030/api/bigdata_demo/orders_offline/_stream_load

 # users_offline
 curl --location-trusted -u user:password \
   -H "label:users_offline_1" \
   -H "column_separator:," \
   -T /absolute/path/to/doris/data/users_offline.csv \
   http://fe_host:8030/api/bigdata_demo/users_offline/_stream_load
 ```

 或参考 `scripts/load_offline_data.sql` 中的说明，改用 Broker Load 方式。

 ### 步骤4：模拟实时数据导入

 ```bash
 curl --location-trusted -u user:password \
   -H "label:events_realtime_1" \
   -H "column_separator:," \
   -T /absolute/path/to/doris/data/events_realtime.csv \
   http://fe_host:8030/api/bigdata_demo/events_realtime/_stream_load
 ```

 > 在生产中，推荐通过 **Routine Load + Kafka** 实现真正的实时流式导入。

 ### 步骤5：验证数据

 ```sql
 USE bigdata_demo;

 -- 查看离线订单明细
 SELECT * FROM orders_offline LIMIT 10;

 -- 查看实时事件明细
 SELECT * FROM events_realtime LIMIT 10;

 -- 快速统计
 SELECT COUNT(*) FROM orders_offline;
 SELECT COUNT(*) FROM events_realtime;
 ```

 ---

 ## 📖 核心知识点速查

 ### 1. Doris 表模型（Key Type）

 | Key 类型 | 说明 | 典型用途 |
 |----------|------|----------|
 | DUPLICATE KEY | 不做聚合，保留重复行 | 行级明细表（日志、订单明细） |
 | AGGREGATE KEY | 同 Key 的聚合列按聚合函数合并 | 指标汇总表（累计 UV、金额） |
 | UNIQUE KEY | 按 Key 覆盖更新 | 早期更新场景（逐步被 Primary Key 替代） |
 | PRIMARY KEY | 主键模型，支持更新 | 维度表、可变更明细表 |

 ### 2. 分区 & 分桶

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

 关注三点：
 - **Key 列**：决定聚合/去重/更新语义  
 - **PARTITION BY**：按时间或业务维度分区，控制冷热数据与管理  
 - **DISTRIBUTED BY HASH**：控制数据在 BE 之间的分布，提高并行度

 ### 3. 物化视图（Materialized View）示例

 ```sql
 CREATE MATERIALIZED VIEW mv_orders_day_city
 AS
 SELECT
     order_date,
     city,
     COUNT(*)    AS order_cnt,
     SUM(amount) AS total_amount
 FROM orders_offline
 GROUP BY order_date, city;
 ```

 查询时：

 ```sql
 SELECT
     order_date,
     city,
     order_cnt,
     total_amount
 FROM orders_offline
 WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31';
 ```

 Doris 查询优化器会自动优选物化视图，降低扫描与聚合成本（需满足匹配条件）。

 ### 4. 常见导入方式（了解）

 - **Stream Load**：HTTP 协议上传本地/应用端的数据，适合小批量或实时近实时导入。
 - **Broker Load**：从 HDFS / 对象存储批量导入（适合大批量离线数据）。
 - **Routine Load**：持续从 Kafka 等消息队列消费数据，适合实时流水。

 ---

 ## 📊 验证数据说明

 ### 数据文件清单

 | 文件名 | 记录数（约） | 用途 | 案例 |
 |--------|--------------|------|------|
 | `orders_offline.csv`  | 15   | 离线订单明细 | 案例1 |
 | `users_offline.csv`   | 8    | 用户基础信息 | 案例1&2 |
 | `events_realtime.csv` | 20   | 模拟实时行为日志 | 案例3 |

 ### 字段示例

 - **orders_offline.csv**：`order_id,user_id,order_date,city,amount,status`  
 - **users_offline.csv**：`user_id,user_name,gender,age,city,register_date`  
 - **events_realtime.csv**：`event_time,user_id,event_type,page,device,os,network,duration`

 所有文件均使用 **CSV 格式**，字段分隔符为 **逗号（,）**。

 ---

 ## 🔧 实战案例概览

 ### 案例1：离线订单统计分析

 **学习目标**：掌握 Doris 在离线批量分析中的基本用法  
 **涉及知识点**：
 - DUPLICATE KEY 表建模  
 - 分区/分桶设计  
 - 批量导入 CSV 数据  
 - 按天/城市/用户维度的聚合统计  

 ### 案例2：离线用户画像宽表

 **学习目标**：基于订单 + 用户信息构建离线画像宽表  
 **涉及知识点**：
 - JOIN 关联  
 - 画像指标计算（累计订单、金额、首末单时间等）  
 - 画像宽表设计（可选择 PRIMARY KEY/UNIQUE KEY）

 ### 案例3：实时埋点与聚合分析

 **学习目标**：理解 Doris 在实时/近实时分析中的典型模式  
 **涉及知识点**：
 - 明细表建模  
 - Stream Load / Routine Load 导入思路  
 - 物化视图聚合  
 - 近实时多维查询（时间 + 页面 + 事件类型）

 ---

 ## 📝 学习建议

 ### 针对有 Hive/Spark/ClickHouse 基础的同学

 1. 把 Doris 当作 **支持实时导入 + 高并发查询的 MPP OLAP 引擎** 来理解。  
 2. 优先掌握：表模型（Key Type）+ 分区分桶 + 物化视图 + 导入方式。  
 3. 对比 Hive/ClickHouse：同样的离线 & 实时场景在 Doris 中如何改写与提速。

 ### 实践路线

 1. 完成 `scripts/setup_tables.sql` + 离线数据导入，跑通订单统计与画像计算。  
 2. 再完成实时埋点导入 + 物化视图相关查询，体验 Doris 的近实时分析能力。  
 3. 最后根据自己的业务，尝试设计 **一个真实的 Doris 明细表 + 一个聚合视图或宽表**。

 ---

 ## ✅ 学习检查清单

 ### 基础能力
 - [ ] 能够搭建并连接 Doris 集群  
 - [ ] 能够创建数据库和带分区/分桶的表  
 - [ ] 能够使用 Stream Load 或 Broker Load 导入 CSV 数据  

 ### 离线分析
 - [ ] 能够完成离线订单统计案例  
 - [ ] 能够基于用户 + 订单构建离线画像宽表  

 ### 实时分析
 - [ ] 能够创建实时事件明细表  
 - [ ] 能够基于物化视图构建分钟级 PV/UV 指标  
 - [ ] 能够查询最近 N 分钟/小时的实时指标

 ---

 ## 🎓 学习成果

 完成本指南后，你将能够：

 - ✅ 理解 Doris 在大数据离线与实时数仓中的定位与优势  
 - ✅ 基于不同 Key 类型设计适合的明细表与宽表  
 - ✅ 搭建小型离线 + 实时一体化分析场景（订单 & 行为日志）  
 - ✅ 为真实业务设计 Doris 数仓层的建模与导入方案

 **祝你 Doris 学习顺利！🚀**

