#!/usr/bin/env bash

# 使用 _bulk 导入示例数据
# 用法：在 elasticsearch 目录下执行：sh scripts/load_data.sh

ES_HOST=${ES_HOST:-"http://localhost:9200"}

echo "Bulk load products..."
curl -s -X POST "$ES_HOST/products/_bulk" \
  -H 'Content-Type: application/x-ndjson' \
  --data-binary "@data/products.jsonl" > /dev/null
echo " done."

echo "Bulk load logs..."
curl -s -X POST "$ES_HOST/logs/_bulk" \
  -H 'Content-Type: application/x-ndjson' \
  --data-binary "@data/logs.jsonl" > /dev/null
echo " done."

echo "Bulk load users..."
curl -s -X POST "$ES_HOST/users/_bulk" \
  -H 'Content-Type: application/x-ndjson' \
  --data-binary "@data/users.jsonl" > /dev/null
echo " done."

