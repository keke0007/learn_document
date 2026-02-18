-- Hive 查询示例
-- 演示 Hive SQL 的各种操作

-- 创建数据库
CREATE DATABASE IF NOT EXISTS mydb;
USE mydb;

-- 创建内部表
CREATE TABLE IF NOT EXISTS users (
    id BIGINT,
    name STRING,
    age INT,
    email STRING,
    department STRING,
    salary DECIMAL(10,2),
    hire_date DATE
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compress'='SNAPPY');

-- 创建外部表
CREATE EXTERNAL TABLE IF NOT EXISTS logs (
    timestamp STRING,
    level STRING,
    message STRING,
    user_id BIGINT
)
PARTITIONED BY (dt STRING, hour STRING)
STORED AS TEXTFILE
LOCATION '/data/logs'
TBLPROPERTIES ('skip.header.line.count'='1');

-- 添加分区
ALTER TABLE logs ADD PARTITION (dt='2024-01-26', hour='10')
LOCATION '/data/logs/2024-01-26/10';

ALTER TABLE logs ADD PARTITION (dt='2024-01-26', hour='11')
LOCATION '/data/logs/2024-01-26/11';

-- 加载数据
LOAD DATA INPATH 'hdfs://namenode:9000/data/users.csv'
INTO TABLE users;

-- 插入数据
INSERT INTO TABLE users
SELECT id, name, age, email, department, salary, hire_date
FROM temp_users
WHERE age > 25;

-- 查询示例1：基本查询
SELECT 
    department,
    COUNT(*) as count,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary,
    MIN(salary) as min_salary
FROM users
WHERE age > 25
GROUP BY department
ORDER BY avg_salary DESC;

-- 查询示例2：窗口函数
SELECT 
    name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank_in_dept,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary
FROM users
WHERE department IS NOT NULL;

-- 查询示例3：连接查询
CREATE TABLE departments (
    dept_code STRING,
    dept_name STRING,
    manager STRING
) STORED AS PARQUET;

SELECT 
    u.name,
    u.department,
    d.dept_name,
    u.salary,
    d.manager
FROM users u
LEFT JOIN departments d ON u.department = d.dept_code
WHERE u.salary > 10000;

-- 查询示例4：子查询
SELECT 
    name,
    salary,
    department
FROM users
WHERE salary > (
    SELECT AVG(salary)
    FROM users
    WHERE department = 'IT'
);

-- 查询示例5：CTE（公共表表达式）
WITH dept_stats AS (
    SELECT 
        department,
        AVG(salary) as avg_salary,
        COUNT(*) as count
    FROM users
    GROUP BY department
)
SELECT 
    u.name,
    u.salary,
    u.department,
    ds.avg_salary,
    CASE 
        WHEN u.salary > ds.avg_salary THEN 'Above Average'
        ELSE 'Below Average'
    END as salary_status
FROM users u
JOIN dept_stats ds ON u.department = ds.department;

-- 查询示例6：分区查询
SELECT 
    level,
    COUNT(*) as count,
    COUNT(DISTINCT user_id) as unique_users
FROM logs
WHERE dt = '2024-01-26' AND hour BETWEEN '10' AND '12'
GROUP BY level;

-- 创建视图
CREATE VIEW IF NOT EXISTS high_salary_users AS
SELECT 
    name,
    department,
    salary
FROM users
WHERE salary > 20000;

-- 使用视图
SELECT * FROM high_salary_users
ORDER BY salary DESC
LIMIT 10;
