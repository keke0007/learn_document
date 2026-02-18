"""
MongoDB 基础与高级开发示例
演示 MongoDB 的文档操作、查询、聚合等
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime

# 连接 MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

print("=== MongoDB 基础操作示例 ===\n")

# 1. 插入文档
print("1. 插入文档")
user = {
    'name': 'Alice',
    'age': 25,
    'email': 'alice@example.com',
    'tags': ['developer', 'python'],
    'created_at': datetime.now()
}
result = collection.insert_one(user)
print(f"Inserted ID: {result.inserted_id}")
print()

# 2. 查询文档
print("2. 查询文档")
user = collection.find_one({'name': 'Alice'})
print(f"Found user: {user}")
print()

# 3. 条件查询
print("3. 条件查询")
users = list(collection.find({'age': {'$gte': 25}}))
print(f"Users with age >= 25: {len(users)}")
print()

# 4. 更新文档
print("4. 更新文档")
result = collection.update_one(
    {'name': 'Alice'},
    {'$set': {'age': 26}, '$push': {'tags': 'mongodb'}}
)
print(f"Modified: {result.modified_count}")
print()

# 5. 聚合管道
print("5. 聚合管道")
pipeline = [
    {'$match': {'age': {'$gte': 25}}},
    {'$group': {
        '_id': '$tags',
        'count': {'$sum': 1},
        'avg_age': {'$avg': '$age'}
    }},
    {'$sort': {'count': -1}}
]
results = list(collection.aggregate(pipeline))
print(f"Aggregation results: {results}")
print()

# 6. 创建索引
print("6. 创建索引")
collection.create_index('email', unique=True)
collection.create_index([('age', ASCENDING), ('name', ASCENDING)])
indexes = list(collection.list_indexes())
print(f"Indexes: {[idx['name'] for idx in indexes]}")
print()

# 7. 排序和分页
print("7. 排序和分页")
users = list(collection.find().sort('age', DESCENDING).limit(5))
print(f"Top 5 users by age: {len(users)}")
print()

print("=== MongoDB 示例完成 ===")
