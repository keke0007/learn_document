1,1725260504000,event01,3      0   0    0
1,1725260505000,event02,4      0   0    0
1,1725260506000,event03,5      0   0    0
1,1725260507000,event03,5      0   0    0
1,1725260508000,event04,5      0   0    0
1,1725260510000,event04,5      0   0    0
1,1725260511000,event05,6      0   0    0
1,1725260512000,addcart,2      1   1    0

1,1725260514000,event04,3      0   1    1
1,1725260518000,event03,2      0   1    1
1,1725260520000,event02,4      0   1    1
1,1725260522000,event06,5      0   1    1
1,1725260523000,event08,3      0   1    1
1,1725260525000,addcart,4      1   2    1

1,1725260528000,event04,3      0   2    2
1,1725260530000,event03,2      0   2    2
1,1725260532000,event02,2      0   2    2
1,1725260534000,event04,2      0   2    2
1,1725260536000,event02,4      0   2    2
1,1725260542000,event06,3      0   2    2
1,1725260544000,event08,6      0   2    2
1,1725260548000,addcart,4      1   3    2

1,1725260556000,event02,3      0   3    3
1,1725260552000,event06,2      0   3    3
1,1725260554000,event08,3      0   3    3


create table user_events(
    user_id      int,
    time_stamp   bigint,
    event_id     string,
    timelong     int
)
row format delimited fields terminated by ','
;

load data local inpath '/root/events.txt' into table user_events;


+----------------------+-------------------------+-----------------------+-----------------------+
| user_events.user_id  | user_events.time_stamp  | user_events.event_id  | user_events.timelong  |
+----------------------+-------------------------+-----------------------+-----------------------+
| 1                    | 1725260504000           | event01               | 3                     |
| 1                    | 1725260505000           | event02               | 4                     |
| 1                    | 1725260506000           | event03               | 5                     |
| 1                    | 1725260507000           | event03               | 5                     |
| 1                    | 1725260508000           | event04               | 5                     |
| 1                    | 1725260510000           | event04               | 5                     |
| 1                    | 1725260511000           | event05               | 6                     |
| 1                    | 1725260512000           | addcart               | 2                     |
| 1                    | 1725260514000           | event04               | 3                     |
| 1                    | 1725260518000           | event03               | 2                     |
| 1                    | 1725260520000           | event02               | 4                     |
| 1                    | 1725260522000           | event06               | 5                     |
| 1                    | 1725260523000           | event08               | 3                     |
| 1                    | 1725260525000           | addcart               | 4                     |
| 1                    | 1725260528000           | event04               | 3                     |
| 1                    | 1725260530000           | event03               | 2                     |
| 1                    | 1725260532000           | event02               | 2                     |
| 1                    | 1725260534000           | event04               | 2                     |
| 1                    | 1725260536000           | event02               | 4                     |
| 1                    | 1725260542000           | event06               | 3                     |
| 1                    | 1725260544000           | event08               | 6                     |
| 1                    | 1725260548000           | addcart               | 4                     |
| 1                    | 1725260556000           | event02               | 3                     |
| 1                    | 1725260552000           | event06               | 2                     |
| 1                    | 1725260554000           | event08               | 3                     |
+----------------------+-------------------------+-----------------------+-----------------------+


-- 1，对addcart打标记

SELECT
   user_id,
   time_stamp,
   event_id,
   timelong,
   if(event_id = 'addcart', 1 ,0) as flag
FROM  user_events
+----------+----------------+-----------+-----------+-------+
| user_id  |   time_stamp   | event_id  | timelong  | flag  |
+----------+----------------+-----------+-----------+-------+
| 1        | 1725260504000  | event01   | 3         | 0     |
| 1        | 1725260505000  | event02   | 4         | 0     |
| 1        | 1725260506000  | event03   | 5         | 0     |
| 1        | 1725260507000  | event03   | 5         | 0     |
| 1        | 1725260508000  | event04   | 5         | 0     |
| 1        | 1725260510000  | event04   | 5         | 0     |
| 1        | 1725260511000  | event05   | 6         | 0     |
| 1        | 1725260512000  | addcart   | 2         | 1     |
| 1        | 1725260514000  | event04   | 3         | 0     |
| 1        | 1725260518000  | event03   | 2         | 0     |
| 1        | 1725260520000  | event02   | 4         | 0     |
| 1        | 1725260522000  | event06   | 5         | 0     |
| 1        | 1725260523000  | event08   | 3         | 0     |
| 1        | 1725260525000  | addcart   | 4         | 1     |
| 1        | 1725260528000  | event04   | 3         | 0     |
| 1        | 1725260530000  | event03   | 2         | 0     |
| 1        | 1725260532000  | event02   | 2         | 0     |
| 1        | 1725260534000  | event04   | 2         | 0     |
| 1        | 1725260536000  | event02   | 4         | 0     |
| 1        | 1725260542000  | event06   | 3         | 0     |
| 1        | 1725260544000  | event08   | 6         | 0     |
| 1        | 1725260548000  | addcart   | 4         | 1     |
| 1        | 1725260556000  | event02   | 3         | 0     |
| 1        | 1725260552000  | event06   | 2         | 0     |
| 1        | 1725260554000  | event08   | 3         | 0     |
+----------+----------------+-----------+-----------+-------+


