#!/usr/bin/env bash

# 基础发布/订阅示例（需本地已启动 MQTT Broker）

BROKER_HOST=${BROKER_HOST:-"localhost"}
BROKER_PORT=${BROKER_PORT:-1883}

echo "订阅主题 test/qos0（另开终端运行本脚本可看到效果）"
echo "mosquitto_sub -h $BROKER_HOST -p $BROKER_PORT -t \"test/qos0\" -q 0"

echo "发布示例消息："
mosquitto_pub -h "$BROKER_HOST" -p "$BROKER_PORT" -t "test/qos0" -m "hello mqtt" -q 0

