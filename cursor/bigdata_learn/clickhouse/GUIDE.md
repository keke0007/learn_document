 # ClickHouse 学习指南（离线 & 实时）

 ## 📚 项目概述

 本指南在 `clickhouse/` 目录下，参考 `hive/` 模块的组织方式，提供 **大数据离线批处理 + 实时分析** 的 ClickHouse 学习路径，包括：

 - **核心知识点**：ClickHouse 基础、表引擎、分布式与分片、副本、物化视图等  
 - **离线场景案例**：T+1 订单宽表统计、用户画像指标离线计算  
 - **实时场景案例**：实时埋点明细入库 + 近实时多维聚合查询  
 - **验证数据**：小规模 CSV 示例数据，方便本地或单机集群快速演练

 ---

 ## 📁 项目结构

```
clickhouse/
├── README.md                     # ClickHouse 知识点总览（详细文档）
├── GUIDE.md                      # 本指南文档（快速入门 + 学习路径）
├── cases/                        # 实战案例目录
│   ├── offline_order_analysis.md # 案例1：离线订单统计分析
│   ├── offline_user_profile.md   # 案例2：离线用户画像指标
│   └── realtime_event_agg.md     # 案例3：实时埋点明细与聚合分析
├── data/                         # 验证数据目录（CSV）
│   ├── orders_offline.csv        # 离线订单数据（约15条）
│   ├── users_offline.csv         # 用户基础信息（约8条）
│   └── events_realtime.csv       # 模拟实时埋点数据（约20条）
└── scripts/                      # SQL / 工具脚本目录
    ├── setup_tables.sql          # 建表脚本：一键创建所有表
    ├── load_offline_data.sql     # 离线场景数据加载
    ├── load_realtime_demo.sql    # 实时场景模拟加载
    └── common_queries.sql        # 常用查询示例（批 + 实时）
```

 ---

 ## 🎯 学习路径（建议 5~7 天）

 ### 阶段一：基础知识（1 天）

 1. **ClickHouse 基本概念**
    - ClickHouse 是什么，适用场景（OLAP，明细 + 多维分析）
    - 与 Hive/Spark 的对比：  
      - Hive：离线批处理，延迟分钟级 ~ 小时级  
      - ClickHouse：实时/近实时分析，延迟秒级  
    - 列式存储 + 向量化执行 + 压缩

 2. **核心组件与架构**
    - Server、Database、Table 的层次结构  
    - MergeTree 系列表引擎的作用  
    - 分片（Shard）与副本（Replica）概念（可先理解单机）

 3. **基础 SQL 使用**
    - 创建/删除数据库与表  
    - 基本查询：`SELECT / WHERE / ORDER BY / GROUP BY / LIMIT`  

 ### 阶段二：表引擎与数据建模（2 天）

 1. **MergeTree 家族**
    - `MergeTree` / `ReplicatedMergeTree`  
    - 主键（PRIMARY KEY）与排序键（ORDER BY）  
    - 分区键（PARTITION BY）：按日期或业务维度

 2. **典型场景建模**
    - 明细事实表：订单明细、行为日志  
    - 维度表：用户信息、产品信息（可使用 `MergeTree` 或 `ReplacingMergeTree`）

 3. **物化视图（Materialized View）**
    - 基于明细流自动生成聚合结果表  
    - 用于实时指标汇总（UV、PV、订单金额汇总等）

 ### 阶段三：离线分析场景（1~2 天）

 1. **离线订单统计（案例1）**
    - 从 `orders_offline.csv` + `users_offline.csv` 加载数据  
    - 典型指标：
      - 每日订单量、金额统计  
      - 用户维度的累计订单数、累计金额  
      - 分城市/渠道/设备的订单指标

 2. **离线用户画像（案例2）**
    - 结合订单 & 用户信息构建简单画像：  
      - 平均客单价、活跃天数、最近一次下单时间  
    - 将结果写入宽表，供下游使用

 ### 阶段四：实时分析场景（1~2 天）

 1. **实时埋点入库（案例3）**
    - 以 `events_realtime.csv` 模拟实时行为日志：  
      - 字段如：`event_time, user_id, event_type, page, device, os, network, duration`  
    - 明细表使用 `MergeTree`（或 `ReplacingMergeTree`）

 2. **实时聚合 + 物化视图**
    - 按分钟/小时维度聚合 PV/UV  
    - 按页面/事件类型统计访问量、停留时长  
    - 使用物化视图自动维护聚合结果

 ---

 ## 🚀 快速开始

 ### 前置要求

 - 已安装 ClickHouse（本地或测试环境），例如：  
   - `clickhouse-server`  
   - `clickhouse-client`

 ### 步骤1：创建数据库

 ```sql
 CREATE DATABASE IF NOT EXISTS bigdata_demo;
 USE bigdata_demo;
 ```

 ### 步骤2：执行建表脚本

 ```bash
 # 在服务器上执行
 clickhouse-client --multiquery < scripts/setup_tables.sql
 ```

 或者在 `clickhouse-client` 中逐条执行脚本中的 SQL。

 ### 步骤3：加载离线数据

 ```bash
 # 修改 load_offline_data.sql 中的本地路径
 clickhouse-client --multiquery < scripts/load_offline_data.sql
 ```

 或手动执行：

 ```sql
 -- 注意修改为实际路径
 INSERT INTO orders_offline FORMAT CSV
 INFILE '/path/to/clickhouse/data/orders_offline.csv';
 ```

 ### 步骤4：模拟实时数据加载

 ```bash
 # 示例：使用 clickhouse-client 循环导入 CSV 中的多行
 clickhouse-client --multiquery < scripts/load_realtime_demo.sql
 ```

 或编写简单脚本（如 Python/Kafka Producer）将事件流写入实时表。

 ### 步骤5：验证数据

 ```sql
 -- 查看离线订单明细
 SELECT * FROM orders_offline LIMIT 10;

 -- 查看实时事件明细
 SELECT * FROM events_realtime LIMIT 10;

 -- 快速统计
 SELECT count() FROM orders_offline;
 SELECT count() FROM events_realtime;
 ```

 ---

 ## 📖 核心知识点速查

 ### 1. 表引擎（Table Engine）

 | 引擎 | 说明 | 典型用途 |
 |------|------|----------|
 | `MergeTree` | 基础列式存储引擎，支持分区/排序/索引 | 明细事实表、离线明细 |
 | `ReplacingMergeTree` | 支持按主键去重/覆盖 | 有更新需求的事实表或维度表 |
 | `SummingMergeTree` | 自动在后台合并时累加数值列 | 累积指标（计数、金额） |
 | `AggregatingMergeTree` | 存储聚合状态 | 高级预聚合场景 |
 | `Distributed` | 分布式路由层 | 多分片集群时做路由与汇总 |

 ### 2. MergeTree 关键语法

 ```sql
 CREATE TABLE orders_offline (
     order_id      UInt32,
     user_id       UInt32,
     order_date    Date,
     city          String,
     amount        Float64,
     status        String
 )
 ENGINE = MergeTree
 PARTITION BY toYYYYMM(order_date)
 ORDER BY (order_date, user_id)
 SETTINGS index_granularity = 8192;
 ```

 关注三点：
 - **PARTITION BY**：减少扫描范围（如按月/天分区）  
 - **ORDER BY**：决定主键和数据物理排序，影响查询性能  
 - **数据类型**：优先使用 `UIntXX/IntXX/Date/DateTime` 等基础类型

 ### 3. 物化视图（Materialized View）

 ```sql
 CREATE TABLE page_view_1min (
     ts_min    DateTime,
     page      String,
     pv        UInt64,
     uv        UInt64
 ) ENGINE = SummingMergeTree()
 PARTITION BY toYYYYMMDD(ts_min)
 ORDER BY (ts_min, page);

 CREATE MATERIALIZED VIEW mv_page_view_1min
 TO page_view_1min
 AS
 SELECT
     toStartOfMinute(event_time) AS ts_min,
     page,
     count() AS pv,
     uniqExact(user_id) AS uv
 FROM events_realtime
 GROUP BY ts_min, page;
 ```

 - 明细表 `events_realtime` 不断写入  
 - 物化视图自动将新数据按分钟聚合写入 `page_view_1min`

 ### 4. 实时 & 离线查询示例

 ```sql
 -- 离线：按天统计订单金额
 SELECT
     order_date,
     count() AS order_cnt,
     sum(amount) AS total_amount
 FROM orders_offline
 GROUP BY order_date
 ORDER BY order_date;

 -- 实时：查询最近 30 分钟的 PV/UV
 SELECT
     ts_min,
     page,
     pv,
     uv
 FROM page_view_1min
 WHERE ts_min >= now() - INTERVAL 30 MINUTE
 ORDER BY ts_min, page;
 ```

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

 **学习目标**：掌握 ClickHouse 在离线批量分析中的基本用法  
 **涉及知识点**：
 - MergeTree 表建模  
 - 批量导入 CSV 数据  
 - 按天/城市/用户维度的聚合统计  

 ### 案例2：离线用户画像指标

 **学习目标**：基于订单 + 用户信息构建简单画像  
 **涉及知识点**：
 - 关联查询（JOIN）  
 - 窗口函数（如 `row_number`、`lag`）  
 - 写入画像宽表，支持下游查询

 ### 案例3：实时埋点与聚合分析

 **学习目标**：构建实时明细 + 物化视图聚合的通用模式  
 **涉及知识点**：
 - 实时写入明细表  
 - 物化视图自动聚合  
 - 近实时多维查询（时间 + 页面 + 事件类型）

 ---

 ## 📝 学习建议

 ### 针对有 Hive/Spark 基础的同学

 1. 把 ClickHouse 当作 **低延迟的列式 OLAP 引擎** 来理解  
 2. 优先掌握：MergeTree 建模 + 物化视图 + 基础 SQL  
 3. 对比 Hive：同样的场景在 ClickHouse 中如何改写/提升性能

 ### 实践路线

 1. 完成 `scripts/setup_tables.sql` + `load_offline_data.sql`，验证离线查询结果  
 2. 再完成 `load_realtime_demo.sql` + 物化视图相关查询，体验“写入即查询”的效果  
 3. 最后根据自己的业务，尝试设计 **一个真实的离线指标表 + 一个实时指标表**

 ---

 ## ✅ 学习检查清单

 ### 基础能力
 - [ ] 能够安装并启动 ClickHouse 服务  
 - [ ] 能够创建数据库和 MergeTree 表  
 - [ ] 能够导入 CSV 文件到表中  

 ### 离线分析
 - [ ] 能够完成离线订单统计案例  
 - [ ] 能够基于用户 + 订单构建简单画像  

 ### 实时分析
 - [ ] 能够创建实时事件明细表  
 - [ ] 能够基于物化视图构建分钟级 PV/UV 指标  
 - [ ] 能够查询最近 N 分钟/小时的实时指标

 ---

 ## 🎓 学习成果

 完成本指南后，你将能够：

 - ✅ 理解 ClickHouse 在大数据离线与实时分析中的定位与优势  
 - ✅ 基于 MergeTree 系列表引擎设计适合的表结构  
 - ✅ 搭建小型离线 + 实时一体化分析场景（订单 & 行为日志）  
 - ✅ 为真实业务设计 ClickHouse 数仓层的明细表和宽表

 **祝你 ClickHouse 学习顺利！🚀**

