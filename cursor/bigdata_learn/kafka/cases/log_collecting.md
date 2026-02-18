# 案例2：日志采集管道（Kafka）

## 一、案例目标

- 将应用日志以 JSON 形式发送到 Kafka。
- 为后续 Elasticsearch/ClickHouse 等日志分析系统提供数据源。

---

## 二、Topic 设计

- 日志 Topic：`demo_logs`
  - 可按服务拆分：`logs.order-service`、`logs.user-service` 等（可扩展）。

---

## 三、示例日志消息（见 `data/sample_messages.jsonl`）

```json
{"level":"INFO","service":"order","msg":"order created","order_id":1001}
{"level":"ERROR","service":"order","msg":"payment failed","order_id":1002}
```

---

## 四、生产日志消息

```bash
$KAFKA_BIN/kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic demo_logs < data/sample_messages.jsonl
```

---

## 五、练习建议

1. 为不同服务设计不同日志 Topic，并通过通配或消费组实现统一消费。  
2. 思考如何在日志中加入时间戳与 TraceId，方便后续关联分析。  

