# 案例2：网络IO模型（BIO / NIO / AIO / epoll / Reactor）

## 案例目标
理解网络IO的演进路径，以及为什么中间件（如 Nginx、Netty、Kafka）选择 NIO/epoll：
- **BIO（Blocking IO）**：阻塞式，一连接一线程
- **NIO（Non-blocking IO）**：非阻塞 + Selector
- **AIO（Asynchronous IO）**：异步IO
- **epoll（Linux）**：高效的事件通知机制
- **Reactor 模式**：事件驱动的设计模式

## 一、BIO（Blocking IO）：阻塞式IO

### 一句话讲明白
BIO 就是“一个连接一个线程”，线程在等待数据时会阻塞，不能做其他事情。

### 代码示例（见 `fio/scripts/network_io_demo.java`）

```java
ServerSocket serverSocket = new ServerSocket(8080);
while (true) {
    Socket clientSocket = serverSocket.accept(); // 阻塞等待连接
    new Thread(() -> {
        // 处理这个连接的读写（也是阻塞的）
        BufferedReader in = new BufferedReader(...);
        String line = in.readLine(); // 阻塞等待数据
    }).start();
}
```

### 问题
- **线程资源消耗大**：1 万个连接需要 1 万个线程。
- **上下文切换开销**：线程多了，CPU 花在切换线程上的时间比干活的时间还多。

---

## 二、NIO（Non-blocking IO）：非阻塞IO + Selector

### 一句话讲明白
NIO 用“一个线程 + Selector”管理多个连接，哪个连接有数据就处理哪个，没有数据的连接不阻塞。

### 核心组件
- **Channel**：连接通道（ServerSocketChannel、SocketChannel）
- **Buffer**：数据缓冲区（ByteBuffer）
- **Selector**：事件选择器（监听哪些 Channel 有事件）

### 代码示例（见 `fio/scripts/network_io_demo.java`）

```java
ServerSocketChannel serverChannel = ServerSocketChannel.open();
serverChannel.configureBlocking(false); // 非阻塞模式
Selector selector = Selector.open();
serverChannel.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    selector.select(); // 阻塞直到有事件就绪
    for (SelectionKey key : selector.selectedKeys()) {
        if (key.isAcceptable()) {
            // 接受新连接
        } else if (key.isReadable()) {
            // 读取数据（非阻塞）
        }
    }
}
```

### 优势
- **一个线程管理多个连接**：1 万个连接可能只需要几十个线程。
- **事件驱动**：只处理“有数据可读/可写”的连接。

---

## 三、epoll（Linux 的高效事件通知）

### 一句话讲明白
epoll 是 Linux 提供的高效事件通知机制，比传统的 select/poll 更高效，能处理大量并发连接。

### 为什么 epoll 更快？
- **select/poll**：每次都要把“所有文件描述符”传给内核，内核遍历一遍找出就绪的。
- **epoll**：内核维护一个“就绪列表”，只返回就绪的文件描述符，不需要遍历全部。

### 类比
- select/poll：你问“这 1 万个连接里哪些有数据？”，内核要一个个检查。
- epoll：内核主动告诉你“这 3 个连接有数据了”，你直接处理这 3 个就行。

### Java NIO 底层
- 在 Linux 上，Java NIO 的 Selector 底层就是 epoll。
- 在 Windows 上，底层是 IOCP（另一种高效机制）。

---

## 四、Reactor 模式（事件驱动）

### 一句话讲明白
Reactor 模式就是“事件循环 + 事件分发 + 事件处理”，用一个线程（或线程池）处理所有IO事件。

### 单 Reactor 单线程
```
主线程（Reactor）：
  - 监听连接事件（accept）
  - 监听读写事件（read/write）
  - 分发事件给对应的 Handler 处理
```

### 单 Reactor 多线程
```
主线程（Reactor）：
  - 只负责监听和分发事件
工作线程池：
  - 处理业务逻辑（解码、计算、编码）
```

### 多 Reactor 多线程（Netty 采用）
```
主 Reactor（Boss Group）：
  - 只负责接受连接
子 Reactor（Worker Group）：
  - 负责连接的读写事件
工作线程池：
  - 处理业务逻辑
```

### 为什么中间件都用 Reactor？
- **高并发**：一个线程管理大量连接。
- **低延迟**：事件驱动，有数据就处理，不空转。
- **可扩展**：可以按需增加 Reactor 线程和工作线程。

---

## 五、AIO（Asynchronous IO）：异步IO

### 一句话讲明白
AIO 是“真正的异步IO”，发起IO请求后立即返回，IO完成后通过回调通知你。

### 与 NIO 的区别
- **NIO**：非阻塞，但还是要“轮询”检查是否有数据可读。
- **AIO**：异步，内核准备好数据后主动通知你，你不需要轮询。

### 代码示例（见 `fio/scripts/network_io_demo.java`）

```java
AsynchronousServerSocketChannel serverChannel = 
    AsynchronousServerSocketChannel.open();
serverChannel.accept(null, new CompletionHandler() {
    @Override
    public void completed(AsynchronousSocketChannel client, Void attachment) {
        // 连接建立后的回调
        client.read(buffer, buffer, new CompletionHandler() {
            @Override
            public void completed(Integer result, ByteBuffer buffer) {
                // 数据读取完成后的回调
            }
        });
    }
});
```

### 为什么 AIO 用得少？
- **Linux AIO 不完善**：Linux 的 AIO 主要支持文件IO，网络IO的 AIO 支持不好。
- **NIO + epoll 已经够用**：NIO 配合 epoll 已经能实现高并发，AIO 的收益不明显。

---

## 验证脚本

参考 `fio/scripts/network_io_demo.java`：
- BIO Server：一个连接一个线程
- NIO Server：一个线程管理多个连接
- AIO Server：异步IO（演示用）

### 性能对比（概念）
- **BIO**：1 万连接 ≈ 1 万线程，内存和CPU开销大。
- **NIO**：1 万连接 ≈ 10-100 线程，内存和CPU开销小。
- **AIO**：理论上更高效，但实际使用场景有限。

---

## 常见坑
- **NIO 的“空轮询”Bug**：某些情况下 select() 会立即返回但没有任何事件，需要特殊处理。
- **Buffer 的 flip()/clear()**：NIO 的 Buffer 需要手动管理 position/limit，容易出错。
- **Reactor 线程阻塞**：如果 Reactor 线程里做了耗时操作，会影响所有连接的响应。
