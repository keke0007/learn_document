# Redis 高性能原理与高级应用案例（深入版）

## 案例概述

本案例深入 Redis 高性能原理、数据结构组合机制、高级应用场景。**重点：单线程事件循环、内存模型、数据结构编码、持久化机制、真实业务场景设计。**

---

## 🚀 高性能原理

### 1. 单线程事件循环模型

**为什么单线程还能高性能？**
- **避免锁竞争**：单线程执行命令，无需加锁
- **CPU 缓存友好**：数据局部性好，缓存命中率高
- **网络 IO 非阻塞**：使用 epoll/kqueue，单线程处理大量连接
- **内存操作**：所有操作在内存中，速度极快

**事件循环机制：**
```
aeMain() 主循环
  -> aeProcessEvents()
    -> epoll_wait() 等待事件（最多等待 1ms）
      -> 处理文件事件（客户端请求）
        -> readQueryFromClient() 读取命令
        -> processCommand() 处理命令
        -> addReply() 回复客户端
      -> 处理时间事件（定时任务）
        -> serverCron() 定期任务
          -> 过期键清理
          -> 持久化检查
          -> 主从复制检查
    -> beforesleep() 事件循环前处理
      -> 处理客户端缓冲区
      -> 处理 AOF 缓冲区
```

**性能优势：**
- **QPS**：单机 10万+ QPS（简单命令）
- **延迟**：P99 延迟 < 1ms（内存操作）
- **并发**：单线程处理 10万+ 并发连接

---

### 2. 内存模型与数据结构编码

**Redis 对象系统：**
- **统一抽象**：所有数据类型都是 `robj`（Redis Object）
- **多编码**：同一数据类型有多种编码方式，根据数据大小自动选择

**String 编码：**
- **INT 编码**：整数字符串（`-128` 到 `127`，或 `-2^63` 到 `2^63-1`）
- **EMBSTR 编码**：短字符串（≤44字节），对象和字符串在同一内存块
- **RAW 编码**：长字符串（>44字节），对象和字符串分离

**Hash 编码：**
- **ZIPLIST 编码**：小哈希表（≤512个元素，所有值≤64字节）
  - 内存紧凑，适合小对象
- **HASHTABLE 编码**：大哈希表（超过 ZIPLIST 限制）
  - 使用字典（dict），支持 O(1) 查找

**List 编码：**
- **ZIPLIST 编码**：小列表（≤512个元素，所有值≤64字节）
- **QUICKLIST 编码**：大列表（快速列表 = 双向链表 + ZIPLIST）
  - 每个节点是一个 ZIPLIST，支持压缩

**Set 编码：**
- **INTSET 编码**：整数集合（所有元素都是整数，元素数量≤512）
- **HASHTABLE 编码**：大集合（使用字典，值为 NULL）

**Sorted Set 编码：**
- **ZIPLIST 编码**：小有序集合（≤128个元素，所有值≤64字节）
- **SKIPLIST 编码**：大有序集合（跳表 + 字典）
  - 跳表：支持 O(log N) 范围查询
  - 字典：支持 O(1) 成员查找

**内存优化：**
- **编码自动选择**：根据数据大小自动选择最优编码
- **压缩**：ZIPLIST、QUICKLIST 支持压缩
- **共享对象**：小整数（0-9999）共享，减少内存占用

---

### 3. 渐进式 Rehash 机制

**为什么需要 Rehash？**
- 哈希表负载因子过高（`used/size > 1`）→ 哈希冲突增加 → 性能下降
- 需要扩容哈希表，但一次性 rehash 会阻塞服务

**渐进式 Rehash 流程：**
```
触发 Rehash
  -> 创建新哈希表（ht[1]），大小为 ht[0].used * 2
    -> 设置 rehashidx = 0
      -> 每次操作时，迁移 1 个桶
        -> rehashidx++
          -> 所有桶迁移完成
            -> ht[0] = ht[1]，ht[1] = NULL，rehashidx = -1
```

**Rehash 期间的查找：**
- 先在 ht[0] 查找，找不到再在 ht[1] 查找
- 写入操作直接写入 ht[1]

**性能保证：**
- **分步迁移**：每次操作迁移 1 个桶，避免长时间阻塞
- **最多访问空桶**：每次最多访问 `n*10` 个空桶，避免无限循环

