#!/usr/bin/env bash

# 传感器上报示例

BROKER_HOST=${BROKER_HOST:-"localhost"}
BROKER_PORT=${BROKER_PORT:-1883}

mosquitto_pub -h "$BROKER_HOST" -p "$BROKER_PORT" \
  -t "devices/device1/sensors/temperature" \
  -m '{"value":23.5,"unit":"C","ts":"2024-03-14T10:00:01Z"}' \
  -q 1

