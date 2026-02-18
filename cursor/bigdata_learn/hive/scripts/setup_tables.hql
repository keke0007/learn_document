-- Hive 表创建脚本
-- 使用前请先创建数据库：CREATE DATABASE IF NOT EXISTS test_db; USE test_db;

-- ============================================
-- 案例1：员工管理
-- ============================================

-- 创建员工表
CREATE TABLE IF NOT EXISTS employee (
    id INT,
    name STRING,
    age INT,
    salary DOUBLE,
    department STRING,
    hire_date DATE
)
COMMENT '员工表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- 创建部门表
CREATE TABLE IF NOT EXISTS department (
    dept_id STRING,
    dept_name STRING,
    location STRING,
    employee_count INT
)
COMMENT '部门表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================
-- 案例2：销售数据分析
-- ============================================

-- 创建订单表
CREATE TABLE IF NOT EXISTS orders (
    order_id INT,
    order_date DATE,
    customer_id STRING,
    product_id STRING,
    quantity INT,
    total_amount DOUBLE
)
COMMENT '订单表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- 创建产品表
CREATE TABLE IF NOT EXISTS products (
    product_id STRING,
    product_name STRING,
    price DOUBLE,
    category STRING
)
COMMENT '产品表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- 创建客户表
CREATE TABLE IF NOT EXISTS customers (
    customer_id STRING,
    customer_name STRING,
    city STRING,
    age INT,
    register_date DATE
)
COMMENT '客户表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================
-- 案例3：用户行为分析
-- ============================================

-- 创建用户访问日志表
CREATE TABLE IF NOT EXISTS user_logs (
    log_time TIMESTAMP,
    user_id STRING,
    action_type STRING,
    page_url STRING,
    duration INT
)
COMMENT '用户访问日志表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- 创建用户信息表
CREATE TABLE IF NOT EXISTS users (
    user_id STRING,
    user_name STRING,
    gender STRING,
    age INT,
    city STRING,
    register_date DATE,
    vip_level STRING
)
COMMENT '用户信息表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
