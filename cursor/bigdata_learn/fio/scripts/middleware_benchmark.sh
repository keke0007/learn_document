#!/bin/bash
# 中间件IO性能测试脚本示例

echo "=== Redis 性能测试 ==="
# 使用 redis-benchmark
redis-benchmark -h localhost -p 6379 \
    -c 100 \              # 100个并发客户端
    -n 100000 \           # 总共10万次请求
    -d 100 \              # 数据大小100字节
    -t get,set \          # 测试get和set命令
    --csv

echo ""
echo "=== Kafka 性能测试 ==="
# Producer 压测
kafka-producer-perf-test.sh \
    --topic test-topic \
    --num-records 1000000 \
    --record-size 1024 \
    --throughput 10000 \
    --producer-props \
        bootstrap.servers=localhost:9092 \
        batch.size=16384 \
        linger.ms=10

# Consumer 压测
kafka-consumer-perf-test.sh \
    --topic test-topic \
    --messages 1000000 \
    --broker-list localhost:9092 \
    --threads 4

echo ""
echo "=== RocketMQ 性能测试 ==="
# 使用 RocketMQ 自带的压测工具
# 注意：需要先创建topic和consumer group
# sh mqadmin sendMessage -n localhost:9876 -t test-topic -m "test message" -c 1000

echo ""
echo "=== 系统IO监控（iostat）==="
# 监控磁盘IO（每2秒刷新，共5次）
iostat -x 2 5
