create table t_hit_rat(
username string,
seq   int,
is_hit int

)
row format delimited fields terminated by ','
;


load data local inpath '/root/hit.txt' into table t_hit_rat;


--------------

SELECT
  *
FROM  t_hit_rat
WHERE is_hit = 1

+---------------------+----------------+-------------------+
| t_hit_rat.username  | t_hit_rat.seq  | t_hit_rat.is_hit  |
+---------------------+----------------+-------------------+
| a                   | 1              | 1                 |
| a                   | 2              | 1                 |
| a                   | 4              | 1                 |
| b                   | 2              | 1                 |
| b                   | 3              | 1                 |
| b                   | 4              | 1                 |
| c                   | 2              | 1                 |
| c                   | 3              | 1                 |
| c                   | 4              | 1                 |
| c                   | 5              | 1                 |
| c                   | 7              | 1                 |
| c                   | 8              | 1                 |
| c                   | 9              | 1                 |
+---------------------+----------------+-------------------+



SELECT
username,
seq,
seq - row_number() over(partition by username order by seq ) as diff

FROM (
    SELECT
      *
    FROM  t_hit_rat
    WHERE is_hit = 1

) tmp1


+-----------+------+-------+
| username  | seq  | diff  |
+-----------+------+-------+
| a         | 1    | 0     |
| a         | 2    | 0     |
| a         | 4    | 1     |

| b         | 2    | 1     |
| b         | 3    | 1     |
| b         | 4    | 1     |

| c         | 2    | 1     |
| c         | 3    | 1     |
| c         | 4    | 1     |
| c         | 5    | 1     |

| c         | 7    | 2     |
| c         | 8    | 2     |
| c         | 9    | 2     |
+-----------+------+-------+



SELECT

    username,
    count(1) as cnt

FROM
( 
    SELECT
    username,
    seq,
    seq - row_number() over(partition by username order by seq ) as diff

    FROM (
        SELECT
          *
        FROM  t_hit_rat
        WHERE is_hit = 1

    ) tmp1

) tmp2
GROUP by username,diff
having count(1)>=3

+-----------+------+
| username  | cnt  |
+-----------+------+
| b         | 3    |
| c         | 4    |
| c         | 3    |
+-----------+------+



SELECT
username,
max(cnt) as max_hitcnt

FROM (
    SELECT

        username,
        count(1) as cnt

    FROM
    ( 
        SELECT
        username,
        seq,
        seq - row_number() over(partition by username order by seq ) as diff

        FROM (
            SELECT
              *
            FROM  t_hit_rat
            WHERE is_hit = 1

        ) tmp1

    ) tmp2
    GROUP by username,diff
    having count(1)>=3
) tmp3
GROUP BY username


+-----------+-------------+
| username  | max_hitcnt  |
+-----------+-------------+
| b         | 3           |
| c         | 4           |
+-----------+-------------+