---

### 4. 持久化机制（RDB + AOF）

**RDB 快照：**
- **触发条件**：
  - 手动：`SAVE`（阻塞）、`BGSAVE`（后台）
  - 自动：`save 900 1`（900秒内至少1个键变化）
- **优势**：文件小、恢复快
- **劣势**：可能丢失最后一次快照后的数据

**AOF 追加：**
- **触发条件**：每个命令执行后追加到 AOF 缓冲区
- **同步策略**：
  - `always`：每个命令都同步（最安全，性能最低）
  - `everysec`：每秒同步一次（平衡，默认）
  - `no`：由操作系统决定（性能最高，安全性最低）
- **优势**：数据安全，最多丢失 1 秒数据
- **劣势**：文件大、恢复慢

**AOF 重写：**
- **触发条件**：
  - AOF 文件大小 > `auto-aof-rewrite-min-size`（默认 64MB）
  - AOF 文件增长率 > `auto-aof-rewrite-percentage`（默认 100%）
- **重写过程**：
  - Fork 子进程，遍历数据库，生成新的 AOF 文件
  - 父进程继续处理命令，增量 AOF 写入缓冲区
  - 子进程完成后，合并增量 AOF

**混合持久化（RDB + AOF）：**
- AOF 文件开头是 RDB 格式，后面是 AOF 格式
- 优势：结合 RDB 和 AOF 的优点

---

### 5. 主从复制与哨兵模式

**主从复制流程：**
```
SLAVEOF 命令
  -> 连接主节点
    -> 发送 PSYNC 命令
      -> 全量复制（FULLRESYNC）
        -> 主节点生成 RDB
        -> 发送 RDB 到从节点
        -> 从节点加载 RDB
      -> 增量复制（CONTINUE）
        -> 从复制积压缓冲区获取命令
        -> 执行命令
```

**复制积压缓冲区（Replication Backlog）：**
- **作用**：存储最近执行的命令，支持增量复制
- **大小**：`repl-backlog-size`（默认 1MB）
- **机制**：FIFO 队列，新命令覆盖旧命令

**哨兵模式（Sentinel）：**
- **功能**：
  - 监控主从节点健康状态
  - 自动故障转移（主节点故障，选举新主节点）
  - 配置提供者（客户端从哨兵获取主节点地址）
- **故障转移流程**：
  - 哨兵检测主节点故障（`down-after-milliseconds`）
  - 选举 Leader 哨兵
  - Leader 哨兵选举新主节点（从 ISR 中选择）
  - 通知其他从节点切换主节点

---

## 🔧 数据结构组合功能

### 组合1：分布式锁 + 过期时间

**数据结构组合：**
- **String**：存储锁的值（唯一标识）
- **EXPIRE**：设置过期时间，防止死锁

**分布式锁设计：**
```python
import redis
import uuid
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def acquire_lock(lock_name, timeout=10, expire_time=30):
    """
    获取分布式锁
    - lock_name: 锁名称
    - timeout: 获取锁的超时时间（秒）
    - expire_time: 锁的过期时间（秒）
    """
    lock_key = f"lock:{lock_name}"
    lock_value = str(uuid.uuid4())  # 唯一标识
    
    end_time = time.time() + timeout
    while time.time() < end_time:
        # SET NX EX：如果不存在则设置，并设置过期时间
        if r.set(lock_key, lock_value, nx=True, ex=expire_time):
            return lock_value
        time.sleep(0.001)  # 短暂等待后重试
    
    return None

def release_lock(lock_name, lock_value):
    """
    释放分布式锁（Lua 脚本保证原子性）
    """
    lock_key = f"lock:{lock_name}"
    lua_script = """
    if redis.call('GET', KEYS[1]) == ARGV[1] then
        return redis.call('DEL', KEYS[1])
    else
        return 0
    end
    """
    return r.eval(lua_script, 1, lock_key, lock_value)
```

**使用场景：**
- 防止重复提交（订单创建、支付处理）
- 分布式任务调度（避免重复执行）
- 资源竞争控制（库存扣减）

---

### 组合2：计数器 + 滑动窗口限流

