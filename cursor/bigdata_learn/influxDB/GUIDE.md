## InfluxDB 学习指南（时序数据 & 监控）

## 📚 项目概述

本指南在 `influxDB/` 目录下，参考 `hive/`、`clickhouse/`、`doris/`、`oracle/`、`PostgreSQL/`、`mongoDB/`、`elasticsearch/`、`redis/` 等模块的组织方式，提供一套系统的 **InfluxDB 学习路径**，重点覆盖：

- **核心知识点**：时序数据模型（measurement/tag/field/time）、Line Protocol、Retention Policy、Continuous Query/Task、基本查询与聚合。
- **案例场景**：CPU/内存监控、HTTP 请求指标（QPS/延迟）、保留策略与下采样。
- **验证数据**：小规模 CSV/Line Protocol 示例数据，方便在本地 InfluxDB 实例中动手练习。

---

## 📁 项目结构

```
influxDB/
├── README.md                        # InfluxDB 知识点总览（详细文档）
├── GUIDE.md                         # 本指南文档（学习路径 + 快速上手）
├── cases/                           # 实战案例目录
│   ├── metrics_basics.md            # 案例1：基础时序写入与查询（CPU 指标）
│   ├── http_request_monitoring.md   # 案例2：HTTP 请求监控与聚合分析
│   └── retention_downsampling.md    # 案例3：保留策略与下采样
├── data/                            # 验证数据（CSV/line protocol）
│   ├── cpu_metrics.lp               # CPU 指标 Line Protocol 示例
│   └── http_requests.lp             # HTTP 请求指标 Line Protocol 示例
└── scripts/                         # CLI/HTTP 示例（示意）
    ├── write_cpu.sh                 # 写入 CPU 指标示例
    ├── write_http.sh                # 写入 HTTP 请求示例
    └── common_queries.txt           # 常用 InfluxQL/Flux 查询示例
```

---

## 🎯 学习路径（建议 2~3 天）

### 阶段一：基础入门（0.5 天）

- 安装并启动 InfluxDB（本地或 Docker），使用 `influx` CLI 或 Web UI 连接。
- 了解数据库/桶（bucket）、measurement/tag/field/time 的概念。

### 阶段二：数据模型与写入（1 天）

- 熟悉 Line Protocol 格式（measurement, tags, fields, timestamp）。
- 通过 CLI/HTTP 写入 CPU 与 HTTP 请求示例数据（案例1、案例2）。

### 阶段三：查询与聚合（1~1.5 天）

- 使用 InfluxQL 或 Flux 完成基础查询与聚合：
  - 区间过滤、GROUP BY time()、均值/最大值/95 分位数等。
- 学习 Retention Policy 与 Continuous Query/Task 完成历史数据下采样（案例3）。

---

## 🚀 快速开始

> 下面以 InfluxDB 1.x + InfluxQL 为例（Flux 思路类似，可在 Web UI 中使用）。

### 步骤1：创建数据库与保留策略（Retention Policy）

```sql
CREATE DATABASE metrics;
-- 可选：创建自定义保留策略，例如保留 7 天
CREATE RETENTION POLICY "rp_7d" ON "metrics" DURATION 7d REPLICATION 1 DEFAULT;
```

### 步骤2：写入示例数据（Line Protocol）

在 `influxDB/` 目录下：

```bash
# 写入 CPU 指标
sh scripts/write_cpu.sh

# 写入 HTTP 请求指标
sh scripts/write_http.sh
```

或手动：

```bash
influx -database 'metrics' -execute "INSERT cpu,host=server1,region=beijing usage_user=12.3,usage_system=5.6"
```

### 步骤3：基础查询

```sql
USE metrics;

-- 最近 10 条 CPU 指标
SELECT * FROM cpu ORDER BY time DESC LIMIT 10;

-- 按 1 分钟粒度统计平均 user 使用率
SELECT MEAN(usage_user)
FROM cpu
WHERE time > now() - 1h
GROUP BY time(1m), host fill(null);
```

---

## 📖 核心知识点速查

- **数据模型**：
  - measurement：类似“表名”，如 `cpu`、`http_requests`。
  - tag：带索引的标签（低基数），如 `host`、`region`、`status`。
  - field：不索引的数值/文本字段，如 `usage_user`、`latency_ms`。
  - time：时间戳。
- **Line Protocol**：`measurement,tag1=v1,tag2=v2 field1=val1,field2=val2 <timestamp>`
- **Retention Policy**：控制数据保留时间。
- **下采样**：通过 Continuous Query/Task 将高频数据聚合为低频数据保存。

---

## 📊 验证数据说明

- `data/cpu_metrics.lp`：包含若干 `cpu` measurement 行，tags 示例：`host`、`region`，fields 示例：`usage_user`、`usage_system`。
- `data/http_requests.lp`：包含若干 `http_requests` measurement 行，tags 示例：`service`、`status`，fields 示例：`count`、`latency_ms`。

---

## 🔧 实战案例概览

- `metrics_basics.md`：CPU 指标写入、基础查询与按时间粒度聚合。
- `http_request_monitoring.md`：HTTP 请求 QPS/延迟统计与按状态码聚合。
- `retention_downsampling.md`：为 metrics 数据库配置保留策略与下采样查询。

---

## ✅ 学习检查清单

- [ ] 能够使用 Line Protocol 正确写入 measurement/tag/field/time。
- [ ] 能够使用 InfluxQL/Flux 查询最近一段时间的时序数据并按时间聚合。
- [ ] 能够配置简单的 Retention Policy 与下采样逻辑。

---

## 🎓 学习成果

完成本指南后，你将能够：

- 使用 InfluxDB 存储与查询 CPU、HTTP 请求等典型时序指标。
- 为监控/告警系统提供基础的时序数据支持。
- 理解时序数据库在“高频写入 + 时间聚合分析”场景下的优势与边界。

