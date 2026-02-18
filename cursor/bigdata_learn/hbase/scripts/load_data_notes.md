数据加载说明（示意）：

- 可使用 HBase 自带的 ImportTsv 工具将 `data/users.tsv` / `data/orders.tsv` 导入表中。
- 或者使用 MapReduce/Spark/Flink 程序读取 TSV 后使用 HBase API 写入。

