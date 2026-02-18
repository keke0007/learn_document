# 高性能IO模型学习指南（费曼学习法）：磁盘IO + 网络IO

> 目标：把中间件高性能的磁盘IO与网络IO模型学到“能解释清楚 + 能调优 + 能用工具验证”的程度。

本目录自带：
- **验证脚本**：`fio/scripts/`
  - `fio_disk_test.sh`（磁盘IO测试）
  - `network_io_demo.java`（BIO/NIO/AIO示例）
  - `middleware_benchmark.sh`（中间件性能测试）
- **案例**：`fio/cases/`
  - `cases/README.md`（索引）
  - 4 个案例文档（磁盘IO / 网络IO / 性能调优 / 中间件实战）
- **测试数据**：`fio/data/test_data.txt`

---

## 0. 费曼学习法在IO模型上的用法

对每个知识点，都按这 5 步：
- **一句话讲明白**：讲给没做过性能优化的人也能听懂
- **关键术语补齐**：同步/异步、阻塞/非阻塞、事件驱动、零拷贝
- **能写出的最小示例**：代码片段或命令行示例
- **能观察的指标**：IOPS、吞吐量、延迟、QPS
- **能解释的调优思路**：什么时候用什么模型、如何定位瓶颈

---

## 1. 学习知识点清单

### 1.1 磁盘IO模型

#### 同步IO vs 异步IO
- **一句话**：同步IO会阻塞等待，异步IO通过回调/事件通知。
- **你必须知道**：
  - 同步IO：简单但吞吐低
  - 异步IO：复杂但吞吐高，适合高并发场景

#### 直接IO vs 缓冲IO
- **一句话**：直接IO绕过内核缓存，缓冲IO先到页缓存再复制到用户空间。
- **你必须知道**：
  - 缓冲IO：适合数据会被多次读取
  - 直接IO：适合数据只读一次，不想占用缓存

#### 零拷贝（Zero-Copy）
- **一句话**：减少数据在内存中的复制次数，让数据直接从源到目标。
- **你必须知道**：
  - mmap：内存映射文件
  - sendfile：Linux系统调用，文件到网络
  - 适用场景：大文件传输、消息队列

### 1.2 网络IO模型

#### BIO（Blocking IO）
- **一句话**：一个连接一个线程，线程在等待数据时会阻塞。
- **问题**：线程资源消耗大，不适合高并发。

#### NIO（Non-blocking IO）
- **一句话**：一个线程 + Selector 管理多个连接，事件驱动。
- **核心组件**：Channel、Buffer、Selector
- **优势**：高并发、低资源消耗

#### epoll（Linux事件通知）
- **一句话**：高效的事件通知机制，只返回就绪的文件描述符。
- **为什么快**：不需要遍历所有文件描述符

#### Reactor模式
- **一句话**：事件循环 + 事件分发 + 事件处理。
- **变体**：
  - 单Reactor单线程
  - 单Reactor多线程
  - 多Reactor多线程（Netty采用）

#### AIO（Asynchronous IO）
- **一句话**：真正的异步IO，IO完成后通过回调通知。
- **现状**：Linux网络IO的AIO支持不好，实际使用少。

### 1.4 中间件IO模型实战

#### Redis
- **网络IO**：单线程 + epoll
- **磁盘IO**：异步持久化（AOF/RDB）
- **核心优势**：内存操作快，单线程无锁竞争

#### Kafka
- **网络IO**：NIO + Selector + 线程池
- **磁盘IO**：零拷贝（sendfile）+ 顺序写 + 批量发送
- **核心优势**：高吞吐，适合大数据量

#### RocketMQ
- **网络IO**：Netty（NIO + epoll）
- **磁盘IO**：mmap + 顺序写 + 异步刷盘
- **核心优势**：低延迟，适合事务消息

### 1.5 性能测试工具

#### fio（磁盘IO测试）
- **关键参数**：`--rw`、`--bs`、`--iodepth`、`--direct`
- **观察指标**：IOPS、吞吐量、延迟

#### iostat（实时监控）
- **关键指标**：%util、r/s/w/s、rkB/s/wkB/s、await、svctm
- **调优思路**：根据指标定位瓶颈

#### 网络压测工具
- **ab**：简单快速，适合HTTP接口
- **wrk**：多线程，性能更好
- **JMeter**：功能全面，适合复杂场景

---

## 2. 案例与验证脚本（建议顺序）

### 案例1：磁盘IO模型
- 文档：`cases/01_disk_io_models.md`
- 脚本：`scripts/fio_disk_test.sh`
- 你要学会：
  - 同步IO vs 异步IO的区别
  - 直接IO vs 缓冲IO的选择
  - 零拷贝的原理与应用

### 案例2：网络IO模型
- 文档：`cases/02_network_io_models.md`
- 脚本：`scripts/network_io_demo.java`
- 你要学会：
  - BIO/NIO/AIO的区别
  - epoll为什么高效
  - Reactor模式的设计思想

### 案例3：IO性能调优
- 文档：`cases/03_io_performance_tuning.md`
- 你要学会：
  - 用fio测试磁盘IO性能
  - 用iostat监控磁盘IO
  - 用ab/wrk压测网络IO
  - 根据指标调优

### 案例4：中间件IO模型实战
- 文档：`cases/04_middleware_io_models.md`
- 你要学会：
  - Redis：单线程 + epoll + 内存操作
  - Kafka：零拷贝（sendfile）+ 顺序写 + 批量发送
  - RocketMQ：mmap + 顺序写 + 异步刷盘
  - 理解为什么这些中间件能达到高吞吐、低延迟

---

## 3. 用费曼法把知识点讲“透”的模板

对每个IO模型，按下面的模板复述：

1. **这是什么？（一句话）**
   - "NIO就是非阻塞IO，用一个线程管理多个连接。"
2. **解决什么问题？**
   - "BIO一个连接一个线程，高并发时线程太多，资源消耗大。"
3. **核心机制？**
   - "用Selector监听事件，哪个连接有数据就处理哪个。"
4. **性能如何？为什么？**
   - "高并发、低资源消耗，因为一个线程可以管理大量连接。"
5. **常见坑？**
   - "Buffer的flip()/clear()容易出错，Reactor线程不能阻塞。"

---

## 4. 最终总结：一页速查 Checklist

### 4.1 能用自己的话解释
- **同步IO vs 异步IO**：阻塞等待 vs 回调通知
- **直接IO vs 缓冲IO**：绕过缓存 vs 使用缓存
- **零拷贝**：减少内存复制，提升性能
- **BIO vs NIO**：一连接一线程 vs 一线程多连接
- **epoll**：高效事件通知，只返回就绪的
- **Reactor模式**：事件驱动，高并发设计

### 4.2 能使用的工具
- [ ] 用fio测试磁盘IO性能（IOPS、吞吐量、延迟）
- [ ] 用iostat监控磁盘IO（%util、await、svctm）
- [ ] 用ab/wrk压测网络IO（QPS、延迟、错误率）

### 4.3 能回答的调优问题
- [ ] 什么时候用直接IO，什么时候用缓冲IO？
- [ ] 为什么中间件（Nginx、Netty、Kafka）都用NIO+epoll？
- [ ] 如何根据iostat的输出定位IO瓶颈？
- [ ] Reactor线程数和工作线程数如何设置？
- [ ] Redis/Kafka/RocketMQ 分别用了哪些IO优化技术？
- [ ] 为什么 Kafka 用 sendfile，RocketMQ 用 mmap？
