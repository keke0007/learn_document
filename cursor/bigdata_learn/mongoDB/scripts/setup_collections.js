// MongoDB 学习示例：创建集合与索引

use("bigdata_mongo");

// 用户集合
db.createCollection("users");
db.users.createIndex({ user_id: 1 }, { unique: true });
db.users.createIndex({ city: 1 });
db.users.createIndex({ tags: 1 });

// 订单集合
db.createCollection("orders");
db.orders.createIndex({ order_id: 1 }, { unique: true });
db.orders.createIndex({ user_id: 1, order_date: 1 });
db.orders.createIndex({ city: 1 });

// 事件集合
db.createCollection("events");
db.events.createIndex({ ts: 1 });
db.events.createIndex({ event_type: 1 });
db.events.createIndex({ page: 1 });
db.events.createIndex({ user_id: 1 });

