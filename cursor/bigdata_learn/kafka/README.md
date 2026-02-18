# Kafka 学习总览

`kafka/` 模块整理了 Kafka 在消息队列与事件流场景中的主要知识点，并将它们与 `cases/` + `data/` + `scripts/` 中的案例和验证数据对应起来。

---

## 一、核心知识点概览

- Topic / Partition / Offset 基础概念。
- Producer / Consumer / Consumer Group。
- 消息持久化与顺序（分区内有序）。
- 简单流处理（依靠消费端或后续流引擎实现）。

---

## 二、知识点与案例/数据对照表

| 模块                 | 关键知识点                          | 案例文档                    | 数据文件                 | 脚本文件                      |
|----------------------|-------------------------------------|-----------------------------|--------------------------|-------------------------------|
| 基础生产与消费       | Topic、分区、控制台生产/消费        | `basic_producer_consumer.md`| `sample_messages.jsonl`  | `create_topics.sh`,`basic_producer.sh`,`basic_consumer.sh` |
| 日志采集             | 日志 Topic 设计、JSON 消息格式      | `log_collecting.md`         | `sample_messages.jsonl`  | 同上                          |
| 订单事件流           | 订单事件 Topic 与流式消费           | `order_event_stream.md`     | `sample_messages.jsonl`  | 同上                          |

---

## 三、如何使用本模块学习

1. 阅读 `GUIDE.md`，了解 Kafka 的基础概念与学习路径。
2. 启动本地 Kafka 集群，执行 `scripts/create_topics.sh` 创建示例 Topic。
3. 参考 `cases/` 文档与 `scripts/` 中的命令，使用控制台生产/消费 `data/sample_messages.jsonl` 中的 JSON 消息。

当你能够：

- 熟练使用控制台工具进行消息的生产/消费；
- 理解 Topic、分区与消费组之间的关系；

就基本具备了在项目中使用 Kafka 进行日志/事件传输的核心能力。

