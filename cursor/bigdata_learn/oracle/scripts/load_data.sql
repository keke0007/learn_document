-- Oracle 学习示例：插入验证数据

ALTER SESSION SET CURRENT_SCHEMA = bigdata_user;

-- 部门数据
INSERT INTO departments (dept_id, dept_name, location) VALUES (10, '研发部', '北京');
INSERT INTO departments (dept_id, dept_name, location) VALUES (20, '市场部', '上海');
INSERT INTO departments (dept_id, dept_name, location) VALUES (30, '财务部', '深圳');
INSERT INTO departments (dept_id, dept_name, location) VALUES (40, '人力资源部', '广州');

-- 员工数据
INSERT INTO employees (emp_id, emp_name, dept_id, salary, hire_date)
VALUES (1001, '张三', 10, 12000, DATE '2020-01-15');
INSERT INTO employees VALUES (1002, '李四', 10, 15000, DATE '2019-03-20');
INSERT INTO employees VALUES (1003, '王五', 20, 10000, DATE '2021-07-01');
INSERT INTO employees VALUES (1004, '赵六', 20,  9000, DATE '2022-02-10');
INSERT INTO employees VALUES (1005, '小红', 30,  8000, DATE '2018-11-05');
INSERT INTO employees VALUES (1006, '小明', 30,  9500, DATE '2019-06-18');
INSERT INTO employees VALUES (1007, '小李', 40,  7000, DATE '2020-09-30');
INSERT INTO employees VALUES (1008, '小王', 40,  7200, DATE '2021-12-12');
INSERT INTO employees VALUES (1009, '老刘', 10, 18000, DATE '2017-05-03');
INSERT INTO employees VALUES (1010, '老王', 20, 11000, DATE '2016-08-22');

-- 客户数据
INSERT INTO customers (customer_id, customer_name, city, level)
VALUES ('C001', '张三', '北京', '金卡');
INSERT INTO customers VALUES ('C002', '李四', '上海', '银卡');
INSERT INTO customers VALUES ('C003', '王五', '广州', '普通');
INSERT INTO customers VALUES ('C004', '赵六', '深圳', '金卡');
INSERT INTO customers VALUES ('C005', '小红', '杭州', '普通');
INSERT INTO customers VALUES ('C006', '小明', '成都', '银卡');

-- 产品数据
INSERT INTO products (product_id, product_name, category, price)
VALUES ('P001', '手机', '电子产品', 2999.00);
INSERT INTO products VALUES ('P002', '笔记本电脑', '电子产品', 5999.00);
INSERT INTO products VALUES ('P003', '耳机', '电子产品', 299.00);
INSERT INTO products VALUES ('P004', '鼠标', '电子产品',  99.00);
INSERT INTO products VALUES ('P005', '键盘', '电子产品', 199.00);
INSERT INTO products VALUES ('P006', '显示器', '电子产品',1299.00);

-- 订单数据
INSERT INTO orders (order_id, order_date, customer_id, product_id, quantity, total_amount)
VALUES (1001, DATE '2024-01-15', 'C001', 'P001', 1,  2999.00);
INSERT INTO orders VALUES (1002, DATE '2024-01-16', 'C002', 'P002', 1,  5999.00);
INSERT INTO orders VALUES (1003, DATE '2024-01-17', 'C001', 'P003', 3,   897.00);
INSERT INTO orders VALUES (1004, DATE '2024-01-18', 'C003', 'P001', 1,  2999.00);
INSERT INTO orders VALUES (1005, DATE '2024-01-19', 'C002', 'P004', 2,   198.00);
INSERT INTO orders VALUES (1006, DATE '2024-02-01', 'C001', 'P002', 1,  5999.00);
INSERT INTO orders VALUES (1007, DATE '2024-02-02', 'C004', 'P003', 2,   598.00);
INSERT INTO orders VALUES (1008, DATE '2024-02-03', 'C003', 'P001', 3,  8997.00);
INSERT INTO orders VALUES (1009, DATE '2024-02-04', 'C002', 'P004', 1,    99.00);
INSERT INTO orders VALUES (1010, DATE '2024-02-05', 'C001', 'P005', 2,   398.00);
INSERT INTO orders VALUES (1011, DATE '2024-03-10', 'C004', 'P001', 1,  2999.00);
INSERT INTO orders VALUES (1012, DATE '2024-03-11', 'C003', 'P002', 2, 11998.00);
INSERT INTO orders VALUES (1013, DATE '2024-03-12', 'C001', 'P003', 1,   299.00);
INSERT INTO orders VALUES (1014, DATE '2024-03-13', 'C002', 'P004', 3,   297.00);
INSERT INTO orders VALUES (1015, DATE '2024-03-14', 'C004', 'P005', 1,   199.00);

COMMIT;

