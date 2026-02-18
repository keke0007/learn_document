# Redis 源码学习案例（深入版）

## 案例概述

本案例深入 Redis 核心源码，包括数据结构实现、命令执行流程、持久化机制、主从复制、集群模式等。**重点：断点位置、数据结构、单线程模型、持久化机制、基于源码的扩展实验。**

---

## 📍 断点清单（建议按顺序打断点）

### 命令执行断点
1. **`processCommand()`** (server.c L2800) - 命令处理入口
2. **`call()`** (server.c L3200) - 命令调用
3. **`lookupCommand()`** (server.c L2900) - 命令查找
4. **`addReply()`** (networking.c L200) - 回复客户端

### 数据结构断点
1. **`createStringObject()`** (object.c L100) - 创建字符串对象
2. **`createHashObject()`** (object.c L200) - 创建哈希对象
3. **`addReplyBulk()`** (networking.c L300) - 批量回复
4. **`dictFind()`** (dict.c L400) - 字典查找

### 持久化断点
1. **`rdbSaveBackground()`** (rdb.c L1000) - RDB 后台保存
2. **`aofRewriteBackground()`** (aof.c L800) - AOF 后台重写
3. **`rewriteAppendOnlyFileBackground()`** (aof.c L1200) - AOF 重写执行

### 主从复制断点
1. **`replicationFeedSlaves()`** (replication.c L500) - 向从节点发送命令
2. **`syncWithMaster()`** (replication.c L1000) - 与主节点同步
3. **`masterTryPartialResynchronization()`** (replication.c L1500) - 部分重同步

---

## 🔍 关键数据结构

### Redis 对象系统核心数据结构

```c
// server.h
// 1. Redis 对象（所有数据类型的统一抽象）
typedef struct redisObject {
    unsigned type:4;        // 对象类型（STRING/HASH/LIST/SET/ZSET）
    unsigned encoding:4;    // 编码方式（int/embstr/raw/hashtable/ziplist等）
    unsigned lru:LRU_BITS; // LRU 时间戳
    int refcount;           // 引用计数
    void *ptr;              // 指向实际数据的指针
} robj;

// 2. 字符串对象
struct sdshdr {
    unsigned int len;       // 字符串长度
    unsigned int free;      // 剩余空间
    char buf[];             // 字符数组
};

// 3. 哈希对象（字典）
typedef struct dict {
    dictType *type;         // 类型特定函数
    dictEntry **table;      // 哈希表数组
    unsigned long size;     // 哈希表大小
    unsigned long sizemask; // 哈希表大小掩码
    unsigned long used;     // 已使用节点数
} dict;

// 4. 列表对象（快速列表）
typedef struct quicklist {
    quicklistNode *head;    // 头节点
    quicklistNode *tail;    // 尾节点
    unsigned long count;    // 元素总数
    unsigned long len;      // 节点数量
    int fill;               // 每个节点的最大元素数
    unsigned int compress;   // 压缩深度
} quicklist;
```

### 事件循环核心数据结构

```c
// ae.h
// 1. 事件循环
typedef struct aeEventLoop {
    int maxfd;              // 最大文件描述符
    int setsize;            // 事件集合大小
    long long timeEventNextId; // 下一个时间事件 ID
    time_t lastTime;        // 上次处理时间事件的时间
    aeFileEvent *events;    // 文件事件数组
    aeFiredEvent *fired;    // 已就绪事件数组
    aeTimeEvent *timeEventHead; // 时间事件链表
    int stop;               // 停止标志
    void *apidata;          // 多路复用库的特定数据
    aeBeforeSleepProc *beforesleep; // 事件循环前的处理函数
    aeBeforeSleepProc *aftersleep;  // 事件循环后的处理函数
} aeEventLoop;

// 2. 文件事件
typedef struct aeFileEvent {
    int mask;               // 事件类型（AE_READABLE/AE_WRITABLE）
    aeFileProc *rfileProc;  // 读事件处理函数
    aeFileProc *wfileProc; // 写事件处理函数
    void *clientData;       // 客户端数据
} aeFileEvent;

// 3. 时间事件
typedef struct aeTimeEvent {
    long long id;           // 时间事件 ID
    long when_sec;          // 秒
    long when_ms;           // 毫秒
    aeTimeProc *timeProc;   // 时间事件处理函数
    aeEventFinalizerProc *finalizerProc; // 事件终结函数
    void *clientData;       // 客户端数据
    struct aeTimeEvent *prev; // 前驱节点
    struct aeTimeEvent *next; // 后继节点
} aeTimeEvent;
```

