# PostgreSQL 学习指南（基础 & 进阶）

## 📚 项目概述

本指南在 `PostgreSQL/` 目录下，参考 `hive/`、`clickhouse/`、`doris/`、`oracle/` 模块的组织方式，提供一套系统的 **PostgreSQL 学习路径**，重点覆盖：

- **核心知识点**：PostgreSQL 架构、数据类型、约束与索引、事务与锁、SQL/JSON、CTE & 窗口函数、扩展与性能调优  
- **案例场景**：员工与部门管理、订单与销售分析、JSON 日志与分析  
- **验证数据**：小规模示例数据（员工、部门、客户、产品、订单、JSON 日志），方便本地或测试库中动手练习

---

## 📁 项目结构

```
PostgreSQL/
├── README.md                      # PostgreSQL 知识点总览（详细文档）
├── GUIDE.md                       # 本指南文档（学习路径 + 快速上手）
├── cases/                         # 实战案例目录
│   ├── employee_management.md     # 案例1：员工与部门管理
│   ├── sales_analysis.md          # 案例2：订单与销售分析
│   └── json_event_analysis.md     # 案例3：JSON 事件日志与分析
├── data/                          # 验证数据（CSV/JSON）
│   ├── employees.csv              # 员工数据（约10条）
│   ├── departments.csv            # 部门数据（约4条）
│   ├── customers.csv              # 客户数据（约6条）
│   ├── products.csv               # 产品数据（约6条）
│   ├── orders.csv                 # 订单数据（约15条）
│   └── events.jsonl               # JSON 行日志数据（约15条）
└── scripts/                       # SQL 脚本目录
    ├── setup_schema.sql           # 创建数据库/Schema（示意）
    ├── setup_tables.sql           # 建表脚本：一键创建所有表
    ├── load_data.sql              # 数据加载脚本（COPY/INSERT）
    └── common_queries.sql         # 常用查询与练习 SQL
```

---

## 🎯 学习路径（建议 5~7 天）

### 阶段一：基础入门（1 天）

1. **PostgreSQL 基本概念**
   - 特点：开源、事务型、SQL 标准支持度高、扩展能力强
   - 典型场景：OLTP、分析型查询、中小型数据仓库、地理/JSON 应用

2. **架构与对象**
   - 数据库（Database）、Schema、表、索引、视图、序列
   - 角色（Role）与权限（GRANT/REVOKE）

3. **基础 SQL 操作**
   - DDL：`CREATE / ALTER / DROP`
   - DML：`INSERT / UPDATE / DELETE`
   - 查询：`SELECT / WHERE / ORDER BY / GROUP BY / HAVING`

### 阶段二：数据类型与建模（2 天）

1. **数据类型**
   - 数值：`smallint / integer / bigint / numeric / real / double precision`
   - 字符：`varchar / text`
   - 日期时间：`date / timestamp [with time zone]`
   - 布尔：`boolean`
   - JSON：`json / jsonb`

2. **约束与索引**
   - 约束：`PRIMARY KEY / UNIQUE / NOT NULL / CHECK / FOREIGN KEY`
   - 索引：B-tree 索引、组合索引、部分索引（PARTIAL）、表达式索引（EXPRESSION）

3. **经典建模实践**
   - 员工 & 部门（案例1）
   - 客户 & 订单 & 产品（案例2）

### 阶段三：高级 SQL 特性（1~2 天）

1. **窗口函数 & CTE**
   - `OVER (PARTITION BY ... ORDER BY ...)` 窗口函数
   - 公共表表达式：`WITH ... AS (...)`
   - 运行总计、排行、分组 TOP N

2. **JSON/JSONB**
   - JSONB 列存储事件日志
   - 操作符：`->` / `->>` / `#>>` / `@>` 等
   - JSON 索引：`GIN` 索引

3. **视图与物化视图**
   - 普通视图：逻辑封装查询
   - 物化视图：缓存查询结果，`REFRESH MATERIALIZED VIEW`

### 阶段四：事务、锁与性能（1~2 天）

1. **事务与隔离级别**
   - ACID 特性
   - 默认隔离级别：`READ COMMITTED`
   - `SERIALIZABLE`、`REPEATABLE READ` 简要了解

