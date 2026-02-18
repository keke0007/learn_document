# Hive 学习知识点

## 目录
1. [Hive 基础概念](#1-hive-基础概念)
2. [数据类型](#2-数据类型)
3. [DDL 操作](#3-ddl-操作)
4. [DML 操作](#4-dml-操作)
5. [查询语句](#5-查询语句)
6. [内置函数](#6-内置函数)
7. [分区和分桶](#7-分区和分桶)
8. [窗口函数](#8-窗口函数)
9. [案例与验证数据](#9-案例与验证数据)

---

## 1. Hive 基础概念

### 1.1 什么是 Hive
- Hive 是基于 Hadoop 的数据仓库工具
- 将结构化的数据文件映射为一张数据库表
- 提供类 SQL 查询功能（HQL）
- 本质是将 SQL 转换为 MapReduce 任务

### 1.2 Hive 架构
- **元数据存储**：Metastore（通常使用 MySQL/PostgreSQL）
- **驱动**：Driver（SQL 编译器、优化器、执行器）
- **执行引擎**：MapReduce/Tez/Spark

---

## 2. 数据类型

### 2.1 基本数据类型
- **TINYINT**：1字节整数
- **SMALLINT**：2字节整数
- **INT**：4字节整数
- **BIGINT**：8字节整数
- **FLOAT**：单精度浮点数
- **DOUBLE**：双精度浮点数
- **BOOLEAN**：布尔类型
- **STRING**：字符串
- **TIMESTAMP**：时间戳
- **DATE**：日期

### 2.2 集合数据类型
- **ARRAY**：数组，如 `array<string>`
- **MAP**：键值对，如 `map<string,int>`
- **STRUCT**：结构体，如 `struct<name:string,age:int>`

---

## 3. DDL 操作

### 3.1 创建数据库
```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS test_db
COMMENT '测试数据库'
LOCATION '/user/hive/warehouse/test_db.db';

-- 查看数据库
SHOW DATABASES;

-- 使用数据库
USE test_db;
```

### 3.2 创建表
```sql
-- 创建内部表（管理表）
CREATE TABLE IF NOT EXISTS employee (
    id INT,
    name STRING,
    age INT,
    salary DOUBLE,
    department STRING
)
COMMENT '员工表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- 创建外部表
CREATE EXTERNAL TABLE IF NOT EXISTS employee_external (
    id INT,
    name STRING,
    age INT,
    salary DOUBLE,
    department STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION '/user/hive/external/employee';

-- 创建分区表
CREATE TABLE IF NOT EXISTS employee_partitioned (
    id INT,
    name STRING,
    age INT,
    salary DOUBLE
)
PARTITIONED BY (department STRING, year INT)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- 创建分桶表
CREATE TABLE IF NOT EXISTS employee_bucketed (
    id INT,
    name STRING,
    age INT,
    salary DOUBLE,
    department STRING
)
CLUSTERED BY (id) INTO 4 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

### 3.3 修改表
```sql
-- 重命名表
ALTER TABLE employee RENAME TO employee_new;

-- 添加列
ALTER TABLE employee ADD COLUMNS (email STRING);

-- 修改列
ALTER TABLE employee CHANGE COLUMN age age INT COMMENT '年龄';

-- 删除表
DROP TABLE IF EXISTS employee;
```

---

## 4. DML 操作

### 4.1 加载数据
```sql
-- 从本地文件加载
LOAD DATA LOCAL INPATH '/path/to/employee.txt' INTO TABLE employee;

-- 从 HDFS 加载
LOAD DATA INPATH '/user/hive/data/employee.txt' INTO TABLE employee;

-- 覆盖加载
LOAD DATA LOCAL INPATH '/path/to/employee.txt' OVERWRITE INTO TABLE employee;
```

### 4.2 插入数据
```sql
-- 插入单条数据
INSERT INTO TABLE employee VALUES (1, '张三', 25, 5000.0, 'IT');

-- 插入多条数据
INSERT INTO TABLE employee VALUES
(1, '张三', 25, 5000.0, 'IT'),
(2, '李四', 30, 8000.0, 'HR'),
(3, '王五', 28, 6000.0, 'IT');

-- 从查询结果插入
INSERT INTO TABLE employee
SELECT id, name, age, salary, department FROM employee_temp;

-- 动态分区插入
INSERT INTO TABLE employee_partitioned PARTITION(department, year)
SELECT id, name, age, salary, department, year FROM employee_source;
```

### 4.3 更新和删除（Hive 2.0+）
```sql
-- 更新数据（需要启用 ACID 支持）
UPDATE employee SET salary = 6000.0 WHERE id = 1;

-- 删除数据
DELETE FROM employee WHERE id = 1;
```

---

## 5. 查询语句

### 5.1 基本查询
```sql
-- SELECT 查询
SELECT * FROM employee;

-- 条件查询
SELECT name, salary FROM employee WHERE salary > 5000;

-- 排序
SELECT * FROM employee ORDER BY salary DESC;

-- 限制结果
SELECT * FROM employee LIMIT 10;
```

### 5.2 聚合查询
```sql
-- GROUP BY
SELECT department, AVG(salary) as avg_salary, COUNT(*) as count
FROM employee
GROUP BY department;

-- HAVING
SELECT department, AVG(salary) as avg_salary
FROM employee
GROUP BY department
HAVING AVG(salary) > 6000;
```

### 5.3 连接查询
```sql
-- 内连接
SELECT e.name, d.department_name
FROM employee e
INNER JOIN department d ON e.department = d.department_id;

-- 左连接
SELECT e.name, d.department_name
FROM employee e
LEFT JOIN department d ON e.department = d.department_id;

-- 右连接
SELECT e.name, d.department_name
FROM employee e
RIGHT JOIN department d ON e.department = d.department_id;

-- 全外连接
SELECT e.name, d.department_name
FROM employee e
FULL OUTER JOIN department d ON e.department = d.department_id;
```

### 5.4 子查询
```sql
-- 子查询
SELECT name, salary
FROM employee
WHERE salary > (SELECT AVG(salary) FROM employee);

-- IN 子查询
SELECT * FROM employee
WHERE department IN (SELECT department_id FROM department WHERE location = '北京');
```

---

## 6. 内置函数

### 6.1 字符串函数
```sql
-- CONCAT：连接字符串
SELECT CONCAT(name, '-', department) FROM employee;

-- SUBSTRING：截取字符串
SELECT SUBSTRING(name, 1, 2) FROM employee;

-- UPPER/LOWER：大小写转换
SELECT UPPER(name), LOWER(department) FROM employee;

-- TRIM：去除空格
SELECT TRIM(name) FROM employee;

-- SPLIT：分割字符串
SELECT SPLIT(name, '-')[0] FROM employee;
```

### 6.2 数学函数
```sql
-- ROUND：四舍五入
SELECT ROUND(salary, 2) FROM employee;

-- CEIL/FLOOR：向上/向下取整
SELECT CEIL(salary), FLOOR(salary) FROM employee;

-- ABS：绝对值
SELECT ABS(salary) FROM employee;

-- RAND：随机数
SELECT RAND() FROM employee;
```

### 6.3 日期函数
```sql
-- CURRENT_DATE：当前日期
SELECT CURRENT_DATE();

-- YEAR/MONTH/DAY：提取日期部分
SELECT YEAR(hire_date), MONTH(hire_date), DAY(hire_date) FROM employee;

-- DATE_ADD/DATE_SUB：日期加减
SELECT DATE_ADD(CURRENT_DATE(), 7);
SELECT DATE_SUB(CURRENT_DATE(), 7);

-- DATEDIFF：日期差
SELECT DATEDIFF(CURRENT_DATE(), hire_date) FROM employee;
```

### 6.4 条件函数
```sql
-- IF：条件判断
SELECT IF(salary > 5000, '高薪', '普通') FROM employee;

-- CASE WHEN：多条件判断
SELECT 
    CASE 
        WHEN salary > 8000 THEN '高薪'
        WHEN salary > 5000 THEN '中等'
        ELSE '普通'
    END as salary_level
FROM employee;

-- COALESCE：返回第一个非空值
SELECT COALESCE(name, '未知') FROM employee;
```

---

## 7. 分区和分桶

### 7.1 分区
```sql
-- 创建分区
ALTER TABLE employee_partitioned ADD PARTITION(department='IT', year=2024);

-- 查看分区
SHOW PARTITIONS employee_partitioned;

-- 删除分区
ALTER TABLE employee_partitioned DROP PARTITION(department='IT', year=2024);

-- 查询分区数据
SELECT * FROM employee_partitioned WHERE department='IT' AND year=2024;
```

### 7.2 分桶
```sql
-- 分桶查询
SELECT * FROM employee_bucketed TABLESAMPLE(BUCKET 1 OUT OF 4 ON id);
```

---

## 8. 窗口函数

### 8.1 排名函数
```sql
-- ROW_NUMBER：行号
SELECT 
    name, 
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
FROM employee;

-- RANK：排名（相同值相同排名，跳过后续排名）
SELECT 
    name, 
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank
FROM employee;

-- DENSE_RANK：密集排名（相同值相同排名，不跳过）
SELECT 
    name, 
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employee;
```

### 8.2 聚合窗口函数
```sql
-- SUM/AVG/COUNT 窗口函数
SELECT 
    name,
    salary,
    SUM(salary) OVER (PARTITION BY department) as dept_total,
    AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employee;
```

### 8.3 偏移函数
```sql
-- LAG/LEAD：前一行/后一行
SELECT 
    name,
    salary,
    LAG(salary, 1) OVER (ORDER BY salary) as prev_salary,
    LEAD(salary, 1) OVER (ORDER BY salary) as next_salary
FROM employee;

-- FIRST_VALUE/LAST_VALUE：首值/末值
SELECT 
    name,
    salary,
    FIRST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary) as first_salary,
    LAST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary) as last_salary
FROM employee;
```

---

## 9. 案例与验证数据

详见以下文件：
- [案例1：员工管理案例](cases/employee_management.md)
- [案例2：销售数据分析](cases/sales_analysis.md)
- [案例3：用户行为分析](cases/user_behavior.md)
- [验证数据文件](data/)
