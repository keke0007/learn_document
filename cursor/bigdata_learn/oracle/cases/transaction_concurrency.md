# 案例3：事务与并发控制（Oracle）

## 一、案例目标

- **场景**：两个会话同时修改同一行数据，引发锁等待；观察 Oracle 的事务行为与一致性读特性。
- **目标**：
  - 熟悉 `COMMIT / ROLLBACK / SAVEPOINT` 的作用。
  - 理解行级锁的行为以及锁等待现象。
  - 观察“读已提交 + 一致性读”的效果。

> 本案例不依赖额外数据文件，直接复用 `employees`、`orders` 等表即可。

---

## 二、环境准备

1. 确保已执行 `scripts/setup_tables.sql` 与 `scripts/load_data.sql`，创建并填充示例表。
2. 准备两个会话（Session A 和 Session B），可以分别在两个 SQL*Plus / SQL Developer 连接中操作。

---

## 三、事务基础示例

### 1. 显式事务控制

在任意会话中：

```sql
-- 查询某员工当前薪资
SELECT salary FROM employees WHERE emp_id = 1001;

-- 给该员工加薪 1000
UPDATE employees
SET salary = salary + 1000
WHERE emp_id = 1001;

-- 此时尚未提交，另一个会话看不到加薪效果（读已提交）
-- 可以设置保存点
SAVEPOINT before_bonus;

-- 如果发现加多了，可以回滚到保存点
UPDATE employees
SET salary = salary + 5000
WHERE emp_id = 1001;

ROLLBACK TO before_bonus;

-- 最终确认后提交
COMMIT;
```

---

## 四、行级锁与并发更新

### 步骤示例：两个会话更新同一行

#### 1. Session A：开启事务并锁定一行

```sql
-- Session A
ALTER SESSION SET CURRENT_SCHEMA = bigdata_user;

-- 查看当前薪资
SELECT emp_id, emp_name, salary
FROM employees
WHERE emp_id = 1002;

-- 更新员工 1002 的薪资（不提交）
UPDATE employees
SET salary = salary + 2000
WHERE emp_id = 1002;

-- 保持会话不提交/不回滚，行被加锁
```

#### 2. Session B：尝试更新同一行

```sql
-- Session B
ALTER SESSION SET CURRENT_SCHEMA = bigdata_user;

UPDATE employees
SET salary = salary + 1000
WHERE emp_id = 1002;
```

此时：
- Session B 的 `UPDATE` 会 **等待**，直到 Session A `COMMIT` 或 `ROLLBACK`。

#### 3. Session A：选择提交或回滚

```sql
-- Session A
COMMIT;
```

结果：
- Session B 的更新继续执行，在 Session A 已更新的基础上再加 1000。

你可以在 Session B 中再查询验证薪资：

```sql
SELECT emp_id, emp_name, salary
FROM employees
WHERE emp_id = 1002;
```

---

## 五、一致性读与快照

### 步骤示例：更新中读取数据

1. Session A 更新但不提交：

```sql
-- Session A
UPDATE employees
SET salary = salary + 3000
WHERE emp_id = 1003;
```

2. Session B 查询同一行：

```sql
-- Session B
SELECT emp_id, emp_name, salary
FROM employees
WHERE emp_id = 1003;
```

现象：
- Session B 看到的是 **更新前** 的薪资（基于 Undo 的一致性读），不会被正在进行的未提交事务“污染”（无脏读）。

3. 当 Session A `COMMIT` 后，Session B 再查询即可看到更新后的新值。

---

## 六、练习建议

1. 尝试让两个会话在不同顺序更新两行数据，模拟死锁场景，观察 Oracle 如何检测并回滚其中一个事务。
2. 在更新前使用 `SELECT ... FOR UPDATE` 显式加锁，体会其对后续会话行为的影响。
3. 将本案例和你在 MySQL/PostgreSQL 中看到的事务与锁行为进行对比，加深对 Oracle 一致性读实现方式的理解。 +

