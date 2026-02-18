# 案例1：基础数据模型与表设计（HBase）

## 一、案例目标

- 理解 RowKey、列族、列限定符与 Cell 的基础概念。
- 通过小表示例熟悉 HBase shell 的常用命令：`create` / `put` / `get` / `scan`。

---

## 二、示例表设计

- 表名：`user_profile`
- RowKey：`user_id`（如 `u_0001`）
- 列族：
  - `info`：基础信息（`name`、`city` 等）
  - `stat`：统计信息（`login_count` 等）

---

## 三、建表与操作示例（HBase shell）

```ruby
create 'user_profile', { NAME => 'info', VERSIONS => 1 }, { NAME => 'stat', VERSIONS => 1 }

put 'user_profile', 'u_0001', 'info:name', '张三'
put 'user_profile', 'u_0001', 'info:city', '北京'
put 'user_profile', 'u_0001', 'stat:login_count', '10'

get 'user_profile', 'u_0001'

scan 'user_profile', { STARTROW => 'u_0001', STOPROW => 'u_0010' }
```

---

## 四、练习建议

1. 根据 `data/users.tsv` 中的用户数据，为每个用户插入一行记录，RowKey 可采用 `u_<user_id>` 形式。  
2. 为表添加一个新列族 `ext`，用于存储扩展信息（例如 `ext:tags`）。  

