# 案例1：基础数据结构与常用命令（Redis）

## 一、案例目标

- 通过一组简单的命令，快速掌握 Redis 五大基础数据结构的用法：
  - String / Hash / List / Set / Sorted Set。

---

## 二、示例命令（可参考 `scripts/basic_datatypes.redis`）

### 1. String

```bash
SET counter 0
INCR counter
GET counter
```

### 2. Hash（用户信息）

```bash
HSET user:1 name "张三" age 25 city "北京"
HGETALL user:1
HGET user:1 name
HINCRBY user:1 age 1
```

### 3. List（简单消息队列）

```bash
LPUSH msg_queue "msg1"
LPUSH msg_queue "msg2"
LRANGE msg_queue 0 -1
RPOP msg_queue
```

### 4. Set（标签集合）

```bash
SADD user:1:tags "金卡" "高价值"
SMEMBERS user:1:tags
SISMEMBER user:1:tags "金卡"
```

### 5. Sorted Set（排行榜）

```bash
ZADD rank:score 100 "user1"
ZADD rank:score 200 "user2"
ZREVRANGE rank:score 0 -1 WITHSCORES
```

---

## 三、练习建议

1. 基于 `data/users.json` 里的用户 ID，批量构造 `user:<id>` 的 Hash 结构。  
2. 为一个简单活动设计排行榜 `rank:event2024`，用 ZSet 存储用户得分并输出前 10 名。  

