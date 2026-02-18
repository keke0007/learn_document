"""
异步编程示例
演示 asyncio 的使用
"""

import asyncio
import time

# 1. 基础异步函数
async def fetch_data(url):
    """模拟异步数据获取"""
    print(f"Fetching {url}")
    await asyncio.sleep(1)  # 模拟IO操作
    return f"Data from {url}"

async def main():
    """主函数"""
    urls = ['url1', 'url2', 'url3']
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# 2. 异步上下文管理器
class AsyncFileManager:
    """异步文件管理器"""
    async def __aenter__(self):
        print("Opening file")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing file")
        await asyncio.sleep(0.1)

async def use_async_context():
    """使用异步上下文管理器"""
    async with AsyncFileManager() as fm:
        print("Using file")

# 3. 异步生成器
async def async_generator():
    """异步生成器"""
    for i in range(5):
        await asyncio.sleep(0.5)
        yield i

async def consume_async_generator():
    """消费异步生成器"""
    async for value in async_generator():
        print(f"Received: {value}")

# 4. 异步锁
async def worker_with_lock(lock, num):
    """带锁的工作函数"""
    async with lock:
        print(f"Worker {num} acquired lock")
        await asyncio.sleep(1)
        print(f"Worker {num} released lock")

async def main_with_lock():
    """使用锁的主函数"""
    lock = asyncio.Lock()
    tasks = [worker_with_lock(lock, i) for i in range(5)]
    await asyncio.gather(*tasks)

# 5. 异步队列
async def producer(queue):
    """生产者"""
    for i in range(5):
        await asyncio.sleep(0.5)
        await queue.put(i)
        print(f"Produced: {i}")

async def consumer(queue):
    """消费者"""
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed: {item}")
        queue.task_done()

async def main_with_queue():
    """使用队列的主函数"""
    queue = asyncio.Queue()
    
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))
    
    await producer_task
    await queue.put(None)
    await consumer_task

# 6. 异步超时
async def slow_operation():
    """慢操作"""
    await asyncio.sleep(5)
    return "Done"

async def with_timeout():
    """带超时的操作"""
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("Operation timed out")

# 7. 性能对比
async def io_task():
    """IO任务"""
    await asyncio.sleep(1)
    return "Done"

async def test_async_performance():
    """测试异步性能"""
    start = time.time()
    tasks = [io_task() for _ in range(10)]
    await asyncio.gather(*tasks)
    async_time = time.time() - start
    print(f"Async (10 tasks): {async_time:.4f}s")

def test_sync_performance():
    """测试同步性能"""
    start = time.time()
    for _ in range(10):
        time.sleep(1)
    sync_time = time.time() - start
    print(f"Sync (10 tasks): {sync_time:.4f}s")

# 使用示例
if __name__ == "__main__":
    print("=== 基础异步函数 ===")
    results = asyncio.run(main())
    print(f"Results: {results}\n")
    
    print("=== 异步上下文管理器 ===")
    asyncio.run(use_async_context())
    print()
    
    print("=== 异步生成器 ===")
    asyncio.run(consume_async_generator())
    print()
    
    print("=== 异步锁 ===")
    asyncio.run(main_with_lock())
    print()
    
    print("=== 异步队列 ===")
    asyncio.run(main_with_queue())
    print()
    
    print("=== 异步超时 ===")
    asyncio.run(with_timeout())
    print()
    
    print("=== 性能对比 ===")
    asyncio.run(test_async_performance())
    test_sync_performance()
