+----------------+----------------------+------------------------+--------------------+--------------------+-----------------------+
| user_login.id  | user_login.username  | user_login.login_date  | user_login.device  | user_login.gender  | user_login.stay_long  |
+----------------+----------------------+------------------------+--------------------+--------------------+-----------------------+
| 1              | aaa                  | 2024-08-01             | android            | male               | 5                     |
| 1              | aaa                  | 2024-08-01             | android            | male               | 5                     |
| 1              | aaa                  | 2024-08-01             | android            | male               | 5                     |
| 2              | bbb                  | 2024-08-01             | android            | male               | 3                     |
| 2              | bbb                  | 2024-08-01             | android            | male               | 3                     |
| 3              | ccc                  | 2024-08-01             | ios                | male               | 2                     |
| 4              | ddd                  | 2024-08-01             | ios                | female             | 6                     |
| 1              | aaa                  | 2024-08-02             | android            | male               | 4                     |
| 2              | bbb                  | 2024-08-02             | android            | male               | 2                     |
| 3              | ccc                  | 2024-08-02             | ios                | male               | 2                     |
| 5              | eee                  | 2024-08-02             | ios                | female             | 5                     |
| 1              | aaa                  | 2024-08-03             | android            | male               | 5                     |
| 1              | aaa                  | 2024-08-03             | android            | male               | 5                     |
| 5              | eee                  | 2024-08-03             | ios                | female             | 5                     |
| 1              | aaa                  | 2024-08-04             | ios                | male               | 6                     |
| 3              | ccc                  | 2024-08-04             | ios                | male               | 6                     |
| 2              | bbb                  | 2024-08-05             | ios                | male               | 6                     |
| 1              | aaa                  | 2024-08-05             | ios                | male               | 2                     |
| 1              | aaa                  | 2024-08-05             | ios                | male               | 2                     |
| 2              | bbb                  | 2024-08-06             | android            | male               | 1                     |
+----------------+----------------------+------------------------+--------------------+--------------------+-----------------------+


-- -- 9. 查询如下结果：
-- 用户  日期      访问时长   累计时长
-- 1    2024-08-01      30        30
-- 1    2024-08-02      50        80
-- 1    2024-08-02      20        100


-- 首先，求个人每天的访问时长

SELECT
    id,
    login_date,
    sum(stay_long) as perday_long

FROM user_login
GROUP BY id,login_date


-- 然后，对上面的数据追加一个累计字段（sum over)

SELECT
id,
login_date,
perday_long,
sum(perday_long) over(partition by id order by login_date) as accu_long

FROM (
    SELECT
        id,
        login_date,
        sum(stay_long) as perday_long

    FROM user_login
    GROUP BY id,login_date
) tmp1

+-----+-------------+--------------+------------+
| id  | login_date  | perday_long  | accu_long  |
+-----+-------------+--------------+------------+
| 1   | 2024-08-01  | 15           | 15         |
| 1   | 2024-08-02  | 4            | 19         |
| 1   | 2024-08-03  | 10           | 29         |
| 1   | 2024-08-04  | 6            | 35         |
| 1   | 2024-08-05  | 4            | 39         |
| 2   | 2024-08-01  | 6            | 6          |
| 2   | 2024-08-02  | 2            | 8          |
| 2   | 2024-08-05  | 6            | 14         |
| 2   | 2024-08-06  | 1            | 15         |
| 3   | 2024-08-01  | 2            | 2          |
| 3   | 2024-08-02  | 2            | 4          |
| 3   | 2024-08-04  | 6            | 10         |
| 4   | 2024-08-01  | 6            | 6          |
| 5   | 2024-08-02  | 5            | 5          |
| 5   | 2024-08-03  | 5            | 10         |
+-----+-------------+--------------+------------+