**数据结构组合：**
- **String**：存储计数器值
- **EXPIRE**：设置过期时间，实现滑动窗口
- **INCR**：原子性递增

**滑动窗口限流设计：**
```python
def sliding_window_limit(user_id, limit=100, window=60):
    """
    滑动窗口限流
    - user_id: 用户ID
    - limit: 限制次数
    - window: 时间窗口（秒）
    """
    key = f"rate_limit:{user_id}"
    current_time = int(time.time())
    window_start = current_time - window + 1
    
    # 使用 Lua 脚本保证原子性
    lua_script = """
    local key = KEYS[1]
    local window_start = tonumber(ARGV[1])
    local limit = tonumber(ARGV[2])
    local window = tonumber(ARGV[3])
    
    -- 清理过期数据
    redis.call('ZREMRANGEBYSCORE', key, 0, window_start - 1)
    
    -- 获取当前计数
    local count = redis.call('ZCARD', key)
    
    if count < limit then
        -- 添加当前时间戳
        redis.call('ZADD', key, current_time, current_time)
        redis.call('EXPIRE', key, window)
        return 1
    else
        return 0
    end
    """
    
    result = r.eval(
        lua_script,
        1,
        key,
        window_start,
        limit,
        window
    )
    
    return result == 1
```

**优化版本（使用 String + 多时间窗口）：**
```python
def sliding_window_limit_v2(user_id, limit=100, window=60):
    """
    滑动窗口限流（优化版：使用多个时间窗口）
    """
    current_time = int(time.time())
    windows = []
    
    # 创建多个时间窗口（每个窗口 1 秒）
    for i in range(window):
        window_key = f"rate_limit:{user_id}:{current_time - i}"
        windows.append(window_key)
    
    # 批量获取计数
    pipe = r.pipeline()
    for key in windows:
        pipe.get(key)
    counts = pipe.execute()
    
    # 计算总计数
    total = sum(int(c) if c else 0 for c in counts)
    
    if total < limit:
        # 增加当前窗口计数
        current_window = f"rate_limit:{user_id}:{current_time}"
        r.incr(current_window)
        r.expire(current_window, window)
        return True
    else:
        return False
```

---

### 组合3：排行榜 + 实时更新

**数据结构组合：**
- **Sorted Set**：存储排行榜（score = 分数，member = 用户ID）
- **Hash**：存储用户详细信息（可选）

**排行榜设计：**
```python
def update_leaderboard(user_id, score):
    """
    更新排行榜
    """
    r.zadd('leaderboard', {user_id: score})

def get_leaderboard(top_n=10):
    """
    获取排行榜 Top N
    """
    # 获取 Top N（按分数降序）
    top_users = r.zrevrange('leaderboard', 0, top_n - 1, withscores=True)
    
    # 获取用户排名
    rankings = []
    for user_id, score in top_users:
        rank = r.zrevrank('leaderboard', user_id)
        rankings.append({
            'user_id': user_id,
            'score': score,
            'rank': rank + 1  # 排名从1开始
        })
    
    return rankings

def get_user_rank(user_id):
    """
    获取用户排名
    """
    rank = r.zrevrank('leaderboard', user_id)
    score = r.zscore('leaderboard', user_id)
    return {
        'user_id': user_id,
        'rank': rank + 1 if rank is not None else None,
        'score': score if score is not None else 0
    }

def get_users_in_range(min_score, max_score):
    """
    获取分数范围内的用户
    """
    return r.zrangebyscore('leaderboard', min_score, max_score, withscores=True)
```

**使用场景：**
- 游戏排行榜（积分、等级）
- 活动排行榜（参与度、贡献度）
- 商品排行榜（销量、评分）

---

## 💼 高级应用场景案例

### 场景1：秒杀系统（高并发场景）

**业务需求：**
- 商品库存有限（如 1000 件）
- 大量用户同时抢购（10万+ 并发）
- 保证库存不超卖
- 防止重复购买

**架构设计：**
```
用户请求
  -> 网关（限流）
    -> 秒杀服务
      -> Redis（库存扣减）
        -> 成功：写入订单队列
        -> 失败：返回库存不足
      -> 订单服务（异步处理）
        -> 数据库（最终一致性）
```

