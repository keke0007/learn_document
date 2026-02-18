#!/usr/bin/env bash

# Elasticsearch 索引与映射创建示例
# 用法：在 elasticsearch 目录下执行：sh scripts/setup_indices.sh

ES_HOST=${ES_HOST:-"http://localhost:9200"}

echo "Create products index..."
curl -s -X PUT "$ES_HOST/products" -H 'Content-Type: application/json' -d '
{
  "mappings": {
    "properties": {
      "product_id": { "type": "keyword" },
      "name":       { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
      "category":   { "type": "keyword" },
      "brand":      { "type": "keyword" },
      "price":      { "type": "float" },
      "tags":       { "type": "keyword" }
    }
  }
}
' > /dev/null
echo " done."

echo "Create logs index..."
curl -s -X PUT "$ES_HOST/logs" -H 'Content-Type: application/json' -d '
{
  "mappings": {
    "properties": {
      "ts":      { "type": "date" },
      "level":   { "type": "keyword" },
      "service": { "type": "keyword" },
      "message": { "type": "text" }
    }
  }
}
' > /dev/null
echo " done."

echo "Create users index..."
curl -s -X PUT "$ES_HOST/users" -H 'Content-Type: application/json' -d '
{
  "mappings": {
    "properties": {
      "user_id":    { "type": "keyword" },
      "name":       { "type": "keyword" },
      "city":       { "type": "keyword" },
      "last_login": { "type": "date" },
      "tags":       { "type": "keyword" }
    }
  }
}
' > /dev/null
echo " done."

