 # MongoDB 学习总览

 `mongoDB/` 模块整理了 MongoDB 在实际开发中需要掌握的主要知识点，并将它们与 `cases/` + `data/` + `scripts/` 中的案例和验证数据对应起来。

 与 `GUIDE.md` 的学习路径相比，本文件更偏向“知识点清单 + 案例索引”。

 ---

 ## 一、核心概念与对象

 ### 1. 文档模型

 - 文档（Document）：一条记录，以 BSON/JSON 形式存储。
 - 集合（Collection）：一组文档，相当于关系型中的“表”。
 - 数据库（Database）：集合的逻辑容器。

 ### 2. 与关系型数据库的对应

 | 关系型           | MongoDB          |
 |------------------|------------------|
 | 数据库（Database） | 数据库（Database） |
 | 表（Table）      | 集合（Collection） |
 | 行（Row）        | 文档（Document）   |
 | 列（Column）     | 字段（Field）     |

 **对应案例：**
 - `cases/user_profile_modeling.md`

 ---

 ## 二、数据类型与基础操作

 ### 1. 常用数据类型（BSON）

 - 字符串：`String`
 - 数字：`NumberInt / NumberLong / NumberDecimal`
 - 布尔：`Boolean`
 - 日期：`Date`
 - 数组：`Array`
 - 对象：`Document`

 ### 2. 基础 CRUD

 - 插入：`insertOne()` / `insertMany()`
 - 查询：`find()` / `findOne()`
 - 更新：`updateOne()` / `updateMany()`
 - 删除：`deleteOne()` / `deleteMany()`

 **对应案例：**
 - `cases/user_profile_modeling.md`

 ---

 ## 三、文档建模与索引

 ### 1. 文档建模

 - 嵌入文档（Embedded Documents）：适合紧密关联、一起读取的数据。
 - 引用（References）：适合复用/解耦，或数据量较大的关联。
 - 一对多、多对多建模模式。

 ### 2. 索引

 - 单字段索引：`db.collection.createIndex({ field: 1 })`
 - 复合索引：`{ field1: 1, field2: -1 }`
 - 唯一索引：`{ unique: true }`

 **对应案例：**
 - `cases/user_profile_modeling.md`
 - `scripts/setup_collections.js`

 ---

 ## 四、聚合管道（Aggregation Pipeline）

 ### 1. 常见阶段

 - `$match`：过滤文档（类似 SQL 的 `WHERE`）
 - `$project`：投影字段（`SELECT` 某些列）
 - `$group`：分组聚合（`GROUP BY` + 聚合函数）
 - `$sort`：排序（`ORDER BY`）
 - `$limit / $skip`：分页
 - `$lookup`：集合关联（类似左连接）

 ### 2. 使用场景

 - 销售统计：按时间/城市/用户维度分析订单（案例2）。
 - 日志统计：按事件类型/页面/设备统计行为（案例3）。

 **对应案例：**
 - `cases/order_sales_analysis.md`
 - `cases/event_log_analysis.md`

 ---

 ## 五、事务与副本集（概要）

 ### 1. 单文档原子性

 - 单个文档的更新（包括嵌入文档）天然是原子操作。

 ### 2. 多文档事务（了解）

 - 需要运行在副本集或分片集群上。
 - 使用会话（`session`）与事务 API：
   - `session.startTransaction()` / `session.commitTransaction()` / `session.abortTransaction()`

 ### 3. 副本集与分片（概念性了解）

 - 副本集：高可用与读扩展。
 - 分片：水平扩展海量数据。

 ---

 ## 六、知识点与案例/数据对照表

 | 模块               | 关键知识点                         | 案例文档                     | 数据文件              | 脚本文件                |
 |--------------------|------------------------------------|------------------------------|-----------------------|-------------------------|
 | 文档模型与 CRUD    | 文档/集合、插入/查询/更新/删除     | `user_profile_modeling.md`   | `users.json`          | `setup_collections.js`,`load_data.js` |
 | 订单与销售分析     | 聚合管道、分组统计、排序与过滤     | `order_sales_analysis.md`    | `orders.json`,`users.json` | `common_queries.js`     |
 | 事件日志分析       | JSON 文档、聚合统计                | `event_log_analysis.md`      | `events.jsonl`        | `common_queries.js`     |

 ---

 ## 七、如何使用本模块学习

 1. 阅读 `GUIDE.md`，了解整体学习路线与环境准备方式（安装 MongoDB、使用 `mongosh` 等）。
 2. 在 `mongoDB/` 目录下依次运行：
    - `scripts/setup_collections.js`：创建数据库、集合与索引。
    - `scripts/load_data.js`：从 `data/` 加载用户、订单与事件日志。
    - `scripts/common_queries.js`：执行常用查询与聚合。
 3. 打开 `cases/` 中的三个案例文档，对照里面的说明在 `mongosh` 中修改和扩展查询。

 当你能够：

 - 为一个业务场景设计合理的 MongoDB 文档结构；
 - 使用 CRUD 与索引高效完成常见读写操作；
 - 基于聚合管道完成多维度统计与分析；

 基本就掌握了 MongoDB 在日常开发中的核心用法。

