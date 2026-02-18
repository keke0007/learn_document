## Redis 学习指南（缓存 & 存储）

## 📚 项目概述

本指南在 `redis/` 目录下，参考 `hive/`、`clickhouse/`、`doris/`、`oracle/`、`PostgreSQL/`、`mongoDB/`、`elasticsearch/` 等模块的组织方式，提供一套系统的 **Redis 学习路径**，重点覆盖：

- **核心知识点**：数据结构（String/Hash/List/Set/ZSet）、键过期与内存淘汰、事务与 Lua、持久化（RDB/AOF）、发布订阅、简单分布式锁。
- **案例场景**：缓存热点数据（用户/商品）、排行榜、计数器与限流、简单消息队列。
- **验证数据**：小规模示例数据（用户信息、访问计数、排行榜等），方便在本地 Redis 实例中动手练习。

---

## 📁 项目结构

```
redis/
├── README.md                      # Redis 知识点总览（详细文档）
├── GUIDE.md                       # 本指南文档（学习路径 + 快速上手）
├── cases/                         # 实战案例目录
│   ├── basic_datatypes.md         # 案例1：基础数据结构与常用命令
│   ├── cache_user_profile.md      # 案例2：用户信息缓存与过期策略
│   └── ranking_and_counter.md     # 案例3：排行榜与计数/限流
├── data/                          # 验证数据（简单文本/JSON）
│   ├── users.json                 # 用户基本信息示例
│   └── hot_keys.txt               # 热点 Key 示例说明
└── scripts/                       # redis-cli 脚本示例（示意）
    ├── basic_datatypes.redis      # 基础数据结构命令
    ├── cache_user_profile.redis   # 缓存用户信息相关命令
    └── ranking_and_counter.redis  # 排行榜与计数器相关命令
```

---

## 🎯 学习路径（建议 2~3 天）

### 阶段一：基础入门（0.5 天）

- 安装与启动 Redis，本地通过 `redis-cli` 连接。
- 认识数据库/Key/Value 概念。

### 阶段二：核心数据结构与命令（1 天）

- String / Hash / List / Set / Sorted Set 的典型用法（案例1）。
- 键过期与 TTL：`EXPIRE` / `TTL`。

### 阶段三：缓存与业务场景（1~1.5 天）

- 用户信息缓存：缓存穿透/雪崩的简单处理思路（案例2）。
- 排行榜与计数器：活动排行榜、访问计数、简单限流（案例3）。
- 简单事务（`MULTI/EXEC`）与 Lua 概念（了解）。

---

## 🚀 快速开始

> 假设本地 Redis 运行在 `127.0.0.1:6379`。

### 步骤1：连接 Redis

```bash
redis-cli -h 127.0.0.1 -p 6379
```

### 步骤2：基础命令练习（可参考 `scripts/basic_datatypes.redis`）

```bash
# String
SET user:1:name "张三"
GET user:1:name

# Hash
HSET user:1 name "张三" age 25 city "北京"
HGETALL user:1

# List
LPUSH recent_logs "log1"
LPUSH recent_logs "log2"
LRANGE recent_logs 0 -1
```

### 步骤3：根据 `cases/` 文档完成缓存、排行榜等场景练习

---

## 📖 核心知识点速查

- **数据结构**：String / Hash / List / Set / Sorted Set。
- **过期策略**：`EXPIRE key seconds`、`TTL key`。
- **持久化**（了解）：RDB 快照与 AOF 日志。
- **简单事务与 Lua**：`MULTI/EXEC`、`EVAL`，常用于计数/扣减等原子操作。

---

## 📊 验证数据说明

- `data/users.json`：用户 ID 与基础信息样例，用于构造缓存 Key 与 Hash 结构。
- `data/hot_keys.txt`：热点 Key 示例说明（如 `user:<id>`、`product:<id>`、`rank:<name>` 等）。

---

## 🔧 实战案例概览

- `basic_datatypes.md`：所有基础数据结构与常用命令的集中练习。
- `cache_user_profile.md`：设计用户信息缓存 Key、设置过期与缓存更新策略。
- `ranking_and_counter.md`：使用 Sorted Set + String 实现排行榜与计数/限流。

---

## ✅ 学习检查清单

- [ ] 能够熟练使用 Redis 五大基础数据结构。
- [ ] 能够为简单缓存场景设计 Key 与过期策略。
- [ ] 能够使用 Sorted Set 和计数器完成排行榜与统计需求。

---

## 🎓 学习成果

完成本指南后，你将能够：

- 将 Redis 用作应用的高性能缓存层。
- 在 Redis 中实现基础排行榜、计数与简单限流功能。
- 理解 Redis 在“高读写、低延迟”场景下的典型用法。

