# 案例3：排行榜与计数/限流（Redis）

## 一、案例目标

- 使用 Sorted Set 实现简单排行榜。
- 使用 String 计数器实现访问统计与基础限流。

---

## 二、排行榜（Sorted Set）

Key 设计：`rank:event2024`

示例命令（可参考 `scripts/ranking_and_counter.redis`）：

```bash
ZADD rank:event2024 100 "user1"
ZADD rank:event2024 200 "user2"
ZADD rank:event2024 150 "user3"

ZREVRANGE rank:event2024 0 -1 WITHSCORES          # 查看排行榜
ZREVRANK rank:event2024 "user1"                   # 查看 user1 排名
ZINCRBY rank:event2024 50 "user1"                 # 为 user1 增加得分
```

---

## 三、计数器与简单限流（String + EXPIRE）

示例：统计接口 `/api/login` 每分钟访问次数：

Key 设计：`cnt:login:<yyyyMMddHHmm>`

```bash
INCR cnt:login:202403141000
EXPIRE cnt:login:202403141000 120   # 保留 2 分钟
```

伪代码：

1. 计算当前分钟 Key。
2. `INCR` 计数并设置短过期。
3. 如果计数超过阈值（如每分钟 > 100），则拒绝请求，实现简单限流。

---

## 四、练习建议

1. 基于 `data/hot_keys.txt` 中的示例，设计多个排行榜（如日榜、总榜）并操作试验。  
2. 为不同接口设计不同的限流 Key，观察在高并发下计数器行为。  

