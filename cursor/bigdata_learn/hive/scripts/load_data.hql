-- Hive 数据加载脚本
-- 注意：请根据实际路径修改数据文件路径

-- ============================================
-- 案例1：员工管理 - 加载数据
-- ============================================

-- 加载员工数据（本地文件）
LOAD DATA LOCAL INPATH '/path/to/hive/data/employee.txt' INTO TABLE employee;

-- 加载部门数据（本地文件）
LOAD DATA LOCAL INPATH '/path/to/hive/data/department.txt' INTO TABLE department;

-- 如果数据在 HDFS 上，使用以下命令：
-- LOAD DATA INPATH '/user/hive/data/employee.txt' INTO TABLE employee;
-- LOAD DATA INPATH '/user/hive/data/department.txt' INTO TABLE department;

-- ============================================
-- 案例2：销售数据分析 - 加载数据
-- ============================================

LOAD DATA LOCAL INPATH '/path/to/hive/data/orders.txt' INTO TABLE orders;
LOAD DATA LOCAL INPATH '/path/to/hive/data/products.txt' INTO TABLE products;
LOAD DATA LOCAL INPATH '/path/to/hive/data/customers.txt' INTO TABLE customers;

-- ============================================
-- 案例3：用户行为分析 - 加载数据
-- ============================================

LOAD DATA LOCAL INPATH '/path/to/hive/data/user_logs.txt' INTO TABLE user_logs;
LOAD DATA LOCAL INPATH '/path/to/hive/data/users.txt' INTO TABLE users;
