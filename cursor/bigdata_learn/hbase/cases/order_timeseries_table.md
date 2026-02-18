# 案例3：订单/日志时间序列表设计（HBase）

## 一、案例目标

- 为订单或日志数据设计时间序列 RowKey。
- 支持按用户 + 时间区间高效 Scan。

---

## 二、数据示例（来自 `data/orders.tsv`）

`order_id	user_id	order_time	amount`

```text
1001	1	2024-03-14 10:00:01	299.00
1002	1	2024-03-14 10:05:00	599.00
```

---

## 三、RowKey 设计

- 表名：`orders`
- RowKey 示例：`<user_id>#<reverse_timestamp>`
  - 如：`1#1700000000000`（使用倒序时间戳保证最近数据排前面，便于按用户 Scan 最近订单）
- 列族：`d`（detail）
  - `d:order_id`、`d:amount` 等。

示例（HBase shell）：

```ruby
create 'orders', { NAME => 'd', VERSIONS => 1 }

put 'orders', '1#1700000000000', 'd:order_id', '1001'
put 'orders', '1#1700000000000', 'd:amount', '299.00'
```

---

## 四、练习建议

1. 结合订单时间，使用简单脚本将 `order_time` 转换为时间戳，并构造倒序 RowKey 写入 HBase。  
2. 实验按 RowKey 范围 Scan 最近 N 条订单的效率，并与“order_id 作为 RowKey”的方案比较。  

