// MongoDB 学习示例：常用查询与聚合
// 在 mongosh 中运行：load("scripts/common_queries.js");

use("bigdata_mongo");

// =========================
// 用户相关查询
// =========================

// 查询部分用户
print("== Users from 北京 ==");
printjson(
  db.users.find({ city: "北京" }, { _id: 0, user_id: 1, name: 1, city: 1 }).toArray()
);

// 按城市统计用户数
print("== User count by city ==");
printjson(
  db.users.aggregate([
    { $group: { _id: "$city", userCount: { $sum: 1 } } },
    { $sort: { userCount: -1 } }
  ]).toArray()
);

// =========================
// 订单相关查询
// =========================

print("== Total sales summary ==");
printjson(
  db.orders.aggregate([
    {
      $group: {
        _id: null,
        orderCount: { $sum: 1 },
        totalSales: { $sum: "$total_amount" }
      }
    }
  ]).toArray()
);

print("== Monthly sales ==");
printjson(
  db.orders.aggregate([
    {
      $addFields: {
        month: { $substr: ["$order_date", 0, 7] }
      }
    },
    {
      $group: {
        _id: "$month",
        orderCount: { $sum: 1 },
        monthlySales: { $sum: "$total_amount" }
      }
    },
    { $sort: { "_id": 1 } }
  ]).toArray()
);

// =========================
// 事件日志相关查询
// =========================

print("== Event type distribution ==");
printjson(
  db.events.aggregate([
    {
      $group: {
        _id: "$event_type",
        cnt: { $sum: 1 }
      }
    },
    { $sort: { cnt: -1 } }
  ]).toArray()
);

print("== Page view count by page ==");
printjson(
  db.events.aggregate([
    { $match: { event_type: "page_view" } },
    {
      $group: {
        _id: "$page",
        pv: { $sum: 1 }
      }
    },
    { $sort: { pv: -1 } }
  ]).toArray()
);

