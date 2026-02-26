# 如果是 Flink SQL 实现三种时间属性，如何实现，一般使用 
CREATE TABLE 表名 （字段 类型 , ... , action_time AS proctime()）


create table t_order (
`userid` varchar,
`timestamp` bigint,
`money` double,
`category` varchar,
`pt` AS PROCTIME()
) with (
'connector' = 'filesystem',
'path' = 'file:///export/data/input/order.csv',
'format' = 'csv'
);