# 案例1：磁盘IO模型（同步/异步/直接IO/零拷贝）

## 案例目标
理解磁盘IO的几种模型，以及它们对性能的影响：
- **同步IO vs 异步IO**
- **直接IO（Direct IO）vs 缓冲IO**
- **零拷贝（Zero-Copy）**：mmap / sendfile

## 一、同步IO vs 异步IO（费曼式讲解）

### 一句话讲明白
- **同步IO**：发起IO请求后，程序“卡住”等待IO完成，才能继续执行。
- **异步IO**：发起IO请求后，程序继续执行其他事情，IO完成后通过回调/事件通知你。

### 类比
- 同步IO：你去银行排队取钱，必须等叫到你的号才能办业务。
- 异步IO：你取个号，然后去旁边喝咖啡，银行办好了会通知你。

### 代码示例（伪代码）

```java
// 同步IO：read() 会阻塞，直到数据读完
byte[] data = new byte[1024];
int bytesRead = fileInputStream.read(data); // 阻塞在这里
process(data);

// 异步IO：read() 立即返回，通过回调处理数据
fileChannel.read(buffer, position, null, new CompletionHandler() {
    @Override
    public void completed(Integer result, ByteBuffer buffer) {
        process(buffer); // IO完成后才执行这里
    }
});
// 程序继续执行其他代码，不等待IO完成
```

### 性能影响
- **同步IO**：简单但吞吐低，一个线程一次只能处理一个IO请求。
- **异步IO**：复杂但吞吐高，一个线程可以同时处理多个IO请求。

---

## 二、直接IO（Direct IO）vs 缓冲IO（Buffered IO）

### 一句话讲明白
- **缓冲IO**：数据先到内核的页缓存（Page Cache），再复制到用户空间。
- **直接IO**：数据绕过页缓存，直接从磁盘到用户空间。

### 为什么需要直接IO？
- **缓冲IO**：适合“数据会被多次读取”的场景（第二次读可能命中缓存，很快）。
- **直接IO**：适合“数据只读一次，不想占用内存缓存”的场景（数据库、大文件传输）。

### 代码示例（Linux）

```c
// 打开文件时指定 O_DIRECT 标志
int fd = open("/path/to/file", O_RDONLY | O_DIRECT);

// 或者用 fio 测试时指定
fio --direct=1  # 使用直接IO
fio --direct=0  # 使用缓冲IO（默认）
```

### 性能对比（用 fio 测试）

```bash
# 缓冲IO（默认）
fio --name=test --filename=/tmp/test --rw=read --bs=4k --size=1G

# 直接IO
fio --name=test --filename=/tmp/test --rw=read --bs=4k --size=1G --direct=1
```

**观察要点**：
- 直接IO的延迟可能更高（绕过缓存），但内存占用更可控。
- 缓冲IO在小数据量时可能更快（命中缓存），但大数据量时可能因为缓存淘汰而变慢。

---

## 三、零拷贝（Zero-Copy）

### 一句话讲明白
零拷贝就是“减少数据在内存中的复制次数”，让数据从磁盘/网络直接到目标位置，不经过用户空间。

### 传统方式（有拷贝）

```
磁盘 -> 内核缓冲区 -> 用户缓冲区 -> Socket缓冲区 -> 网络
      (拷贝1)        (拷贝2)         (拷贝3)
```

### 零拷贝方式（mmap / sendfile）

```
磁盘 -> 内核缓冲区 -> Socket缓冲区 -> 网络
      (mmap映射)      (sendfile)
```

### 代码示例（Java NIO）

```java
// 使用 FileChannel.transferTo() 实现零拷贝
FileChannel sourceChannel = new FileInputStream("source.txt").getChannel();
FileChannel destChannel = new FileOutputStream("dest.txt").getChannel();

// transferTo 内部可能使用 sendfile 系统调用（零拷贝）
sourceChannel.transferTo(0, sourceChannel.size(), destChannel);
```

### 性能提升
- 传统方式：数据复制 3 次，CPU 和内存开销大。
- 零拷贝：数据复制 1 次（或 0 次），CPU 和内存开销小。
- **适用场景**：大文件传输、消息队列、数据库日志复制。

---

## 验证脚本（fio 测试）

参考 `fio/scripts/fio_disk_test.sh`：
- 顺序读/写测试
- 随机读/写测试
- 混合读写测试

### 期望观察指标
- **IOPS**：每秒IO次数（随机读写常用）
- **吞吐量（Throughput）**：MB/s（顺序读写常用）
- **延迟（Latency）**：平均/最大延迟（ms）

---

## 常见坑
- **直接IO有对齐要求**：缓冲区地址和大小必须是 512 字节的倍数（某些系统）。
- **零拷贝不是万能的**：小文件传输时，零拷贝的开销可能不如传统方式。
- **异步IO需要事件循环**：必须有一个线程/进程负责处理IO完成事件。
