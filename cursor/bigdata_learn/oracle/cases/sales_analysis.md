# 案例2：订单与销售分析（Oracle）

## 一、案例目标

- **场景**：典型电商订单分析，基于客户、产品和订单数据做销售统计与客户价值分析。
- **目标**：
  - 练习多表关联查询（订单 + 客户 + 产品）。
  - 掌握按时间/客户/产品维度的聚合统计。
  - 初步接触执行计划与索引优化思路。

对应数据与脚本：

- 数据文件：`data/customers.csv`、`data/products.csv`、`data/orders.csv`
- 建表脚本：`scripts/setup_tables.sql`
- 加载脚本：`scripts/load_data.sql`
- 查询脚本：`scripts/common_queries.sql`（销售分析部分）

---

## 二、数据说明

### 1. 客户表（customers.csv）

字段：

- `customer_id`：客户 ID（主键）
- `customer_name`：客户姓名
- `city`：所在城市
- `level`：客户级别（如：普通、银卡、金卡）

示例：

```text
customer_id,customer_name,city,level
C001,张三,北京,金卡
C002,李四,上海,银卡
C003,王五,广州,普通
C004,赵六,深圳,金卡
C005,小红,杭州,普通
C006,小明,成都,银卡
```

### 2. 产品表（products.csv）

字段：

- `product_id`：产品 ID（主键）
- `product_name`：产品名称
- `category`：产品类别
- `price`：单价

示例：

```text
product_id,product_name,category,price
P001,手机,电子产品,2999.00
P002,笔记本电脑,电子产品,5999.00
P003,耳机,电子产品,299.00
P004,鼠标,电子产品,99.00
P005,键盘,电子产品,199.00
P006,显示器,电子产品,1299.00
```

### 3. 订单表（orders.csv）

字段：

- `order_id`：订单 ID（主键）
- `order_date`：下单日期
- `customer_id`：客户 ID（外键）
- `product_id`：产品 ID（外键）
- `quantity`：数量
- `total_amount`：订单金额

示例（与大数据模块中的规模类似，便于跨技术对比）：

```text
order_id,order_date,customer_id,product_id,quantity,total_amount
1001,2024-01-15,C001,P001,1,2999.00
1002,2024-01-16,C002,P002,1,5999.00
1003,2024-01-17,C001,P003,3,897.00
1004,2024-01-18,C003,P001,1,2999.00
1005,2024-01-19,C002,P004,2,198.00
1006,2024-02-01,C001,P002,1,5999.00
1007,2024-02-02,C004,P003,2,598.00
1008,2024-02-03,C003,P001,3,8997.00
1009,2024-02-04,C002,P004,1,99.00
1010,2024-02-05,C001,P005,2,398.00
1011,2024-03-10,C004,P001,1,2999.00
1012,2024-03-11,C003,P002,2,11998.00
1013,2024-03-12,C001,P003,1,299.00
1014,2024-03-13,C002,P004,3,297.00
1015,2024-03-14,C004,P005,1,199.00
```

---

## 三、建表与约束（节选）

```sql
CREATE TABLE customers (
    customer_id   VARCHAR2(10)  PRIMARY KEY,
    customer_name VARCHAR2(50)  NOT NULL,
    city          VARCHAR2(50),
    level         VARCHAR2(20)
);

CREATE TABLE products (
    product_id    VARCHAR2(10)  PRIMARY KEY,
    product_name  VARCHAR2(50)  NOT NULL,
    category      VARCHAR2(50),
    price         NUMBER(10,2)  NOT NULL
);

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
```

---

## 四、典型销售分析查询

### 1. 总销售额与订单数

```sql
SELECT
    COUNT(*)        AS order_count,
    SUM(total_amount) AS total_sales
FROM orders;
```

### 2. 按月份统计销售额

```sql
SELECT
    TO_CHAR(order_date, 'YYYY-MM') AS ym,
    COUNT(*)                       AS order_count,
    SUM(total_amount)              AS monthly_sales,
    AVG(total_amount)              AS avg_order_amount
FROM orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY ym;
```

### 3. 产品销量排行

```sql
SELECT
    p.product_name,
    p.category,
    SUM(o.quantity)     AS total_quantity,
    SUM(o.total_amount) AS total_sales
FROM orders o
JOIN products p
  ON o.product_id = p.product_id
GROUP BY p.product_name, p.category
ORDER BY total_sales DESC;
```

### 4. 城市维度销售分析

```sql
SELECT
    c.city,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(o.order_id)             AS order_count,
    SUM(o.total_amount)           AS city_sales
FROM orders o
JOIN customers c
  ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY city_sales DESC;
```

### 5. 客户消费排行

```sql
SELECT
    c.customer_id,
    c.customer_name,
    c.level,
    COUNT(o.order_id)             AS order_count,
    SUM(o.total_amount)           AS total_spent,
    AVG(o.total_amount)           AS avg_order_amount
FROM orders o
JOIN customers c
  ON o.customer_id = c.customer_id
GROUP BY
    c.customer_id, c.customer_name, c.level
ORDER BY total_spent DESC;
```

---

## 五、简单执行计划与索引使用

在 SQL*Plus 或其他工具中，可以使用：

```sql
EXPLAIN PLAN FOR
SELECT
    c.customer_id,
    c.customer_name,
    SUM(o.total_amount) AS total_spent
FROM orders o
JOIN customers c
  ON o.customer_id = c.customer_id
WHERE o.order_date >= DATE '2024-01-01'
GROUP BY c.customer_id, c.customer_name;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

观察：
- 是否使用了 `idx_orders_customer_date` 索引  
- 是否存在全表扫描（FULL TABLE SCAN）  

---

## 六、练习建议

1. 为 `orders` 表添加分区（例如按月份 RANGE 分区），思考在大数据量下对查询和维护的帮助。
2. 编写一个 PL/SQL 存储过程，输入客户 ID，输出该客户在 2024 年的总消费金额。
3. 将本案例与 `hive/cases/sales_analysis.md`、`clickhouse/cases/offline_order_analysis.md` 和 `doris/cases/offline_order_analysis.md` 对比，体会 **OLTP（Oracle）与 OLAP（Hive/ClickHouse/Doris）** 在建模和查询上的差异。 +

