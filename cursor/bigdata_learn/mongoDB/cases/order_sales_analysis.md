# 案例2：订单与销售分析（MongoDB）

## 一、案例目标

- **场景**：基于 MongoDB 中的订单文档，进行基础销售统计（总销售额、按城市/用户/日期维度分析）。
- **目标**：
  - 理解如何在 MongoDB 中存储订单数据。
  - 熟练使用 Aggregation Pipeline 做分组聚合与排序。
  - 为日志/事件分析案例提供订单侧参照。

对应数据与脚本：

- 数据文件：`data/orders.json`、`data/users.json`
- 集合初始化脚本：`scripts/setup_collections.js`
- 数据加载脚本：`scripts/load_data.js`
- 查询脚本：`scripts/common_queries.js`（订单分析部分）

---

## 二、数据结构说明

### 1. 订单文档结构（orders 集合）

字段设计：

- `order_id`：订单 ID
- `user_id`：用户 ID
- `order_date`：下单时间（字符串或 Date）
- `city`：下单城市
- `product`：产品名称（或 `product_id`）
- `quantity`：数量
- `total_amount`：订单金额
- `status`：订单状态（如：`paid`、`cancelled`）

示例文档：

```json
{
  "order_id": 1001,
  "user_id": 1,
  "order_date": "2024-01-15",
  "city": "北京",
  "product": "手机",
  "quantity": 1,
  "total_amount": 2999.00,
  "status": "paid"
}
```

> `data/orders.json` 中包含约 15 条类似记录。

---

## 三、索引与集合设置（节选）

在 `scripts/setup_collections.js` 中可包含类似逻辑：

```javascript
use bigdata_mongo;

db.createCollection("orders");

db.orders.createIndex({ order_id: 1 }, { unique: true });
db.orders.createIndex({ user_id: 1, order_date: 1 });
db.orders.createIndex({ city: 1 });
```

---

## 四、典型销售分析查询

### 1. 总销售额与订单数

```javascript
db.orders.aggregate([
  {
    $group: {
      _id: null,
      orderCount: { $sum: 1 },
      totalSales: { $sum: "$total_amount" }
    }
  }
]);
```

### 2. 按月份统计销售额

假设 `order_date` 为 `"YYYY-MM-DD"` 字符串：

```javascript
db.orders.aggregate([
  {
    $addFields: {
      month: { $substr: ["$order_date", 0, 7] } // "YYYY-MM"
    }
  },
  {
    $group: {
      _id: "$month",
      orderCount: { $sum: 1 },
      monthlySales: { $sum: "$total_amount" },
      avgOrderAmount: { $avg: "$total_amount" }
    }
  },
  { $sort: { _id: 1 } }
]);
```

### 3. 按城市统计销售额

```javascript
db.orders.aggregate([
  {
    $group: {
      _id: "$city",
      orderCount: { $sum: 1 },
      citySales: { $sum: "$total_amount" }
    }
  },
  { $sort: { citySales: -1 } }
]);
```

### 4. 用户消费排行（基于 user_id）

```javascript
db.orders.aggregate([
  {
    $group: {
      _id: "$user_id",
      orderCount: { $sum: 1 },
      totalSpent: { $sum: "$total_amount" },
      avgOrderAmount: { $avg: "$total_amount" }
    }
  },
  { $sort: { totalSpent: -1 } },
  { $limit: 10 }
]);
```

如需关联用户信息（`users` 集合），可使用 `$lookup`：

```javascript
db.orders.aggregate([
  {
    $group: {
      _id: "$user_id",
      orderCount: { $sum: 1 },
      totalSpent: { $sum: "$total_amount" }
    }
  },
  {
    $lookup: {
      from: "users",
      localField: "_id",
      foreignField: "user_id",
      as: "user"
    }
  },
  { $unwind: "$user" },
  {
    $project: {
      _id: 0,
      user_id: "$_id",
      user_name: "$user.name",
      city: "$user.city",
      orderCount: 1,
      totalSpent: 1
    }
  },
  { $sort: { totalSpent: -1 } }
]);
```

---

## 五、练习建议

1. 增加字段 `status` 并按状态统计订单数量与金额（如：已支付/已取消）。  
2. 按 `user_id` + `month` 维度聚合，统计用户每月消费总额，尝试在管道中使用多阶段 `$group`。  
3. 将本案例和关系型数据库中的销售分析（例如 `PostgreSQL/cases/sales_analysis.md`）进行对比，理解 MongoDB 聚合管道与 SQL 聚合的差异与优劣。  

