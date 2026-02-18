# 案例2：电商商品搜索与聚合分析（Elasticsearch）

## 一、案例目标

- **场景**：在商品索引上实现“搜索 + 左侧筛选 + 统计”的常见电商搜索功能。
- **目标**：
  - 基于关键字 + 条件过滤实现基础搜索。
  - 使用 Aggregations 完成按类别/品牌的统计与平均价格计算。

对应数据与脚本：

- 数据文件：`data/products.jsonl`
- 索引脚本：`scripts/setup_indices.sh`
- 加载脚本：`scripts/load_data.sh`

---

## 二、按关键字 + 品牌 + 类别搜索商品

```json
GET products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "手机" } }
      ],
      "filter": [
        { "terms": { "brand": ["Apple", "Huawei"] } },
        { "term":  { "category": "电子产品" } },
        { "range": { "price": { "gte": 2000, "lte": 8000 } } }
      ]
    }
  },
  "sort": [
    { "price": "asc" }
  ],
  "from": 0,
  "size": 20
}
```

---

## 三、按类别与品牌做聚合统计

### 1. 按类别统计商品数量与平均价格

```json
GET products/_search
{
  "size": 0,
  "aggs": {
    "by_category": {
      "terms": { "field": "category" },
      "aggs": {
        "avg_price": { "avg": { "field": "price" } },
        "max_price": { "max": { "field": "price" } }
      }
    }
  }
}
```

### 2. 在关键字搜索结果上做品牌聚合（Facets）

```json
GET products/_search
{
  "size": 10,
  "query": {
    "match": { "name": "手机" }
  },
  "aggs": {
    "by_brand": {
      "terms": {
        "field": "brand",
        "size": 10
      }
    }
  }
}
```

---

## 四、练习建议

1. 在聚合结果中增加 `avg_price`，用于在筛选区域展示“该品牌平均价”。  
2. 设计一个“价格分段”聚合（使用 `range` aggregation），统计不同价格区间内商品数量。  
3. 思考如何将当前的查询/聚合组合封装成对前端友好的 API（例如 `/search?keyword=...&brand=...`）。  

