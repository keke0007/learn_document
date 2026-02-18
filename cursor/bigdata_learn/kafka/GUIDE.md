## Kafka 学习指南（消息队列 & 流处理）

## 📚 项目概述

本指南在 `kafka/` 目录下，参考 `redis/`、`influxDB/`、`mongoDB/`、`elasticsearch/` 等模块的组织方式，提供一套系统的 **Kafka 学习路径**，重点覆盖：

- **核心知识点**：Topic/Partition/Offset、Producer/Consumer、Consumer Group、消息持久化与顺序、简单的流处理概念。
- **案例场景**：基础生产/消费、日志采集、订单事件流、简单实时统计。
- **验证数据**：小规模 JSON 示例消息，方便在本地或测试 Kafka 集群中动手练习。

---

## 📁 项目结构

```
kafka/
├── README.md                         # Kafka 知识点总览（详细文档）
├── GUIDE.md                          # 本指南文档（学习路径 + 快速上手）
├── cases/                            # 实战案例目录
│   ├── basic_producer_consumer.md    # 案例1：基础生产与消费
│   ├── log_collecting.md             # 案例2：日志采集管道
│   └── order_event_stream.md         # 案例3：订单事件流与简单实时统计
├── data/                             # 验证数据（JSON 示例消息）
│   └── sample_messages.jsonl         # 多条 JSON 消息（日志/订单）
└── scripts/                          # kafka-console-* 示例命令（示意）
    ├── create_topics.sh              # 创建 Topic
    ├── basic_producer.sh             # 生产示例消息
    └── basic_consumer.sh             # 消费示例消息
```

---

## 🎯 学习路径（建议 2~3 天）

### 阶段一：基础概念（0.5 天）

- Kafka 架构：Broker、Zookeeper/Controller、Topic、Partition、Replica。
- Producer / Consumer / Consumer Group 概念。

### 阶段二：基础生产与消费（1 天）

- 使用 `kafka-console-producer` / `kafka-console-consumer` 完成消息的发送与消费（案例1）。
- 理解 Offset、分区内顺序、消费位点提交。

### 阶段三：日志与事件流实践（1~1.5 天）

- 日志采集：将应用日志以 JSON 形式写入 Kafka（案例2）。
- 订单事件流：订单创建/支付/取消等事件流转（案例3）。
- 简单实时统计思路（可结合 Flink/Spark 或消费端手动聚合）。

---

## 🚀 快速开始

> 假设你已安装 Kafka，并在本地运行 Zookeeper + Kafka Broker（或使用新版无 ZK 模式）。

### 步骤1：创建 Topic

```bash
sh scripts/create_topics.sh
```

脚本中示例：

```bash
$KAFKA_BIN/kafka-topics.sh --create --topic demo_logs --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

### 步骤2：生产示例消息

```bash
sh scripts/basic_producer.sh
```

或手动：

```bash
$KAFKA_BIN/kafka-console-producer.sh --broker-list localhost:9092 --topic demo_logs
>{"level":"INFO","service":"order","msg":"order created","order_id":1001}
```

### 步骤3：消费示例消息

```bash
sh scripts/basic_consumer.sh
```

或手动：

```bash
$KAFKA_BIN/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic demo_logs --from-beginning
```

---

## 📖 核心知识点速查

- **Topic**：按业务维度划分（如 `demo_logs`、`order_events`）。
- **Partition**：提高并发与吞吐，分区内顺序有保证。
- **Consumer Group**：同组消费者均衡消费消息，实现水平扩展。

---

## 📊 验证数据说明

- `data/sample_messages.jsonl`：包含若干 JSON 行，既可作为日志，也可视作订单事件示例，便于通过 `kafka-console-producer` 直接粘贴发送。

---

## 🔧 实战案例概览

- `basic_producer_consumer.md`：从零搭建 Topic，使用控制台工具生产与消费消息。
- `log_collecting.md`：模拟应用日志通过 Kafka 传输，为下游存储（如 Elasticsearch）做准备。
- `order_event_stream.md`：设计订单事件 Topic 与消息结构，为实时统计和风控埋下基础。

---

## ✅ 学习检查清单

- [ ] 能够创建 Topic 并理解分区数量的含义。
- [ ] 能够使用控制台工具生产与消费 JSON 消息。
- [ ] 能从 Topic 设计上区分出日志流与业务事件流。

---

## 🎓 学习成果

完成本指南后，你将能够：

- 使用 Kafka 作为日志与业务事件的传输总线。
- 为下游大数据/实时计算系统（Flink/Spark/ClickHouse 等）提供可靠的消息输入。
- 在实际项目中设计基本合理的 Topic 与分区方案。

