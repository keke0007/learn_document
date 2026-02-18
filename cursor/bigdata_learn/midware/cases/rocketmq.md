# RocketMQ 高性能原理与高级应用案例（深入版）

## 案例概述

本案例深入 RocketMQ 高性能原理、数据结构组合机制、高级应用场景。**重点：顺序写磁盘、零拷贝、事务消息机制、顺序消息保证、真实业务场景设计。**

---

## 🚀 高性能原理

### 1. 顺序写磁盘与零拷贝

**顺序写磁盘优势：**
- **机械硬盘**：顺序写 100MB/s，随机写 < 1MB/s（100倍差距）
- **SSD**：顺序写 500MB/s，随机写 50MB/s（10倍差距）
- RocketMQ 采用 append-only 顺序写，充分利用磁盘带宽

**CommitLog 设计：**
- **所有消息写入同一个文件**：`CommitLog`，顺序写入
- **ConsumeQueue**：消费队列，存储消息在 CommitLog 中的位置
- **IndexFile**：索引文件，支持按时间/Key 查询

**文件结构：**
```
CommitLog/
  ├─ 00000000000000000000  # 1GB 一个文件
  ├─ 00000000001073741824
  └─ ...

ConsumeQueue/
  ├─ TopicA/
  │   ├─ 0/  # Queue 0
  │   │   ├─ 00000000000000000000  # 30万条消息一个文件
  │   │   └─ 00000000001800000000
  │   └─ 1/  # Queue 1
  └─ TopicB/
      └─ ...

IndexFile/
  ├─ 20240126100000  # 按小时创建
  └─ 20240126110000
```

**零拷贝机制：**
- **MappedByteBuffer**：内存映射文件，减少数据拷贝
- **sendfile**：Linux 零拷贝系统调用
- **性能提升**：2-3 倍吞吐量

---

### 2. 顺序消息保证机制

**顺序消息原理：**
- **同一 Queue 内顺序**：同一 Queue 的消息顺序消费
- **Queue 选择**：使用 MessageQueueSelector 选择 Queue
- **消费顺序**：单线程消费，保证顺序

**Queue 选择策略：**
```java
// 按订单ID选择Queue，保证同一订单的消息在同一Queue
MessageQueueSelector selector = new MessageQueueSelector() {
    @Override
    public MessageQueue select(List<MessageQueue> mqs, Message msg, Object arg) {
        String orderId = (String) arg;
        int index = Math.abs(orderId.hashCode()) % mqs.size();
        return mqs.get(index);
    }
};

// 发送顺序消息
SendResult result = producer.send(msg, selector, orderId);
```

**消费顺序保证：**
- **顺序消费模式**：`MessageListenerOrderly`，单线程消费
- **锁机制**：每个 Queue 一把锁，保证同一 Queue 顺序消费
- **失败重试**：顺序消息失败后，会阻塞后续消息消费

---

### 3. 事务消息机制

**事务消息流程：**
```
1. Producer 发送 Half 消息（事务消息）
   -> Broker 存储 Half 消息（对 Consumer 不可见）
     -> 执行本地事务
       -> 发送 Commit/Rollback 消息
         -> Broker 提交/回滚消息
           -> Consumer 消费消息
```

**Half 消息机制：**
- **Half 消息**：事务消息的中间状态，对 Consumer 不可见
- **事务状态**：`COMMIT_MESSAGE`、`ROLLBACK_MESSAGE`、`UNKNOWN`
- **事务回查**：如果 Producer 未发送 Commit/Rollback，Broker 会回查事务状态

**事务回查机制：**
- **回查时机**：Half 消息发送后，如果长时间未收到 Commit/Rollback
- **回查频率**：默认每 1 分钟回查一次，最多回查 15 次
- **回查逻辑**：调用 Producer 的 `checkLocalTransaction` 方法

---

### 4. 延时消息机制

**延时消息实现：**
- **延时级别**：18 个固定延时级别（1s, 5s, 10s, 30s, 1m, 2m, 3m, 4m, 5m, 6m, 7m, 8m, 9m, 10m, 20m, 30m, 1h, 2h）
- **延时队列**：`SCHEDULE_TOPIC_XXXX`，每个延时级别一个队列
- **定时任务**：定时扫描延时队列，将到期的消息投递到目标 Topic