### 持久化核心数据结构

```c
// rdb.h
// 1. RDB 保存状态
typedef struct rdbSaveInfo {
    long long dirty;        // 修改的键数量
    long long start_time;   // 开始时间
    int save_type;          // 保存类型（RDB_SAVE_NONE/RDB_SAVE_AOF等）
} rdbSaveInfo;

// aof.h
// 2. AOF 缓冲区
struct redisServer {
    sds aof_buf;            // AOF 缓冲区
    int aof_fsync;          // AOF 同步策略
    int aof_state;          // AOF 状态
    int aof_rewrite_perc;   // AOF 重写百分比阈值
    int aof_rewrite_min_size; // AOF 重写最小大小
};
```

---

## 🧵 线程模型

### Redis 单线程事件循环模型
- **主线程**：单线程执行所有命令（`processCommand()`）
- **事件循环**：`aeMain()` 使用 epoll/kqueue/select 处理文件事件和时间事件
- **后台线程**：RDB/AOF 持久化在后台线程执行（`rdbSaveBackground()`、`aofRewriteBackground()`）

### 命令执行流程
```
客户端请求 -> acceptTcpHandler() -> 创建客户端 -> 读取命令 -> processCommand() -> call() -> 执行命令 -> addReply() -> 回复客户端
```

### 事件循环流程
```
aeMain() -> aeProcessEvents() -> 处理文件事件 -> 处理时间事件 -> beforesleep() -> 返回
```

---

## 📚 源码追踪（深入版）

### 案例1：命令执行流程（完整链路）

**完整调用链：**
```
客户端发送命令
  -> acceptTcpHandler() (networking.c L500)
    -> acceptCommonHandler() (networking.c L600)
      -> createClient() (networking.c L100)
        -> 创建客户端对象
          -> client *c = zmalloc(sizeof(client))
          -> 初始化客户端状态
  -> readQueryFromClient() (networking.c L1500)
    -> 读取命令到输入缓冲区
      -> c->querybuf = sdsMakeRoomFor(c->querybuf, readlen)
    -> processInputBuffer() (networking.c L2000)
      -> processCommand() (server.c L2800)
        -> lookupCommand() (server.c L2900)
          -> 查找命令表
            -> dictFind(server.commands, c->argv[0]->ptr)
        -> call() (server.c L3200)
          -> 执行命令
            -> c->cmd->proc(c)
          -> 记录慢查询
            -> slowlogPushEntryIfNeeded()
          -> 传播命令（主从复制）
            -> replicationFeedSlaves()
          -> 追加到 AOF
            -> feedAppendOnlyFile()
        -> addReply() (networking.c L200)
          -> 添加到回复缓冲区
            -> _addReplyToBuffer()
          -> 注册写事件
            -> aeCreateFileEvent(server.el, c->fd, AE_WRITABLE, sendReplyToClient, c)
```

**关键源码位置：**
- `processCommand()` - `server.c:2800`
- `call()` - `server.c:3200`
- `lookupCommand()` - `server.c:2900`
- `addReply()` - `networking.c:200`

