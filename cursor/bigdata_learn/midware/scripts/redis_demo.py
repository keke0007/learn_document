"""
Redis 基础与高级开发示例
演示 Redis 的各种数据结构和操作
"""

import redis
from datetime import datetime, timedelta

# 连接 Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

print("=== Redis 基础操作示例 ===\n")

# 1. String 操作
print("1. String 操作")
r.set('name', 'Redis', ex=3600)  # 设置过期时间1小时
print(f"GET name: {r.get('name')}")
r.incr('counter')
r.incrby('counter', 5)
print(f"GET counter: {r.get('counter')}")
print()

# 2. Hash 操作
print("2. Hash 操作")
r.hset('user:1', mapping={
    'name': 'Alice',
    'age': '25',
    'email': 'alice@example.com'
})
print(f"HGETALL user:1: {r.hgetall('user:1')}")
r.hincrby('user:1', 'age', 1)
print(f"HGET user:1 age: {r.hget('user:1', 'age')}")
print()

# 3. List 操作
print("3. List 操作")
r.lpush('list', 'item1', 'item2', 'item3')
r.rpush('list', 'item4')
print(f"LRANGE list 0 -1: {r.lrange('list', 0, -1)}")
print(f"LPOP list: {r.lpop('list')}")
print()

# 4. Set 操作
print("4. Set 操作")
r.sadd('tags', 'python', 'redis', 'database')
print(f"SMEMBERS tags: {r.smembers('tags')}")
print(f"SISMEMBER tags python: {r.sismember('tags', 'python')}")
print()

# 5. Sorted Set 操作
print("5. Sorted Set 操作")
r.zadd('leaderboard', {'player1': 100, 'player2': 200, 'player3': 150})
print(f"ZRANGE leaderboard 0 -1 WITHSCORES: {r.zrange('leaderboard', 0, -1, withscores=True)}")
print(f"ZRANK leaderboard player2: {r.zrank('leaderboard', 'player2')}")
print()

# 6. Bitmap 操作
print("6. Bitmap 操作")
r.setbit('visits:2024-01-26', 100, 1)
r.setbit('visits:2024-01-26', 101, 1)
print(f"BITCOUNT visits:2024-01-26: {r.bitcount('visits:2024-01-26')}")
print()

# 7. HyperLogLog 操作
print("7. HyperLogLog 操作")
r.pfadd('unique_visitors', 'user1', 'user2', 'user3')
r.pfadd('unique_visitors', 'user2', 'user4')
print(f"PFCOUNT unique_visitors: {r.pfcount('unique_visitors')}")
print()

# 8. 发布订阅
print("8. 发布订阅示例（需要运行订阅者）")
r.publish('channel', 'Hello from publisher')
print("Message published to 'channel'")
print()

# 9. 管道操作
print("9. 管道批量操作")
pipe = r.pipeline()
for i in range(10):
    pipe.set(f'key{i}', f'value{i}')
results = pipe.execute()
print(f"Set {len(results)} keys using pipeline")
print()

# 10. 事务操作
print("10. 事务操作")
pipe = r.pipeline()
pipe.multi()
pipe.set('tx_key1', 'value1')
pipe.set('tx_key2', 'value2')
pipe.execute()
print("Transaction executed")
print()

print("=== Redis 示例完成 ===")