**延时消息流程：**
```
发送延时消息
  -> 计算目标投递时间
    -> 投递到延时队列（SCHEDULE_TOPIC_XXXX）
      -> 定时任务扫描
        -> 到期后投递到目标 Topic
          -> Consumer 消费
```

---

### 5. 消息过滤机制

**Tag 过滤：**
- **Tag 设置**：消息设置 Tag，Consumer 订阅时指定 Tag
- **过滤方式**：Broker 端过滤，减少网络传输
- **性能优势**：只传输匹配的消息，提高效率

**SQL 过滤：**
- **过滤表达式**：使用 SQL92 语法过滤消息
- **支持字段**：消息属性（Property）
- **性能影响**：SQL 过滤需要解析表达式，性能略低于 Tag 过滤

---

## 🔧 数据结构组合功能

### 组合1：顺序消息 + 事务消息

**数据结构组合：**
- **顺序消息**：保证同一业务键的消息顺序
- **事务消息**：保证消息和本地事务的一致性

**订单系统设计：**
```python
from rocketmq.client import TransactionMQProducer, Message, TransactionStatus

# 创建事务生产者
producer = TransactionMQProducer('OrderProducerGroup')
producer.set_name_server_address('localhost:9876')

class OrderTransactionListener:
    def execute_local_transaction(self, msg):
        """
        执行本地事务
        """
        try:
            order_data = json.loads(msg.body.decode('utf-8'))
            order_id = order_data['order_id']
            
            # 1. 创建订单（数据库）
            create_order(order_data)
            
            # 2. 扣减库存（数据库）
            deduct_inventory(order_data['items'])
            
            # 3. 发送顺序消息（保证同一订单的消息顺序）
            order_msg = Message(
                'order-events',
                json.dumps({
                    'order_id': order_id,
                    'event_type': 'order_created',
                    'data': order_data
                }).encode('utf-8')
            )
            order_msg.set_keys(order_id)  # 使用订单ID作为key
            
            # 选择Queue（保证顺序）
            selector = lambda mqs, msg, arg: mqs[hash(arg) % len(mqs)]
            producer.send(order_msg, selector, order_id)
            
            return TransactionStatus.COMMIT
        except Exception as e:
            return TransactionStatus.ROLLBACK
    
    def check_local_transaction(self, msg):
        """
        检查本地事务状态（事务回查）
        """
        order_data = json.loads(msg.body.decode('utf-8'))
        order_id = order_data['order_id']
        
        # 检查订单状态
        order = get_order(order_id)
        if order and order['status'] == 'created':
            return TransactionStatus.COMMIT
        else:
            return TransactionStatus.ROLLBACK

producer.set_transaction_listener(OrderTransactionListener())
producer.start()

# 发送事务消息
msg = Message(
    'order-transaction',
    json.dumps({
        'order_id': 'ORDER123',
        'user_id': 'user123',
        'items': [{'product_id': 'product1', 'quantity': 1}],
        'total_amount': 100.0
    }).encode('utf-8')
)

result = producer.send_message_in_transaction(msg, None)
```

---

### 组合2：延时消息 + 批量消息

**数据结构组合：**
- **延时消息**：延迟投递消息
- **批量消息**：批量发送，提高吞吐量

**定时任务系统设计：**
```python
from rocketmq.client import Producer, Message

producer = Producer('TaskProducerGroup')
producer.set_name_server_address('localhost:9876')
producer.start()

# 批量发送延时消息
def schedule_tasks(tasks, delay_level):
    """
    批量调度任务
    - tasks: 任务列表
    - delay_level: 延时级别（1-18）
    """
    messages = []
    
    for task in tasks:
        msg = Message(
            'task-topic',
            json.dumps(task).encode('utf-8')
        )
        msg.set_delay_time_level(delay_level)  # 设置延时级别
        msg.set_keys(task['task_id'])  # 设置消息键
        messages.append(msg)
    
    # 批量发送
    result = producer.send_batch(messages)
    return result

# 使用示例
tasks = [
    {'task_id': 'task1', 'action': 'send_email', 'data': {...}},
    {'task_id': 'task2', 'action': 'generate_report', 'data': {...}},
    {'task_id': 'task3', 'action': 'cleanup_data', 'data': {...}}
]

# 延时 1 小时执行（delay_level=13，约1小时）
schedule_tasks(tasks, delay_level=13)
```

---

