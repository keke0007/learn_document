-- Doris 实时数据导入示例（模拟）

-- 一次性导入模拟埋点数据（Stream Load）
-- curl --location-trusted -u user:password \
--   -H "label:events_realtime_1" \
--   -H "column_separator:," \
--   -T C:/Users/ke/Desktop/bigdata_learn/doris/data/events_realtime.csv \
--   http://fe_host:8030/api/bigdata_demo/events_realtime/_stream_load

