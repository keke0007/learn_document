"""
生成器和迭代器示例
演示生成器的各种用法
"""

from itertools import islice, cycle, count

# 1. 基础生成器函数
def fibonacci(n):
    """生成斐波那契数列"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# 2. 无限生成器
def infinite_counter(start=0):
    """无限计数器"""
    while True:
        yield start
        start += 1

# 3. 生成器表达式
def generator_expression_demo():
    """生成器表达式示例"""
    # 列表推导式（占用内存）
    squares_list = [x**2 for x in range(10)]
    print(f"List: {squares_list}")
    
    # 生成器表达式（节省内存）
    squares_gen = (x**2 for x in range(10))
    print(f"Generator: {list(squares_gen)}")

# 4. 生成器链式调用
def numbers():
    """生成数字"""
    for i in range(5):
        yield i

def squares(nums):
    """生成平方"""
    for num in nums:
        yield num ** 2

def evens(nums):
    """过滤偶数"""
    for num in nums:
        if num % 2 == 0:
            yield num

# 5. 迭代器协议
class CountDown:
    """自定义迭代器"""
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start

# 6. 生成器实现协程
def coroutine_demo():
    """协程示例"""
    def producer():
        for i in range(5):
            value = yield i
            print(f"Received: {value}")
    
    gen = producer()
    next(gen)  # 启动生成器
    for i in range(5):
        try:
            value = gen.send(i * 2)
            print(f"Produced: {value}")
        except StopIteration:
            break

# 7. 使用 itertools
def itertools_demo():
    """itertools 模块示例"""
    # islice：切片生成器
    print("islice:")
    for num in islice(infinite_counter(), 5):
        print(num, end=' ')
    print()
    
    # cycle：循环迭代
    print("cycle:")
    for item in islice(cycle(['A', 'B', 'C']), 7):
        print(item, end=' ')
    print()
    
    # count：计数器
    print("count:")
    for num in islice(count(10, 2), 5):
        print(num, end=' ')
    print()

# 8. 生成器性能对比
def performance_demo():
    """性能对比示例"""
    import time
    import sys
    
    # 列表推导式
    start = time.time()
    lst = [x**2 for x in range(1000000)]
    list_time = time.time() - start
    list_size = sys.getsizeof(lst)
    
    # 生成器表达式
    start = time.time()
    gen = (x**2 for x in range(1000000))
    gen_time = time.time() - start
    gen_size = sys.getsizeof(gen)
    
    print(f"List comprehension: {list_time:.4f}s, size: {list_size} bytes")
    print(f"Generator expression: {gen_time:.4f}s, size: {gen_size} bytes")
    print(f"Memory saved: {(list_size - gen_size) / list_size * 100:.2f}%")

# 使用示例
if __name__ == "__main__":
    print("=== 斐波那契数列 ===")
    for num in fibonacci(10):
        print(num, end=' ')
    print("\n")
    
    print("=== 无限生成器（限制10个） ===")
    for num in islice(infinite_counter(), 10):
        print(num, end=' ')
    print("\n")
    
    print("=== 生成器表达式 ===")
    generator_expression_demo()
    print()
    
    print("=== 生成器链式调用 ===")
    result = list(evens(squares(numbers())))
    print(f"Result: {result}\n")
    
    print("=== 自定义迭代器 ===")
    for num in CountDown(5):
        print(num, end=' ')
    print("\n")
    
    print("=== itertools 模块 ===")
    itertools_demo()
    print()
    
    print("=== 性能对比 ===")
    performance_demo()
