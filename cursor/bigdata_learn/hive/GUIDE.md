# Hive 学习指南

## 📚 项目概述

本指南提供了完整的 Hive 学习资源，包括基础知识、实战案例和验证数据，帮助你系统掌握 Hive 数据仓库技术。

---

## 📁 项目结构

```
hive/
├── README.md                    # Hive 知识点总览（详细文档）
├── GUIDE.md                     # 本指南文档（快速入门）
├── cases/                       # 实战案例目录
│   ├── employee_management.md   # 案例1：员工管理系统
│   ├── sales_analysis.md        # 案例2：销售数据分析
│   └── user_behavior.md         # 案例3：用户行为分析
├── data/                        # 验证数据目录
│   ├── employee.txt             # 员工数据（10条记录）
│   ├── department.txt           # 部门数据（3条记录）
│   ├── orders.txt               # 订单数据（15条记录）
│   ├── products.txt             # 产品数据（5条记录）
│   ├── customers.txt            # 客户数据（4条记录）
│   ├── user_logs.txt            # 用户日志数据（24条记录）
│   └── users.txt                # 用户信息数据（5条记录）
└── scripts/                     # SQL 脚本目录
    ├── setup_tables.hql         # 建表脚本（一键创建所有表）
    ├── load_data.hql            # 数据加载脚本
    └── common_queries.hql       # 常用查询示例
```

---

## 🎯 学习路径

### 阶段一：基础知识（1-2天）
1. **Hive 基础概念**
   - 了解 Hive 架构和原理
   - 理解 Hive 与 Hadoop 的关系
   - 掌握元数据存储机制

2. **数据类型**
   - 学习基本数据类型（INT, STRING, DOUBLE 等）
   - 掌握集合数据类型（ARRAY, MAP, STRUCT）

3. **DDL 操作**
   - 创建数据库和表
   - 理解内部表和外部表
   - 学习分区表和分桶表

### 阶段二：数据操作（2-3天）
1. **DML 操作**
   - 数据加载（LOAD DATA）
   - 数据插入（INSERT）
   - 数据更新和删除（Hive 2.0+）

2. **查询语句**
   - 基本查询（SELECT, WHERE, ORDER BY）
   - 聚合查询（GROUP BY, HAVING）
   - 连接查询（JOIN）
   - 子查询

3. **内置函数**
   - 字符串函数
   - 数学函数
   - 日期函数
   - 条件函数

### 阶段三：高级特性（3-4天）
1. **分区和分桶**
   - 分区表的设计和使用
   - 分桶表的应用场景

2. **窗口函数**
   - 排名函数（ROW_NUMBER, RANK, DENSE_RANK）
   - 聚合窗口函数
   - 偏移函数（LAG, LEAD）

3. **性能优化**
   - 分区裁剪
   - 分桶优化
   - 查询优化技巧

### 阶段四：实战案例（3-5天）
1. **案例1：员工管理** - 基础操作练习
2. **案例2：销售数据分析** - 复杂查询和窗口函数
3. **案例3：用户行为分析** - 时间序列分析和用户画像

---

## 🚀 快速开始

### 前置要求
- 已安装 Hadoop 集群
- 已安装 Hive
- 已配置 Hive Metastore（推荐使用 MySQL）

### 步骤1：创建数据库
```sql
CREATE DATABASE IF NOT EXISTS test_db;
USE test_db;
```

### 步骤2：创建表
```bash
# 在 Hive 命令行执行
hive -f scripts/setup_tables.hql
```

或者手动执行：
```sql
-- 创建员工表
CREATE TABLE IF NOT EXISTS employee (
    id INT,
    name STRING,
    age INT,
    salary DOUBLE,
    department STRING,
    hire_date DATE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

### 步骤3：加载数据
```bash
# 修改 load_data.hql 中的路径为实际路径
# 然后执行
hive -f scripts/load_data.hql
```

或者手动加载：
```sql
-- 加载员工数据（注意修改为实际路径）
LOAD DATA LOCAL INPATH '/path/to/hive/data/employee.txt' INTO TABLE employee;
```

### 步骤4：验证数据
```sql
-- 查看数据
SELECT * FROM employee LIMIT 10;

