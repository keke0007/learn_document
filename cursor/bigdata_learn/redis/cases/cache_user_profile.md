# 案例2：用户信息缓存与过期策略（Redis）

## 一、案例目标

- 使用 Redis 缓存数据库中的用户信息，减少数据库压力。
- 设计合理的 Key、过期时间与更新流程。

---

## 二、Key 设计与结构

- 用户信息缓存 Key：`cache:user:<id>`
  - 类型：Hash
  - 字段：`name`、`age`、`city` 等。

示例：

```bash
HSET cache:user:1 name "张三" age 25 city "北京"
EXPIRE cache:user:1 3600   # 缓存 1 小时
```

---

## 三、典型读写流程（伪代码）

### 1. 读取用户信息（读缓存 + 回源）

1. 从 Redis 读取 `cache:user:<id>`：
   - 如果命中，直接返回。
   - 未命中，则从 DB 查询，并写入 Redis，设置过期，再返回。

### 2. 更新用户信息

1. 先更新 DB。
2. 同步更新或删除 Redis 对应 Key：
   - 方式一：`DEL cache:user:<id>`，下次访问重新加载。
   - 方式二：直接更新 Hash 字段。

---

## 四、示例命令（可参考 `scripts/cache_user_profile.redis`）

```bash
# 假设从 DB 查到用户数据后，写入缓存
HSET cache:user:1 name "张三" age 25 city "北京"
EXPIRE cache:user:1 3600

# 读取
HGETALL cache:user:1
TTL cache:user:1
```

---

## 五、练习建议

1. 为 `users.json` 中的各个用户构造缓存，并对其中部分设置不同 TTL，观察过期行为。  
2. 思考并记录如何防止“缓存雪崩”（如随机过期时间）与“缓存穿透”（如空值缓存）。  

