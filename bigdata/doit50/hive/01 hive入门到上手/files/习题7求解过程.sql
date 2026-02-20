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


--  全局TOPN：  本月，访问次数最多的前3名用户及其访问次数 
--  全局TOPN：  本月，男性中访问次数最多的前3名用户及其访问次数 
SELECT
    id,
    count(1) as cnt
FROM  user_login
group by id


+-----+------+
| id  | cnt  |
+-----+------+
| 1   | 9    |
| 2   | 5    |
| 3   | 3    |
| 4   | 1    |
| 5   | 2    |
+-----+------+



SELECT
    id,
    count(1) as cnt
FROM  user_login
group by id
order by cnt desc 
limit 3

+-----+------+
| id  | cnt  |
+-----+------+
| 1   | 9    |
| 2   | 5    |
| 3   | 3    |
+-----+------+



--  分组TOPN：  本月，各性别中访问次数最多的前3名用户及其访问次数 

男性,1,....
男性,2,....
男性,3,....

女性,1,....
女性,2,....
女性,3,....


SELECT
    gender ,
    id, 
    count(1) as cnt 
FROM user_login
group by gender,id


+---------+-----+------+
| gender  | id  | cnt  |
+---------+-----+------+
| male    | 1   | 9    |  1
| male    | 2   | 5    |  2
| male    | 3   | 3    |  3

| female  | 4   | 1    |  1
| female  | 5   | 2    |  2
+---------+-----+------+

SELECT
    gender,
    id,
    cnt,
    row_number() over(partition by gender order by cnt desc ) as rn 
FROM ( 

    SELECT
        gender ,
        id, 
        count(1) as cnt 
    FROM user_login
    group by gender,id

) tmp1

+---------+-----+------+-----+
| gender  | id  | cnt  | rn  |
+---------+-----+------+-----+
| female  | 5   | 2    | 1   |
| female  | 4   | 1    | 2   |
| male    | 1   | 9    | 1   |
| male    | 2   | 5    | 2   |
| male    | 3   | 3    | 3   |
+---------+-----+------+-----+

SELECT
    gender,
    id,
    cnt,
    rn
FROM (

    SELECT
        gender,
        id,
        cnt,
        row_number() over(partition by gender order by cnt desc ) as rn 
    FROM ( 

        SELECT
            gender ,
            id, 
            count(1) as cnt 
        FROM user_login
        group by gender,id

    ) tmp1

) tmp2 
WHERE rn<=2

+---------+-----+------+-----+
| gender  | id  | cnt  | rn  |
+---------+-----+------+-----+
| female  | 5   | 2    | 1   |
| female  | 4   | 1    | 2   |
| male    | 1   | 9    | 1   |
| male    | 2   | 5    | 2   |
+---------+-----+------+-----+