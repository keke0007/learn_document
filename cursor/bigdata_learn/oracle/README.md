 # Oracle 学习总览

 本文是 `oracle/` 模块的总览文档，整理 Oracle 数据库在实际开发中需要掌握的主要知识点，并将它们与 `cases/` + `data/` + `scripts/` 中的案例和验证数据关联起来。

 与 `GUIDE.md` 的学习路线不同，这里更偏向“知识点清单 + 案例索引”。

 ---

 ## 一、架构与基础对象

 ### 1. 核心架构

 - **实例（Instance）**：内存结构（SGA）+ 后台进程（DBWn、LGWR、SMON、PMON等）
 - **数据库（Database）**：数据文件、控制文件、重做日志文件（Redo Log）
 - **表空间（Tablespace）**：逻辑存储单元，包含若干数据文件
 - **Schema（用户）**：拥有一组数据库对象的命名空间

 ### 2. 常见对象

 - 表（Table）
 - 索引（Index）
 - 视图（View）
 - 序列（Sequence）
 - 同义词（Synonym）
 - 存储过程/函数/包（PL/SQL）

 **对应案例：**
 - `cases/employee_management.md`：基础表与外键、索引使用

 ---

 ## 二、数据类型与约束

 ### 1. 常用数据类型

 - `NUMBER(p,s)`：数值类型（ID、金额、数量）
 - `VARCHAR2(n)`：变长字符串（姓名、城市等）
 - `CHAR(n)`：定长字符串（性别、状态码等）
 - `DATE`：日期 + 时间
 - `TIMESTAMP`：高精度时间

 ### 2. 约束类型

 - `PRIMARY KEY`：主键约束
 - `UNIQUE`：唯一约束
 - `NOT NULL`：非空约束
 - `FOREIGN KEY`：外键约束
 - `CHECK`：自定义检查约束

 **对应案例：**
 - `cases/employee_management.md` 使用主键、外键和非空约束

 ---

 ## 三、SQL 查询与数据建模

 ### 1. DDL / DML / DQL

 - DDL：`CREATE / ALTER / DROP`  
 - DML：`INSERT / UPDATE / DELETE`  
 - DQL：`SELECT`

 ### 2. 多表关联与聚合

 - 连接：`INNER JOIN / LEFT JOIN`
 - 聚合：`COUNT / SUM / AVG / MIN / MAX`
 - 分组与过滤：`GROUP BY / HAVING`

 ### 3. 数据建模实践

 - 员工-部门模型：一对多关系
 - 客户-订单-产品模型：多表关联

 **对应案例：**
 - `cases/employee_management.md`（员工 & 部门）
 - `cases/sales_analysis.md`（订单 & 销售）

 ---

 ## 四、事务、锁与并发控制

 ### 1. 事务特性

 - ACID：原子性、一致性、隔离性、持久性
 - 显式事务控制：`COMMIT / ROLLBACK / SAVEPOINT`

 ### 2. 锁机制（概要）

 - 行级锁：`SELECT ... FOR UPDATE` / `UPDATE` 等引起
 - 表级锁：DDL 操作可能触发表锁
 - 一致性读（基于 Undo），避免读写冲突

 ### 3. 并发问题

 - 脏读、不可重复读、幻读（Oracle 通过多版本读避免脏读）
 - 锁等待和死锁的简单示例（两会话交叉更新）

 **对应案例：**
 - `cases/transaction_concurrency.md`

 ---

 ## 五、索引、执行计划与性能（入门）

 ### 1. 索引类型

 - B*Tree 索引（最常用）
 - 组合索引（多列索引）
 - 唯一索引
 - 函数索引（基于表达式）

 ### 2. 执行计划

 - 使用 `EXPLAIN PLAN` 或 `AUTOTRACE` 查看：
   - 全表扫描（FULL TABLE SCAN）
   - 索引范围扫描（INDEX RANGE SCAN）
   - 嵌套循环（NESTED LOOPS）

 ### 3. 优化思路（基础）

 - 为高频过滤/连接列创建合适索引
 - 避免在索引列上使用函数封装导致索引失效
 - 减少不必要的 `SELECT *`，只查需要的列

 **对应案例：**
 - `cases/sales_analysis.md` 中对订单和客户/产品的查询优化

 ---

 ## 六、PL/SQL 与存储过程（概览）

 ### 1. 匿名块

 ```sql
 DECLARE
   v_total NUMBER;
 BEGIN
   SELECT SUM(total_amount)
     INTO v_total
     FROM orders
     WHERE order_date >= DATE '2024-01-01';

   DBMS_OUTPUT.PUT_LINE('Total: ' || v_total);
 END;
 /
 ```

 ### 2. 存储过程与函数

 - 存储过程：完成一段业务逻辑，可无返回值
 - 函数：返回单一值，可在 SQL 中调用（需注意副作用）

 **对应案例：**
 - 在 `cases/sales_analysis.md` 中可扩展一个“计算客户年度消费”的存储过程

 ---

 ## 七、知识点与案例/数据对照表

 | 模块           | 关键知识点                           | 案例文档                     | 数据文件                            | 脚本文件                 |
 |----------------|--------------------------------------|------------------------------|-------------------------------------|--------------------------|
 | 架构与对象     | 实例/数据库/表空间/Schema           | `GUIDE.md`                   | -                                   | `setup_schema.sql`（示意） |
 | 基础建模与约束 | 主键/外键/索引                       | `employee_management.md`     | `employees.csv`,`departments.csv`   | `setup_tables.sql`,`load_data.sql` |
 | 员工与部门分析 | 员工分布、部门平均薪资              | `employee_management.md`     | 同上                                | `common_queries.sql`     |
 | 订单与销售分析 | 多表关联、聚合与执行计划            | `sales_analysis.md`          | `customers.csv`,`products.csv`,`orders.csv` | `common_queries.sql`     |
 | 事务与并发     | COMMIT/ROLLBACK、锁等待、并发示例   | `transaction_concurrency.md` | 复用员工/订单等表                   | `common_queries.sql`     |

 ---

 ## 八、如何使用本模块学习

 1. 阅读 `GUIDE.md` 了解整体学习路径与环境准备步骤。
 2. 执行 `scripts/setup_tables.sql` 和 `scripts/load_data.sql` 在本地 Oracle 数据库中创建示例表和数据。
 3. 按顺序阅读并实践 `cases/employee_management.md`、`cases/sales_analysis.md`、`cases/transaction_concurrency.md`，对照 `scripts/common_queries.sql` 运行查询与事务操作。
 4. 在理解示例的基础上，尝试：
    - 为现有表增加字段与约束；
    - 设计新索引并观察执行计划变化；
    - 编写一个简单的 PL/SQL 存储过程。

 当你能：

 - 熟练创建/修改表结构与约束；
 - 理解常见查询的执行路径（全表扫描 vs 索引）；
 - 正确地使用事务控制语句处理并发更新；

 就基本具备了在日常开发中使用 Oracle 的核心能力。

