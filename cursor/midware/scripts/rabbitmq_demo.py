"""
RabbitMQ 基础与高级开发示例
演示 RabbitMQ 的消息发送和消费
"""

import pika
import time

print("=== RabbitMQ 基础操作示例 ===\n")

# 连接 RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

# 1. 声明队列
print("1. 声明队列")
channel.queue_declare(queue='hello', durable=True)
print("Queue 'hello' declared")
print()

# 2. 发送消息
print("2. 发送消息")
channel.basic_publish(
    exchange='',
    routing_key='hello',
    body='Hello World!',
    properties=pika.BasicProperties(
        delivery_mode=2,  # 消息持久化
    )
)
print("Message sent")
print()

# 3. 消费消息（回调函数）
print("3. 消费消息")
def callback(ch, method, properties, body):
    print(f"Received: {body.decode('utf-8')}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue='hello',
    on_message_callback=callback,
    auto_ack=False
)

print("Waiting for messages. To exit press CTRL+C")
print("(This will run indefinitely - press Ctrl+C to stop)")
# channel.start_consuming()  # 取消注释以实际运行

connection.close()
print("\n=== RabbitMQ 示例完成 ===")
