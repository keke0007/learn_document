# Oracle 学习指南（基础 & 进阶）

## 📚 项目概述

本指南在 `oracle/` 目录下，参考 `hive/`、`clickhouse/`、`doris/` 模块的组织方式，提供一套系统的 **Oracle 数据库学习路径**，重点覆盖：

- **核心知识点**：Oracle 架构、表空间与用户、SQL/PLSQL、事务与锁、索引与执行计划、分区表、备份恢复等  
- **案例场景**：员工与部门管理、订单与销售分析、事务与并发控制  
- **验证数据**：小规模示例数据（员工、部门、订单等），方便在本地或测试库中动手练习

---

## 📁 项目结构

```
oracle/
├── README.md                      # Oracle 知识点总览（详细文档）
├── GUIDE.md                       # 本指南文档（学习路径 + 快速上手）
├── cases/                         # 实战案例目录
│   ├── employee_management.md     # 案例1：员工与部门管理
│   ├── sales_analysis.md          # 案例2：订单与销售分析
│   └── transaction_concurrency.md # 案例3：事务与并发控制
├── data/                          # 验证数据（CSV/TXT）
│   ├── employees.csv              # 员工数据（约10条）
│   ├── departments.csv            # 部门数据（约4条）
│   ├── customers.csv              # 客户数据（约6条）
│   ├── products.csv               # 产品数据（约6条）
│   └── orders.csv                 # 订单数据（约15条）
└── scripts/                       # SQL 脚本目录
    ├── setup_schema.sql           # 创建用户/表空间（示意）
    ├── setup_tables.sql           # 建表脚本：一键创建所有表
    ├── load_data.sql              # 数据加载脚本（INSERT）
    └── common_queries.sql         # 常用查询与练习 SQL
```

---

## 🎯 学习路径（建议 5~7 天）

### 阶段一：基础入门（1 天）

1. **Oracle 基本概念**
   - Oracle 是什么、典型应用场景（OLTP、企业核心业务库）
   - Oracle 与 MySQL/PostgreSQL 的主要区别（表空间、SEGMENT、Redo/Undo 等）

2. **架构与对象**
   - 实例（Instance）、数据库（Database）、表空间（Tablespace）
   - 用户（Schema）、表、索引、视图、序列（Sequence）、同义词（Synonym）

3. **基础 SQL 操作**
   - 建库/建用户（DBA 视角了解即可）
   - DDL：`CREATE TABLE` / `ALTER TABLE` / `DROP TABLE`  
   - DML：`INSERT / UPDATE / DELETE / SELECT`

### 阶段二：SQL 与数据建模（2 天）

1. **单表 & 多表查询**
   - 选择投影与过滤：`SELECT / WHERE / ORDER BY / GROUP BY / HAVING`
   - 连接：`INNER JOIN / LEFT JOIN / RIGHT JOIN`
   - 子查询与集合操作：`IN / EXISTS / UNION / INTERSECT / MINUS`

2. **约束与索引**
   - 主键（PRIMARY KEY）、唯一约束（UNIQUE）、非空（NOT NULL）、外键（FOREIGN KEY）、检查（CHECK）
   - B*Tree 索引、组合索引、唯一索引、函数索引（了解）

3. **数据建模实践**
   - 员工 & 部门模型（案例1）
   - 客户 & 订单 & 产品模型（案例2）

### 阶段三：事务、锁与性能（1~2 天）

1. **事务与并发控制**
   - 事务 ACID 特性
   - 隐式事务与显式事务（`COMMIT/ROLLBACK/SAVEPOINT`）
   - 锁类型（行锁、表锁）、常见等待/死锁现象（案例3）

2. **执行计划与优化（入门）**
   - `EXPLAIN PLAN`、`AUTOTRACE` 基本用法
   - 全表扫描 vs 索引扫描
   - 简单 SQL 优化思路（合理使用索引、避免不必要的函数包装等）

3. **分区表（了解）**
   - 范围分区（RANGE），按日期或业务主键分区
   - 分区裁剪的好处

### 阶段四：PL/SQL 与高级特性（1~2 天）

1. **PL/SQL 基础**
   - 匿名块、变量、控制语句（IF、LOOP）
   - 游标（Cursor）的简单使用
   - 存储过程（Procedure）、函数（Function）

2. **触发器（Trigger）与业务约束**
   - 行级触发器、语句级触发器
   - 插入/更新前后触发的业务检查

3. **备份与恢复（了解）**
   - 逻辑备份（`expdp/impdp`）
   - 物理备份（RMAN 概念性了解）

---

## 🚀 快速开始

> 以下脚本以本地开发数据库为例，你可以使用 SQL*Plus、SQL Developer 或其他图形工具执行。

### 步骤1：准备用户与表空间（DBA 已配置可跳过）

```sql
-- 以下仅为示意，实际表空间路径与权限需 DBA 调整
CREATE TABLESPACE bigdata_ts
  DATAFILE 'bigdata_ts01.dbf'
  SIZE 200M
  AUTOEXTEND ON NEXT 50M MAXSIZE UNLIMITED;

CREATE USER bigdata_user
  IDENTIFIED BY bigdata_pass
  DEFAULT TABLESPACE bigdata_ts
  TEMPORARY TABLESPACE temp;

GRANT CONNECT, RESOURCE TO bigdata_user;
```

### 步骤2：切换到学习用户并创建表

```sql
ALTER SESSION SET CURRENT_SCHEMA = bigdata_user;
@scripts/setup_tables.sql
```

或在工具中打开 `scripts/setup_tables.sql` 直接执行。

