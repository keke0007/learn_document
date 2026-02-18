## 📚 项目概述

本指南在 `elasticsearch/` 目录下，参考 `hive/`、`clickhouse/`、`doris/`、`oracle/`、`PostgreSQL/`、`mongoDB/` 模块的组织方式，提供一套系统的 **Elasticsearch 学习路径**，重点覆盖：

- **核心知识点**：索引与文档、倒排索引、映射（Mapping）、分词与分析器、查询 DSL、聚合（Aggregations）、分页与排序、简单调优。
- **案例场景**：商品搜索、日志检索与聚合分析、用户行为搜索。
- **验证数据**：小规模 JSON/JSONL 示例数据（商品、日志、用户行为），方便在本地 ES 集群中动手练习。

---

## 📁 项目结构

```
elasticsearch/
├── README.md                        # Elasticsearch 知识点总览（详细文档）
├── GUIDE.md                         # 本指南文档（学习路径 + 快速上手）
├── cases/                           # 实战案例目录
│   ├── basic_search.md              # 案例1：基础全文检索与过滤
│   ├── ecommerce_search.md          # 案例2：电商商品搜索与聚合分析
│   └── log_analysis.md              # 案例3：日志检索与聚合分析
├── data/                            # 验证数据（JSON/JSONL）
│   ├── products.jsonl               # 商品数据（约10条）
│   ├── logs.jsonl                   # 应用日志数据（约15条）
│   └── users.jsonl                  # 用户行为数据（约10条）
└── scripts/                         # REST/cURL 脚本示例
    ├── setup_indices.sh             # 创建索引与映射
    ├── load_data.sh                 # 使用 _bulk 导入示例数据
    └── common_queries.sh            # 常用查询与聚合示例
```

---

## 🎯 学习路径（建议 3~5 天）

### 阶段一：基础入门（0.5~1 天）

- 了解 Cluster / Node / Index / Shard / Replica 等核心概念。
- 熟悉 REST API 调用方式（curl 或 Kibana Dev Tools）。

### 阶段二：索引、映射与分词（1 天）

- 掌握索引与 Mapping 的基础配置。
- 理解 `text` / `keyword` 字段的差异与使用场景。
- 设计商品索引字段与类型（案例2）。

### 阶段三：查询 DSL 与聚合（1~2 天）

- 掌握 `match` / `term` / `bool` / `range` 等查询。
- 使用 Aggregations 完成按品牌/类别/价格区间的统计（案例2）。

### 阶段四：日志分析与简单调优（0.5~1 天）

- 建模日志索引（时间字段、级别、服务名等）。
- 使用 `date_histogram` + `terms` 做日志趋势和错误统计（案例3）。

---

## 🚀 快速开始

> 假设 Elasticsearch 运行在 `http://localhost:9200`。

1. 执行 `scripts/setup_indices.sh` 创建索引与映射。
2. 执行 `scripts/load_data.sh` 通过 `_bulk` 导入 `data/` 下的示例数据。
3. 执行 `scripts/common_queries.sh` 或将其中的请求复制到 Kibana Dev Tools 中运行。

---

## 📖 核心知识点速查

- **映射（Mapping）**：决定字段类型和分析方式（`text`/`keyword`/`date` 等）。
- **查询 DSL**：用 JSON 描述的查询语法，核心是 `query` + 可选的 `aggs`。
- **聚合（Aggregations）**：用于统计分析，常见有 `terms`、`date_histogram`、`avg`、`sum` 等。

---

## 📊 验证数据说明

- `products.jsonl`：商品文档（包含 `name`、`category`、`brand`、`price` 等字段）。
- `logs.jsonl`：日志文档（包含 `ts`、`level`、`service`、`message` 等字段）。
- `users.jsonl`：可扩展用于行为分析的用户事件数据。

---

## 🔧 实战案例概览

- **basic_search.md**：从最简单的全文检索与过滤入手，熟悉查询 DSL。
- **ecommerce_search.md**：构建带筛选和聚合的电商搜索场景。
- **log_analysis.md**：基于时间和服务维度的日志聚合分析。

---

## ✅ 学习检查清单

- [ ] 能够创建索引并配置基本映射。
- [ ] 能够使用查询 DSL 完成常见检索与过滤。
- [ ] 能够编写简单聚合查询完成统计分析。

---

## 🎓 学习成果

完成本指南后，你将能够：

- 使用 Elasticsearch 为搜索场景设计索引与查询。
- 通过聚合完成商品与日志的基础统计分析。
- 结合其他大数据组件，在项目中引入 Elasticsearch 作为搜索与分析引擎。

