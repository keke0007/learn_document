-- 1,从行为日志表找账号为null的设备id
/*
SELECT
device_id

FROM (
    SELECT
    device_id
    FROM event_log
    WHERE user_name is null
    GROUP BY device_id 
) tmp1
WHERE device_id NOT IN (
    SELECT
    device_id
    FROM device_bind

    UNION 

    SELECT
    device_id
    FROM tmp_device 
)
*/
-----------------------

-------1,从行为日志表找账号为null的设备id-----------------
SELECT  
   tmp1.device_id
FROM 
(

    SELECT
    device_id
    FROM event_log
    WHERE user_name is null
    GROUP BY device_id 
) tmp1

LEFT JOIN 
(
    SELECT
    device_id
    FROM device_bind

    UNION 

    SELECT
    device_id
    FROM tmp_device 
) tmp2 
ON tmp1.device_id = tmp2.device_id
WHERE tmp2.device_id is null


+-----------------+
| tmp1.device_id  |
+-----------------+
| d106            |  
+-----------------+ 
| d127            |   -- 测试数据不存在
+-----------------+

-------2,为找到的设备id，生成临时id ，并把结果覆盖掉原来的临时id表 -----------------


-- 关联到最大id
SELECT
device_id,
max_id

FROM 
(
    SELECT  
       tmp1.device_id
    FROM 
    (

        SELECT
        device_id
        FROM event_log
        WHERE user_name is null
        GROUP BY device_id 
    ) tmp1

    LEFT JOIN 
    (
        SELECT
        device_id
        FROM device_bind

        UNION 

        SELECT
        device_id
        FROM tmp_device 
    ) tmp2 
    ON tmp1.device_id = tmp2.device_id
    WHERE tmp2.device_id is null
) a 
JOIN 
( SELECT MAX(tmp_id) as max_id from tmp_device ) b 



+------------+---------+
| device_id  | max_id  |
+------------+---------+
| d106       | 100002  |
+------------+---------+
| d127       | 100002  |  -- 测试数据不存在
+------------+---------+


-- 生成rownumber + 最大id => 临时id

INSERT INTO TABLE tmp_device 

SELECT
device_id,
max_id + row_number() over()  as tmp_id

FROM 
(
    SELECT  
       tmp1.device_id
    FROM 
    (

        SELECT
        device_id
        FROM event_log
        WHERE user_name is null
        GROUP BY device_id 
    ) tmp1

    LEFT JOIN 
    (
        SELECT
        device_id
        FROM device_bind

        UNION 

        SELECT
        device_id
        FROM tmp_device 
    ) tmp2 
    ON tmp1.device_id = tmp2.device_id
    WHERE tmp2.device_id is null
) a 
JOIN 
( SELECT MAX(tmp_id) as max_id from tmp_device ) b 



+------------+---------+
| device_id  | tmp_id  |
+------------+---------+
| d106       | 100003  |
+------------+---------+