CREATE TABLE IF NOT EXISTS t_order(
    oid BIGINT,
    price double,
    create_time BIGINT,   # 存储时间戳类型
    rt as to_timestamp(from_unixtime(create_time))
)