# 案例1：员工与部门管理（PostgreSQL）

## 一、案例目标

- **场景**：典型的人力资源（HR）子系统，涉及员工与部门关系、部门平均薪资等基础查询。
- **目标**：
  - 掌握在 PostgreSQL 中创建表、约束和索引。
  - 练习常见的单表、多表查询与聚合。
  - 为后续订单分析和 JSON 日志分析打基础。

对应数据与脚本：

- 数据文件：`data/employees.csv`、`data/departments.csv`
- 建表脚本：`scripts/setup_tables.sql`
- 加载脚本：`scripts/load_data.sql`（或使用 `\copy`）
- 查询脚本：`scripts/common_queries.sql`（员工/部门部分）

---

## 二、数据说明

### 1. 部门表（departments.csv）

字段：

- `dept_id`：部门 ID（主键）
- `dept_name`：部门名称
- `location`：所在城市

示例数据：

```text
dept_id,dept_name,location
10,研发部,北京
20,市场部,上海
30,财务部,深圳
40,人力资源部,广州
```

### 2. 员工表（employees.csv）

字段：

- `emp_id`：员工 ID（主键）
- `emp_name`：姓名
- `dept_id`：部门 ID（外键）
- `salary`：薪资
- `hire_date`：入职日期

示例数据：

```text
emp_id,emp_name,dept_id,salary,hire_date
1001,张三,10,12000,2020-01-15
1002,李四,10,15000,2019-03-20
1003,王五,20,10000,2021-07-01
1004,赵六,20,9000,2022-02-10
1005,小红,30,8000,2018-11-05
1006,小明,30,9500,2019-06-18
1007,小李,40,7000,2020-09-30
1008,小王,40,7200,2021-12-12
1009,老刘,10,18000,2017-05-03
1010,老王,20,11000,2016-08-22
```

---

## 三、建表与约束（节选）

```sql
SET search_path TO bigdata_demo;

CREATE TABLE departments (
    dept_id    integer       PRIMARY KEY,
    dept_name  varchar(50)   NOT NULL,
    location   varchar(50)
);

CREATE TABLE employees (
    emp_id     integer       PRIMARY KEY,
    emp_name   varchar(50)   NOT NULL,
    dept_id    integer       REFERENCES departments(dept_id),
    salary     numeric(10,2),
    hire_date  date
);

CREATE INDEX idx_employees_dept_salary
ON employees (dept_id, salary);
```

> 完整建表语句见 `scripts/setup_tables.sql`。

---

## 四、典型查询示例

### 1. 查询所有员工及其所在部门

```sql
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
```

### 2. 每个部门的员工数与平均薪资

```sql
SELECT
    d.dept_name,
    COUNT(e.emp_id) AS emp_count,
    AVG(e.salary)   AS avg_salary,
    MAX(e.salary)   AS max_salary,
    MIN(e.salary)   AS min_salary
FROM departments d
LEFT JOIN employees e
  ON d.dept_id = e.dept_id
GROUP BY d.dept_name
ORDER BY emp_count DESC;
```

### 3. 工资高于本部门平均薪资的员工

```sql
SELECT
    e.emp_id,
    e.emp_name,
    d.dept_name,
    e.salary
FROM employees e
JOIN departments d
  ON e.dept_id = d.dept_id
WHERE e.salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE dept_id = e.dept_id
)
ORDER BY d.dept_name, e.salary DESC;
```

### 4. 按入职年份统计员工数量

```sql
SELECT
    date_part('year', hire_date) AS hire_year,
    COUNT(*)                     AS emp_count
FROM employees
GROUP BY hire_year
ORDER BY hire_year;
```

---

## 五、练习建议

1. 为员工表增加字段 `job_title`（职位），并统计各职位的平均薪资与员工数。  
2. 创建一个只包含“北京/上海”部门员工的视图，并基于视图做统计查询。  
3. 使用 `EXPLAIN ANALYZE` 查看上述查询的执行计划，观察 `idx_employees_dept_salary` 是否被使用。  

