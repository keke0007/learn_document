# 案例1：员工管理案例

## 案例描述
创建一个员工管理系统，包含员工基本信息、部门信息，并进行各种统计分析。

## 数据准备

### 1. 员工表数据 (employee.txt)
```
1,张三,25,5000.0,IT,2023-01-15
2,李四,30,8000.0,HR,2022-06-20
3,王五,28,6000.0,IT,2023-03-10
4,赵六,35,12000.0,Sales,2021-09-05
5,孙七,27,5500.0,IT,2023-05-18
6,周八,32,9000.0,HR,2022-11-12
7,吴九,29,7000.0,Sales,2023-02-28
8,郑十,26,4800.0,IT,2023-07-01
9,钱一,31,8500.0,HR,2022-08-15
10,陈二,33,11000.0,Sales,2021-12-20
```

### 2. 部门表数据 (department.txt)
```
IT,技术部,北京,50
HR,人力资源部,上海,20
Sales,销售部,广州,30
```

## 建表语句

```sql
-- 创建员工表
CREATE TABLE IF NOT EXISTS employee (
    id INT,
    name STRING,
    age INT,
    salary DOUBLE,
    department STRING,
    hire_date DATE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- 创建部门表
CREATE TABLE IF NOT EXISTS department (
    dept_id STRING,
    dept_name STRING,
    location STRING,
    employee_count INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

## 加载数据

```sql
-- 加载员工数据
LOAD DATA LOCAL INPATH '/path/to/employee.txt' INTO TABLE employee;

-- 加载部门数据
LOAD DATA LOCAL INPATH '/path/to/department.txt' INTO TABLE department;
```

## 查询案例

### 1. 基本查询
```sql
-- 查询所有员工
SELECT * FROM employee;

-- 查询 IT 部门员工
SELECT * FROM employee WHERE department = 'IT';

-- 查询薪资大于 6000 的员工
SELECT name, salary, department 
FROM employee 
WHERE salary > 6000 
ORDER BY salary DESC;
```

### 2. 聚合统计
```sql
-- 各部门平均薪资
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary,
    MIN(salary) as min_salary,
    SUM(salary) as total_salary
FROM employee
GROUP BY department;

-- 年龄分组统计
SELECT 
    CASE 
        WHEN age < 25 THEN '25岁以下'
        WHEN age < 30 THEN '25-30岁'
        WHEN age < 35 THEN '30-35岁'
        ELSE '35岁以上'
    END as age_group,
    COUNT(*) as count,
    AVG(salary) as avg_salary
FROM employee
GROUP BY 
    CASE 
        WHEN age < 25 THEN '25岁以下'
        WHEN age < 30 THEN '25-30岁'
        WHEN age < 35 THEN '30-35岁'
        ELSE '35岁以上'
    END;
```

### 3. 连接查询
```sql
-- 员工和部门信息关联
SELECT 
    e.name,
    e.salary,
    e.department,
    d.dept_name,
    d.location
FROM employee e
LEFT JOIN department d ON e.department = d.dept_id;

-- 各部门员工详情
SELECT 
    d.dept_name,
    d.location,
    e.name,
    e.salary,
    e.age
FROM department d
LEFT JOIN employee e ON d.dept_id = e.department
ORDER BY d.dept_name, e.salary DESC;
```

### 4. 窗口函数
```sql
-- 各部门薪资排名
SELECT 
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    RANK() OVER (ORDER BY salary DESC) as overall_rank
FROM employee;

-- 各部门薪资累计
SELECT 
    name,
    department,
    salary,
    SUM(salary) OVER (PARTITION BY department ORDER BY salary DESC) as cumulative_salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary
FROM employee;
```

### 5. 子查询
```sql
-- 查询薪资高于部门平均薪资的员工
SELECT 
    name,
    department,
    salary
FROM employee e1
WHERE salary > (
    SELECT AVG(salary) 
    FROM employee e2 
    WHERE e2.department = e1.department
);

-- 查询各部门薪资最高的员工
SELECT 
    name,
    department,
    salary
FROM employee e1
WHERE salary = (
    SELECT MAX(salary) 
    FROM employee e2 
    WHERE e2.department = e1.department
);
```

### 6. 日期函数
```sql
-- 计算员工工作年限
SELECT 
    name,
    hire_date,
    DATEDIFF(CURRENT_DATE(), hire_date) as days_worked,
    ROUND(DATEDIFF(CURRENT_DATE(), hire_date) / 365.0, 2) as years_worked
FROM employee;

-- 按入职年份统计
SELECT 
    YEAR(hire_date) as hire_year,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary
FROM employee
GROUP BY YEAR(hire_date)
ORDER BY hire_year;
```

## 预期结果

### 各部门统计结果
```
department | employee_count | avg_salary | max_salary | min_salary | total_salary
-----------|----------------|------------|------------|------------|-------------
HR         | 3              | 8500.0     | 9000.0     | 8000.0     | 25500.0
IT         | 4              | 5575.0     | 6000.0     | 4800.0     | 22300.0
Sales      | 3              | 10000.0    | 12000.0    | 7000.0     | 30000.0
```

### 薪资排名（前5名）
```
name | department | salary | overall_rank
-----|------------|--------|--------------
赵六 | Sales      | 12000.0| 1
陈二 | Sales      | 11000.0| 2
周八 | HR         | 9000.0 | 3
钱一 | HR         | 8500.0 | 4
李四 | HR         | 8000.0 | 5
```
