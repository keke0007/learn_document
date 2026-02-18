-- Hive 常用查询示例

-- ============================================
-- 1. 基本查询
-- ============================================

-- 查询所有数据
SELECT * FROM employee LIMIT 10;

-- 条件查询
SELECT name, salary FROM employee WHERE salary > 5000;

-- 排序
SELECT * FROM employee ORDER BY salary DESC LIMIT 5;

-- ============================================
-- 2. 聚合查询
-- ============================================

-- 分组统计
SELECT 
    department,
    COUNT(*) as count,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary,
    MIN(salary) as min_salary
FROM employee
GROUP BY department;

-- 使用 HAVING 过滤
SELECT 
    department,
    AVG(salary) as avg_salary
FROM employee
GROUP BY department
HAVING AVG(salary) > 6000;

-- ============================================
-- 3. 连接查询
-- ============================================

-- 内连接
SELECT 
    e.name,
    e.salary,
    d.dept_name,
    d.location
FROM employee e
INNER JOIN department d ON e.department = d.dept_id;

-- 左连接
SELECT 
    e.name,
    e.salary,
    d.dept_name
FROM employee e
LEFT JOIN department d ON e.department = d.dept_id;

-- ============================================
-- 4. 子查询
-- ============================================

-- 子查询示例
SELECT name, salary
FROM employee
WHERE salary > (SELECT AVG(salary) FROM employee);

-- IN 子查询
SELECT * FROM employee
WHERE department IN (
    SELECT dept_id FROM department WHERE location = '北京'
);

-- ============================================
-- 5. 窗口函数
-- ============================================

-- ROW_NUMBER
SELECT 
    name,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employee;

-- RANK
SELECT 
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank
FROM employee;

-- 累计求和
SELECT 
    name,
    salary,
    SUM(salary) OVER (PARTITION BY department ORDER BY salary DESC) as cumulative
FROM employee;

-- ============================================
-- 6. 字符串函数
-- ============================================

-- 字符串连接
SELECT CONCAT(name, '-', department) as info FROM employee;

-- 字符串截取
SELECT SUBSTRING(name, 1, 2) as short_name FROM employee;

-- 大小写转换
SELECT UPPER(name), LOWER(department) FROM employee;

-- ============================================
-- 7. 日期函数
-- ============================================

-- 当前日期
SELECT CURRENT_DATE();

-- 提取日期部分
SELECT 
    name,
    YEAR(hire_date) as hire_year,
    MONTH(hire_date) as hire_month,
    DAY(hire_date) as hire_day
FROM employee;

-- 日期差
SELECT 
    name,
    DATEDIFF(CURRENT_DATE(), hire_date) as days_worked
FROM employee;

-- ============================================
-- 8. 条件函数
-- ============================================

-- IF 函数
SELECT 
    name,
    salary,
    IF(salary > 5000, '高薪', '普通') as level
FROM employee;

-- CASE WHEN
SELECT 
    name,
    salary,
    CASE 
        WHEN salary > 8000 THEN '高薪'
        WHEN salary > 5000 THEN '中等'
        ELSE '普通'
    END as salary_level
FROM employee;

-- ============================================
-- 9. 集合函数
-- ============================================

-- 去重统计
SELECT COUNT(DISTINCT department) as dept_count FROM employee;

-- 分组去重
SELECT 
    department,
    COUNT(DISTINCT id) as employee_count
FROM employee
GROUP BY department;
