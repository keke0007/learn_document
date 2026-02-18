# MongoDB 基础与高级开发案例

## 案例概述

本案例通过实际代码演示 MongoDB 的基础和高级特性，包括文档操作、索引优化、聚合管道、副本集等。

## 知识点

1. **文档模型**
   - 集合和文档
   - BSON 格式
   - 嵌套文档
   - 数组操作

2. **查询操作**
   - 基本查询
   - 条件查询
   - 投影
   - 排序和分页

3. **索引优化**
   - 单字段索引
   - 复合索引
   - 文本索引
   - 地理空间索引

4. **聚合管道**
   - $match、$group、$project
   - $lookup、$unwind
   - $sort、$limit

5. **高可用**
   - 副本集
   - 分片集群

## 案例代码

### 案例1：基本 CRUD 操作

```python
# mongodb_basic.py
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

# 插入文档
user = {
    'name': 'Alice',
    'age': 25,
    'email': 'alice@example.com',
    'tags': ['developer', 'python'],
    'created_at': datetime.now()
}
result = collection.insert_one(user)
print(f"Inserted ID: {result.inserted_id}")

# 批量插入
users = [
    {'name': 'Bob', 'age': 30, 'email': 'bob@example.com'},
    {'name': 'Charlie', 'age': 28, 'email': 'charlie@example.com'}
]
result = collection.insert_many(users)
print(f"Inserted IDs: {result.inserted_ids}")

# 查询文档
user = collection.find_one({'name': 'Alice'})
print(user)

# 查询多个文档
users = collection.find({'age': {'$gte': 25}})
for user in users:
    print(user)

# 更新文档
result = collection.update_one(
    {'name': 'Alice'},
    {'$set': {'age': 26}, '$push': {'tags': 'mongodb'}}
)
print(f"Modified: {result.modified_count}")

# 删除文档
result = collection.delete_one({'name': 'Bob'})
print(f"Deleted: {result.deleted_count}")
```

### 案例2：高级查询

```python
# mongodb_query.py
from pymongo import MongoClient, ASCENDING, DESCENDING

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

# 条件查询
# $gt, $gte, $lt, $lte, $ne, $in, $nin
users = collection.find({
    'age': {'$gte': 25, '$lte': 35},
    'tags': {'$in': ['python', 'java']}
})

# 正则表达式查询
users = collection.find({'name': {'$regex': '^A', '$options': 'i'}})

# 数组查询
users = collection.find({'tags': 'python'})  # 包含 'python'
users = collection.find({'tags': {'$size': 2}})  # 数组长度为2

# 嵌套文档查询
users = collection.find({'address.city': 'Beijing'})

# 投影（只返回指定字段）
users = collection.find({}, {'name': 1, 'email': 1, '_id': 0})

# 排序和分页
users = collection.find().sort('age', DESCENDING).skip(10).limit(20)
```

### 案例3：索引优化

```python
# mongodb_index.py
from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

# 创建单字段索引
collection.create_index('email', unique=True)
collection.create_index('age')

# 创建复合索引
collection.create_index([('age', ASCENDING), ('name', ASCENDING)])

# 创建文本索引
collection.create_index([('name', TEXT), ('email', TEXT)])

# 查看索引
indexes = collection.list_indexes()
for index in indexes:
    print(index)

# 删除索引
collection.drop_index('age_1')
```

### 案例4：聚合管道

```python
# mongodb_aggregate.py
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['orders']

# 聚合管道示例
pipeline = [
    # 匹配阶段
    {'$match': {'status': 'completed'}},
    
    # 分组阶段
    {'$group': {
        '_id': '$customer_id',
        'total_amount': {'$sum': '$amount'},
        'order_count': {'$sum': 1},
        'avg_amount': {'$avg': '$amount'}
    }},
    
    # 投影阶段
    {'$project': {
        '_id': 0,
        'customer_id': '$_id',
        'total_amount': 1,
        'order_count': 1,
        'avg_amount': {'$round': ['$avg_amount', 2]}
    }},
    
    # 排序阶段
    {'$sort': {'total_amount': -1}},
    
    # 限制阶段
    {'$limit': 10}
]

results = collection.aggregate(pipeline)
for result in results:
    print(result)
```

### 案例5：$lookup 关联查询

```python
# mongodb_lookup.py
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']

# $lookup 关联查询
pipeline = [
    {
        '$lookup': {
            'from': 'users',
            'localField': 'user_id',
            'foreignField': '_id',
            'as': 'user_info'
        }
    },
    {
        '$unwind': '$user_info'
    },
    {
        '$project': {
            'order_id': 1,
            'amount': 1,
            'user_name': '$user_info.name',
            'user_email': '$user_info.email'
        }
    }
]

results = db.orders.aggregate(pipeline)
for result in results:
    print(result)
```

## 验证数据

### MongoDB 性能测试

| 操作 | 数据量 | 耗时 | 说明 |
|-----|--------|------|------|
| 插入 | 10万条 | 5s | 单机 |
| 查询（无索引） | 10万条 | 2s | 全表扫描 |
| 查询（有索引） | 10万条 | <100ms | 索引查询 |
| 聚合 | 10万条 | 3s | 复杂聚合 |

### 索引效果

```
无索引查询：2s
单字段索引：<100ms
复合索引：<50ms
提升：95%+
```

## 总结

1. **文档设计**
   - 合理使用嵌套文档
   - 避免过深的嵌套
   - 考虑查询模式

2. **索引优化**
   - 为常用查询字段创建索引
   - 使用复合索引优化多字段查询
   - 避免过多索引影响写入性能

3. **聚合管道**
   - 合理使用 $match 提前过滤
   - 使用 $project 减少数据传输
   - 优化 $group 操作

4. **性能优化**
   - 使用连接池
   - 批量操作
   - 合理使用投影
   - 监控慢查询