2. **锁与并发控制**
   - 行级锁、表级锁、死锁检测
   - MVCC（多版本并发控制）与快照读

3. **性能调优入门**
   - `EXPLAIN / EXPLAIN ANALYZE`
   - 使用索引 vs 顺序扫描（Seq Scan）
   - VACUUM/ANALYZE 概念（维护统计信息与空间回收）

---

## 🚀 快速开始

> 你可以使用 `psql`、pgAdmin 等客户端执行脚本。以下示例以 `psql` 为基础。

### 步骤1：准备数据库与 Schema

```sql
-- 在超级用户或具有创建权限的角色下执行
CREATE DATABASE bigdata_learn;

\c bigdata_learn

CREATE SCHEMA IF NOT EXISTS bigdata_demo;
SET search_path TO bigdata_demo;
```

或在 `bigdata_learn` 数据库中执行：

```sql
\i scripts/setup_schema.sql
```

### 步骤2：执行建表脚本

```sql
\c bigdata_learn
\i scripts/setup_tables.sql
```

### 步骤3：加载验证数据

可以直接使用 `COPY` / `\copy` 从 `data/` 目录导入：

```sql
-- 在 psql 中，客户端 COPY（\copy）更方便访问本地文件
\c bigdata_learn
SET search_path TO bigdata_demo;

\copy departments FROM 'data/departments.csv' CSV HEADER;
\copy employees   FROM 'data/employees.csv'   CSV HEADER;
\copy customers   FROM 'data/customers.csv'   CSV HEADER;
\copy products    FROM 'data/products.csv'    CSV HEADER;
\copy orders      FROM 'data/orders.csv'      CSV HEADER;

-- JSON 行日志（events.jsonl）可以用 INSERT + jsonb_populate_record 等方式加载，脚本中会给简单示例
\i scripts/load_data.sql
```

### 步骤4：执行常用查询验证

```sql
\i scripts/common_queries.sql
```

例如：

```sql
-- 员工与部门
SELECT e.emp_id, e.emp_name, d.dept_name, e.salary
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;

-- 月度销售额
SELECT date_trunc('month', order_date) AS month,
       COUNT(*)                         AS order_count,
       SUM(total_amount)                AS total_sales
FROM orders
GROUP BY month
ORDER BY month;
```

---

## 📖 核心知识点速查

### 1. 常用数据类型示例

| 类型             | 说明               | 示例                         |
|------------------|--------------------|------------------------------|
| `integer`        | 32 位整数          | 员工 ID、数量等              |
| `bigint`         | 64 位整数          | 订单 ID                      |
| `numeric(10,2)`  | 精确小数           | 金额、价格                   |
| `varchar(n)`     | 变长字符串         | 姓名、城市                   |
| `text`           | 长文本             | 备注、日志信息               |
| `date`           | 日期               | `'2024-03-01'`               |
| `timestamp`      | 日期 + 时间        | `'2024-03-01 10:00:00'`      |
| `boolean`        | 布尔               | `true / false`               |
| `jsonb`          | 二进制 JSON 存储   | 事件日志、灵活属性           |

### 2. 约束与索引示例

```sql
CREATE TABLE employees (
    emp_id    integer      PRIMARY KEY,
    emp_name  varchar(50)  NOT NULL,
    dept_id   integer      REFERENCES departments(dept_id),
    salary    numeric(10,2),
    hire_date date
);

CREATE INDEX idx_employees_dept_salary
ON employees (dept_id, salary);
```

### 3. 窗口函数与 CTE 示例

```sql
-- 每个部门按工资排序并标记名次
SELECT
    emp_id,
    emp_name,
    dept_id,
    salary,
    RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS salary_rank
FROM employees;

-- 使用 CTE 做多步查询
WITH monthly_sales AS (
  SELECT
      date_trunc('month', order_date) AS month,
      SUM(total_amount)               AS total_sales
  FROM orders
  GROUP BY date_trunc('month', order_date)
)
SELECT *
FROM monthly_sales
WHERE total_sales > 10000;
```

### 4. JSONB 基础操作

假设有表：