### 组合3：消息过滤 + 消费模式

**数据结构组合：**
- **Tag 过滤**：Broker 端过滤，减少网络传输
- **集群模式**：负载均衡消费
- **广播模式**：所有消费者都消费

**日志收集系统设计：**
```python
from rocketmq.client import PushConsumer, ConsumeStatus

# 创建消费者（集群模式）
consumer = PushConsumer('LogConsumerGroup')
consumer.set_name_server_address('localhost:9876')

# 订阅日志Topic，只消费ERROR级别的日志
consumer.subscribe('logs', 'ERROR')  # Tag过滤

def on_message(msg):
    try:
        log_data = json.loads(msg.body.decode('utf-8'))
        
        # 处理ERROR日志
        process_error_log(log_data)
        
        return ConsumeStatus.CONSUME_SUCCESS
    except Exception as e:
        # 处理失败，稍后重试
        return ConsumeStatus.RECONSUME_LATER

consumer.register_message_listener(on_message)
consumer.start()

# 创建广播消费者（所有节点都消费）
broadcast_consumer = PushConsumer('BroadcastConsumerGroup')
broadcast_consumer.set_consume_message_batch_max_size(1)  # 广播模式
broadcast_consumer.subscribe('config-updates', '*')

def on_broadcast_message(msg):
    # 配置更新，所有节点都需要更新
    update_config(json.loads(msg.body.decode('utf-8')))
    return ConsumeStatus.CONSUME_SUCCESS

broadcast_consumer.register_message_listener(on_broadcast_message)
broadcast_consumer.start()
```

---

## 💼 高级应用场景案例

### 场景1：订单系统最终一致性

**业务需求：**
- 订单创建后，异步处理库存扣减、支付处理、物流通知
- 保证最终一致性（订单状态最终一致）
- 支持补偿机制（失败后回滚）

**Topic 和 Queue 设计：**
```python
# Topic: order-events
# Queue: 4个（按订单ID哈希，保证同一订单的消息顺序）

# 1. 订单创建消息
order_created_msg = Message(
    'order-events',
    json.dumps({
        'order_id': 'ORDER123',
        'event_type': 'order_created',
        'user_id': 'user123',
        'items': [...],
        'total_amount': 100.0
    }).encode('utf-8')
)
order_created_msg.set_keys('ORDER123')  # 使用订单ID作为key

# 2. 发送顺序消息（保证同一订单的消息顺序）
selector = lambda mqs, msg, arg: mqs[hash(arg) % len(mqs)]
producer.send(order_created_msg, selector, 'ORDER123')
```

**消费者设计：**
```python
# 库存服务消费者
def process_inventory(msg):
    event = json.loads(msg.body.decode('utf-8'))
    order_id = event['order_id']
    
    try:
        # 扣减库存
        deduct_inventory(event['items'])
        
        # 发送库存扣减成功消息
        inventory_msg = Message(
            'order-events',
            json.dumps({
                'order_id': order_id,
                'event_type': 'inventory_deducted',
                'status': 'success'
            }).encode('utf-8')
        )
        inventory_msg.set_keys(order_id)
        producer.send(inventory_msg, selector, order_id)
        
        return ConsumeStatus.CONSUME_SUCCESS
    except Exception as e:
        # 库存不足，发送补偿消息
        compensate_msg = Message(
            'order-events',
            json.dumps({
                'order_id': order_id,
                'event_type': 'order_cancelled',
                'reason': 'insufficient_inventory'
            }).encode('utf-8')
        )
        compensate_msg.set_keys(order_id)
        producer.send(compensate_msg, selector, order_id)
        
        return ConsumeStatus.CONSUME_SUCCESS

# 支付服务消费者
def process_payment(msg):
    event = json.loads(msg.body.decode('utf-8'))
    order_id = event['order_id']
    
    if event['event_type'] == 'inventory_deducted':
        try:
            # 处理支付
            process_payment(order_id, event['total_amount'])
            
            # 发送支付成功消息
            payment_msg = Message(
                'order-events',
                json.dumps({
                    'order_id': order_id,
                    'event_type': 'payment_success',
                    'status': 'success'
                }).encode('utf-8')
            )
            payment_msg.set_keys(order_id)
            producer.send(payment_msg, selector, order_id)
            
            return ConsumeStatus.CONSUME_SUCCESS
        except Exception as e:
            # 支付失败，发送补偿消息
            compensate_msg = Message(
                'order-events',
                json.dumps({
                    'order_id': order_id,
                    'event_type': 'order_cancelled',
                    'reason': 'payment_failed'
                }).encode('utf-8')
            )
            compensate_msg.set_keys(order_id)
            producer.send(compensate_msg, selector, order_id)
            
            return ConsumeStatus.CONSUME_SUCCESS
```

