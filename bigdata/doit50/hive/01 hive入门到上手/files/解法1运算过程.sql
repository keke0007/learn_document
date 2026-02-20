1,aaa,2024-08-01,android,male,5
1,aaa,2024-08-01,android,male,5
1,aaa,2024-08-01,android,male,5
2,bbb,2024-08-01,android,male,3
2,bbb,2024-08-01,android,male,3
3,ccc,2024-08-01,ios,male,2
4,ddd,2024-08-01,ios,female,6
1,aaa,2024-08-02,android,male,4
2,bbb,2024-08-02,android,male,2
3,ccc,2024-08-02,ios,male,2
5,eee,2024-08-02,ios,female,5
1,aaa,2024-08-03,android,male,5
1,aaa,2024-08-03,android,male,5
5,eee,2024-08-03,ios,female,5
1,aaa,2024-08-04,ios,male,6
3,ccc,2024-08-04,ios,male,6
2,bbb,2024-08-05,ios,male,6
1,aaa,2024-08-05,ios,male,2
1,aaa,2024-08-05,ios,male,2
2,bbb,2024-08-06,android,male,1



select
id,login_date
from user_login 
group by id,login_date

---
+-----+-------------+
| id  | login_date  |
+-----+-------------+
| 1   | 2024-08-01  |   
| 1   | 2024-08-02  |   
| 1   | 2024-08-03  |   
| 1   | 2024-08-04  |   
| 1   | 2024-08-05  |   

| 2   | 2024-08-01  |
| 2   | 2024-08-02  |
| 2   | 2024-08-05  |
| 2   | 2024-08-06  |

| 3   | 2024-08-01  |
| 3   | 2024-08-02  |
| 3   | 2024-08-04  |

| 4   | 2024-08-01  |
| 5   | 2024-08-02  |
| 5   | 2024-08-03  |
+-----+-------------+

----

with tmp as (
    select
        id,login_date
    from user_login 
    group by id,login_date
) 
select
  id,
  login_date,
  row_number() over(partition by id order by login_date) as rn 
from tmp 

+-----+-------------+-----+
| id  | login_date  | rn  |
+-----+-------------+-----+
| 1   | 2024-08-01  | 1   |
| 1   | 2024-08-02  | 2   |
| 1   | 2024-08-03  | 3   |
| 1   | 2024-08-04  | 4   |
| 1   | 2024-08-05  | 5   |

| 2   | 2024-08-01  | 1   |
| 2   | 2024-08-02  | 2   |
| 2   | 2024-08-05  | 3   |
| 2   | 2024-08-06  | 4   |

| 3   | 2024-08-01  | 1   |
| 3   | 2024-08-02  | 2   |
| 3   | 2024-08-04  | 3   |

| 4   | 2024-08-01  | 1   |

| 5   | 2024-08-02  | 1   |
| 5   | 2024-08-03  | 2   |
+-----+-------------+-----+


with tmp as (
    select
        id,login_date
    from user_login 
    group by id,login_date
) 

select

id,
login_date,
date_sub(to_date(login_date),rn) as diff


from (
    select
      id,
      login_date,
      row_number() over(partition by id order by login_date) as rn 
    from tmp 
) tmp2

+-----+-------------+-------------+
| id  | login_date  |    diff     |
+-----+-------------+-------------+
| 1   | 2024-08-01  | 2024-07-31  |
| 1   | 2024-08-02  | 2024-07-31  |
| 1   | 2024-08-03  | 2024-07-31  |
| 1   | 2024-08-04  | 2024-07-31  |
| 1   | 2024-08-05  | 2024-07-31  |

| 2   | 2024-08-01  | 2024-07-31  |
| 2   | 2024-08-02  | 2024-07-31  |

| 2   | 2024-08-05  | 2024-08-02  |
| 2   | 2024-08-06  | 2024-08-02  |

| 3   | 2024-08-01  | 2024-07-31  |
| 3   | 2024-08-02  | 2024-07-31  |
| 3   | 2024-08-04  | 2024-08-01  |

| 4   | 2024-08-01  | 2024-07-31  |

| 5   | 2024-08-02  | 2024-08-01  |
| 5   | 2024-08-03  | 2024-08-01  |
+-----+-------------+-------------+


with tmp as (
    select
        id,login_date
    from user_login 
    group by id,login_date
) 

select
id,
count(1) as lx_days

from (
    select

    id,
    login_date,
    date_sub(to_date(login_date),rn) as diff
    from (
        select
          id,
          login_date,
          row_number() over(partition by id order by login_date) as rn 
        from tmp 
    ) tmp2

)  tmp3 

group by id,diff
having count(1)>=3



+-----+----------+
| id  | lx_days  |
+-----+----------+
| 1   | 5        |
| 1   | 6        |

| 2   | 2        |
| 2   | 2        |
| 3   | 2        |
| 3   | 1        |
| 4   | 1        |
| 5   | 2        |
+-----+----------+



with tmp as (
    select
        id,login_date
    from user_login 
    group by id,login_date
) 

select
    id,
    max(lx_days) as max_lx_days
from (
    select
    id,
    count(1) as lx_days

    from (
        select
          id,
          login_date,
          date_sub(to_date(login_date),row_number() over(partition by id order by login_date)) as diff
        from tmp 
    )  tmp3 

    group by id,diff
    having count(1)>=3
) tmp4
group by id 