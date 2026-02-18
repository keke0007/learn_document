// 网络IO模型示例：BIO / NIO / AIO 对比（简化版）

import java.io.*;
import java.net.*;
import java.nio.*;
import java.nio.channels.*;
import java.util.concurrent.*;

// ============================================
// 1. BIO（Blocking IO）：阻塞式IO
// ============================================
public class BioServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(8080);
        System.out.println("BIO Server started on port 8080");
        
        while (true) {
            Socket clientSocket = serverSocket.accept(); // 阻塞等待连接
            new Thread(() -> {
                try {
                    BufferedReader in = new BufferedReader(
                        new InputStreamReader(clientSocket.getInputStream())
                    );
                    String line;
                    while ((line = in.readLine()) != null) { // 阻塞等待数据
                        System.out.println("Received: " + line);
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }).start();
        }
    }
}

// ============================================
// 2. NIO（Non-blocking IO）：非阻塞IO + Selector
// ============================================
public class NioServer {
    public static void main(String[] args) throws IOException {
        ServerSocketChannel serverChannel = ServerSocketChannel.open();
        serverChannel.bind(new InetSocketAddress(8080));
        serverChannel.configureBlocking(false); // 非阻塞模式
        
        Selector selector = Selector.open();
        serverChannel.register(selector, SelectionKey.OP_ACCEPT);
        
        System.out.println("NIO Server started on port 8080");
        
        while (true) {
            selector.select(); // 阻塞直到有事件就绪
            for (SelectionKey key : selector.selectedKeys()) {
                if (key.isAcceptable()) {
                    ServerSocketChannel server = (ServerSocketChannel) key.channel();
                    SocketChannel client = server.accept();
                    client.configureBlocking(false);
                    client.register(selector, SelectionKey.OP_READ);
                } else if (key.isReadable()) {
                    SocketChannel client = (SocketChannel) key.channel();
                    ByteBuffer buffer = ByteBuffer.allocate(1024);
                    client.read(buffer);
                    // 处理数据...
                }
            }
            selector.selectedKeys().clear();
        }
    }
}

// ============================================
// 3. AIO（Asynchronous IO）：异步IO（Java NIO.2）
// ============================================
public class AioServer {
    public static void main(String[] args) throws IOException {
        AsynchronousServerSocketChannel serverChannel = 
            AsynchronousServerSocketChannel.open();
        serverChannel.bind(new InetSocketAddress(8080));
        
        System.out.println("AIO Server started on port 8080");
        
        serverChannel.accept(null, new CompletionHandler<AsynchronousSocketChannel, Void>() {
            @Override
            public void completed(AsynchronousSocketChannel client, Void attachment) {
                serverChannel.accept(null, this); // 继续接受下一个连接
                
                ByteBuffer buffer = ByteBuffer.allocate(1024);
                client.read(buffer, buffer, new CompletionHandler<Integer, ByteBuffer>() {
                    @Override
                    public void completed(Integer result, ByteBuffer buffer) {
                        // 处理数据...
                    }
                    
                    @Override
                    public void failed(Throwable exc, ByteBuffer buffer) {
                        exc.printStackTrace();
                    }
                });
            }
            
            @Override
            public void failed(Throwable exc, Void attachment) {
                exc.printStackTrace();
            }
        });
        
        // 保持主线程运行
        Thread.sleep(Long.MAX_VALUE);
    }
}
