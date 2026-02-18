# 中间件基础与高级开发知识点总览

## 📚 目录

1. [Redis](#1-redis)
2. [MongoDB](#2-mongodb)
3. [InfluxDB](#3-influxdb)
4. [Elasticsearch](#4-elasticsearch)
5. [RabbitMQ](#5-rabbitmq)
6. [RocketMQ](#6-rocketmq)
7. [Kafka](#7-kafka)
8. [MinIO](#8-minio)

---

## 1. Redis

### 1.1 基础数据结构

**String（字符串）**
- 基本操作：SET、GET、INCR、DECR
- 应用场景：缓存、计数器、分布式锁

**Hash（哈希表）**
- 基本操作：HSET、HGET、HGETALL
- 应用场景：对象存储、用户信息

**List（列表）**
- 基本操作：LPUSH、RPUSH、LPOP、RPOP
- 应用场景：队列、栈、消息列表

**Set（集合）**
- 基本操作：SADD、SMEMBERS、SISMEMBER
- 应用场景：去重、集合运算、标签

**Sorted Set（有序集合）**
- 基本操作：ZADD、ZRANGE、ZRANK
- 应用场景：排行榜、范围查询

### 1.2 高级数据结构

**Bitmap（位图）**
- 应用场景：用户签到、活跃度统计

**HyperLogLog**
- 应用场景：基数统计、UV 统计

**Stream（流）**
- 应用场景：消息队列、日志流

### 1.3 持久化机制

**RDB（快照）**
- 优点：文件小、恢复快
- 缺点：可能丢失数据

**AOF（追加文件）**
- 优点：数据安全
- 缺点：文件大、恢复慢

### 1.4 高可用

**主从复制**
- 读写分离
- 数据备份

**哨兵模式**
- 自动故障转移
- 高可用

**集群模式**
- 水平扩展
- 数据分片

---

## 2. MongoDB

### 2.1 文档模型

**集合和文档**
- Collection：集合
- Document：文档
- Field：字段

**BSON 格式**
- 二进制 JSON
- 支持更多数据类型

### 2.2 查询操作

**基本查询**
- find()：查询文档
- findOne()：查询单个文档

**条件查询**
- $gt、$gte、$lt、$lte：比较操作
- $in、$nin：包含操作
- $regex：正则表达式

**聚合管道**
- $match：过滤
- $group：分组
- $project：投影
- $sort：排序
- $lookup：关联查询

### 2.3 索引优化

**索引类型**
- 单字段索引
- 复合索引
- 文本索引
- 地理空间索引

**索引优化**
- 为常用查询字段创建索引
- 避免过多索引影响写入性能

---

## 3. InfluxDB

### 3.1 数据模型

**核心概念**
- Database：数据库
- Measurement：表
- Tag：标签（索引）
- Field：字段（值）
- Timestamp：时间戳

**数据组织**
- Tag 用于过滤和分组
- Field 存储实际值

### 3.2 保留策略

**Retention Policy**
- 数据保留时间
- 自动删除过期数据

**Continuous Query**
- 预聚合数据
- 节省存储空间

### 3.3 查询语言

**InfluxQL**
- SQL-like 查询语言
- 时间序列查询

**Flux**
- 新的查询语言
- 更强大的功能

---

## 4. Elasticsearch

### 4.1 索引结构

**核心概念**
- Index：索引
- Document：文档
- Field：字段
- Mapping：映射

**倒排索引**
- 词到文档的映射
- 快速全文搜索

### 4.2 查询 DSL

**Match Query**
- 全文搜索
- 分词匹配

**Term Query**
- 精确匹配
- 不分词

**Bool Query**
- 组合查询
- must、should、must_not、filter

**Range Query**
- 范围查询
- 数值、日期范围

### 4.3 聚合分析

**Metrics Aggregations**
- avg、sum、max、min
- 指标计算

**Bucket Aggregations**
- terms、date_histogram
- 分组统计

---

## 5. RabbitMQ

### 5.1 核心概念

**Exchange（交换机）**
- Direct：直接交换机
- Topic：主题交换机
- Fanout：扇出交换机
- Headers：头交换机

**Queue（队列）**
- 消息存储
- 持久化

**Binding（绑定）**
- 交换机和队列的连接
- Routing Key：路由键

### 5.2 消息确认

**生产者确认**
- 消息发送确认
- 可靠性保证

**消费者确认**
- 手动确认
- 自动确认

### 5.3 高级特性

**死信队列**
- 处理失败消息
- 消息重试

**延迟队列**
- 延时消息
- 定时任务

---

## 6. RocketMQ

### 6.1 核心概念

**Topic 和 Queue**
- Topic：主题
- Queue：队列
- 消息存储

**Producer 和 Consumer**
- Producer：生产者
- Consumer：消费者
- Consumer Group：消费者组

### 6.2 消息类型

**普通消息**
- 一般场景
- 高吞吐量

**顺序消息**
- 保证顺序
- 同一队列

**事务消息**
- 分布式事务
- 两阶段提交

**延时消息**
- 定时任务
- 延时处理

---

## 7. Kafka

### 7.1 核心概念

**Topic 和 Partition**
- Topic：主题
- Partition：分区
- 消息存储

**Producer 和 Consumer**
- Producer：生产者
- Consumer：消费者
- Consumer Group：消费者组

### 7.2 消息存储

**顺序写入**
- 磁盘顺序写入
- 高性能

**分段存储**
- 日志分段
- 索引文件

**日志压缩**
- 保留最新值
- 节省空间

### 7.3 高级特性

**事务消息**
- 精确一次语义
- 事务 Producer

**流处理**
- Kafka Streams
- 实时处理

---

## 8. MinIO

### 8.1 核心概念

**对象存储**
- Bucket：存储桶
- Object：对象
- Key：对象键

**S3 兼容**
- Amazon S3 API
- 标准接口

### 8.2 操作类型

**上传对象**
- 文件上传
- 字符串上传
- 多部分上传

**下载对象**
- 文件下载
- 流式下载

**列出对象**
- 列出所有对象
- 前缀过滤

### 8.3 访问控制

**Access Key 和 Secret Key**
- 访问凭证
- 安全认证

**Policy**
- 访问策略
- 权限控制

**Presigned URL**
- 临时访问
- 预签名 URL

---

## 📊 面试重点总结

### 高频面试题

1. **Redis**
   - 数据结构和使用场景
   - 持久化机制对比
   - 缓存穿透、击穿、雪崩
   - 主从复制和哨兵模式

2. **MongoDB**
   - 文档模型设计
   - 索引优化
   - 聚合管道
   - 副本集和分片

3. **Elasticsearch**
   - 倒排索引原理
   - 查询 DSL
   - 聚合分析
   - 集群管理

4. **消息队列**
   - RabbitMQ vs RocketMQ vs Kafka
   - 消息可靠性保证
   - 顺序消息
   - 事务消息

5. **InfluxDB**
   - 时序数据模型
   - 数据保留策略
   - 连续查询

6. **MinIO**
   - 对象存储概念
   - S3 兼容性
   - 分布式部署

### 手写代码题

1. **Redis**
   - 实现分布式锁
   - 实现消息队列
   - 实现排行榜

2. **MongoDB**
   - 聚合查询
   - 关联查询
   - 索引优化

3. **Elasticsearch**
   - 复杂查询
   - 聚合分析
   - 高亮显示

4. **消息队列**
   - Producer 实现
   - Consumer 实现
   - 消息确认机制

---

**最后更新：2026-01-26**
