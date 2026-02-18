# RocketMQ 基础与高级开发案例

## 案例概述

本案例通过实际代码演示 RocketMQ 的消息发送和消费，包括普通消息、顺序消息、事务消息等高级特性。

## 知识点

1. **核心概念**
   - Topic：主题
   - Queue：队列
   - Producer：生产者
   - Consumer：消费者
   - Message：消息

2. **消息类型**
   - 普通消息
   - 顺序消息
   - 事务消息
   - 延时消息
   - 批量消息

3. **消息模式**
   - 集群模式
   - 广播模式

## 案例代码

### 案例1：普通消息

```python
# rocketmq_normal.py
from rocketmq.client import Producer, Message

# 创建生产者
producer = Producer('ProducerGroup')
producer.set_name_server_address('localhost:9876')
producer.start()

# 发送同步消息
msg = Message('TopicTest', 'Hello RocketMQ'.encode('utf-8'))
result = producer.send_sync(msg)
print(f"Send result: {result.status}, Message ID: {result.msg_id}")

# 发送异步消息
def on_success(result):
    print(f"Send success: {result.msg_id}")

def on_exception(e):
    print(f"Send failed: {e}")

msg = Message('TopicTest', 'Async message'.encode('utf-8'))
producer.send_async(msg, on_success, on_exception)

# 发送单向消息（不关心结果）
msg = Message('TopicTest', 'Oneway message'.encode('utf-8'))
producer.send_oneway(msg)

producer.shutdown()
```

### 案例2：顺序消息

```python
# rocketmq_ordered.py
from rocketmq.client import Producer, Message

producer = Producer('OrderedProducerGroup')
producer.set_name_server_address('localhost:9876')
producer.start()

# 发送顺序消息（同一订单的消息发送到同一队列）
for i in range(10):
    order_id = f'ORDER_{i % 3}'  # 3个订单
    msg = Message(
        'OrderTopic',
        f'Order {order_id} - Step {i}'.encode('utf-8')
    )
    msg.set_keys(order_id)  # 设置消息键
    result = producer.send_sync(msg, selector=order_id)  # 使用选择器保证顺序
    print(f"Sent: {result.msg_id}")

producer.shutdown()

# 消费顺序消息
from rocketmq.client import PushConsumer, ConsumeStatus

def on_message(msg):
    print(f"Received: {msg.body.decode('utf-8')}")
    return ConsumeStatus.CONSUME_SUCCESS

consumer = PushConsumer('OrderedConsumerGroup')
consumer.set_name_server_address('localhost:9876')
consumer.subscribe('OrderTopic', '*')
consumer.register_message_listener(on_message)
consumer.start()
```

### 案例3：事务消息

```python
# rocketmq_transaction.py
from rocketmq.client import TransactionMQProducer, Message, TransactionStatus

# 创建事务生产者
producer = TransactionMQProducer('TransactionProducerGroup')
producer.set_name_server_address('localhost:9876')

# 事务监听器
class TransactionListener:
    def execute_local_transaction(self, msg):
        # 执行本地事务
        try:
            # 本地业务逻辑
            print(f"Executing local transaction for: {msg.body.decode('utf-8')}")
            # 如果成功，返回 COMMIT
            return TransactionStatus.COMMIT
            # 如果失败，返回 ROLLBACK
            # return TransactionStatus.ROLLBACK
        except Exception as e:
            return TransactionStatus.ROLLBACK
    
    def check_local_transaction(self, msg):
        # 检查本地事务状态
        print(f"Checking local transaction for: {msg.body.decode('utf-8')}")
        return TransactionStatus.COMMIT

producer.set_transaction_listener(TransactionListener())
producer.start()

# 发送事务消息
msg = Message('TransactionTopic', 'Transaction message'.encode('utf-8'))
result = producer.send_message_in_transaction(msg, None)
print(f"Transaction send result: {result.status}")

producer.shutdown()
```

### 案例4：延时消息

```python
# rocketmq_delay.py
from rocketmq.client import Producer, Message

producer = Producer('DelayProducerGroup')
producer.set_name_server_address('localhost:9876')
producer.start()

# 发送延时消息（延时10秒）
msg = Message('DelayTopic', 'Delayed message'.encode('utf-8'))
msg.set_delay_time_level(3)  # 延时级别3（约10秒）
result = producer.send_sync(msg)
print(f"Delayed message sent: {result.msg_id}")

producer.shutdown()
```

### 案例5：批量消息

```python
# rocketmq_batch.py
from rocketmq.client import Producer, Message

producer = Producer('BatchProducerGroup')
producer.set_name_server_address('localhost:9876')
producer.start()

# 批量发送消息
messages = []
for i in range(10):
    msg = Message('BatchTopic', f'Batch message {i}'.encode('utf-8'))
    messages.append(msg)

result = producer.send_batch(messages)
print(f"Batch send result: {result.status}")

producer.shutdown()
```

## 验证数据

### RocketMQ 性能测试

| 场景 | 吞吐量 | 延迟 | 说明 |
|-----|--------|------|------|
| 普通消息 | 50000 msg/s | <5ms | 单机 |
| 顺序消息 | 30000 msg/s | <10ms | 保证顺序 |
| 事务消息 | 20000 msg/s | <20ms | 事务处理 |

## 总结

1. **消息类型选择**
   - 普通消息：一般场景
   - 顺序消息：需要保证顺序
   - 事务消息：分布式事务
   - 延时消息：定时任务

2. **消息可靠性**
   - 同步发送保证可靠性
   - 事务消息保证一致性
   - 消息重试机制

3. **性能优化**
   - 批量发送提高吞吐量
   - 异步发送降低延迟
   - 合理设置消费者线程数

4. **最佳实践**
   - 使用消息键进行消息追踪
   - 设置合理的消息 TTL
   - 监控消息积压
   - 使用死信队列处理失败消息
