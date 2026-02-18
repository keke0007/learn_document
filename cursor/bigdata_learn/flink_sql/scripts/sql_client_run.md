# Flink SQL Client 运行说明（本目录案例）

> 目标：用 Flink 自带 SQL Client 直接执行 `flink_sql/cases/` 中的 SQL。

## 1) 启动 SQL Client

在 Flink 安装目录下：
```bash
./bin/sql-client.sh
```

## 2) 路径说明（非常重要）

案例里 `CREATE TABLE ... WITH ('path'='...')` 的 `path`：
- **推荐使用绝对路径**（Windows 下请使用 `file:///C:/...` 形式）
- 你可以把本项目 `flink_sql/data/` 的绝对路径替换进去

示例（把 `C:/Users/ke/Desktop/bigdata_learn` 换成你的实际路径）：
```sql
'path' = 'file:///C:/Users/ke/Desktop/bigdata_learn/flink_sql/data/orders.csv'
```

## 3) 输出验证建议

案例默认使用 `connector = 'print'` 输出到控制台：
- 适合学习与验证
- 生产环境请替换为 Kafka / Upsert-Kafka / JDBC 等 sink（并配合 checkpoint）

