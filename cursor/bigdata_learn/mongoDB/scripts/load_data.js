// MongoDB 学习示例：加载 users / orders / events 数据
// 在 mongo/mongosh 中运行：load("scripts/load_data.js");

use("bigdata_mongo");

// 方式一：使用 mongoimport（推荐在命令行执行）：
// mongoimport --db bigdata_mongo --collection users  --file data/users.json  --jsonArray
// mongoimport --db bigdata_mongo --collection orders --file data/orders.json --jsonArray
// mongoimport --db bigdata_mongo --collection events --file data/events.jsonl --type json --jsonArray false

// 方式二：在 mongosh 内部读取文件（示意，需确保 can read file）：
// 注意：某些环境中不支持直接读取本地文件，这里仅做思路演示。

// 示例：如果你的环境支持 cat()，可以这样加载 JSON 数组：
/*
var usersData = JSON.parse(cat("data/users.json"));
db.users.insertMany(usersData);

var ordersData = JSON.parse(cat("data/orders.json"));
db.orders.insertMany(ordersData);

// events.jsonl 每行一个 JSON 文本
var raw = cat("data/events.jsonl").split("\n").filter(l => l.trim().length > 0);
var eventsDocs = raw.map(l => JSON.parse(l));
db.events.insertMany(eventsDocs);
*/

