#!/usr/bin/env bash

# 设备控制指令发布示例

BROKER_HOST=${BROKER_HOST:-"localhost"}
BROKER_PORT=${BROKER_PORT:-1883}

mosquitto_pub -h "$BROKER_HOST" -p "$BROKER_PORT" \
  -t "devices/device1/control" \
  -m '{"cmd":"switch","target":"relay1","state":"ON","ts":"2024-03-14T10:05:00Z"}' \
  -q 1

