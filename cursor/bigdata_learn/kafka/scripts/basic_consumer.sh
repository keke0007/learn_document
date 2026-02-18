#!/usr/bin/env bash

# 使用控制台消费者消费示例消息

KAFKA_BIN=${KAFKA_BIN:-"$HOME/kafka/bin"}
BOOTSTRAP=${BOOTSTRAP:-"localhost:9092"}

"$KAFKA_BIN/kafka-console-consumer.sh" \
  --bootstrap-server "$BOOTSTRAP" \
  --topic demo_logs \
  --from-beginning

