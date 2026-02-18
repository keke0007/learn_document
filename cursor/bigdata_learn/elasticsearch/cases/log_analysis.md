# 案例3：日志检索与聚合分析（Elasticsearch）

## 一、案例目标

- **场景**：分析应用日志，按时间和服务维度统计访问量、错误数等。
- **目标**：
  - 设计简单的日志索引结构。
  - 使用 `date_histogram` 和 `terms` 进行多维聚合。

对应数据与脚本：

- 数据文件：`data/logs.jsonl`
- 索引脚本：`scripts/setup_indices.sh`
- 加载脚本：`scripts/load_data.sh`

---

## 二、日志文档结构示例

```json
{ "index": {} }
{ "ts": "2024-03-14T10:00:01", "level": "INFO", "service": "order-service", "message": "order created", "order_id": 1001 }
```

字段说明：

- `ts`：时间戳（date）
- `level`：日志级别（INFO/WARN/ERROR 等）
- `service`：服务名（如 order-service、user-service）
- `message`：日志消息
- 其他业务字段（如 `order_id`）

---

## 三、常用日志查询与聚合

### 1. 最近 10 分钟的 ERROR 日志

```json
GET logs/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "level": "ERROR" } }
      ],
      "filter": [
        { "range": { "ts": { "gte": "now-10m" } } }
      ]
    }
  },
  "sort": [
    { "ts": "desc" }
  ],
  "size": 50
}
```

### 2. 按服务统计 ERROR 数量

```json
GET logs/_search
{
  "size": 0,
  "query": {
    "term": { "level": "ERROR" }
  },
  "aggs": {
    "by_service": {
      "terms": { "field": "service" }
    }
  }
}
```

### 3. 按时间统计所有日志数量（按分钟）

```json
GET logs/_search
{
  "size": 0,
  "aggs": {
    "logs_over_time": {
      "date_histogram": {
        "field": "ts",
        "fixed_interval": "1m",
        "min_doc_count": 0
      }
    }
  }
}
```

---

## 四、练习建议

1. 将上面的 `logs_over_time` 聚合与按 `service` 的 `terms` 聚合组合（嵌套聚合）以绘制不同服务的错误趋势。  
2. 为 `message` 字段增加 `text` 类型分词，尝试用 `match` 查询某些关键字（如“timeout”）。  
3. 思考如何在生产环境中按天或按月切分日志索引，并结合生命周期管理（ILM）自动做冷热数据管理。  