**命令表查找机制：**
```c
// server.c
struct redisCommand *lookupCommand(sds name) {
    return dictFetchValue(server.commands, name);
}

// 命令注册
void populateCommandTable(void) {
    int j;
    struct redisCommand *c;
    
    for (j = 0; j < numcommands; j++) {
        c = redisCommandTable + j;
        dictAdd(server.commands, sdsnew(c->name), c);
    }
}
```

---

### 案例2：字符串对象实现（深入机制）

**字符串对象编码方式：**
1. **INT 编码**：整数字符串（`OBJ_ENCODING_INT`）
2. **EMBSTR 编码**：短字符串（≤44字节，`OBJ_ENCODING_EMBSTR`）
3. **RAW 编码**：长字符串（>44字节，`OBJ_ENCODING_RAW`）

**字符串对象创建流程：**
```c
// object.c
robj *createStringObject(const char *ptr, size_t len) {
    if (len <= OBJ_ENCODING_EMBSTR_SIZE_LIMIT) {
        return createEmbeddedStringObject(ptr, len);
    } else {
        return createRawStringObject(ptr, len);
    }
}

// EMBSTR 编码（对象和字符串在同一内存块）
robj *createEmbeddedStringObject(const char *ptr, size_t len) {
    robj *o = zmalloc(sizeof(robj)+sizeof(struct sdshdr8)+len+1);
    struct sdshdr8 *sh = (void*)(o+1);
    
    o->type = OBJ_STRING;
    o->encoding = OBJ_ENCODING_EMBSTR;
    o->ptr = sh+1;
    o->refcount = 1;
    
    sh->len = len;
    sh->alloc = len;
    sh->flags = SDS_TYPE_8;
    if (ptr) {
        memcpy(sh->buf, ptr, len);
        sh->buf[len] = '\0';
    } else {
        memset(sh->buf, 0, len+1);
    }
    
    return o;
}
```

**SDS（Simple Dynamic String）优势：**
- O(1) 获取长度（`len` 字段）
- 二进制安全（不以 `\0` 结尾）
- 预分配空间（减少内存重分配）
- 兼容 C 字符串（`buf` 字段）

---

### 案例3：哈希对象实现（深入机制）

**哈希对象编码方式：**
1. **ZIPLIST 编码**：小哈希表（≤512个元素，所有值≤64字节）
2. **HASHTABLE 编码**：大哈希表（超过 ZIPLIST 限制）

**哈希表实现（字典）：**
```c
// dict.c
// 1. 字典结构
typedef struct dict {
    dictType *type;         // 类型特定函数
    dictEntry **table;      // 哈希表数组（两个，用于 rehash）
    unsigned long size;     // 哈希表大小
    unsigned long sizemask; // 哈希表大小掩码（size-1）
    unsigned long used;     // 已使用节点数
    int rehashidx;          // rehash 索引（-1表示未进行 rehash）
} dict;

// 2. 哈希表节点
typedef struct dictEntry {
    void *key;              // 键
    union {
        void *val;
        uint64_t u64;
        int64_t s64;
        double d;
    } v;                    // 值
    struct dictEntry *next; // 指向下一个节点（解决哈希冲突）
} dictEntry;

// 3. 哈希算法（MurmurHash2）
uint64_t dictGenHashFunction(const void *key, int len) {
    return MurmurHash2(key, len, 5381);
}
```

