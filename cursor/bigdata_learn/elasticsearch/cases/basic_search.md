# 案例1：基础全文检索与过滤（Elasticsearch）

## 一、案例目标

- **场景**：在商品索引上进行最基础的搜索和过滤。
- **目标**：
  - 熟悉索引文档结构。
  - 掌握 `match`、`term`、`bool` 查询的基本用法。
  - 体验分页与排序。

对应数据与脚本：

- 数据文件：`data/products.jsonl`
- 索引脚本：`scripts/setup_indices.sh`
- 加载脚本：`scripts/load_data.sh`
- 查询脚本：`scripts/common_queries.sh`（商品部分）

---

## 二、商品文档结构示例

```json
{ "index": { "_id": 1 } }
{ "product_id": 1, "name": "旗舰手机", "category": "电子产品", "brand": "Apple", "price": 6999.0, "tags": ["手机", "5G"] }
```

字段说明：

- `product_id`：商品 ID（keyword）
- `name`：商品名称（text + keyword）
- `category`：类别（keyword）
- `brand`：品牌（keyword）
- `price`：价格（float）
- `tags`：标签数组（keyword）

---

## 三、典型查询示例（可在 Dev Tools 中执行）

### 1. 全文搜索商品名称中包含“手机”

```json
GET products/_search
{
  "query": {
    "match": {
      "name": "手机"
    }
  }
}
```

### 2. 精确过滤品牌为 Apple 的商品

```json
GET products/_search
{
  "query": {
    "term": {
      "brand": "Apple"
    }
  }
}
```

### 3. 组合查询：名称包含“手机”，品牌为 Apple，价格在区间内

```json
GET products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "手机" } }
      ],
      "filter": [
        { "term":  { "brand": "Apple" } },
        { "range": { "price": { "gte": 3000, "lte": 8000 } } }
      ]
    }
  },
  "sort": [
    { "price": "asc" }
  ],
  "from": 0,
  "size": 10
}
```

---

## 四、练习建议

1. 为 `products` 索引增加一个 `on_sale` 布尔字段，练习在 `filter` 中加入布尔过滤条件。  
2. 使用 `multi_match` 在 `name` 与 `tags` 上同时搜索关键字。  
3. 尝试只返回 `product_id` 和 `name` 字段（使用 `_source` 或 `stored_fields`），体会返回字段裁剪对带宽的影响。  

