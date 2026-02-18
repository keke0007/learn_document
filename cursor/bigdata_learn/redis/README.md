# Redis 学习总览

`redis/` 模块整理了 Redis 在缓存、计数和排行榜场景中的主要知识点，并将它们与 `cases/` + `data/` + `scripts/` 中的案例和验证数据对应起来。

---

## 一、核心知识点概览

- 数据结构：String / Hash / List / Set / Sorted Set。
- 过期与淘汰：TTL、过期策略（了解 LFU/LRU）。
- 持久化：RDB / AOF 基础概念。
- 典型场景：缓存、排行榜、计数器与限流、简单消息队列（List/Stream）。

---

## 二、知识点与案例/数据对照表

| 模块                 | 关键知识点                               | 案例文档                    | 数据文件         | 脚本文件                      |
|----------------------|------------------------------------------|-----------------------------|------------------|-------------------------------|
| 基础数据结构         | String/Hash/List/Set/ZSet 常用命令       | `basic_datatypes.md`       | `users.json`     | `basic_datatypes.redis`       |
| 用户缓存             | Key 设计、TTL 设置、缓存读写策略         | `cache_user_profile.md`    | `users.json`     | `cache_user_profile.redis`    |
| 排行榜与计数/限流    | Sorted Set 排行榜、计数器、自增与过期    | `ranking_and_counter.md`   | `hot_keys.txt`   | `ranking_and_counter.redis`   |

---

## 三、如何使用本模块学习

1. 阅读 `GUIDE.md` 了解学习路径与环境准备（安装 Redis、使用 `redis-cli`）。
2. 打开 `cases/` 中的案例文档，对照 `scripts/` 下的 `.redis` 文件在 `redis-cli` 中逐条执行命令。
3. 根据 `data/` 中的样例，扩展自己的 Key 数据与测试场景。

当你能够：

- 熟练掌握基础数据结构的使用；
- 为常见业务设计合适的 Redis Key 和过期策略；
- 用 Sorted Set 和自增计数实现简单排行榜和统计；

就基本具备了在项目中使用 Redis 解决性能与缓存问题的能力。