**Redis 设计：**
```python
# 1. 商品库存（String）
r.set('stock:product:1001', 1000)

# 2. 用户购买记录（Set，防止重复购买）
r.sadd('purchased:product:1001', user_id)

# 3. 秒杀队列（List，异步处理订单）
r.lpush('seckill:queue:product:1001', order_data)
```

**库存扣减（Lua 脚本保证原子性）：**
```python
lua_script = """
local stock_key = KEYS[1]
local purchased_key = KEYS[2]
local queue_key = KEYS[3]
local user_id = ARGV[1]
local product_id = ARGV[2]

-- 检查是否已购买
if redis.call('SISMEMBER', purchased_key, user_id) == 1 then
    return {0, 'already_purchased'}
end

-- 检查库存
local stock = tonumber(redis.call('GET', stock_key))
if stock <= 0 then
    return {0, 'out_of_stock'}
end

-- 扣减库存
local new_stock = redis.call('DECR', stock_key)

-- 记录购买
redis.call('SADD', purchased_key, user_id)

-- 加入订单队列
local order_data = cjson.encode({
    user_id = user_id,
    product_id = product_id,
    timestamp = redis.call('TIME')[1]
})
redis.call('LPUSH', queue_key, order_data)

return {1, 'success', new_stock}
"""

def seckill(user_id, product_id):
    stock_key = f'stock:product:{product_id}'
    purchased_key = f'purchased:product:{product_id}'
    queue_key = f'seckill:queue:product:{product_id}'
    
    result = r.eval(lua_script, 3, stock_key, purchased_key, queue_key, user_id, product_id)
    
    if result[0] == 1:
        return {'success': True, 'stock': result[2]}
    else:
        return {'success': False, 'reason': result[1]}
```

**性能优化：**
- **预热**：提前将库存加载到 Redis
- **限流**：网关层限流，减少 Redis 压力
- **异步处理**：订单写入队列，异步处理，提高响应速度
- **库存回退**：订单超时未支付，库存回退

**验证数据：**
- **QPS**：10万+ QPS（单 Redis 实例）
- **延迟**：P99 延迟 < 5ms（库存扣减）
- **成功率**：99.9%+（库存充足时）

---

### 场景2：分布式会话存储（Session 共享）

**业务需求：**
- 多服务共享用户会话（微服务架构）
- 会话过期自动清理
- 支持会话刷新（延长过期时间）

**Session 设计：**
```python
import json
import time

def create_session(user_id, session_data, expire_time=3600):
    """
    创建会话
    - user_id: 用户ID
    - session_data: 会话数据
    - expire_time: 过期时间（秒）
    """
    session_id = str(uuid.uuid4())
    session_key = f'session:{session_id}'
    
    # 存储会话数据（Hash）
    r.hset(session_key, mapping={
        'user_id': user_id,
        'data': json.dumps(session_data),
        'created_at': time.time(),
        'last_access': time.time()
    })
    
    # 设置过期时间
    r.expire(session_key, expire_time)
    
    # 用户ID -> Session ID 映射（Set）
    r.sadd(f'user_sessions:{user_id}', session_id)
    r.expire(f'user_sessions:{user_id}', expire_time)
    
    return session_id

def get_session(session_id):
    """
    获取会话
    """
    session_key = f'session:{session_id}'
    session_data = r.hgetall(session_key)
    
    if not session_data:
        return None
    
    # 更新最后访问时间
    r.hset(session_key, 'last_access', time.time())
    r.expire(session_key, 3600)  # 刷新过期时间
    
    return {
        'user_id': session_data[b'user_id'].decode(),
        'data': json.loads(session_data[b'data'].decode()),
        'created_at': float(session_data[b'created_at'].decode()),
        'last_access': float(session_data[b'last_access'].decode())
    }

def delete_session(session_id):
    """
    删除会话
    """
    session_key = f'session:{session_id}'
    session_data = r.hget(session_key, 'user_id')
    
    if session_data:
        user_id = session_data.decode()
        r.srem(f'user_sessions:{user_id}', session_id)
    
    r.delete(session_key)

def get_user_sessions(user_id):
    """
    获取用户所有会话（支持多设备登录）
    """
    session_ids = r.smembers(f'user_sessions:{user_id}')
    sessions = []
    
    for session_id in session_ids:
        session = get_session(session_id.decode())
        if session:
            sessions.append(session)
    
    return sessions
```

