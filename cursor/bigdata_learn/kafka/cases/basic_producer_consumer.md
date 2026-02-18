# 案例1：基础生产与消费（Kafka）

## 一、案例目标

- 使用控制台工具完成最基础的 Kafka 消息生产与消费。
- 理解 Topic、分区、Offset 的基本行为。

---

## 二、准备工作

- 启动 Zookeeper（如使用 2.x 版本）和 Kafka Broker：

```bash
$KAFKA_BIN/zookeeper-server-start.sh config/zookeeper.properties
$KAFKA_BIN/kafka-server-start.sh config/server.properties
```

---

## 三、创建 Topic

```bash
$KAFKA_BIN/kafka-topics.sh --create \
  --topic demo_logs \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
```

---

## 四、生产与消费示例

### 1. 生产消息

```bash
$KAFKA_BIN/kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic demo_logs
>{"level":"INFO","service":"order","msg":"order created","order_id":1001}
>{"level":"ERROR","service":"order","msg":"payment failed","order_id":1002}
```

### 2. 消费消息

```bash
$KAFKA_BIN/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic demo_logs \
  --from-beginning
```

---

## 五、练习建议

1. 修改 Topic 分区数与消费者组数量，观察同组消费者如何分摊分区。  
2. 使用消费者组参数 `--group demo_group`，体验 Offset 提交与重新消费的差异。  

