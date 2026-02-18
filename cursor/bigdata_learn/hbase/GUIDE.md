## HBase 学习指南（NoSQL 列族存储）

## 📚 项目概述

本指南在 `hbase/` 目录下，参考 `hive/`、`clickhouse/`、`doris/`、`redis/`、`influxDB/` 等模块的组织方式，提供一套系统的 **HBase 学习路径**，重点覆盖：

- **核心知识点**：数据模型（RowKey / Column Family / Column / Version）、Region 与分布式存储、RowKey 设计、基本读写与 Scan、与 Hadoop/Hive 集成简要概念。
- **案例场景**：用户画像宽表、订单明细行存储、时间序列日志表。
- **验证数据**：小规模 CSV/TSV 示例数据，方便在本地或测试 HBase 集群中动手练习。

---

## 📁 项目结构

```
hbase/
├── README.md                         # HBase 知识点总览（详细文档）
├── GUIDE.md                          # 本指南文档（学习路径 + 快速上手）
├── cases/                            # 实战案例目录
│   ├── basic_datamodel.md            # 案例1：基础数据模型与表设计
│   ├── user_profile_table.md         # 案例2：用户画像宽表（RowKey 设计）
│   └── order_timeseries_table.md     # 案例3：订单/日志时间序列表
├── data/                             # 验证数据（CSV/TSV）
│   ├── users.tsv                     # 用户信息示例
│   └── orders.tsv                    # 订单明细示例
└── scripts/                          # HBase shell 示例脚本（示意）
    ├── create_tables.hbase           # 建表示例
    ├── load_data_notes.md            # 数据加载说明（HBase shell / ImportTsv）
    └── common_commands.hbase         # 常用增删改查命令示例
```

---

## 🎯 学习路径（建议 2~3 天）

### 阶段一：基础概念（0.5 天）

- HBase 架构：HRegionServer、HMaster、ZooKeeper、HDFS 存储。
- 数据模型：RowKey、Column Family、Column Qualifier、Timestamp、Cell。

### 阶段二：表设计与 RowKey 设计（1 天）

- 宽表理念：列族设计（如 `info`、`stat` 等）。
- RowKey 设计原则：前缀热点、散列前缀、时间倒序等。
- 基于用户与订单两个场景进行表设计（案例2、案例3）。

### 阶段三：基本操作与集成（1~1.5 天）

- 使用 HBase shell 完成建表、Put、Get、Scan 与 Delete（案例1）。
- 简要了解与 MapReduce/Hive 的集成方式（如 Hive 外表映射 HBase 表）。

---

## 🚀 快速开始

> 以下示例假定你已有本地或测试 HBase 集群，并可通过 `hbase shell` 连接。

### 步骤1：进入 HBase shell

```bash
hbase shell
```

### 步骤2：创建示例表（也可参考 `scripts/create_tables.hbase`）

```ruby
create 'user_profile', { NAME => 'info', VERSIONS => 1 }, { NAME => 'stat', VERSIONS => 1 }
create 'orders', { NAME => 'd', VERSIONS => 1 }
```

### 步骤3：写入与查询示例

```ruby
put 'user_profile', 'u_0001', 'info:name', '张三'
put 'user_profile', 'u_0001', 'info:city', '北京'
get 'user_profile', 'u_0001'

scan 'user_profile', { STARTROW => 'u_0001', STOPROW => 'u_0009' }
```

---

## 📖 核心知识点速查

- **RowKey**：按字典序排序，决定数据在 Region 上的分布与 Scan 范围。
- **列族（Column Family）**：物理存储单位，同一列族中的列在 HFile 上聚集存储。
- **版本**：同一 Cell 不同时间戳可保留多版本（默认 1）。

---

## 📊 验证数据说明

- `data/users.tsv`：简单用户信息（`user_id\tname\tcity`），用于构建 `user_profile` 表的数据来源。
- `data/orders.tsv`：订单明细（`order_id\tuser_id\torder_time\tamount`），用于构建时间序列表或按用户聚合的订单表。

---

## 🔧 实战案例概览

- `basic_datamodel.md`：通过小表示例理解 RowKey、列族与列限定符。
- `user_profile_table.md`：以 `user_id` 为 RowKey 设计用户画像宽表，将多维信息存入不同列族/列。
- `order_timeseries_table.md`：以时间维度（如 `user_id#timestamp`）设计订单/日志时间序列表。

---

## ✅ 学习检查清单

- [ ] 能够使用 HBase shell 创建表、插入与查询数据。
- [ ] 理解 RowKey 设计对热点与 Scan 性能的影响。
- [ ] 能为用户/订单等常见业务设计基本合理的 HBase 表。

---

## 🎓 学习成果

完成本指南后，你将能够：

- 理解 HBase 在大数据生态中（与 Hadoop/Hive/Spark 协同）的角色。
- 使用 HBase 存储与查询宽表或时间序列型业务数据。
- 为需要随机读写、大表存储的场景设计初步可用的 HBase 表结构。

