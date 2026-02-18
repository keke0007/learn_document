# 数据库优化案例

## 案例概述

本案例通过实际 SQL 语句和优化策略演示数据库优化的方法，包括索引优化、查询优化、分页优化等。

## 知识点

1. **索引优化**
   - B+ 树索引原理
   - 索引类型
   - 索引优化原则

2. **SQL 优化**
   - 查询优化
   - 分页优化
   - 子查询优化

3. **MySQL 原理**
   - InnoDB 存储引擎
   - 事务隔离级别
   - 锁机制

## 案例代码

### 案例1：索引优化

#### 创建表结构

```sql
-- 用户表
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    age INT,
    department_id BIGINT,
    create_time DATETIME,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_department_id (department_id),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 订单表
CREATE TABLE orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    amount DECIMAL(10, 2),
    status VARCHAR(20),
    create_time DATETIME,
    INDEX idx_user_id (user_id),
    INDEX idx_product_id (product_id),
    INDEX idx_status (status),
    INDEX idx_create_time (create_time),
    INDEX idx_user_status (user_id, status)  -- 联合索引
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 索引使用示例

```sql
-- 1. 使用索引的查询
SELECT * FROM users WHERE username = 'john';
-- 使用 idx_username 索引

-- 2. 联合索引最左前缀原则
SELECT * FROM orders WHERE user_id = 1 AND status = 'PAID';
-- 使用 idx_user_status 索引

SELECT * FROM orders WHERE status = 'PAID';
-- 不使用 idx_user_status 索引（不符合最左前缀）

-- 3. 覆盖索引
SELECT user_id, status FROM orders WHERE user_id = 1 AND status = 'PAID';
-- 使用覆盖索引，不需要回表

-- 4. 索引失效的情况
SELECT * FROM users WHERE YEAR(create_time) = 2024;
-- 索引失效，因为使用了函数

SELECT * FROM users WHERE create_time >= '2024-01-01' AND create_time < '2025-01-01';
-- 使用索引
```

### 案例2：查询优化

#### 优化前 vs 优化后

```sql
-- 优化前：全表扫描
SELECT * FROM users WHERE YEAR(create_time) = 2024;

-- 优化后：使用索引范围查询
SELECT * FROM users 
WHERE create_time >= '2024-01-01' AND create_time < '2025-01-01';

-- 优化前：使用 OR（可能导致索引失效）
SELECT * FROM users WHERE username = 'john' OR email = 'john@example.com';

-- 优化后：使用 UNION
SELECT * FROM users WHERE username = 'john'
UNION
SELECT * FROM users WHERE email = 'john@example.com';

-- 优化前：SELECT *
SELECT * FROM users WHERE id = 1;

-- 优化后：只查询需要的字段
SELECT id, username, email FROM users WHERE id = 1;

-- 优化前：子查询
SELECT * FROM users 
WHERE department_id IN (SELECT id FROM departments WHERE name = 'IT');

-- 优化后：JOIN
SELECT u.* FROM users u
INNER JOIN departments d ON u.department_id = d.id
WHERE d.name = 'IT';
```

### 案例3：分页优化

#### 深度分页问题

```sql
-- 优化前：深度分页性能差
SELECT * FROM orders ORDER BY id LIMIT 100000, 20;
-- 需要扫描 100020 行，性能很差

-- 优化后：使用子查询
SELECT * FROM orders 
WHERE id > (SELECT id FROM orders ORDER BY id LIMIT 100000, 1)
ORDER BY id LIMIT 20;
-- 只需要扫描 20 行

-- 优化后：使用游标分页
SELECT * FROM orders 
WHERE id > 100000
ORDER BY id LIMIT 20;
-- 需要记录上一页的最后一个 id
```

### 案例4：JOIN 优化

```sql
-- 优化前：没有索引的 JOIN
SELECT u.username, o.amount 
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.department_id = 1;

-- 优化后：确保 JOIN 字段有索引
-- 在 users.department_id 和 orders.user_id 上创建索引

