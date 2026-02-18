-- PostgreSQL 学习示例：在 bigdata_demo 下创建示例表

SET search_path TO bigdata_demo;

-- 部门表
CREATE TABLE IF NOT EXISTS departments (
    dept_id    integer       PRIMARY KEY,
    dept_name  varchar(50)   NOT NULL,
    location   varchar(50)
);

-- 员工表
CREATE TABLE IF NOT EXISTS employees (
    emp_id     integer       PRIMARY KEY,
    emp_name   varchar(50)   NOT NULL,
    dept_id    integer       REFERENCES departments(dept_id),
    salary     numeric(10,2),
    hire_date  date
);

CREATE INDEX IF NOT EXISTS idx_employees_dept_salary
ON employees (dept_id, salary);

-- 客户表
CREATE TABLE IF NOT EXISTS customers (
    customer_id   varchar(10)  PRIMARY KEY,
    customer_name varchar(50)  NOT NULL,
    city          varchar(50),
    level         varchar(20)
);

-- 产品表
CREATE TABLE IF NOT EXISTS products (
    product_id    varchar(10)  PRIMARY KEY,
    product_name  varchar(50)  NOT NULL,
    category      varchar(50),
    price         numeric(10,2) NOT NULL
);

-- 订单表
CREATE TABLE IF NOT EXISTS orders (
    order_id      integer      PRIMARY KEY,
    order_date    date         NOT NULL,
    customer_id   varchar(10)  NOT NULL REFERENCES customers(customer_id),
    product_id    varchar(10)  NOT NULL REFERENCES products(product_id),
    quantity      integer,
    total_amount  numeric(12,2)
);

CREATE INDEX IF NOT EXISTS idx_orders_customer_date
ON orders (customer_id, order_date);

-- JSON 事件表
CREATE TABLE IF NOT EXISTS events (
    id      bigserial PRIMARY KEY,
    ts      timestamp NOT NULL,
    payload jsonb     NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_payload_gin
ON events
USING gin (payload);

