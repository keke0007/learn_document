# Elasticsearch 学习总览

`elasticsearch/` 模块整理了 Elasticsearch 在搜索与日志分析中的主要知识点，并将它们与 `cases/` + `data/` + `scripts/` 中的案例和验证数据对应起来。

---

## 一、核心概念与对象

- **Index**：逻辑索引，类似关系型数据库的“表”。
- **Document**：JSON 文档，一条记录。
- **Field**：文档中的字段。
- **Shard / Replica**：分片与副本，用于扩展性与高可用。

对应案例：`GUIDE.md`、`cases/basic_search.md`

---

## 二、字段类型与映射

- 字段类型：`text`、`keyword`、`integer`、`float`、`boolean`、`date` 等。
- 常见模式：一个字段同时定义为 `text` + `keyword`，既支持全文搜索又支持聚合/排序。

对应案例：`cases/ecommerce_search.md`

---

## 三、查询 DSL 与聚合

- 查询：
  - 全文：`match`、`multi_match`
  - 精确：`term`、`terms`
  - 组合：`bool`（`must` / `should` / `filter`）
  - 范围：`range`
- 聚合：
  - 桶聚合：`terms`、`date_histogram`
  - 度量聚合：`sum`、`avg`、`max`、`min`

对应案例：
- `cases/basic_search.md`
- `cases/ecommerce_search.md`
- `cases/log_analysis.md`

---

## 四、知识点与案例/数据对照表

| 模块             | 关键知识点                   | 案例文档                 | 数据文件               | 脚本文件                 |
|------------------|------------------------------|--------------------------|------------------------|--------------------------|
| 基础搜索         | 索引/文档、match/term 查询   | `basic_search.md`        | `products.jsonl`       | `setup_indices.sh`,`common_queries.sh` |
| 电商搜索与聚合   | 过滤、排序、terms/avg 聚合   | `ecommerce_search.md`    | `products.jsonl`       | `load_data.sh`,`common_queries.sh`     |
| 日志分析         | date_histogram、按服务聚合   | `log_analysis.md`        | `logs.jsonl`           | 同上                      |

---

## 五、如何使用本模块学习

1. 阅读 `GUIDE.md`，了解整体学习路径。
2. 按 `scripts/setup_indices.sh` 创建索引与映射。
3. 按 `scripts/load_data.sh` 导入 `data/` 下的 JSONL 示例数据。
4. 对照 `cases/` 文档和 `scripts/common_queries.sh` 中的请求，在 Kibana Dev Tools 或命令行中实际执行。

当你能：

- 为简单商品与日志场景设计合适的映射；
- 熟练编写查询 DSL 和基础聚合；

基本就具备了在项目中使用 Elasticsearch 的核心能力。

