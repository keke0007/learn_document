"""
装饰器示例
演示各种装饰器的用法和实现
"""

from functools import wraps
import time
import random

# 1. 基础装饰器
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")
    return f"Greeted {name}"

# 2. 计时装饰器
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
    return "Done"

# 3. 重试装饰器
def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed, retrying...")
            return None
        return wrapper
    return decorator

@retry(max_attempts=3)
def unreliable_function():
    if random.random() < 0.5:
        raise ValueError("Random failure")
    return "Success"

# 4. 缓存装饰器
def cache(func):
    cache_dict = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in cache_dict:
            print("Cache hit")
            return cache_dict[key]
        print("Cache miss")
        result = func(*args, **kwargs)
        cache_dict[key] = result
        return result
    return wrapper

@cache
def expensive_function(n):
    print(f"Computing {n}...")
    return n * n

# 5. 类装饰器
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} has been called {self.count} times")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    return f"Hello, {name}!"

# 6. 属性装饰器
class PropertyDemo:
    def __init__(self):
        self._value = 0
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        if val < 0:
            raise ValueError("Value must be non-negative")
        self._value = val
    
    @value.deleter
    def value(self):
        del self._value

# 7. 类方法装饰器
class MyClass:
    class_var = "Class variable"
    
    def __init__(self, value):
        self.instance_var = value
    
    @classmethod
    def class_method(cls):
        return cls.class_var
    
    @staticmethod
    def static_method():
        return "Static method"
    
    def instance_method(self):
        return self.instance_var

# 使用示例
if __name__ == "__main__":
    print("=== 基础装饰器 ===")
    result = say_hello("Python")
    print(f"Result: {result}\n")
    
    print("=== 计时装饰器 ===")
    slow_function()
    print()
    
    print("=== 重试装饰器 ===")
    for _ in range(3):
        try:
            result = unreliable_function()
            print(f"Result: {result}\n")
            break
        except ValueError as e:
            print(f"Error: {e}\n")
    
    print("=== 缓存装饰器 ===")
    print(expensive_function(5))
    print(expensive_function(5))
    print()
    
    print("=== 类装饰器 ===")
    greet("World")
    greet("Python")
    print()
    
    print("=== 属性装饰器 ===")
    obj = PropertyDemo()
    obj.value = 10
    print(f"Value: {obj.value}")
    # obj.value = -1  # 会抛出 ValueError
    print()
    
    print("=== 类方法和静态方法 ===")
    print(MyClass.class_method())
    print(MyClass.static_method())
    obj = MyClass("Instance")
    print(obj.instance_method())
