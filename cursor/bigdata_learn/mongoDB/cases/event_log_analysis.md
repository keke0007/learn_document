# 案例3：事件/日志聚合分析（MongoDB）

## 一、案例目标

- **场景**：应用埋点或访问日志以 JSON 文档形式写入 MongoDB，对事件类型、页面、设备等维度进行统计分析。
- **目标**：
  - 掌握使用集合存储 JSON 事件文档。
  - 使用 Aggregation Pipeline 完成基础 PV/事件统计。
  - 与订单分析案例形成对比，理解 MongoDB 在日志场景中的使用方式。

对应数据与脚本：

- 数据文件：`data/events.jsonl`
- 集合初始化脚本：`scripts/setup_collections.js`
- 数据加载脚本：`scripts/load_data.js`
- 查询脚本：`scripts/common_queries.js`（事件分析部分）

---

## 二、数据结构说明

### 1. 事件文档结构（events 集合）

字段设计：

- `ts`：事件时间（ISO8601 字符串或 Date）
- `user_id`：用户 ID
- `event_type`：事件类型（如：`page_view`、`click`）
- `page`：页面路径（如：`/home`、`/product`）
- `device`：设备类型（如：`ios`、`android`、`pc`）
- `duration`：停留时长（秒，可选）

`events.jsonl` 中每行一个 JSON 对象，例如：

```json
{"ts":"2024-03-14T10:00:01","user_id":1,"event_type":"page_view","page":"/home","device":"ios","duration":12}
{"ts":"2024-03-14T10:00:05","user_id":2,"event_type":"page_view","page":"/home","device":"android","duration":8}
```

---

## 三、集合与索引（节选）

在 `scripts/setup_collections.js` 中可包含类似逻辑：

```javascript
use bigdata_mongo;

db.createCollection("events");

db.events.createIndex({ ts: 1 });
db.events.createIndex({ event_type: 1 });
db.events.createIndex({ page: 1 });
db.events.createIndex({ user_id: 1 });
```

---

## 四、典型事件分析查询

### 1. 查询最近 N 条事件

```javascript
db.events.find({})
  .sort({ ts: -1 })
  .limit(10);
```

### 2. 统计不同事件类型的数量

```javascript
db.events.aggregate([
  {
    $group: {
      _id: "$event_type",
      cnt: { $sum: 1 }
    }
  },
  { $sort: { cnt: -1 } }
]);
```

### 3. 按页面统计 PV 与平均停留时长

```javascript
db.events.aggregate([
  {
    $match: {
      event_type: "page_view",
      duration: { $exists: true }
    }
  },
  {
    $group: {
      _id: "$page",
      pv: { $sum: 1 },
      avgDuration: { $avg: "$duration" }
    }
  },
  { $sort: { pv: -1 } }
]);
```

### 4. 最近 10 分钟内按设备统计 PV

（假设 `ts` 存为 Date 类型；如果是字符串，可在加载时转换）

```javascript
const tenMinutesAgo = new Date(Date.now() - 10 * 60 * 1000);

db.events.aggregate([
  {
    $match: {
      ts: { $gte: tenMinutesAgo },
      event_type: "page_view"
    }
  },
  {
    $group: {
      _id: "$device",
      pv: { $sum: 1 }
    }
  },
  { $sort: { pv: -1 } }
]);
```

---

## 五、练习建议

1. 为事件增加字段 `session_id`，统计每个 `session` 内的页面数与总停留时长。  
2. 基于 `page` 和 `event_type` 维度做联合聚合（如：统计不同页面上的点击数与浏览数之比）。  
3. 将本案例与 PostgreSQL 的 JSONB 事件分析案例对比，体会 MongoDB 在日志场景中的优势（天然 JSON 文档存储 + 聚合管道）与不足（如复杂事务能力）。  