**渐进式 Rehash 机制：**
```c
// dict.c
// 1. 触发 rehash 的条件
if (d->ht[0].used >= d->ht[0].size && 
    (dict_can_resize || d->ht[0].used/d->ht[0].size > dict_force_resize_ratio)) {
    return dictExpand(d, d->ht[0].used*2);
}

// 2. 渐进式 rehash（每次 rehash 一个桶）
int dictRehash(dict *d, int n) {
    int empty_visits = n*10; // 最多访问 n*10 个空桶
    
    if (!dictIsRehashing(d)) return 0;
    
    while(n-- && d->ht[0].used != 0) {
        dictEntry *de, *nextde;
        
        // 找到非空桶
        while(d->ht[0].table[d->rehashidx] == NULL) {
            d->rehashidx++;
            if (--empty_visits == 0) return 1;
        }
        
        // 迁移该桶的所有节点
        de = d->ht[0].table[d->rehashidx];
        while(de) {
            uint64_t h;
            nextde = de->next;
            h = dictHashKey(d, de->key) & d->ht[1].sizemask;
            de->next = d->ht[1].table[h];
            d->ht[1].table[h] = de;
            d->ht[0].used--;
            d->ht[1].used++;
            de = nextde;
        }
        d->ht[0].table[d->rehashidx] = NULL;
        d->rehashidx++;
    }
    
    // 检查是否完成 rehash
    if (d->ht[0].used == 0) {
        zfree(d->ht[0].table);
        d->ht[0] = d->ht[1];
        _dictReset(&d->ht[1]);
        d->rehashidx = -1;
        return 0;
    }
    
    return 1;
}
```

---

### 案例4：RDB 持久化机制（深入流程）

**RDB 保存流程：**
```
bgsave 命令
  -> rdbSaveBackground() (rdb.c L1000)
    -> fork() 创建子进程
      -> 子进程执行 rdbSave()
        -> rdbSave() (rdb.c L1200)
          -> 打开 RDB 文件
            -> fp = fopen(tmpfile, "w")
          -> 写入 RDB 头部
            -> rdbSaveHeader()
          -> 遍历数据库
            -> for (j = 0; j < server.dbnum; j++)
              -> 遍历键空间
                -> dictScan()
                  -> 保存键值对
                    -> rdbSaveKeyValuePair()
          -> 写入 RDB 尾部
            -> rdbSaveFooter()
          -> 同步到磁盘
            -> fflush() -> fsync()
          -> 重命名临时文件
            -> rename(tmpfile, filename)
      -> 父进程继续处理命令
        -> 记录后台保存信息
          -> server.rdb_child_pid = childpid
```

**RDB 文件格式：**
```
+------------------+
| RDB 头部（5字节） |
+------------------+
| 数据库 0         |
| 数据库 1         |
| ...              |
+------------------+
| RDB 尾部（1字节） |
+------------------+
```

**关键源码位置：**
- `rdbSaveBackground()` - `rdb.c:1000`
- `rdbSave()` - `rdb.c:1200`
- `rdbSaveKeyValuePair()` - `rdb.c:800`

---

### 案例5：AOF 持久化机制（深入流程）

**AOF 追加流程：**
```
命令执行
  -> call() (server.c L3200)
    -> feedAppendOnlyFile() (aof.c L500)
      -> 格式化命令
        -> catAppendOnlyGenericCommand()
      -> 追加到 AOF 缓冲区
        -> server.aof_buf = sdscatlen(server.aof_buf, buf, len)
      -> 根据同步策略写入磁盘
        -> flushAppendOnlyFile() (aof.c L600)
          -> write() 写入系统缓冲区
            -> write(server.aof_fd, server.aof_buf, sdslen(server.aof_buf))
          -> fsync() 同步到磁盘（根据策略）
            -> if (server.aof_fsync == AOF_FSYNC_ALWAYS) fsync()
            -> if (server.aof_fsync == AOF_FSYNC_EVERYSEC) aof_background_fsync()
```

**AOF 重写流程：**
```
BGREWRITEAOF 命令
  -> rewriteAppendOnlyFileBackground() (aof.c L1200)
    -> fork() 创建子进程
      -> 子进程执行 rewriteAppendOnlyFile()
        -> 创建临时 AOF 文件
          -> snprintf(tmpfile, 256, "temp-rewriteaof-%d.aof", (int)getpid())
        -> 遍历数据库
          -> for (j = 0; j < server.dbnum; j++)
            -> 遍历键空间
              -> dictScan()
                -> 重写键值对
                  -> rewriteAppendOnlyFileRio()
        -> 同步到磁盘
          -> fflush() -> fsync()
        -> 发送信号给父进程
          -> kill(getppid(), SIGUSR1)
      -> 父进程继续处理命令
        -> 记录后台重写信息
          -> server.aof_child_pid = childpid
        -> 接收子进程信号
          -> backgroundRewriteDoneHandler()
            -> 合并增量 AOF
              -> aofRewriteBufferWrite()
```

