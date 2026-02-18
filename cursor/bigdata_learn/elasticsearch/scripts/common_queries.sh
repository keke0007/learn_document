#!/usr/bin/env bash

# 常用查询与聚合示例（以 curl 形式展示）
# 可参考这里的请求内容复制到 Kibana Dev Tools 中执行。

ES_HOST=${ES_HOST:-"http://localhost:9200"}

echo
echo "== 示例：搜索名称包含 '手机' 的商品 =="
curl -s -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d '
{
  "query": {
    "match": { "name": "手机" }
  },
  "size": 5
}
'

echo
echo "== 示例：按品牌聚合商品数量和平均价格 =="
curl -s -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d '
{
  "size": 0,
  "aggs": {
    "by_brand": {
      "terms": { "field": "brand" },
      "aggs": {
        "avg_price": { "avg": { "field": "price" } }
      }
    }
  }
}
'

echo
echo "== 示例：按分钟统计日志数量（近 10 分钟） =="
curl -s -X GET "$ES_HOST/logs/_search?pretty" -H 'Content-Type: application/json' -d '
{
  "size": 0,
  "query": {
    "range": {
      "ts": { "gte": "now-10m" }
    }
  },
  "aggs": {
    "logs_over_time": {
      "date_histogram": {
        "field": "ts",
        "fixed_interval": "1m",
        "min_doc_count": 0
      }
    }
  }
}
'

