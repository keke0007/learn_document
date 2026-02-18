# HBase 学习总览

`hbase/` 模块整理了 HBase 在列族存储与大表场景中的主要知识点，并将它们与 `cases/` + `data/` + `scripts/` 中的案例和验证数据对应起来。

---

## 一、核心知识点概览

- 数据模型：RowKey / Column Family / Column Qualifier / Timestamp / Cell。
- 表与 Region：Region 切分、热点问题简单概念。
- RowKey 设计：前缀与散列、时间序列 RowKey。
- 基本操作：Put / Get / Scan / Delete（HBase shell）。

---

## 二、知识点与案例/数据对照表

| 模块                   | 关键知识点                        | 案例文档                      | 数据文件         | 脚本文件                       |
|------------------------|-----------------------------------|-------------------------------|------------------|--------------------------------|
| 基础数据模型与操作     | RowKey、列族、Put/Get/Scan       | `basic_datamodel.md`         | `users.tsv`      | `create_tables.hbase`,`common_commands.hbase` |
| 用户画像宽表           | RowKey 设计、宽表、多列族        | `user_profile_table.md`      | `users.tsv`      | 同上                           |
| 订单/日志时间序列表    | 时间序 RowKey、Scan 范围         | `order_timeseries_table.md`  | `orders.tsv`     | 同上                           |

---

## 三、如何使用本模块学习

1. 阅读 `GUIDE.md` 了解 HBase 的基本概念与学习路径。
2. 在 HBase shell 中执行 `scripts/create_tables.hbase` 创建示例表。
3. 参考 `cases/` 文档与 `scripts/common_commands.hbase` 中的命令，对 `data/` 中的 TSV 数据进行映射与操作（可通过 ImportTsv 或外部程序写入）。

当你能够：

- 熟练使用 HBase shell 进行基本数据操作；
- 为用户与订单等业务设计合理的 RowKey 与列族；

就基本具备了在项目中使用 HBase 的核心能力。

