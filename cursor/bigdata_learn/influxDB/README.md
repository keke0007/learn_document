# InfluxDB 学习总览

`influxDB/` 模块整理了 InfluxDB 在时序数据与监控场景中的主要知识点，并将它们与 `cases/` + `data/` + `scripts/` 中的案例和验证数据对应起来。

---

## 一、核心知识点概览

- 时序数据模型：measurement / tag / field / time。
- Line Protocol 写入格式。
- Retention Policy（保留策略）与 Continuous Query/Task（下采样）。
- 基本查询与聚合（InfluxQL 或 Flux）。

---

## 二、知识点与案例/数据对照表

| 模块                   | 关键知识点                              | 案例文档                        | 数据文件                | 脚本文件                     |
|------------------------|-----------------------------------------|---------------------------------|-------------------------|------------------------------|
| 基础时序写入与查询     | measurement/tag/field/time、Line Protocol | `metrics_basics.md`             | `cpu_metrics.lp`        | `write_cpu.sh`,`common_queries.txt` |
| HTTP 请求监控          | QPS/延迟统计、按服务/状态聚合           | `http_request_monitoring.md`    | `http_requests.lp`      | `write_http.sh`,`common_queries.txt` |
| 保留策略与下采样       | Retention Policy、时间粒度下采样        | `retention_downsampling.md`     | 同上                    | 同上                         |

---

## 三、如何使用本模块学习

1. 阅读 `GUIDE.md`，确认本地 InfluxDB 版本与 CLI/Flux 使用方式。
2. 在 `influxDB/` 目录下使用 `scripts/write_cpu.sh`、`scripts/write_http.sh` 将 `data/` 中的示例指标写入数据库。
3. 打开 `cases/` 中的案例文档，对照 `scripts/common_queries.txt` 中的查询在 CLI 或 Web UI 中实际执行。

当你能够：

- 正确理解并使用 measurement/tag/field/time；
- 写入和查询 CPU 与 HTTP 请求等基础指标；
- 配置简单保留策略与下采样逻辑；

就基本具备了在项目中使用 InfluxDB 做监控与时序分析的能力。

