import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * 并发编程演示
 */
public class ConcurrencyDemo {
    // volatile 保证可见性
    private volatile boolean flag = false;
    
    // AtomicInteger 保证原子性
    private AtomicInteger count = new AtomicInteger(0);
    
    /**
     * 演示 synchronized 的使用
     */
    public synchronized void synchronizedMethod() {
        count.incrementAndGet();
    }
    
    /**
     * 演示 volatile 的可见性
     */
    public void volatileDemo() {
        Thread thread1 = new Thread(() -> {
            while (!flag) {
                // 空循环等待
            }
            System.out.println("Thread 1: flag is true");
        });
        
        Thread thread2 = new Thread(() -> {
            try {
                Thread.sleep(1000);
                flag = true;
                System.out.println("Thread 2: set flag to true");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        
        thread1.start();
        thread2.start();
    }
    
    /**
     * 演示线程池的使用
     */
    public void threadPoolDemo() {
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            5,                          // 核心线程数
            10,                         // 最大线程数
            60L,                        // 空闲线程存活时间
            TimeUnit.SECONDS,           // 时间单位
            new LinkedBlockingQueue<>(100), // 工作队列
            new ThreadFactory() {        // 线程工厂
                @Override
                public Thread newThread(Runnable r) {
                    Thread t = new Thread(r);
                    t.setName("CustomThread-" + t.getId());
                    return t;
                }
            },
            new ThreadPoolExecutor.CallerRunsPolicy() // 拒绝策略
        );
        
        for (int i = 0; i < 20; i++) {
            final int taskId = i;
            executor.execute(() -> {
                System.out.println("Task " + taskId + " executed by " + Thread.currentThread().getName());
            });
        }
        
        executor.shutdown();
    }
    
    /**
     * 演示 CountDownLatch
     */
    public void countDownLatchDemo() throws InterruptedException {
        int threadCount = 5;
        CountDownLatch latch = new CountDownLatch(threadCount);
        
        for (int i = 0; i < threadCount; i++) {
            new Thread(() -> {
                try {
                    System.out.println(Thread.currentThread().getName() + " is working");
                    Thread.sleep(1000);
                    latch.countDown();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }).start();
        }
        
        latch.await();
        System.out.println("All threads completed");
    }
    
    /**
     * 演示 CompletableFuture
     */
    public void completableFutureDemo() {
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return "Result 1";
        });
        
        CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return "Result 2";
        });
        
        CompletableFuture<String> combined = future1.thenCombine(future2, (r1, r2) -> r1 + " + " + r2);
        
        combined.thenAccept(result -> System.out.println("Combined result: " + result));
    }
    
    public static void main(String[] args) throws InterruptedException {
        ConcurrencyDemo demo = new ConcurrencyDemo();
        
        System.out.println("Concurrency Demo");
        System.out.println("================");
        
        // 取消注释以运行不同的测试
        // demo.volatileDemo();
        // demo.threadPoolDemo();
        // demo.countDownLatchDemo();
        // demo.completableFutureDemo();
    }
}