**性能指标：**
- **吞吐量**：10万订单/分钟（单Topic）
- **延迟**：P99 延迟 < 200ms（端到端）
- **可靠性**：消息不丢失（同步发送 + 事务消息）

---

### 场景2：实时数据同步（CDC）

**业务需求：**
- 数据库变更实时同步到缓存、搜索引擎
- 保证数据一致性（最终一致）
- 支持数据过滤（只同步需要的字段）

**数据同步架构：**
```
MySQL（主库）
  -> Canal（CDC工具）
    -> RocketMQ（消息队列）
      -> 多个消费者
        ├─ Redis（缓存更新）
        ├─ Elasticsearch（搜索索引更新）
        └─ 其他系统
```

**消息设计：**
```python
# Canal 发送变更消息到 RocketMQ
canal_msg = Message(
    'db-changes',
    json.dumps({
        'database': 'mydb',
        'table': 'users',
        'event_type': 'UPDATE',  # INSERT/UPDATE/DELETE
        'before': {
            'id': 1,
            'name': 'Alice',
            'age': 25
        },
        'after': {
            'id': 1,
            'name': 'Alice',
            'age': 26
        },
        'timestamp': datetime.now().isoformat()
    }).encode('utf-8')
)

canal_msg.set_keys('mydb.users.1')  # 使用数据库.表.主键作为key
producer.send(canal_msg)
```

**消费者设计：**
```python
# Redis 缓存更新消费者
def update_cache(msg):
    change = json.loads(msg.body.decode('utf-8'))
    table = change['table']
    event_type = change['event_type']
    
    if table == 'users':
        user_id = change['after']['id']
        
        if event_type == 'DELETE':
            # 删除缓存
            redis_client.delete(f'user:{user_id}')
        else:
            # 更新缓存
            user_data = change['after']
            redis_client.hset(
                f'user:{user_id}',
                mapping=user_data
            )
            redis_client.expire(f'user:{user_id}', 3600)
    
    return ConsumeStatus.CONSUME_SUCCESS

# Elasticsearch 索引更新消费者
def update_search_index(msg):
    change = json.loads(msg.body.decode('utf-8'))
    table = change['table']
    event_type = change['event_type']
    
    if table == 'users':
        user_data = change['after'] if event_type != 'DELETE' else change['before']
        user_id = user_data['id']
        
        if event_type == 'DELETE':
            # 删除索引
            es.delete(index='users', id=user_id)
        else:
            # 更新索引
            es.index(index='users', id=user_id, body=user_data)
    
    return ConsumeStatus.CONSUME_SUCCESS
```

**性能指标：**
- **吞吐量**：50万变更/分钟（单Topic）
- **延迟**：端到端延迟 < 500ms（包含索引更新）
- **可靠性**：消息不丢失（同步发送）

---

### 场景3：分布式任务调度

**业务需求：**
- 定时任务调度（延迟执行）
- 任务优先级（高优先级任务先执行）
- 任务重试（失败后重试）
- 任务结果通知

