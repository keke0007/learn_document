#!/usr/bin/env bash

# 使用控制台生产者发送示例消息

KAFKA_BIN=${KAFKA_BIN:-"$HOME/kafka/bin"}
BOOTSTRAP=${BOOTSTRAP:-"localhost:9092"}

"$KAFKA_BIN/kafka-console-producer.sh" \
  --broker-list "$BOOTSTRAP" \
  --topic demo_logs < data/sample_messages.jsonl