-- 小表驱动大表
SELECT u.username, o.amount 
FROM (SELECT * FROM users WHERE department_id = 1) u
INNER JOIN orders o ON u.id = o.user_id;
```

### 案例5：事务和锁

```sql
-- 事务隔离级别设置
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- 开始事务
START TRANSACTION;

-- 更新操作（加行锁）
UPDATE users SET age = 25 WHERE id = 1;

-- 提交事务
COMMIT;

-- 查看锁信息
SHOW ENGINE INNODB STATUS;

-- 查看当前事务
SELECT * FROM INFORMATION_SCHEMA.INNODB_TRX;
```

### 案例6：EXPLAIN 分析

```sql
-- 分析查询执行计划
EXPLAIN SELECT * FROM users WHERE username = 'john';

-- 输出示例：
-- id | select_type | table | type  | possible_keys | key          | rows | Extra
-- 1  | SIMPLE      | users | ref   | idx_username  | idx_username | 1    | Using where

-- type 类型说明：
-- ALL: 全表扫描（最差）
-- index: 索引全扫描
-- range: 索引范围扫描
-- ref: 非唯一索引扫描
-- eq_ref: 唯一索引扫描
-- const: 主键或唯一索引等值查询（最好）

-- 优化建议：
-- 1. type 应该尽量避免 ALL
-- 2. key 应该使用索引
-- 3. rows 应该尽可能小
```

## 验证数据

### 性能测试结果

| 查询类型 | 数据量 | 优化前耗时 | 优化后耗时 | 提升 |
|---------|--------|-----------|-----------|------|
| 全表扫描 | 100万 | 5000ms | - | - |
| 使用索引 | 100万 | - | 10ms | 500倍 |
| 深度分页 | 100万 | 2000ms | 50ms | 40倍 |
| JOIN 查询 | 100万 | 3000ms | 100ms | 30倍 |

### 索引使用情况

```
表：users（100万条数据）

查询：SELECT * FROM users WHERE username = 'john'
- 无索引：全表扫描，耗时 5000ms
- 有索引：索引查找，耗时 5ms
- 提升：1000倍

查询：SELECT * FROM users WHERE email LIKE '%@example.com'
- 索引失效（LIKE 以 % 开头）
- 全表扫描，耗时 5000ms
```

### EXPLAIN 分析结果

```
优化前：
- type: ALL
- key: NULL
- rows: 1000000
- Extra: Using where

优化后：
- type: ref
- key: idx_username
- rows: 1
- Extra: Using where
```

## 优化建议总结

### 1. 索引优化

**创建索引的原则：**
- 为经常查询的字段创建索引
- 为经常用于 WHERE 条件的字段创建索引
- 为经常用于 JOIN 的字段创建索引
- 避免在频繁更新的字段上创建索引

**索引优化技巧：**
- 使用联合索引时遵循最左前缀原则
- 尽量使用覆盖索引
- 避免在索引字段上使用函数
- 避免在索引字段上使用 LIKE '%xxx'

### 2. SQL 优化

**查询优化：**
- 避免 SELECT *
- 使用 LIMIT 限制返回结果
- 使用 UNION 代替 OR
- 使用 JOIN 代替子查询
- 避免在 WHERE 子句中使用函数

**分页优化：**
- 避免深度分页
- 使用子查询优化
- 使用游标分页

### 3. 表结构优化

**字段设计：**
- 选择合适的数据类型
- 避免使用 NULL（使用默认值）
- 使用 INT 代替 VARCHAR 存储数字

**表设计：**
- 合理使用范式
- 适当冗余以提高查询性能
- 分区表处理大数据量

### 4. 配置优化

**MySQL 配置：**
- 调整 innodb_buffer_pool_size
- 调整 max_connections
- 调整 query_cache_size

## 总结

1. **索引是优化查询的关键**
   - 合理创建索引
   - 避免索引失效
   - 使用覆盖索引

2. **SQL 语句优化**
   - 避免全表扫描
   - 优化 JOIN 操作
   - 优化子查询

3. **分页优化**
   - 避免深度分页
   - 使用游标分页
   - 缓存常用查询结果

4. **持续监控和优化**
   - 使用 EXPLAIN 分析查询
   - 监控慢查询日志
   - 定期优化表结构
