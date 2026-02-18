# 案例2：销售数据分析

## 案例描述
分析销售数据，包括订单信息、产品信息、客户信息，进行销售趋势分析和客户行为分析。

## 数据准备

### 1. 订单表数据 (orders.txt)
```
1001,2024-01-15,C001,P001,2,299.00
1002,2024-01-16,C002,P002,1,599.00
1003,2024-01-17,C001,P003,3,899.00
1004,2024-01-18,C003,P001,1,299.00
1005,2024-01-19,C002,P004,2,199.00
1006,2024-02-01,C001,P002,1,599.00
1007,2024-02-02,C004,P003,2,599.00
1008,2024-02-03,C003,P001,3,897.00
1009,2024-02-04,C002,P004,1,199.00
1010,2024-02-05,C001,P005,2,399.00
1011,2024-03-10,C004,P001,1,299.00
1012,2024-03-11,C003,P002,2,1198.00
1013,2024-03-12,C001,P003,1,299.00
1014,2024-03-13,C002,P004,3,597.00
1015,2024-03-14,C004,P005,1,199.00
```

### 2. 产品表数据 (products.txt)
```
P001,手机,299.00,电子产品
P002,笔记本电脑,599.00,电子产品
P003,耳机,299.00,电子产品
P004,鼠标,199.00,电子产品
P005,键盘,199.00,电子产品
```

### 3. 客户表数据 (customers.txt)
```
C001,张三,北京,25,2023-01-01
C002,李四,上海,30,2023-02-15
C003,王五,广州,28,2023-03-20
C004,赵六,深圳,35,2023-04-10
```

## 建表语句

```sql
-- 创建订单表
CREATE TABLE IF NOT EXISTS orders (
    order_id INT,
    order_date DATE,
    customer_id STRING,
    product_id STRING,
    quantity INT,
    total_amount DOUBLE
)
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
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

## 加载数据

```sql
LOAD DATA LOCAL INPATH '/path/to/orders.txt' INTO TABLE orders;
LOAD DATA LOCAL INPATH '/path/to/products.txt' INTO TABLE products;
LOAD DATA LOCAL INPATH '/path/to/customers.txt' INTO TABLE customers;
```

## 查询案例

### 1. 销售统计
```sql
-- 总销售额
SELECT SUM(total_amount) as total_sales FROM orders;

-- 每月销售额
SELECT 
    YEAR(order_date) as year,
    MONTH(order_date) as month,
    COUNT(*) as order_count,
    SUM(total_amount) as monthly_sales,
    AVG(total_amount) as avg_order_amount
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year, month;

-- 每日销售额趋势
SELECT 
    order_date,
    COUNT(*) as order_count,
    SUM(total_amount) as daily_sales
FROM orders
GROUP BY order_date
ORDER BY order_date;
```

### 2. 产品分析
```sql
-- 产品销量排行
SELECT 
    p.product_name,
    p.category,
    SUM(o.quantity) as total_quantity,
    SUM(o.total_amount) as total_sales,
    COUNT(DISTINCT o.order_id) as order_count
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name, p.category
ORDER BY total_sales DESC;

-- 分类销售额
SELECT 
    category,
    COUNT(DISTINCT product_id) as product_count,
    SUM(total_amount) as category_sales,
    AVG(total_amount) as avg_order_amount
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY category
ORDER BY category_sales DESC;
```

### 3. 客户分析
```sql
-- 客户消费排行
SELECT 
    c.customer_name,
    c.city,
    COUNT(DISTINCT o.order_id) as order_count,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_name, c.city
ORDER BY total_spent DESC;

-- 城市销售分析
SELECT 
    c.city,
    COUNT(DISTINCT c.customer_id) as customer_count,
    COUNT(DISTINCT o.order_id) as order_count,
    SUM(o.total_amount) as city_sales
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY city_sales DESC;

-- 客户年龄分组分析
SELECT 
    CASE 
        WHEN c.age < 25 THEN '25岁以下'
        WHEN c.age < 30 THEN '25-30岁'
        WHEN c.age < 35 THEN '30-35岁'
        ELSE '35岁以上'
    END as age_group,
    COUNT(DISTINCT c.customer_id) as customer_count,
    SUM(o.total_amount) as total_sales,
    AVG(o.total_amount) as avg_spent
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY 
    CASE 
        WHEN c.age < 25 THEN '25岁以下'
        WHEN c.age < 30 THEN '25-30岁'
        WHEN c.age < 35 THEN '30-35岁'
        ELSE '35岁以上'
    END;
```

### 4. 窗口函数分析
```sql
-- 每月销售额及累计销售额
SELECT 
    YEAR(order_date) as year,
    MONTH(order_date) as month,
    SUM(total_amount) as monthly_sales,
    SUM(SUM(total_amount)) OVER (ORDER BY YEAR(order_date), MONTH(order_date)) as cumulative_sales
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year, month;

-- 客户订单排名
SELECT 
    c.customer_name,
    o.order_date,
    o.total_amount,
    ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY o.order_date) as order_sequence,
    SUM(o.total_amount) OVER (PARTITION BY c.customer_id ORDER BY o.order_date) as cumulative_spent
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY c.customer_name, o.order_date;
```

### 5. 复购分析
```sql
-- 复购客户（购买次数>=2）
SELECT 
    c.customer_name,
    COUNT(DISTINCT o.order_id) as order_count,
    SUM(o.total_amount) as total_spent,
    MIN(o.order_date) as first_order_date,
    MAX(o.order_date) as last_order_date,
    DATEDIFF(MAX(o.order_date), MIN(o.order_date)) as days_between
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_name
HAVING COUNT(DISTINCT o.order_id) >= 2
ORDER BY order_count DESC;
```

### 6. 关联分析
```sql
-- 订单详情（三表关联）
SELECT 
    o.order_id,
    o.order_date,
    c.customer_name,
    c.city,
    p.product_name,
    p.category,
    o.quantity,
    o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
ORDER BY o.order_date DESC;
```

## 预期结果

### 每月销售额
```
year | month | order_count | monthly_sales | avg_order_amount
-----|-------|-------------|---------------|-----------------
2024 | 1     | 5           | 2295.00       | 459.00
2024 | 2     | 5           | 2692.00       | 538.40
2024 | 3     | 5           | 2592.00       | 518.40
```

### 产品销量排行（Top 3）
```
product_name | category | total_quantity | total_sales | order_count
-------------|----------|----------------|-------------|-------------
笔记本电脑   | 电子产品 | 4              | 2396.00     | 4
手机         | 电子产品 | 7              | 2093.00     | 7
耳机         | 电子产品 | 6              | 1794.00     | 6
```

### 客户消费排行
```
customer_name | city | order_count | total_spent | avg_order_amount
--------------|------|-------------|-------------|-----------------
张三          | 北京 | 5           | 2095.00     | 419.00
李四          | 上海 | 4           | 1596.00     | 399.00
王五          | 广州 | 3           | 2394.00     | 798.00
赵六          | 深圳 | 3           | 1197.00     | 399.00
```
