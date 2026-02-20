+----------------+------------------------+--------------------+-----------------------+
| user_login.id  | user_login.login_date  | user_login.gender  | user_login.stay_long  |
+----------------+------------------------+--------------------+-----------------------+
| 1              | 2024-08-01             | male               | 5                     |
| 1              | 2024-08-01             | male               | 5                     |
| 1              | 2024-08-01             | male               | 5                     |
| 2              | 2024-08-01             | male               | 3                     |
| 2              | 2024-08-01             | male               | 3                     |
| 3              | 2024-08-01             | male               | 2                     |
| 4              | 2024-08-01             | female             | 6                     |
| 1              | 2024-08-02             | male               | 4                     |
| 2              | 2024-08-02             | male               | 2                     |
| 3              | 2024-08-02             | male               | 2                     |
| 5              | 2024-08-02             | female             | 5                     |
| 1              | 2024-08-03             | male               | 5                     |
| 1              | 2024-08-03             | male               | 5                     |
| 5              | 2024-08-03             | female             | 5                     |
| 1              | 2024-08-04             | male               | 6                     |
| 3              | 2024-08-04             | male               | 6                     |
| 2              | 2024-08-05             | male               | 6                     |
| 1              | 2024-08-05             | male               | 2                     |
| 1              | 2024-08-05             | male               | 2                     |
| 2              | 2024-08-06             | male               | 1                     |
+----------------+------------------------+--------------------+-----------------------+

-- 6. 本月，查询 各性别 访问总时长 最长的前2名 用户及访问总时长
-- 审题： 首先要计算出每个用户的访问总时长
--        然后，按性别分区，在分区中，排序，找到排在最前面的3行

select 
    gender,
    id,
    sum(stay_long) as user_amt_timelong
from user_login 
group by gender,id 

+---------+-----+--------------------+
| gender  | id  | user_amt_timelong  |
+---------+-----+--------------------+
| male    | 1   | 39                 |
| male    | 2   | 15                 |
| male    | 3   | 10                 |

| female  | 4   | 6                  |
| female  | 5   | 10                 |
+---------+-----+--------------------+

select 
   gender,
   id,
   user_amt_timelong,
   row_number() over(partition by gender order by user_amt_timelong desc) as rn 

from (
    select 
        gender,
        id,
        sum(stay_long) as user_amt_timelong
    from user_login 
    group by gender,id 
) tmp1 
where rn<=2


+---------+-----+--------------------+-----+
| gender  | id  | user_amt_timelong  | rn  |
+---------+-----+--------------------+-----+
| female  | 5   | 10                 | 1   |
| female  | 4   | 6                  | 2   |

| male    | 1   | 39                 | 1   |
| male    | 2   | 15                 | 2   |
| male    | 3   | 10                 | 3   |
+---------+-----+--------------------+-----+


select
    gender,
    id,
    user_amt_timelong,
    rn

from (
    select 
       gender,
       id,
       user_amt_timelong,
       row_number() over(partition by gender order by user_amt_timelong desc) as rn 

    from (
        select 
            gender,
            id,
            sum(stay_long) as user_amt_timelong
        from user_login 
        group by gender,id 
    ) tmp1 
) tmp2 
where rn<=2


+---------+-----+--------------------+-----+
| gender  | id  | user_amt_timelong  | rn  |
+---------+-----+--------------------+-----+
| female  | 5   | 10                 | 1   |
| female  | 4   | 6                  | 2   |
| male    | 1   | 39                 | 1   |
| male    | 2   | 15                 | 2   |
+---------+-----+--------------------+-----+