-- 统计记录数
SELECT COUNT(*) FROM employee;
```

---

## 📖 核心知识点速查

### 1. 数据类型
| 类型 | 说明 | 示例 |
|------|------|------|
| INT | 整数 | `25` |
| STRING | 字符串 | `'张三'` |
| DOUBLE | 浮点数 | `5000.0` |
| DATE | 日期 | `'2023-01-15'` |
| TIMESTAMP | 时间戳 | `'2024-01-15 09:15:23'` |
| ARRAY | 数组 | `array<string>` |
| MAP | 键值对 | `map<string,int>` |
| STRUCT | 结构体 | `struct<name:string,age:int>` |

### 2. 常用 DDL 语句
```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS db_name;

-- 创建表
CREATE TABLE table_name (col1 type1, col2 type2);

-- 创建分区表
CREATE TABLE table_name (...) PARTITIONED BY (col type);

-- 创建外部表
CREATE EXTERNAL TABLE table_name (...) LOCATION '/path';

-- 查看表结构
DESC table_name;

-- 删除表
DROP TABLE table_name;
```

### 3. 常用 DML 语句
```sql
-- 加载数据
LOAD DATA LOCAL INPATH '/path/file.txt' INTO TABLE table_name;

-- 插入数据
INSERT INTO TABLE table_name VALUES (1, 'value1', 100);

-- 从查询插入
INSERT INTO TABLE table_name SELECT * FROM source_table;
```

### 4. 常用查询函数
```sql
-- 字符串函数
CONCAT(str1, str2)           -- 连接字符串
SUBSTRING(str, start, len)    -- 截取字符串
UPPER(str) / LOWER(str)       -- 大小写转换

-- 日期函数
CURRENT_DATE()                -- 当前日期
YEAR(date) / MONTH(date)      -- 提取年月
DATEDIFF(date1, date2)        -- 日期差

-- 条件函数
IF(condition, true_val, false_val)  -- 条件判断
CASE WHEN ... THEN ... END          -- 多条件判断
COALESCE(val1, val2)                -- 返回第一个非空值
```

### 5. 窗口函数
```sql
-- 排名函数
ROW_NUMBER() OVER (PARTITION BY col ORDER BY col)
RANK() OVER (ORDER BY col)
DENSE_RANK() OVER (ORDER BY col)

-- 聚合窗口函数
SUM(col) OVER (PARTITION BY col ORDER BY col)
AVG(col) OVER (PARTITION BY col)

-- 偏移函数
LAG(col, n) OVER (ORDER BY col)    -- 前n行
LEAD(col, n) OVER (ORDER BY col)   -- 后n行
```

---

## 💡 实战案例概览

### 案例1：员工管理系统
**学习目标**：掌握基本查询、聚合统计、连接查询

**涉及知识点**：
- 基本 SELECT 查询
- GROUP BY 聚合
- JOIN 连接
- 子查询
- 窗口函数基础

**数据规模**：
- 员工表：10 条记录
- 部门表：3 条记录

**典型查询**：
- 各部门平均薪资统计
- 薪资排名
- 员工与部门信息关联

### 案例2：销售数据分析
**学习目标**：掌握复杂查询、时间序列分析、多表关联

**涉及知识点**：
- 多表 JOIN
- 时间函数应用
- 窗口函数高级用法
- 复购分析
- 销售趋势分析

**数据规模**：
- 订单表：15 条记录
- 产品表：5 条记录
- 客户表：4 条记录

**典型查询**：
- 每月销售额统计
- 产品销量排行
- 客户消费分析
- 复购客户识别

### 案例3：用户行为分析
**学习目标**：掌握时间序列分析、用户画像、行为路径分析

**涉及知识点**：
- 时间戳处理
- 用户活跃度分析
- 行为路径追踪
- 转化漏斗分析
- 用户画像构建

**数据规模**：
- 用户日志表：24 条记录
- 用户信息表：5 条记录

**典型查询**：
- 每日活跃用户（DAU）
- 用户访问路径分析
- 页面转化漏斗
- 用户行为画像

---

## 📊 数据说明

### 数据文件格式
所有数据文件采用 **CSV 格式**，字段分隔符为 **逗号（,）**

### 数据文件清单

| 文件名 | 记录数 | 用途 | 案例 |
|--------|--------|------|------|
| employee.txt | 10 | 员工基本信息 | 案例1 |
| department.txt | 3 | 部门信息 | 案例1 |
| orders.txt | 15 | 订单数据 | 案例2 |
| products.txt | 5 | 产品信息 | 案例2 |
| customers.txt | 4 | 客户信息 | 案例2 |
| user_logs.txt | 24 | 用户访问日志 | 案例3 |
| users.txt | 5 | 用户基本信息 | 案例3 |

### 数据字段说明

**employee.txt** 字段：
- id, name, age, salary, department, hire_date

**department.txt** 字段：
- dept_id, dept_name, location, employee_count

**orders.txt** 字段：
- order_id, order_date, customer_id, product_id, quantity, total_amount

**products.txt** 字段：
- product_id, product_name, price, category

**customers.txt** 字段：
- customer_id, customer_name, city, age, register_date

**user_logs.txt** 字段：
- log_time, user_id, action_type, page_url, duration

**users.txt** 字段：
- user_id, user_name, gender, age, city, register_date, vip_level

---

## 🔧 使用技巧

### 1. 路径配置
- **本地文件**：使用 `LOAD DATA LOCAL INPATH`
- **HDFS 文件**：使用 `LOAD DATA INPATH`（去掉 LOCAL）
- 路径可以是绝对路径或相对路径

### 2. 数据加载
```sql
-- 追加数据
LOAD DATA LOCAL INPATH '/path/file.txt' INTO TABLE table_name;

