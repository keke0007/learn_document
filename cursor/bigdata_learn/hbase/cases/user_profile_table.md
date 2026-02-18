# 案例2：用户画像宽表设计（HBase）

## 一、案例目标

- 使用 HBase 存储用户画像宽表，将多维属性放入不同列族/列。
- 通过 RowKey 设计支持按用户 ID 快速查询画像信息。

---

## 二、表设计

- 表名：`user_profile`
- RowKey：`user_id`（如 `u_0001`）
- 列族：
  - `info`：基础信息（`name`、`gender`、`city`、`age`）
  - `stat`：行为统计（`login_count`、`last_login` 等）

示例（HBase shell）：

```ruby
create 'user_profile', { NAME => 'info', VERSIONS => 1 }, { NAME => 'stat', VERSIONS => 1 }
```

---

## 三、数据示例（来自 `data/users.tsv`）

`user_id	name	city`

```text
1	张三	北京
2	李四	上海
```

可转换为：

```ruby
put 'user_profile', 'u_0001', 'info:name', '张三'
put 'user_profile', 'u_0001', 'info:city', '北京'
```

---

## 四、练习建议

1. 在 `stat` 列族中为每个用户增加 `stat:login_count` 与 `stat:last_login` 列，模拟登录统计。  
2. 思考 RowKey 如果直接使用数值（如 `1`）与加前缀/补零（如 `u_0001`）在 Scan 范围上的差异。  