### 步骤3：加载验证数据

```sql
@scripts/load_data.sql
```

示例（`load_data.sql` 中会包含类似多条 `INSERT` 语句）：

```sql
INSERT INTO departments (dept_id, dept_name, location)
VALUES (10, '研发部', '北京');
-- ...
COMMIT;
```

### 步骤4：执行常用查询验证

```sql
-- 查看员工与部门
SELECT e.emp_id, e.emp_name, d.dept_name, e.salary
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;

-- 查看订单与客户
SELECT o.order_id, c.customer_name, o.order_date, o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```

---

## 📖 核心知识点速查

### 1. 常用数据类型

| 类型           | 说明         | 示例                      |
|----------------|--------------|---------------------------|
| `NUMBER(p,s)`  | 数值         | `NUMBER(10,2)` 金额       |
| `VARCHAR2(n)`  | 可变长字符串 | `VARCHAR2(50)`            |
| `CHAR(n)`      | 固定长度字符 | `CHAR(2)`                 |
| `DATE`         | 日期+时间    | `'2024-03-01'`            |
| `TIMESTAMP`    | 精确时间     | `TIMESTAMP '2024-03-01 10:00:00'` |

### 2. 常见约束 & 索引示例

```sql
CREATE TABLE employees (
    emp_id     NUMBER(10)      PRIMARY KEY,
    emp_name   VARCHAR2(50)    NOT NULL,
    dept_id    NUMBER(10),
    salary     NUMBER(10,2),
    hire_date  DATE,
    CONSTRAINT fk_emp_dept
        FOREIGN KEY (dept_id)
        REFERENCES departments(dept_id)
);

CREATE INDEX idx_emp_dept_salary
ON employees (dept_id, salary);
```

### 3. 事务与锁（简要）

```sql
-- 显式事务控制
UPDATE employees SET salary = salary + 1000 WHERE emp_id = 1001;
SAVEPOINT before_bonus;
-- ...
ROLLBACK TO before_bonus;
COMMIT;
```

理解：
- Oracle 默认 **读已提交（READ COMMITTED）**，支持多版本读（Undo Segment）  
- 长事务/大批量更新可能导致 Undo 膨胀、阻塞或快照过旧错误

---

## 📊 验证数据说明

### 数据文件清单

| 文件名           | 记录数（约） | 用途           | 案例     |
|------------------|--------------|----------------|----------|
| `employees.csv`  | 10           | 员工信息       | 案例1    |
| `departments.csv`| 4            | 部门信息       | 案例1    |
| `customers.csv`  | 6            | 客户信息       | 案例2    |
| `products.csv`   | 6            | 产品信息       | 案例2    |
| `orders.csv`     | 15           | 订单信息       | 案例2    |

字段示例（详细见 `data/` 文件）：
- `employees.csv`：`emp_id,emp_name,dept_id,salary,hire_date`  
- `departments.csv`：`dept_id,dept_name,location`  
- `customers.csv`：`customer_id,customer_name,city,level`  
- `products.csv`：`product_id,product_name,category,price`  
- `orders.csv`：`order_id,order_date,customer_id,product_id,quantity,total_amount`

---

## 🔧 实战案例概览

### 案例1：员工与部门管理

**学习目标**：掌握基础建模、外键、简单查询和聚合。  
**涉及知识点**：
- 主键/外键约束
- JOIN 查询
- 部门平均薪资、员工分布等聚合分析

### 案例2：订单与销售分析

**学习目标**：基于订单、客户、产品做多维度统计。  
**涉及知识点**：
- 多表关联（客户、产品、订单）
- 按日期/客户/产品维度统计销售额与数量
- 简单执行计划查看与索引使用

### 案例3：事务与并发控制

**学习目标**：理解 Oracle 事务、锁与并发控制机制。  
**涉及知识点**：
- 显式事务控制（COMMIT/ROLLBACK）
- 行锁争用示例（两个会话更新同一行）
- 读已提交与一致性读行为观察

---

## 📝 学习建议

### 针对已有数据库基础的同学

1. 将 Oracle 当作 **企业级 OLTP 数据库的标准代表** 来理解。  
2. 优先掌握：表空间/用户、约束与索引、事务与锁、基本 SQL/PLSQL。  
3. 对比 MySQL/PostgreSQL：同一建模和查询在 Oracle 中的写法与性能特征。

### 实践路线

1. 按 `scripts/setup_tables.sql` + `load_data.sql` 跑通案例1与案例2的查询。  
2. 使用两个会话按 `cases/transaction_concurrency.md` 的步骤模拟锁冲突与事务控制。  
3. 选取自己熟悉的一个业务表结构，尝试用 Oracle 风格重建并编写 PL/SQL 存储过程。

---

## ✅ 学习检查清单

### 基础能力
- [ ] 能够连接 Oracle 数据库并切换到指定 Schema  
- [ ] 能够创建表、约束与索引  
- [ ] 能够执行基本的 DML 和查询  

### 进阶能力
- [ ] 能够解读简单执行计划并判断是否走索引  
- [ ] 能够使用事务控制语句处理复杂更新  
- [ ] 能够编写简单的 PL/SQL 块或存储过程  

---

## 🎓 学习成果

完成本指南后，你将能够：

- ✅ 理解 Oracle 在企业数据系统中的定位与优势  
- ✅ 使用 Oracle 完成常见的建模、查询与事务处理  
- ✅ 针对小型业务场景设计合理的表结构与索引，并进行基本优化  

**祝你 Oracle 学习顺利！🚀**

