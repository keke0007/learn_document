"""
设计模式示例
演示常用设计模式的实现
"""

from abc import ABC, abstractmethod

# 1. 单例模式
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# 2. 工厂模式
class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")

# 3. 观察者模式
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self, event):
        for observer in self._observers:
            observer.update(event)

class Observer(ABC):
    @abstractmethod
    def update(self, event):
        pass

class ConcreteObserver(Observer):
    def __init__(self, name):
        self.name = name
    
    def update(self, event):
        print(f"{self.name} received event: {event}")

# 4. 策略模式
class Strategy(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

class AddStrategy(Strategy):
    def execute(self, a, b):
        return a + b

class SubtractStrategy(Strategy):
    def execute(self, a, b):
        return a - b

class Context:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy):
        self.strategy = strategy
    
    def execute_strategy(self, a, b):
        return self.strategy.execute(a, b)

# 5. 装饰器模式
class Component(ABC):
    @abstractmethod
    def operation(self):
        pass

class ConcreteComponent(Component):
    def operation(self):
        return "ConcreteComponent"

class Decorator(Component):
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return self._component.operation()

class ConcreteDecoratorA(Decorator):
    def operation(self):
        return f"ConcreteDecoratorA({self._component.operation()})"

# 使用示例
if __name__ == "__main__":
    print("=== 单例模式 ===")
    s1 = Singleton()
    s2 = Singleton()
    print(f"s1 is s2: {s1 is s2}\n")
    
    print("=== 工厂模式 ===")
    dog = AnimalFactory.create_animal("dog")
    cat = AnimalFactory.create_animal("cat")
    print(f"Dog says: {dog.speak()}")
    print(f"Cat says: {cat.speak()}\n")
    
    print("=== 观察者模式 ===")
    subject = Subject()
    observer1 = ConcreteObserver("Observer1")
    observer2 = ConcreteObserver("Observer2")
    subject.attach(observer1)
    subject.attach(observer2)
    subject.notify("Event occurred\n")
    
    print("=== 策略模式 ===")
    context = Context(AddStrategy())
    print(f"10 + 5 = {context.execute_strategy(10, 5)}")
    context.set_strategy(SubtractStrategy())
    print(f"10 - 5 = {context.execute_strategy(10, 5)}\n")
    
    print("=== 装饰器模式 ===")
    component = ConcreteComponent()
    decorator = ConcreteDecoratorA(component)
    print(decorator.operation())
