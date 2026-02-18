#!/usr/bin/env bash

# 创建示例 Topic

KAFKA_BIN=${KAFKA_BIN:-"$HOME/kafka/bin"}
BOOTSTRAP=${BOOTSTRAP:-"localhost:9092"}

"$KAFKA_BIN/kafka-topics.sh" --create --topic demo_logs --bootstrap-server "$BOOTSTRAP" --partitions 3 --replication-factor 1
"$KAFKA_BIN/kafka-topics.sh" --create --topic order_events --bootstrap-server "$BOOTSTRAP" --partitions 3 --replication-factor 1

