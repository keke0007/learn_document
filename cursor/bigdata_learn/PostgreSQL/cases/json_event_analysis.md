# 案例3：JSON 事件日志分析（PostgreSQL）

## 一、案例目标

- **场景**：应用埋点或行为日志以 JSON 形式写入 PostgreSQL，通过 JSONB + GIN 索引进行分析。
- **目标**：
  - 练习 `jsonb` 类型的使用与查询。
  - 掌握 GIN 索引和常见 JSON 操作符。
  - 完成简单的 PV/事件统计与路径分析。

对应数据与脚本：

- 数据文件：`data/events.jsonl`（一行一个 JSON 对象）
- 建表脚本：`scripts/setup_tables.sql`
- 加载脚本：`scripts/load_data.sql`（JSON 部分）
- 查询脚本：`scripts/common_queries.sql`（事件分析部分）

---

## 二、数据说明（events.jsonl）

字段（JSON 中的 key）：

- `ts`：事件时间（ISO8601 字符串）
- `user_id`：用户 ID
- `event_type`：事件类型（如：`page_view`、`click`）
- `page`：页面路径
- `device`：设备类型（如：`ios`、`android`、`pc`）
- `duration`：停留时长（秒，可选）

示例几行：

```json
{"ts":"2024-03-14T10:00:01","user_id":1,"event_type":"page_view","page":"/home","device":"ios","duration":12}
{"ts":"2024-03-14T10:00:05","user_id":2,"event_type":"page_view","page":"/home","device":"android","duration":8}
{"ts":"2024-03-14T10:00:10","user_id":1,"event_type":"click","page":"/product","device":"ios","duration":5}
{"ts":"2024-03-14T10:01:02","user_id":3,"event_type":"page_view","page":"/home","device":"pc","duration":20}
...
```

---

## 三、表结构与索引（节选）

```sql
SET search_path TO bigdata_demo;

CREATE TABLE events (
    id      bigserial PRIMARY KEY,
    ts      timestamp NOT NULL,
    payload jsonb     NOT NULL
);

-- 常用字段上的 GIN 索引
CREATE INDEX idx_events_payload_gin
ON events
USING gin (payload);

-- 或者为特定键创建表达式索引
CREATE INDEX idx_events_event_type
ON events ((payload ->> 'event_type'));
```

---

## 四、数据加载思路（示例）

### 1. 使用 `\copy` + `jsonb` 转换

一种简单方式是先导入到临时表，再转换：

```sql
CREATE TEMP TABLE raw_events (line text);

\copy raw_events FROM 'data/events.jsonl';

INSERT INTO events (ts, payload)
SELECT
    (jsonb_extract_path_text(line::jsonb, 'ts'))::timestamp AS ts,
    line::jsonb AS payload
FROM raw_events;
```

> 实际使用时可在 `scripts/load_data.sql` 中写好上述逻辑。

---

## 五、典型 JSON 分析查询

### 1. 查询某类型事件

```sql
SELECT id, ts, payload
FROM events
WHERE payload ->> 'event_type' = 'page_view'
ORDER BY ts
LIMIT 10;
```

### 2. 统计每种事件类型的数量

```sql
SELECT
    payload ->> 'event_type' AS event_type,
    COUNT(*)                 AS cnt
FROM events
GROUP BY payload ->> 'event_type'
ORDER BY cnt DESC;
```

### 3. 按页面统计 PV 与平均停留时长

```sql
SELECT
    payload ->> 'page' AS page,
    COUNT(*)           AS pv,
    AVG( (payload ->> 'duration')::numeric ) AS avg_duration
FROM events
WHERE payload ? 'duration'
GROUP BY page
ORDER BY pv DESC;
```

### 4. 最近 10 分钟内按设备统计 PV

```sql
SELECT
    payload ->> 'device' AS device,
    COUNT(*)             AS pv
FROM events
WHERE ts >= now() - interval '10 minutes'
  AND payload ->> 'event_type' = 'page_view'
GROUP BY device
ORDER BY pv DESC;
```

---

## 六、练习建议

1. 为 `events` 设计更细粒度的表达式索引（如 `(payload ->> 'page')`），比较查询性能差异。  
2. 增加字段 `session_id` 到 JSON 中，并基于该字段做简单的会话分析（每个 session 的页面序列）。  
3. 对比在 ClickHouse/Doris 中对埋点数据的处理方式，思考 PostgreSQL 适合扮演的角色（如：小规模实时分析、准实时监控等）。  

