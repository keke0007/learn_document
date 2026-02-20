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




-- 8. 查询本月，每个用户 访问时长最长的前3个日期

-- 先每个用户，每天的总访问时长
SELECT
    login_date,    -- 日期
    id,            -- 用户id
    sum(stay_long) as perday_long    -- 天访问时长

FROM user_login
GROUP BY login_date,id


-- 再按 用户分区  ，按天访问时长排序 ，打行号 

SELECT

    id,
    login_date,
    perday_long,
    row_number() over(PARTITION BY id ORDER BY perday_long desc ) as rn



FROM (

    SELECT
        login_date,    -- 日期
        id,            -- 用户id
        sum(stay_long) as perday_long    -- 天访问时长

    FROM user_login
    GROUP BY login_date,id

) tmp1


-- 然后过滤出rn<=3的数据即可
SELECT
id,
login_date,
perday_long,
rn

FROM (
    SELECT
        id,
        login_date,
        perday_long,
        row_number() over(PARTITION BY id ORDER BY perday_long desc ) as rn



    FROM (

        SELECT
            login_date,    -- 日期
            id,            -- 用户id
            sum(stay_long) as perday_long    -- 天访问时长

        FROM user_login
        GROUP BY login_date,id

    ) tmp1
) tmp2
WHERE rn<=2

+-----+-------------+--------------+-----+
| id  | login_date  | perday_long  | rn  |
+-----+-------------+--------------+-----+
| 1   | 2024-08-01  | 15           | 1   |
| 1   | 2024-08-03  | 10           | 2   |
| 2   | 2024-08-05  | 6            | 1   |
| 2   | 2024-08-01  | 6            | 2   |
| 3   | 2024-08-04  | 6            | 1   |
| 3   | 2024-08-01  | 2            | 2   |
| 4   | 2024-08-01  | 6            | 1   |
| 5   | 2024-08-03  | 5            | 1   |
| 5   | 2024-08-02  | 5            | 2   |
+-----+-------------+--------------+-----+