# 案例3：IO性能调优实战（fio / iostat / 网络压测）

## 案例目标
学会用工具测试和调优IO性能：
- **fio**：磁盘IO性能测试
- **iostat**：实时监控磁盘IO
- **网络压测**：ab / wrk / JMeter
- **调优思路**：参数调整与瓶颈定位

## 一、fio 磁盘IO测试

### 一句话讲明白
fio 是专门用来测试磁盘IO性能的工具，可以模拟各种读写场景。

### 关键参数
- `--rw`：读写模式（read/write/randread/randwrite/randrw）
- `--bs`：块大小（4k/8k/64k）
- `--iodepth`：IO深度（并发IO数）
- `--direct`：是否使用直接IO
- `--ioengine`：IO引擎（libaio/sync/psync）

### 测试脚本（见 `fio/scripts/fio_disk_test.sh`）

```bash
# 顺序读测试
fio --name=seq_read \
    --filename=/tmp/test_file \
    --size=1G \
    --rw=read \
    --bs=4k \
    --direct=1 \
    --ioengine=libaio \
    --iodepth=32 \
    --runtime=60

# 随机写测试
fio --name=rand_write \
    --filename=/tmp/test_file \
    --rw=randwrite \
    --bs=4k \
    --iodepth=32
```

### 期望输出指标
- **IOPS**：`iops=50000`（每秒5万次IO）
- **吞吐量**：`bw=200MiB/s`（每秒200MB）
- **延迟**：`lat (usec)`：平均延迟（微秒）

---

## 二、iostat 实时监控

### 一句话讲明白
iostat 可以实时查看磁盘的IO使用情况，帮你定位IO瓶颈。

### 常用命令

```bash
# 每2秒刷新一次，显示5次
iostat -x 2 5

# 只看某个磁盘
iostat -x /dev/sda 2
```

### 关键指标解读
- **%util**：磁盘利用率（接近100%说明磁盘很忙）
- **r/s, w/s**：每秒读写次数（IOPS）
- **rkB/s, wkB/s**：每秒读写数据量（吞吐量）
- **await**：平均等待时间（ms），越大说明IO越慢
- **svctm**：平均服务时间（ms），磁盘处理一个IO的时间

### 调优思路
- **%util 高但 IOPS 低**：可能是随机IO，考虑用SSD或增加IO深度。
- **await 高**：可能是IO队列太长，考虑增加IO深度或优化应用逻辑。
- **rkB/s/wkB/s 低**：可能是块大小太小，考虑增大块大小。

---

## 三、网络IO压测

### 工具选择
- **ab（Apache Bench）**：简单快速，适合HTTP接口压测
- **wrk**：多线程，性能更好
- **JMeter**：功能全面，适合复杂场景

### ab 示例

```bash
# 1000个请求，10个并发
ab -n 1000 -c 10 http://localhost:8080/api/test

# 期望输出
Requests per second: 5000 [#/sec]
Time per request: 2.000 [ms]
```

### wrk 示例

```bash
# 10个线程，100个连接，持续30秒
wrk -t10 -c100 -d30s http://localhost:8080/api/test
```

---

## 四、调优思路总结

### 磁盘IO调优
1. **选择合适的IO模式**：
   - 随机IO → SSD + 高IO深度
   - 顺序IO → HDD也可以，但SSD更快
2. **调整IO深度（iodepth）**：
   - 太小：磁盘利用率低
   - 太大：延迟增加，可能适得其反
   - 通常 16-64 是合理范围
3. **使用直接IO**：
   - 数据库、大文件传输 → 考虑直接IO
   - 小文件、频繁读取 → 缓冲IO可能更好

### 网络IO调优
1. **选择合适的IO模型**：
   - 高并发 → NIO + epoll（Reactor模式）
   - 低并发 → BIO也可以
2. **调整线程数**：
   - Reactor线程：通常 = CPU核心数
   - 工作线程：根据业务耗时调整
3. **调整缓冲区大小**：
   - Socket缓冲区：`SO_RCVBUF` / `SO_SNDBUF`
   - 应用缓冲区：根据消息大小调整

---

## 验证脚本

参考 `fio/scripts/` 目录：
- `fio_disk_test.sh`：磁盘IO测试
- `network_io_demo.java`：网络IO模型示例

### 期望观察
- **磁盘IO**：IOPS、吞吐量、延迟
- **网络IO**：QPS（每秒请求数）、延迟、错误率

---

## 常见坑
- **测试环境与生产环境不一致**：测试时用SSD，生产用HDD，结果差异巨大。
- **只关注吞吐量，忽略延迟**：高吞吐但高延迟，用户体验差。
- **没有考虑系统调用开销**：零拷贝虽然减少拷贝，但系统调用本身也有开销。
