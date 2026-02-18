"""
Elasticsearch 基础与高级开发示例
演示 Elasticsearch 的索引、查询、聚合等操作
"""

from elasticsearch import Elasticsearch
from datetime import datetime

# 连接 Elasticsearch
es = Elasticsearch(['localhost:9200'])

print("=== Elasticsearch 基础操作示例 ===\n")

# 1. 创建索引
print("1. 创建索引")
index_body = {
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "standard"
            },
            "content": {
                "type": "text"
            },
            "author": {"type": "keyword"},
            "created_at": {"type": "date"},
            "views": {"type": "integer"}
        }
    }
}
try:
    es.indices.create(index='articles', body=index_body)
    print("Index 'articles' created")
except Exception as e:
    print(f"Index may already exist: {e}")
print()

# 2. 索引文档
print("2. 索引文档")
doc = {
    'title': 'Elasticsearch Guide',
    'content': 'This is a guide to Elasticsearch',
    'author': 'Alice',
    'created_at': datetime.now(),
    'views': 100
}
result = es.index(index='articles', id=1, body=doc)
print(f"Document indexed: {result['result']}")
print()

# 3. Match 查询
print("3. Match 查询")
query = {
    "query": {
        "match": {
            "title": "Elasticsearch"
        }
    }
}
results = es.search(index='articles', body=query)
print(f"Found {results['hits']['total']['value']} documents")
print()

# 4. Bool 查询
print("4. Bool 查询")
query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"title": "Elasticsearch"}}
            ],
            "filter": [
                {"range": {"views": {"gte": 100}}}
            ]
        }
    }
}
results = es.search(index='articles', body=query)
print(f"Bool query results: {results['hits']['total']['value']}")
print()

# 5. 聚合分析
print("5. 聚合分析")
query = {
    "aggs": {
        "avg_views": {
            "avg": {"field": "views"}
        },
        "authors": {
            "terms": {
                "field": "author",
                "size": 10
            }
        }
    }
}
results = es.search(index='articles', body=query)
print(f"Average views: {results['aggregations']['avg_views']['value']}")
print(f"Authors: {[bucket['key'] for bucket in results['aggregations']['authors']['buckets']]}")
print()

print("=== Elasticsearch 示例完成 ===")