-- 2，对标记做sum over

SELECT
    user_id,
    time_stamp,
    event_id,
    timelong,
    flag,
    sum(flag) over(partition by user_id order by time_stamp ) as flag2


FROM ( 

    SELECT
       user_id,
       time_stamp,
       event_id,
       timelong,
       if(event_id = 'addcart', 1 ,0) as flag
    FROM  user_events

) tmp1


-- 3,让flag2 - flag  
SELECT
    user_id,
    time_stamp,
    event_id,
    timelong,
    flag,
    flag2,
    flag2-flag as flag3

FROM (

    SELECT
        user_id,
        time_stamp,
        event_id,
        timelong,
        flag,
        sum(flag) over(partition by user_id order by time_stamp ) as flag2


    FROM ( 

        SELECT
           user_id,
           time_stamp,
           event_id,
           timelong,
           if(event_id = 'addcart', 1 ,0) as flag
        FROM  user_events

    ) tmp1

) tmp2

+----------+----------------+-----------+-----------+-------+--------+--------+
| user_id  |   time_stamp   | event_id  | timelong  | flag  | flag2  | flag3  |
+----------+----------------+-----------+-----------+-------+--------+--------+
| 1        | 1725260504000  | event01   | 3         | 0     | 0      | 0      |
| 1        | 1725260505000  | event02   | 4         | 0     | 0      | 0      |
| 1        | 1725260506000  | event03   | 5         | 0     | 0      | 0      |
| 1        | 1725260507000  | event03   | 5         | 0     | 0      | 0      |
| 1        | 1725260508000  | event04   | 5         | 0     | 0      | 0      |
| 1        | 1725260510000  | event04   | 5         | 0     | 0      | 0      |
| 1        | 1725260511000  | event05   | 6         | 0     | 0      | 0      |
| 1        | 1725260512000  | addcart   | 2         | 1     | 1      | 0      |
| 1        | 1725260514000  | event04   | 3         | 0     | 1      | 1      |
| 1        | 1725260518000  | event03   | 2         | 0     | 1      | 1      |
| 1        | 1725260520000  | event02   | 4         | 0     | 1      | 1      |
| 1        | 1725260522000  | event06   | 5         | 0     | 1      | 1      |
| 1        | 1725260523000  | event08   | 3         | 0     | 1      | 1      |
| 1        | 1725260525000  | addcart   | 4         | 1     | 2      | 1      |
| 1        | 1725260528000  | event04   | 3         | 0     | 2      | 2      |
| 1        | 1725260530000  | event03   | 2         | 0     | 2      | 2      |
| 1        | 1725260532000  | event02   | 2         | 0     | 2      | 2      |
| 1        | 1725260534000  | event04   | 2         | 0     | 2      | 2      |
| 1        | 1725260536000  | event02   | 4         | 0     | 2      | 2      |
| 1        | 1725260542000  | event06   | 3         | 0     | 2      | 2      |
| 1        | 1725260544000  | event08   | 6         | 0     | 2      | 2      |
| 1        | 1725260548000  | addcart   | 4         | 1     | 3      | 2      |
| 1        | 1725260552000  | event06   | 2         | 0     | 3      | 3      |
| 1        | 1725260554000  | event08   | 3         | 0     | 3      | 3      |
| 1        | 1725260556000  | event02   | 3         | 0     | 3      | 3      |
+----------+----------------+-----------+-----------+-------+--------+--------+


--4,按flag3分组聚合

SELECT
 user_id,
 flag3 as addcart_seq,
 sum(timelong) as segment_timelong

FROM (  
    SELECT
        user_id,
        time_stamp,
        event_id,
        timelong,
        flag,
        flag2,
        flag2-flag as flag3

    FROM (

            SELECT
                user_id,
                time_stamp,
                event_id,
                timelong,
                flag,
                sum(flag) over(partition by user_id order by time_stamp ) as flag2


            FROM ( 

                SELECT
                   user_id,
                   time_stamp,
                   event_id,
                   timelong,
                   if(event_id = 'addcart', 1 ,0) as flag
                FROM  user_events

            ) tmp1

        ) tmp2

)tmp3
GROUP BY user_id,flag3


+----------+--------------+-------------------+
| user_id  | addcart_seq  | segment_timelong  |
+----------+--------------+-------------------+
| 1        | 0            | 35                |
| 1        | 1            | 21                |
| 1        | 2            | 26                |
| 1        | 3            | 8                 |
+----------+--------------+-------------------+