**性能优化：**
- **Hash 存储**：会话数据用 Hash，支持部分更新
- **过期时间**：自动过期，无需手动清理
- **刷新机制**：每次访问刷新过期时间，活跃用户会话不过期

---

### 场景3：实时排行榜 + 多维度统计

**业务需求：**
- 游戏积分排行榜（实时更新）
- 多维度统计（总积分、今日积分、本周积分）
- 排行榜分页查询
- 用户排名查询

**数据结构设计：**
```python
# 1. 总积分排行榜（Sorted Set）
r.zadd('leaderboard:total', {user_id: total_score})

# 2. 今日积分排行榜（Sorted Set，每天重置）
today = datetime.now().strftime('%Y-%m-%d')
r.zadd(f'leaderboard:daily:{today}', {user_id: daily_score})

# 3. 本周积分排行榜（Sorted Set，每周重置）
week = datetime.now().strftime('%Y-W%W')
r.zadd(f'leaderboard:weekly:{week}', {user_id: weekly_score})

# 4. 用户详细信息（Hash）
r.hset(f'user:{user_id}', mapping={
    'nickname': nickname,
    'avatar': avatar,
    'level': level,
    'total_score': total_score,
    'daily_score': daily_score,
    'weekly_score': weekly_score
})
```

**排行榜查询：**
```python
def get_leaderboard(leaderboard_type='total', page=1, page_size=20):
    """
    获取排行榜（分页）
    - leaderboard_type: total/daily/weekly
    - page: 页码（从1开始）
    - page_size: 每页数量
    """
    if leaderboard_type == 'total':
        key = 'leaderboard:total'
    elif leaderboard_type == 'daily':
        today = datetime.now().strftime('%Y-%m-%d')
        key = f'leaderboard:daily:{today}'
    elif leaderboard_type == 'weekly':
        week = datetime.now().strftime('%Y-W%W')
        key = f'leaderboard:weekly:{week}'
    else:
        return []
    
    start = (page - 1) * page_size
    end = start + page_size - 1
    
    # 获取排名范围内的用户
    users = r.zrevrange(key, start, end, withscores=True)
    
    # 获取用户详细信息
    rankings = []
    for user_id, score in users:
        user_info = r.hgetall(f'user:{user_id}')
        rankings.append({
            'user_id': user_id.decode() if isinstance(user_id, bytes) else user_id,
            'nickname': user_info.get(b'nickname', b'').decode() if b'nickname' in user_info else '',
            'score': score,
            'rank': start + len(rankings) + 1
        })
    
    return rankings

def get_user_rank(user_id, leaderboard_type='total'):
    """
    获取用户排名
    """
    if leaderboard_type == 'total':
        key = 'leaderboard:total'
    elif leaderboard_type == 'daily':
        today = datetime.now().strftime('%Y-%m-%d')
        key = f'leaderboard:daily:{today}'
    elif leaderboard_type == 'weekly':
        week = datetime.now().strftime('%Y-W%W')
        key = f'leaderboard:weekly:{week}'
    else:
        return None
    
    rank = r.zrevrank(key, user_id)
    score = r.zscore(key, user_id)
    
    if rank is None:
        return None
    
    return {
        'user_id': user_id,
        'rank': rank + 1,
        'score': score if score else 0
    }

def update_score(user_id, score_delta, leaderboard_type='total'):
    """
    更新积分（原子性）
    """
    if leaderboard_type == 'total':
        key = 'leaderboard:total'
        field = 'total_score'
    elif leaderboard_type == 'daily':
        today = datetime.now().strftime('%Y-%m-%d')
        key = f'leaderboard:daily:{today}'
        field = 'daily_score'
    elif leaderboard_type == 'weekly':
        week = datetime.now().strftime('%Y-W%W')
        key = f'leaderboard:weekly:{week}'
        field = 'weekly_score'
    else:
        return False
    
    # 更新排行榜
    new_score = r.zincrby(key, score_delta, user_id)
    
    # 更新用户详细信息
    r.hincrby(f'user:{user_id}', field, score_delta)
    
    return new_score
```