-- 覆盖数据
LOAD DATA LOCAL INPATH '/path/file.txt' OVERWRITE INTO TABLE table_name;
```

### 3. 查询优化
- 使用分区裁剪减少数据扫描
- 合理使用 LIMIT 限制结果集
- 避免 SELECT *，只查询需要的字段
- 使用 EXPLAIN 查看执行计划

### 4. 常见问题

**问题1：日期格式错误**
```sql
-- 确保日期格式为 'YYYY-MM-DD'
-- 如果格式不对，使用函数转换
SELECT TO_DATE('2023/01/15', 'yyyy/MM/dd');
```

**问题2：中文乱码**
```sql
-- 确保 Hive 客户端和文件编码为 UTF-8
-- 检查 hive-site.xml 中的字符集配置
```

**问题3：分区表查询慢**
```sql
-- 使用分区字段过滤
SELECT * FROM table_name WHERE partition_col = 'value';
```

---

## 📝 学习建议

### 初学者
1. 先阅读 `README.md` 了解基础知识
2. 从案例1开始，逐步练习
3. 每个查询都要理解其含义
4. 尝试修改查询条件，观察结果变化

### 进阶学习
1. 完成所有三个案例
2. 尝试组合不同案例的数据
3. 设计自己的查询需求
4. 优化查询性能

### 实践建议
1. **动手实践**：不要只看文档，要实际执行 SQL
2. **理解原理**：了解每个查询背后的执行逻辑
3. **举一反三**：基于案例设计新的查询场景
4. **性能调优**：学习如何优化慢查询

---

## 🔗 相关资源

### 官方文档
- [Apache Hive 官方文档](https://hive.apache.org/)
- [Hive Language Manual](https://cwiki.apache.org/confluence/display/Hive/LanguageManual)

### 推荐阅读
- `README.md` - 详细的知识点文档
- `cases/` - 三个实战案例的详细说明
- `scripts/common_queries.hql` - 常用查询示例

### 扩展学习
- Hive 性能调优
- Hive 与 Spark 集成
- Hive Streaming
- Hive UDF 开发

---

## ✅ 学习检查清单

完成以下任务，确保掌握 Hive 核心技能：

### 基础操作
- [ ] 能够创建数据库和表
- [ ] 能够加载数据到表中
- [ ] 能够执行基本查询
- [ ] 能够使用聚合函数

### 进阶操作
- [ ] 能够使用 JOIN 连接多表
- [ ] 能够使用子查询
- [ ] 能够使用窗口函数
- [ ] 能够创建和使用分区表

### 实战能力
- [ ] 完成案例1的所有查询
- [ ] 完成案例2的所有查询
- [ ] 完成案例3的所有查询
- [ ] 能够独立设计查询需求

---

## 📞 问题反馈

如果在学习过程中遇到问题：
1. 检查 SQL 语法是否正确
2. 确认数据文件路径是否正确
3. 查看 Hive 日志排查错误
4. 参考 `README.md` 中的详细说明

---

## 🎓 学习成果

完成本指南的学习后，你将能够：
- ✅ 熟练使用 Hive 进行数据仓库操作
- ✅ 掌握 Hive SQL 的常用语法和函数
- ✅ 能够进行复杂的数据分析和统计
- ✅ 理解 Hive 的性能优化方法
- ✅ 具备独立开发 Hive 查询的能力

**祝你学习愉快！** 🚀
