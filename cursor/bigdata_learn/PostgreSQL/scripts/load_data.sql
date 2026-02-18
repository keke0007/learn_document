-- PostgreSQL 学习示例：加载 CSV 与 JSON 数据

SET search_path TO bigdata_demo;

-- 建议使用 psql 的 \copy 从本地文件导入：
-- \copy departments FROM 'PostgreSQL/data/departments.csv' CSV HEADER;
-- \copy employees   FROM 'PostgreSQL/data/employees.csv'   CSV HEADER;
-- \copy customers   FROM 'PostgreSQL/data/customers.csv'   CSV HEADER;
-- \copy products    FROM 'PostgreSQL/data/products.csv'    CSV HEADER;
-- \copy orders      FROM 'PostgreSQL/data/orders.csv'      CSV HEADER;

-- JSONL 事件日志加载示例

CREATE TEMP TABLE IF NOT EXISTS raw_events (line text);

-- 在 psql 中执行：
-- \copy raw_events FROM 'PostgreSQL/data/events.jsonl';

INSERT INTO events (ts, payload)
SELECT
    (line::jsonb ->> 'ts')::timestamp AS ts,
    line::jsonb                       AS payload
FROM raw_events;