**任务调度设计：**
```python
# 发送延时任务
def schedule_task(task_data, delay_seconds):
    """
    调度任务
    - task_data: 任务数据
    - delay_seconds: 延迟秒数
    """
    # 计算延时级别
    delay_level = calculate_delay_level(delay_seconds)
    
    msg = Message(
        'task-topic',
        json.dumps(task_data).encode('utf-8')
    )
    msg.set_delay_time_level(delay_level)
    msg.set_keys(task_data['task_id'])
    
    # 根据优先级选择Queue（高优先级Queue先消费）
    if task_data.get('priority') == 'high':
        queue_id = 0  # 高优先级Queue
    else:
        queue_id = 1  # 普通优先级Queue
    
    selector = lambda mqs, msg, arg: mqs[arg % len(mqs)]
    producer.send(msg, selector, queue_id)

# 任务消费
def process_task(msg):
    task_data = json.loads(msg.body.decode('utf-8'))
    task_id = task_data['task_id']
    
    try:
        # 执行任务
        result = execute_task(task_data)
        
        # 发送任务结果
        result_msg = Message(
            'task-results',
            json.dumps({
                'task_id': task_id,
                'status': 'success',
                'result': result
            }).encode('utf-8')
        )
        result_msg.set_keys(task_id)
        producer.send(result_msg)
        
        return ConsumeStatus.CONSUME_SUCCESS
    except Exception as e:
        # 任务失败，检查重试次数
        retry_count = task_data.get('retry_count', 0)
        
        if retry_count < 3:
            # 重试（延迟60秒）
            task_data['retry_count'] = retry_count + 1
            schedule_task(task_data, delay_seconds=60)
            return ConsumeStatus.CONSUME_SUCCESS
        else:
            # 重试次数达到上限，发送失败通知
            failure_msg = Message(
                'task-failures',
                json.dumps({
                    'task_id': task_id,
                    'status': 'failed',
                    'error': str(e)
                }).encode('utf-8')
            )
            failure_msg.set_keys(task_id)
            producer.send(failure_msg)
            
            return ConsumeStatus.CONSUME_SUCCESS
```

**性能指标：**
- **吞吐量**：1万任务/分钟（单Topic）
- **延迟精度**：延时任务误差 < 1s
- **可靠性**：任务不丢失（同步发送）

---

## 🐛 常见坑与排查

### 坑1：消息丢失
**现象**：Producer 发送消息后，Consumer 消费不到
**原因**：
1. 异步发送未等待结果
2. 单向发送（`sendOneway`）不关心结果
3. 消费者自动提交偏移量，处理失败但已提交
**排查**：
1. 使用同步发送（`sendSync`）或异步发送等待结果
2. 使用手动提交偏移量（`CONSUME_SUCCESS`）
3. 监控消息积压（`consumerLag`）

### 坑2：顺序消息乱序
**现象**：顺序消息消费顺序错乱
**原因**：
1. 未使用 MessageQueueSelector 选择Queue
2. 消费模式错误（使用并发消费模式）
3. 消息重试导致乱序
**排查**：
1. 使用 MessageQueueSelector 保证同一业务键的消息在同一Queue
2. 使用顺序消费模式（`MessageListenerOrderly`）
3. 顺序消息失败后，会阻塞后续消息消费

### 坑3：事务消息未提交
**现象**：事务消息一直处于 Half 状态，Consumer 消费不到
**原因**：
1. 本地事务执行失败，但未发送 Rollback
2. 事务回查逻辑错误
3. 网络问题导致 Commit/Rollback 消息丢失
**排查**：
1. 检查本地事务执行逻辑
2. 实现正确的事务回查逻辑
3. 监控事务消息状态（`transactionMsg`）

---

## 验证数据

### RocketMQ 性能测试

| 场景 | 吞吐量 | 延迟 | 说明 |
|-----|--------|------|------|
| 普通消息 | 50000 msg/s | <5ms | 单机，顺序写 |
| 顺序消息 | 30000 msg/s | <10ms | 保证顺序 |
| 事务消息 | 20000 msg/s | <20ms | 事务处理 |
| 批量消息 | 100000 msg/s | <10ms | 批量发送 |

### 存储性能

```
写入速度：100MB/s（单Queue）
读取速度：200MB/s（单Queue）
零拷贝提升：2-3倍吞吐量
```

---

## 总结

1. **高性能原理**
   - 顺序写磁盘（充分利用磁盘带宽）
   - 零拷贝（减少数据拷贝）
   - CommitLog + ConsumeQueue（分离存储和消费）
   - 消息过滤（Broker 端过滤，减少网络传输）

2. **数据结构组合**
   - 顺序消息 + 事务消息：保证顺序和一致性
   - 延时消息 + 批量消息：定时任务调度
   - 消息过滤 + 消费模式：灵活的消息路由

3. **高级应用场景**
   - 订单系统：最终一致性、补偿机制
   - 数据同步：CDC、实时同步
   - 任务调度：延时任务、优先级任务

4. **性能优化核心**
   - 合理设置Queue数量（单Queue 20-50GB）
   - 批量发送消息（减少网络往返）
   - 使用消息过滤（减少网络传输）
   - 监控消息积压（及时发现问题）
