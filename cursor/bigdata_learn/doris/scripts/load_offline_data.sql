-- Doris 离线数据导入示例（思路）
-- 实际执行请在终端使用 curl / Broker Load，根据环境调整。

-- 1. Stream Load 示例（本地 CSV -> Doris）
-- orders_offline
-- curl --location-trusted -u user:password \
--   -H "label:orders_offline_1" \
--   -H "column_separator:," \
--   -T C:/Users/ke/Desktop/bigdata_learn/doris/data/orders_offline.csv \
--   http://fe_host:8030/api/bigdata_demo/orders_offline/_stream_load

-- users_offline
-- curl --location-trusted -u user:password \
--   -H "label:users_offline_1" \
--   -H "column_separator:," \
--   -T C:/Users/ke/Desktop/bigdata_learn/doris/data/users_offline.csv \
--   http://fe_host:8030/api/bigdata_demo/users_offline/_stream_load