```sql
CREATE TABLE events (
    id      bigserial PRIMARY KEY,
    ts      timestamp NOT NULL,
    payload jsonb     NOT NULL
);

CREATE INDEX idx_events_payload_type
ON events USING gin ((payload ->> 'event_type'));
```

基本查询：

```sql
-- 查询指定事件类型
SELECT *
FROM events
WHERE payload ->> 'event_type' = 'page_view';

-- 统计不同 event_type 的数量
SELECT
    payload ->> 'event_type' AS event_type,
    COUNT(*)                 AS cnt
FROM events
GROUP BY payload ->> 'event_type';
```

---

## 📊 验证数据说明

### 数据文件清单

| 文件名          | 记录数（约） | 用途           | 案例     |
|-----------------|--------------|----------------|----------|
| `employees.csv` | 10           | 员工信息       | 案例1    |
| `departments.csv` | 4          | 部门信息       | 案例1    |
| `customers.csv` | 6           | 客户信息       | 案例2    |
| `products.csv`  | 6           | 产品信息       | 案例2    |
| `orders.csv`    | 15          | 订单信息       | 案例2    |
| `events.jsonl`  | 15          | JSON 事件日志   | 案例3    |

字段示例：
- `employees.csv`：`emp_id,emp_name,dept_id,salary,hire_date`  
- `departments.csv`：`dept_id,dept_name,location`  
- `customers.csv`：`customer_id,customer_name,city,level`  
- `products.csv`：`product_id,product_name,category,price`  
- `orders.csv`：`order_id,order_date,customer_id,product_id,quantity,total_amount`  
- `events.jsonl`：每行一个 JSON 对象，如：

```json
{"ts":"2024-03-14T10:00:01","user_id":1,"event_type":"page_view","page":"/home","device":"ios","duration":12}
```

---

## 🔧 实战案例概览

### 案例1：员工与部门管理

**学习目标**：掌握基础建模、约束、索引以及常见查询。  
**涉及知识点**：
- 主键/外键约束
- 连接查询与聚合
- 部门平均薪资、员工分布等

### 案例2：订单与销售分析

**学习目标**：基于订单、客户、产品做多维度统计与分析。  
**涉及知识点**：
- 多表关联  
- 按时间/城市/产品维度聚合  
- 窗口函数与 CTE

### 案例3：JSON 事件日志分析

**学习目标**：使用 `jsonb` 存储与分析半结构化日志。  
**涉及知识点**：
- JSONB 字段设计  
- GIN 索引与 JSON 查询  
- 事件类型统计、路径分析等

---

## 📝 学习建议

### 针对已有数据库基础的同学

1. 将 PostgreSQL 视作 **功能最完整、扩展能力强的通用关系型数据库**。  
2. 优先掌握：类型系统、约束与索引、事务与 MVCC、窗口函数和 CTE、JSONB。  
3. 对比 MySQL/Oracle：同一建模和查询在 PostgreSQL 中的写法与性能特征。

### 实践路线

1. 按 `scripts/setup_tables.sql` + `load_data.sql` 跑通案例1和案例2的所有查询。  
2. 为 `orders` 表增加索引并使用 `EXPLAIN ANALYZE` 比较执行计划。  
3. 完成 JSON 日志表的创建与加载，设计 3~5 个 JSON 分析查询。

---

## ✅ 学习检查清单

### 基础能力
- [ ] 能够连接 PostgreSQL 并切换到 `bigdata_learn` 数据库  
- [ ] 能够创建 Schema、表、约束与索引  
- [ ] 能够使用 `COPY/\copy` 从 CSV 导入数据  

### 进阶能力
- [ ] 能够编写窗口函数与 CTE  
- [ ] 能够使用 `EXPLAIN ANALYZE` 解读执行计划  
- [ ] 能够设计并查询 JSONB 字段  

---

## 🎓 学习成果

完成本指南后，你将能够：

- ✅ 使用 PostgreSQL 完成常见业务建模与查询  
- ✅ 针对结构化与半结构化数据（JSON）进行分析  
- ✅ 理解并利用 PostgreSQL 的事务、索引和高级 SQL 能力为实际项目提供支撑  

**祝你 PostgreSQL 学习顺利！🚀**

