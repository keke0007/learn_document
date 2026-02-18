#!/usr/bin/env bash

# 将 cpu_metrics.lp 写入 InfluxDB 示例

DB_NAME=${DB_NAME:-"metrics"}
INFLUX_CMD=${INFLUX_CMD:-"influx"}

$INFLUX_CMD -database "$DB_NAME" -import -path=./data/cpu_metrics.lp

