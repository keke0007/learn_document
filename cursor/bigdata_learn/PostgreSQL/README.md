 # PostgreSQL 学习总览

 `PostgreSQL/` 模块整理了 PostgreSQL 在实际开发中需要掌握的主要知识点，并将它们与 `cases/` + `data/` + `scripts/` 中的案例和验证数据对应起来。

 与 `GUIDE.md` 的学习路径相比，本文件更偏向“知识点清单 + 案例索引”。

 ---

 ## 一、架构与基础对象

 ### 1. 核心概念

 - 数据库（Database）：逻辑数据库实例，如 `bigdata_learn`
 - Schema：命名空间，如 `bigdata_demo`
 - 表（Table）、索引（Index）、视图（View）、序列（Sequence）
 - 角色（Role）与权限（Privileges）

 ### 2. 连接与工具

 - 命令行客户端：`psql`
 - 图形工具：pgAdmin 等
 - 连接字符串：`postgresql://user:password@host:5432/bigdata_learn`

 **对应案例：**
 - `GUIDE.md` 中的环境说明

 ---

 ## 二、数据类型与约束

 ### 1. 常用数据类型

 - 数值：`smallint` / `integer` / `bigint` / `numeric(p,s)`
 - 字符：`varchar(n)` / `text`
 - 时间：`date` / `timestamp [with time zone]`
 - 布尔：`boolean`
 - JSON：`json` / `jsonb`

 ### 2. 约束类型

 - 主键：`PRIMARY KEY`
 - 唯一：`UNIQUE`
 - 非空：`NOT NULL`
 - 检查：`CHECK`
 - 外键：`FOREIGN KEY ... REFERENCES ...`

 **对应案例：**
 - `cases/employee_management.md`  
 - `cases/sales_analysis.md`

 ---

 ## 三、基础 SQL 与数据建模

 ### 1. DDL / DML / DQL

 - DDL：`CREATE / ALTER / DROP TABLE ...`
 - DML：`INSERT / UPDATE / DELETE`
 - 查询：`SELECT` + 过滤/排序/聚合（`WHERE / ORDER BY / GROUP BY / HAVING`）

 ### 2. 多表关联

 - 内连接：`INNER JOIN`
 - 外连接：`LEFT JOIN / RIGHT JOIN`
 - 多表连接链路（客户-订单-产品）

 **对应案例：**
 - `cases/employee_management.md`：员工 & 部门
 - `cases/sales_analysis.md`：订单 & 销售

 ---

 ## 四、索引、执行计划与优化（入门）

 ### 1. 索引类型

 - B-tree 索引（默认）
 - 组合索引：多列
 - 部分索引（带 WHERE 条件）
 - 表达式索引（基于函数）

 ### 2. 执行计划

 - `EXPLAIN` / `EXPLAIN ANALYZE` 查看计划与实际耗时
 - 关注：Seq Scan / Index Scan / Index Only Scan 等

 ### 3. 优化思路

 - 为高频过滤/连接字段建索引
 - 避免对索引列使用不必要的函数封装
 - 保持统计信息更新（`ANALYZE`）

 **对应案例：**
 - `cases/sales_analysis.md` + `scripts/common_queries.sql`

 ---

 ## 五、事务、锁与并发控制（概要）

 ### 1. 事务控制

 - 显式事务：`BEGIN; ... COMMIT;` / `ROLLBACK;`
 - 保存点：`SAVEPOINT sp; ROLLBACK TO sp;`

 ### 2. 隔离级别

 - `READ COMMITTED`（默认）：每条语句看到的是已提交最新数据
 - `REPEATABLE READ`：事务内部多次查询看到一致快照
 - `SERIALIZABLE`：最强隔离（代价较高）

 ### 3. MVCC 与锁

 - 行级锁：`FOR UPDATE` 等
 - MVCC：通过版本链和快照实现非阻塞读

 **对应案例：**
 - 可参考 `oracle/cases/transaction_concurrency.md` 的思路，在 PostgreSQL 上做对比实验

 ---

 ## 六、CTE、窗口函数与 JSONB

 ### 1. 公共表表达式（CTE）

 - `WITH ... AS (...) SELECT ...`  
 - 适合拆解复杂查询、递归查询（`WITH RECURSIVE`）

 ### 2. 窗口函数

 - 排序与分组窗口：`ROW_NUMBER / RANK / DENSE_RANK`
 - 窗口聚合：`SUM(...) OVER (...)`、`AVG(...) OVER (...)`

 ### 3. JSONB

 - 字段：`jsonb`
 - 操作符：`->` / `->>` / `@>` / `?` 等
 - 索引：`GIN` 索引加速 JSONB 查询

 **对应案例：**
 - `cases/sales_analysis.md`（窗口函数、CTE 可扩展）  
 - `cases/json_event_analysis.md`（JSONB 核心示例）

 ---

 ## 七、知识点与案例/数据对照表

 | 模块             | 关键知识点                                 | 案例文档                    | 数据文件                               | 脚本文件                    |
 |------------------|--------------------------------------------|-----------------------------|----------------------------------------|-----------------------------|
 | 架构与基础对象   | 数据库/Schema/角色                         | `GUIDE.md`                  | -                                      | `setup_schema.sql`（示意） |
 | 员工与部门建模   | 主键/外键、索引、聚合统计                  | `employee_management.md`    | `employees.csv`,`departments.csv`      | `setup_tables.sql`,`load_data.sql` |
 | 订单与销售分析   | 多表关联、聚合、窗口函数、CTE              | `sales_analysis.md`         | `customers.csv`,`products.csv`,`orders.csv` | `common_queries.sql`        |
 | JSON 事件日志分析| JSONB 存储与查询、GIN 索引                 | `json_event_analysis.md`    | `events.jsonl`                         | `setup_tables.sql`,`load_data.sql` |

 ---

 ## 八、如何使用本模块学习

 1. 阅读 `GUIDE.md`，按步骤创建数据库和 Schema，并执行 `setup_tables.sql` 和 `load_data.sql`。
 2. 使用 `\copy` 或 `COPY` 从 `data/` 导入 CSV/JSONL 数据。
 3. 依次实践 `cases/employee_management.md`、`cases/sales_analysis.md`、`cases/json_event_analysis.md` 中的示例查询。
 4. 在 `scripts/common_queries.sql` 的基础上增加自己的查询和实验（如新的窗口函数、JSON 结构等）。

 当你能够：

 - 熟练设计并创建表、约束与索引；
 - 编写多表关联、窗口函数和 CTE 查询；
 - 使用 JSONB 存储并分析半结构化数据；

 基本就具备了在日常开发中有效使用 PostgreSQL 的核心能力。

