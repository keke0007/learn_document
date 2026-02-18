USE bigdata_demo;

-- 请将下面路径修改为你本机的实际路径
-- 例如：C:/Users/ke/Desktop/bigdata_learn/clickhouse/data/orders_offline.csv

INSERT INTO orders_offline
FORMAT CSV
INFILE 'C:/Users/ke/Desktop/bigdata_learn/clickhouse/data/orders_offline.csv';

INSERT INTO users_offline
FORMAT CSV
INFILE 'C:/Users/ke/Desktop/bigdata_learn/clickhouse/data/users_offline.csv';

