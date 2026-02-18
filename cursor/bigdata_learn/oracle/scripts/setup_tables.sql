-- Oracle 学习示例：在 bigdata_user 下创建示例表

ALTER SESSION SET CURRENT_SCHEMA = bigdata_user;

-- 部门表
CREATE TABLE departments (
    dept_id    NUMBER(10)    PRIMARY KEY,
    dept_name  VARCHAR2(50)  NOT NULL,
    location   VARCHAR2(50)
);

-- 员工表
CREATE TABLE employees (
    emp_id     NUMBER(10)    PRIMARY KEY,
    emp_name   VARCHAR2(50)  NOT NULL,
    dept_id    NUMBER(10),
    salary     NUMBER(10,2),
    hire_date  DATE,
    CONSTRAINT fk_emp_dept
        FOREIGN KEY (dept_id)
        REFERENCES departments(dept_id)
);

CREATE INDEX idx_emp_dept_salary
ON employees (dept_id, salary);

-- 客户表
CREATE TABLE customers (
    customer_id   VARCHAR2(10)  PRIMARY KEY,
    customer_name VARCHAR2(50)  NOT NULL,
    city          VARCHAR2(50),
    level         VARCHAR2(20)
);

-- 产品表
CREATE TABLE products (
    product_id    VARCHAR2(10)  PRIMARY KEY,
    product_name  VARCHAR2(50)  NOT NULL,
    category      VARCHAR2(50),
    price         NUMBER(10,2)  NOT NULL
);

-- 订单表
CREATE TABLE orders (
    order_id      NUMBER(10)    PRIMARY KEY,
    order_date    DATE          NOT NULL,
    customer_id   VARCHAR2(10)  NOT NULL,
    product_id    VARCHAR2(10)  NOT NULL,
    quantity      NUMBER(10),
    total_amount  NUMBER(12,2),
    CONSTRAINT fk_order_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),
    CONSTRAINT fk_order_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

CREATE INDEX idx_orders_customer_date
ON orders (customer_id, order_date);

