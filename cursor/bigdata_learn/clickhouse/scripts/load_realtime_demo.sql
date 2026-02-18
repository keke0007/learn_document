USE bigdata_demo;

-- 一次性导入模拟实时埋点数据（演示用）
-- 请将路径改为你本机实际路径

INSERT INTO events_realtime
FORMAT CSV
INFILE 'C:/Users/ke/Desktop/bigdata_learn/clickhouse/data/events_realtime.csv';

