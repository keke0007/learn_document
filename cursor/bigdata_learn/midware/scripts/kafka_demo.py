"""
Kafka 基础与高级开发示例
演示 Kafka 的 Producer 和 Consumer
"""

from kafka import KafkaProducer, KafkaConsumer
import json
import time

print("=== Kafka 基础操作示例 ===\n")

# 1. Producer 示例
print("1. Producer 示例")
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8') if k else None
)

# 发送消息
for i in range(5):
    message = {
        'id': i,
        'timestamp': time.time(),
        'value': f'message_{i}'
    }
    future = producer.send('test-topic', key=f'key_{i}', value=message)
    record_metadata = future.get(timeout=10)
    print(f"Sent: topic={record_metadata.topic}, "
          f"partition={record_metadata.partition}, "
          f"offset={record_metadata.offset}")

producer.flush()
producer.close()
print()

# 2. Consumer 示例
print("2. Consumer 示例")
consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    key_deserializer=lambda k: k.decode('utf-8') if k else None,
    auto_offset_reset='earliest',
    group_id='my-consumer-group',
    consumer_timeout_ms=1000
)

print("Consuming messages (timeout after 1 second):")
for message in consumer:
    print(f"Topic: {message.topic}, "
          f"Partition: {message.partition}, "
          f"Offset: {message.offset}, "
          f"Key: {message.key}, "
          f"Value: {message.value}")

consumer.close()
print("\n=== Kafka 示例完成 ===")
