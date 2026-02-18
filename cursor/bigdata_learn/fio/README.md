# 高性能 IO 模型学习目录（磁盘IO + 网络IO）

本目录专注 **中间件高性能的磁盘IO与网络IO模型** 学习（偏实战与性能调优），配套测试脚本与验证数据。

推荐阅读顺序：
- `GUIDE.md`：IO 模型费曼学习指南（知识点 + 案例 + 验证脚本 + 总结清单）
- `cases/`：拆分后的案例文档（磁盘IO / 网络IO / 性能测试）
- `data/`：配套验证数据与测试文件
- `scripts/`：fio / iostat / 网络压测脚本示例

案例索引：
- `cases/README.md`：案例总览索引页
- `cases/01_disk_io_models.md`：磁盘IO模型（同步/异步/直接IO/零拷贝）
- `cases/02_network_io_models.md`：网络IO模型（BIO/NIO/AIO/epoll/Reactor）
- `cases/03_io_performance_tuning.md`：IO性能调优实战（fio/iostat/网络压测）
- `cases/04_middleware_io_models.md`：中间件IO模型实战（Redis/RocketMQ/Kafka）

目录结构：
```
fio/
├── README.md
├── GUIDE.md
├── cases/
├── data/
└── scripts/
```
