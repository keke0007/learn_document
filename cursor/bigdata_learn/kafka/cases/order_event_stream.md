# 案例3：订单事件流与简单实时统计（Kafka）

## 一、案例目标

- 为订单相关事件（创建、支付、取消等）设计事件流 Topic 与消息结构。
- 为后续实时统计（如每分钟订单数）打基础。

---

## 二、Topic 与消息结构

- Topic：`order_events`
- 示例消息（见 `data/sample_messages.jsonl`）：

```json
{"type":"ORDER_CREATED","order_id":1001,"user_id":1,"ts":"2024-03-14T10:00:01Z"}
{"type":"ORDER_PAID","order_id":1001,"user_id":1,"ts":"2024-03-14T10:01:00Z"}
```

---

## 三、生产订单事件

```bash
$KAFKA_BIN/kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic order_events < data/sample_messages.jsonl
```

---

## 四、消费与实时统计思路

- 简单方式：消费端按时间窗口在内存中统计 `ORDER_CREATED` 数量。
- 进阶方式：结合 Flink/Spark Streaming 从 `order_events` Topic 读取，按窗口聚合写入外部存储。

---

## 五、练习建议

1. 增加更多事件类型（如 `ORDER_CANCELLED`），并在消费端统计不同类型事件数量。  
2. 思考如何在消息中增加分区键（如 `user_id`）以在保持负载均衡的同时保证部分有序性。  

