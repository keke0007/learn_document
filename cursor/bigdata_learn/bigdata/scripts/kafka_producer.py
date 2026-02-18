"""
Kafka Producer 示例
演示如何向 Kafka 发送消息
"""

from kafka import KafkaProducer
import json
import time
from datetime import datetime

# 创建 Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8') if k else None,
    # 可靠性配置
    acks='all',  # 等待所有副本确认
    retries=3,
    max_in_flight_requests_per_connection=1,  # 保证顺序
    # 性能配置
    batch_size=16384,  # 16KB
    linger_ms=10,  # 等待10ms批量发送
    compression_type='snappy'
)

def send_message(topic, key, value):
    """发送消息"""
    future = producer.send(topic, key=key, value=value)
    try:
        record_metadata = future.get(timeout=10)
        print(f"Message sent to topic={record_metadata.topic}, "
              f"partition={record_metadata.partition}, "
              f"offset={record_metadata.offset}")
    except Exception as e:
        print(f"Error sending message: {e}")

# 示例1：发送简单消息
print("=== 示例1：发送简单消息 ===")
for i in range(10):
    message = {
        'id': i,
        'timestamp': datetime.now().isoformat(),
        'value': i * 10
    }
    send_message('test-topic', None, message)
    time.sleep(0.1)

# 示例2：使用 key 保证分区
print("\n=== 示例2：使用 key 保证分区 ===")
for i in range(20):
    user_id = f'user_{i % 5}'  # 5个用户
    message = {
        'user_id': user_id,
        'action': 'click',
        'timestamp': datetime.now().isoformat(),
        'page': f'page_{i % 3}'
    }
    # 使用 user_id 作为 key，保证同一用户的消息发送到同一分区
    send_message('user-events', user_id, message)
    time.sleep(0.1)

# 示例3：批量发送
print("\n=== 示例3：批量发送 ===")
messages = []
for i in range(100):
    message = {
        'id': i,
        'data': f'data_{i}',
        'timestamp': datetime.now().isoformat()
    }
    messages.append(('batch-topic', None, message))

# 批量发送
for topic, key, value in messages:
    producer.send(topic, key=key, value=value)

# 确保所有消息都发送完成
producer.flush()

print("All messages sent")
producer.close()
