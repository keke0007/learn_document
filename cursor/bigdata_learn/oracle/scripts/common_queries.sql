ALTER SESSION SET CURRENT_SCHEMA = bigdata_user;

-- =========================
-- 员工与部门查询
-- =========================

-- 所有员工及其部门
SELECT
    e.emp_id,
    e.emp_name,
    d.dept_name,
    e.salary,
    e.hire_date
FROM employees e
JOIN departments d
  ON e.dept_id = d.dept_id
ORDER BY e.emp_id;

-- 每个部门员工数与平均薪资
SELECT
    d.dept_name,
    COUNT(e.emp_id)   AS emp_count,
    AVG(e.salary)     AS avg_salary
FROM departments d
LEFT JOIN employees e
  ON d.dept_id = e.dept_id
GROUP BY d.dept_name
ORDER BY emp_count DESC;

-- =========================
-- 订单与销售分析
-- =========================

-- 总销售额与订单数
SELECT
    COUNT(*)        AS order_count,
    SUM(total_amount) AS total_sales
FROM orders;

-- 按月份统计销售额
SELECT
    TO_CHAR(order_date, 'YYYY-MM') AS ym,
    COUNT(*)                       AS order_count,
    SUM(total_amount)              AS monthly_sales
FROM orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY ym;

-- 产品销量排行
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

-- =========================
-- 事务与并发（手工按案例操作）
-- =========================

-- 示例：显式事务控制
-- UPDATE employees SET salary = salary + 1000 WHERE emp_id = 1001;
-- SAVEPOINT before_bonus;
-- ...
-- ROLLBACK TO before_bonus;
-- COMMIT;