**AOF 同步策略：**
- **always**：每个命令都同步（最安全，性能最低）
- **everysec**：每秒同步一次（平衡安全性和性能）
- **no**：由操作系统决定（性能最高，安全性最低）

---

### 案例6：主从复制机制（深入流程）

**全量复制流程：**
```
SLAVEOF 命令
  -> replicationSetMaster() (replication.c L200)
    -> connectWithMaster() (replication.c L400)
      -> 连接主节点
        -> anetTcpNonBlockConnect()
      -> 发送 PING
        -> sendSynchronousCommand()
      -> 发送 REPLCONF
        -> sendSynchronousCommand()
      -> 发送 PSYNC
        -> sendSynchronousCommand("PSYNC", "?", "-1", NULL)
        -> 接收 FULLRESYNC 响应
          -> masterTryPartialResynchronization() (replication.c L1500)
            -> 执行全量复制
              -> syncWithMaster() (replication.c L1000)
                -> 接收 RDB 文件
                  -> readSyncBulkPayload()
                -> 清空数据库
                  -> emptyDb()
                -> 加载 RDB
                  -> rdbLoad()
```

**增量复制流程：**
```
主节点执行命令
  -> call() (server.c L3200)
    -> replicationFeedSlaves() (replication.c L500)
      -> 遍历所有从节点
        -> listIter li; listRewind(server.slaves, &li)
          -> 发送命令到从节点
            -> addReplyReplicationBacklog()
              -> 添加到复制积压缓冲区
                -> server.repl_backlog = sdscatlen(server.repl_backlog, ...)
```

**复制积压缓冲区（Replication Backlog）：**
```c
// server.h
struct redisServer {
    char *repl_backlog;         // 复制积压缓冲区
    long long repl_backlog_size; // 缓冲区大小
    long long repl_backlog_histlen; // 缓冲区历史长度
    long long repl_backlog_idx;  // 缓冲区索引
    long long repl_backlog_off;  // 缓冲区偏移量
};
```

---

## 🧪 基于源码扩展实验

### 实验1：自定义 Redis 命令（C 模块开发）

**目标**：实现自定义 Redis 命令，统计字符串长度。

**实现：**
```c
// mymodule.c
#include "redismodule.h"

// 自定义命令：MYSTRLEN key
int MyStrLen_RedisCommand(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {
    if (argc != 2) {
        return RedisModule_WrongArity(ctx);
    }
    
    RedisModuleKey *key = RedisModule_OpenKey(ctx, argv[1], REDISMODULE_READ);
    if (RedisModule_KeyType(key) != REDISMODULE_KEYTYPE_STRING) {
        RedisModule_CloseKey(key);
        return RedisModule_ReplyWithError(ctx, "ERR key is not a string");
    }
    
    size_t len;
    RedisModuleString *str = RedisModule_StringDMA(key, &len, REDISMODULE_READ);
    RedisModule_ReplyWithLongLong(ctx, len);
    RedisModule_CloseKey(key);
    
    return REDISMODULE_OK;
}

// 模块初始化
int RedisModule_OnLoad(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {
    if (RedisModule_Init(ctx, "mymodule", 1, REDISMODULE_APIVER_1) == REDISMODULE_ERR) {
        return REDISMODULE_ERR;
    }
    
    if (RedisModule_CreateCommand(ctx, "mystrlen", MyStrLen_RedisCommand, "readonly", 1, 1, 1) == REDISMODULE_ERR) {
        return REDISMODULE_ERR;
    }
    
    return REDISMODULE_OK;
}
```