**性能优化：**
- **Sorted Set**：O(log N) 排名查询，O(1) 分数更新
- **分页查询**：使用 `ZREVRANGE`，支持高效分页
- **批量更新**：使用 Pipeline，减少网络往返

**验证数据：**
- **QPS**：10万+ QPS（排名查询）
- **延迟**：P99 延迟 < 5ms（排名查询）
- **存储**：100万用户，排行榜数据 < 100MB

---

## 🐛 常见坑与排查

### 坑1：内存溢出（OOM）
**现象**：Redis 内存使用超过 maxmemory，触发淘汰策略
**原因**：
1. 大 Key（String > 10KB，Hash/List/Set/ZSet > 5000个元素）
2. Key 过期时间设置不合理
3. 没有设置 maxmemory 和淘汰策略
**排查**：
1. 使用 `MEMORY USAGE key` 检查 Key 大小
2. 使用 `INFO memory` 查看内存使用情况
3. 使用 `--bigkeys` 选项扫描大 Key
4. 设置合理的 `maxmemory` 和 `maxmemory-policy`

### 坑2：阻塞操作
**现象**：Redis 响应变慢，命令超时
**原因**：
1. 大 Key 操作（`KEYS *`、`SMEMBERS`、`HGETALL`）
2. 全量复制（RDB 文件过大）
3. AOF 重写（磁盘 I/O 阻塞）
**排查**：
1. 使用 `SLOWLOG GET` 查看慢查询
2. 使用 `SCAN` 代替 `KEYS`
3. 使用 `SSCAN`、`HSCAN`、`ZSCAN` 代替 `SMEMBERS`、`HGETALL`、`ZRANGE`
4. 监控 `rdb_bgsave_in_progress` 和 `aof_rewrite_in_progress`

### 坑3：主从复制延迟
**现象**：从节点数据滞后主节点
**原因**：
1. 网络延迟
2. 主节点写入速度过快
3. 从节点处理能力不足
**排查**：
1. 使用 `INFO replication` 查看复制延迟（`master_repl_offset` vs `slave_repl_offset`）
2. 检查网络带宽和延迟
3. 优化从节点配置（增加内存、CPU）
4. 使用 `WAIT` 命令等待复制完成

---

## 验证数据

### Redis 性能测试

| 操作 | QPS | 延迟 | 说明 |
|-----|-----|------|------|
| SET | 100000 | <1ms | 单机，内存操作 |
| GET | 100000 | <1ms | 单机，内存操作 |
| HGETALL | 50000 | <2ms | Hash，小对象 |
| LPUSH | 80000 | <1ms | List，批量操作 |
| ZADD | 60000 | <2ms | Sorted Set，跳表 |

### 内存使用

| 数据类型 | 100万条数据 | 内存占用 |
|---------|------------|---------|
| String | 100万条 | ~100MB |
| Hash | 10万条 | ~50MB |
| List | 100万条 | ~80MB |
| Set | 100万条 | ~120MB |
| Sorted Set | 100万条 | ~150MB |

### 持久化性能

| 操作 | 数据量 | 耗时 | 说明 |
|-----|--------|------|------|
| RDB 保存 | 10GB | 30s | 后台保存 |
| AOF 追加 | 10GB | 实时 | 每秒同步 |
| AOF 重写 | 10GB | 60s | 后台重写 |

---

## 总结

1. **高性能原理**
   - 单线程事件循环（避免锁竞争）
   - 内存操作（所有数据在内存中）
   - 多编码优化（根据数据大小选择最优编码）
   - 渐进式 Rehash（避免阻塞）

2. **数据结构组合**
   - String + EXPIRE：分布式锁、限流
   - Sorted Set + Hash：排行榜、多维度统计
   - List + Set：消息队列、去重

3. **高级应用场景**
   - 秒杀系统：高并发库存扣减、防重复购买
   - 分布式会话：Session 共享、自动过期
   - 实时排行榜：多维度统计、分页查询

4. **性能优化核心**
   - 合理设置过期时间（避免内存泄漏）
   - 使用 Pipeline 批量操作（减少网络往返）
   - 避免大 Key（拆分大对象）
   - 监控内存使用（设置 maxmemory 和淘汰策略）
