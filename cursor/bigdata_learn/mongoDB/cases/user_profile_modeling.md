# 案例1：用户文档与嵌套结构建模（MongoDB）

## 一、案例目标

- **场景**：用户中心，存储用户基本信息、标签和多个地址信息。
- **目标**：
  - 掌握使用文档与嵌套结构存储用户数据。
  - 练习基本的 CRUD 与索引设计。
  - 为订单与日志分析案例提供用户维度基础。

对应数据与脚本：

- 数据文件：`data/users.json`
- 集合初始化脚本：`scripts/setup_collections.js`
- 数据加载脚本：`scripts/load_data.js`
- 查询脚本：`scripts/common_queries.js`（用户部分）

---

## 二、数据结构说明

### 1. 用户文档结构

字段设计（存储在 `users` 集合中）：

- `user_id`：用户 ID（数字或字符串）
- `name`：用户姓名
- `age`：年龄
- `city`：主要城市
- `tags`：标签数组（如“金卡”“高价值”等）
- `addresses`：地址数组，内嵌文档
  - `type`：地址类型（home / work 等）
  - `city`：城市
  - `detail`：详细地址
- `register_date`：注册时间

示例文档：

```json
{
  "user_id": 1,
  "name": "张三",
  "age": 25,
  "city": "北京",
  "tags": ["金卡", "高价值"],
  "addresses": [
    { "type": "home", "city": "北京", "detail": "朝阳区" },
    { "type": "work", "city": "北京", "detail": "中关村" }
  ],
  "register_date": "2023-01-01T00:00:00Z"
}
```

---

## 三、集合与索引设计（节选）

在 `scripts/setup_collections.js` 中可包含类似逻辑：

```javascript
use bigdata_mongo;

db.createCollection("users");

db.users.createIndex({ user_id: 1 }, { unique: true });
db.users.createIndex({ city: 1 });
db.users.createIndex({ "addresses.city": 1 });
```

---

## 四、典型操作与查询

### 1. 插入示例用户（单条）

```javascript
db.users.insertOne({
  user_id: 9,
  name: "新用户",
  age: 22,
  city: "杭州",
  tags: ["普通"],
  addresses: [
    { type: "home", city: "杭州", detail: "西湖区" }
  ],
  register_date: ISODate("2024-01-01T00:00:00Z")
});
```

### 2. 查询北京用户

```javascript
db.users.find(
  { city: "北京" },
  { _id: 0, user_id: 1, name: 1, city: 1, age: 1 }
);
```

### 3. 查询拥有某标签的用户

```javascript
db.users.find(
  { tags: "金卡" },
  { _id: 0, user_id: 1, name: 1, tags: 1 }
);
```

### 4. 查询拥有工作地址且在北京的用户

```javascript
db.users.find(
  { "addresses": { $elemMatch: { type: "work", city: "北京" } } },
  { _id: 0, user_id: 1, name: 1, addresses: 1 }
);
```

### 5. 按城市统计用户数

```javascript
db.users.aggregate([
  { $group: { _id: "$city", userCount: { $sum: 1 } } },
  { $sort: { userCount: -1 } }
]);
```

---

## 五、练习建议

1. 为 `users` 集合增加一个 `level` 字段（普通/银卡/金卡），并编写聚合查询统计各等级用户数量。  
2. 尝试拆分“地址”信息为单独集合 `addresses`，使用 `user_id` 建立关联，对比嵌入 vs 引用两种建模方式的查询写法与优劣。  
3. 基于 `register_date` 字段设计索引，并编写查询统计某时间段内注册的用户数。  

