SET search_path TO bigdata_demo;

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

-- 部门员工数与平均薪资
SELECT
    d.dept_name,
    COUNT(e.emp_id) AS emp_count,
    AVG(e.salary)   AS avg_salary
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
    COUNT(*)          AS order_count,
    SUM(total_amount) AS total_sales
FROM orders;

-- 按月统计销售额
SELECT
    date_trunc('month', order_date) AS month,
    COUNT(*)                        AS order_count,
    SUM(total_amount)               AS monthly_sales
FROM orders
GROUP BY month
ORDER BY month;

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
-- JSON 事件分析
-- =========================

-- 各事件类型数量
SELECT
    payload ->> 'event_type' AS event_type,
    COUNT(*)                 AS cnt
FROM events
GROUP BY payload ->> 'event_type'
ORDER BY cnt DESC;

-- 按页面统计 PV
SELECT
    payload ->> 'page' AS page,
    COUNT(*)           AS pv
FROM events
WHERE payload ->> 'event_type' = 'page_view'
GROUP BY page
ORDER BY pv DESC;