**编译和使用：**
```bash
# 编译模块
gcc -fPIC -shared -o mymodule.so mymodule.c -I /path/to/redis/src

# 加载模块
redis-cli MODULE LOAD /path/to/mymodule.so

# 使用命令
redis-cli MYSTRLEN mykey
```

---

### 实验2：自定义 Lua 脚本（原子操作）

**目标**：实现原子性的计数器递增和过期设置。

**实现：**
```python
# redis_lua_script.py
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Lua 脚本：原子性递增并设置过期时间
lua_script = """
local current = redis.call('GET', KEYS[1])
if current == false then
    current = 0
end
local new_value = current + ARGV[1]
redis.call('SET', KEYS[1], new_value)
if tonumber(ARGV[2]) > 0 then
    redis.call('EXPIRE', KEYS[1], ARGV[2])
end
return new_value
"""

script = r.register_script(lua_script)

# 使用脚本
result = script(keys=['counter'], args=[1, 3600])  # 递增1，设置过期时间3600秒
print(f"Counter value: {result}")
```

**验证**：多线程并发执行，观察计数器是否原子性递增。

---

### 实验3：自定义数据结构（使用 Redis Module）

**目标**：实现自定义的布隆过滤器数据结构。

**实现：**
```c
// bloomfilter.c
#include "redismodule.h"
#include <stdint.h>
#include <string.h>

// 布隆过滤器结构
typedef struct {
    uint8_t *bits;      // 位数组
    size_t size;        // 位数组大小
    uint32_t hash_count; // 哈希函数数量
} BloomFilter;

// 创建布隆过滤器
BloomFilter* BloomFilter_Create(size_t size, uint32_t hash_count) {
    BloomFilter *bf = RedisModule_Alloc(sizeof(BloomFilter));
    bf->bits = RedisModule_Calloc(size, sizeof(uint8_t));
    bf->size = size;
    bf->hash_count = hash_count;
    return bf;
}

// 添加元素
void BloomFilter_Add(BloomFilter *bf, const char *key, size_t keylen) {
    for (uint32_t i = 0; i < bf->hash_count; i++) {
        uint32_t hash = MurmurHash2(key, keylen, i) % (bf->size * 8);
        bf->bits[hash / 8] |= (1 << (hash % 8));
    }
}

// 检查元素是否存在
int BloomFilter_Contains(BloomFilter *bf, const char *key, size_t keylen) {
    for (uint32_t i = 0; i < bf->hash_count; i++) {
        uint32_t hash = MurmurHash2(key, keylen, i) % (bf->size * 8);
        if (!(bf->bits[hash / 8] & (1 << (hash % 8)))) {
            return 0; // 不存在
        }
    }
    return 1; // 可能存在
}
```

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
| SET | 100000 | <1ms | 单机 |
| GET | 100000 | <1ms | 单机 |
| HGETALL | 50000 | <2ms | Hash |
| LPUSH | 80000 | <1ms | List |
| ZADD | 60000 | <2ms | Sorted Set |

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

1. **数据结构核心**
   - Redis 对象系统（统一抽象）
   - SDS（字符串优化）
   - 字典（哈希表实现）
   - 渐进式 Rehash（避免阻塞）

2. **持久化核心**
   - RDB：快照备份，恢复快
   - AOF：追加日志，数据安全
   - 混合模式：RDB + AOF

3. **高可用核心**
   - 主从复制：读写分离
   - 哨兵模式：自动故障转移
   - 集群模式：水平扩展

4. **性能优化核心**
   - 单线程事件循环（避免锁竞争）
   - 管道批量操作（减少网络往返）
   - 合理设置过期时间（避免内存泄漏）

5. **扩展点**
   - Redis Module：自定义命令和数据结构
   - Lua 脚本：原子操作
   - 客户端扩展：连接池、集群客户端
