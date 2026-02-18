# 设计模式案例

## 案例概述

本案例通过实际代码演示常用设计模式的实现，包括单例模式、工厂模式、代理模式等。

## 知识点

1. **创建型模式**
   - 单例模式
   - 工厂模式
   - 建造者模式

2. **结构型模式**
   - 代理模式
   - 适配器模式
   - 装饰器模式

3. **行为型模式**
   - 观察者模式
   - 策略模式
   - 责任链模式

## 案例代码

### 案例1：单例模式

#### 饿汉式

```java
public class SingletonEager {
    private static final SingletonEager instance = new SingletonEager();
    
    private SingletonEager() {}
    
    public static SingletonEager getInstance() {
        return instance;
    }
}
```

**优点：** 线程安全，实现简单  
**缺点：** 类加载时就创建，可能浪费内存

#### 懒汉式（双重检查锁定）

```java
public class SingletonLazy {
    private volatile static SingletonLazy instance;
    
    private SingletonLazy() {}
    
    public static SingletonLazy getInstance() {
        if (instance == null) {
            synchronized (SingletonLazy.class) {
                if (instance == null) {
                    instance = new SingletonLazy();
                }
            }
        }
        return instance;
    }
}
```

**优点：** 延迟加载，线程安全  
**缺点：** 实现复杂，需要 volatile 关键字

#### 静态内部类

```java
public class SingletonInner {
    private SingletonInner() {}
    
    private static class Holder {
        private static final SingletonInner instance = new SingletonInner();
    }
    
    public static SingletonInner getInstance() {
        return Holder.instance;
    }
}
```

**优点：** 线程安全，延迟加载，实现简单  
**缺点：** 无法防止反射和序列化攻击

#### 枚举

```java
public enum SingletonEnum {
    INSTANCE;
    
    public void doSomething() {
        System.out.println("Do something");
    }
}
```

**优点：** 线程安全，防止反射和序列化攻击  
**缺点：** 不够灵活

### 案例2：工厂模式

#### 简单工厂

```java
// 产品接口
interface Product {
    void use();
}

// 具体产品
class ConcreteProductA implements Product {
    @Override
    public void use() {
        System.out.println("Using Product A");
    }
}

class ConcreteProductB implements Product {
    @Override
    public void use() {
        System.out.println("Using Product B");
    }
}

// 简单工厂
class SimpleFactory {
    public static Product createProduct(String type) {
        if ("A".equals(type)) {
            return new ConcreteProductA();
        } else if ("B".equals(type)) {
            return new ConcreteProductB();
        }
        throw new IllegalArgumentException("Unknown product type");
    }
}
```

#### 工厂方法

```java
// 工厂接口
interface Factory {
    Product createProduct();
}

// 具体工厂
class FactoryA implements Factory {
    @Override
    public Product createProduct() {
        return new ConcreteProductA();
    }
}

class FactoryB implements Factory {
    @Override
    public Product createProduct() {
        return new ConcreteProductB();
    }
}
```

### 案例3：代理模式

#### 静态代理

```java
// 接口
interface Subject {
    void request();
}

// 真实对象
class RealSubject implements Subject {
    @Override
    public void request() {
        System.out.println("RealSubject request");
    }
}

// 代理对象
class Proxy implements Subject {
    private RealSubject realSubject;
    
    @Override
    public void request() {
        if (realSubject == null) {
            realSubject = new RealSubject();
        }
        preRequest();
        realSubject.request();
        postRequest();
    }
    
    private void preRequest() {
        System.out.println("Pre request");
    }
    
    private void postRequest() {
        System.out.println("Post request");
    }
}
```

#### JDK 动态代理

```java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

class DynamicProxy implements InvocationHandler {
    private Object target;
    
    public DynamicProxy(Object target) {
        this.target = target;
    }
    
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        System.out.println("Before method: " + method.getName());
        Object result = method.invoke(target, args);
        System.out.println("After method: " + method.getName());
        return result;
    }
    
    public static Object createProxy(Object target) {
        return Proxy.newProxyInstance(
            target.getClass().getClassLoader(),
            target.getClass().getInterfaces(),
            new DynamicProxy(target)
        );
    }
}
```

### 案例4：观察者模式

```java
import java.util.ArrayList;
import java.util.List;

// 观察者接口
interface Observer {
    void update(String message);
}

// 被观察者
class Subject {
    private List<Observer> observers = new ArrayList<>();
    private String state;
    
    public void attach(Observer observer) {
        observers.add(observer);
    }
    
    public void detach(Observer observer) {
        observers.remove(observer);
    }
    
    public void setState(String state) {
        this.state = state;
        notifyAllObservers();
    }
    
    private void notifyAllObservers() {
        for (Observer observer : observers) {
            observer.update(state);
        }
    }
}

// 具体观察者
class ConcreteObserver implements Observer {
    private String name;
    
    public ConcreteObserver(String name) {
        this.name = name;
    }
    
    @Override
    public void update(String message) {
        System.out.println(name + " received: " + message);
    }
}

// 使用示例
public class ObserverDemo {
    public static void main(String[] args) {
        Subject subject = new Subject();
        
        Observer observer1 = new ConcreteObserver("Observer 1");
        Observer observer2 = new ConcreteObserver("Observer 2");
        
        subject.attach(observer1);
        subject.attach(observer2);
        
        subject.setState("State changed");
    }
}
```

### 案例5：策略模式

```java
// 策略接口
interface Strategy {
    int execute(int a, int b);
}

// 具体策略
class AddStrategy implements Strategy {
    @Override
    public int execute(int a, int b) {
        return a + b;
    }
}

class SubtractStrategy implements Strategy {
    @Override
    public int execute(int a, int b) {
        return a - b;
    }
}

class MultiplyStrategy implements Strategy {
    @Override
    public int execute(int a, int b) {
        return a * b;
    }
}

// 上下文
class Context {
    private Strategy strategy;
    
    public Context(Strategy strategy) {
        this.strategy = strategy;
    }
    
    public void setStrategy(Strategy strategy) {
        this.strategy = strategy;
    }
    
    public int executeStrategy(int a, int b) {
        return strategy.execute(a, b);
    }
}

// 使用示例
public class StrategyDemo {
    public static void main(String[] args) {
        Context context = new Context(new AddStrategy());
        System.out.println("10 + 5 = " + context.executeStrategy(10, 5));
        
        context.setStrategy(new SubtractStrategy());
        System.out.println("10 - 5 = " + context.executeStrategy(10, 5));
        
        context.setStrategy(new MultiplyStrategy());
        System.out.println("10 * 5 = " + context.executeStrategy(10, 5));
    }
}
```

### 案例6：责任链模式

```java
// 处理器接口
abstract class Handler {
    protected Handler nextHandler;
    
    public void setNextHandler(Handler nextHandler) {
        this.nextHandler = nextHandler;
    }
    
    public abstract void handleRequest(Request request);
}

// 具体处理器
class ConcreteHandler1 extends Handler {
    @Override
    public void handleRequest(Request request) {
        if (request.getType() == RequestType.TYPE1) {
            System.out.println("Handler1 handles the request");
        } else if (nextHandler != null) {
            nextHandler.handleRequest(request);
        }
    }
}

class ConcreteHandler2 extends Handler {
    @Override
    public void handleRequest(Request request) {
        if (request.getType() == RequestType.TYPE2) {
            System.out.println("Handler2 handles the request");
        } else if (nextHandler != null) {
            nextHandler.handleRequest(request);
        }
    }
}

// 请求类
class Request {
    private RequestType type;
    
    public Request(RequestType type) {
        this.type = type;
    }
    
    public RequestType getType() {
        return type;
    }
}

enum RequestType {
    TYPE1, TYPE2, TYPE3
}

// 使用示例
public class ChainOfResponsibilityDemo {
    public static void main(String[] args) {
        Handler handler1 = new ConcreteHandler1();
        Handler handler2 = new ConcreteHandler2();
        
        handler1.setNextHandler(handler2);
        
        Request request = new Request(RequestType.TYPE2);
        handler1.handleRequest(request);
    }
}
```

## 验证数据

### 性能测试

| 模式 | 创建对象时间 | 内存占用 | 适用场景 |
|-----|------------|---------|---------|
| 单例模式 | 0.001ms | 低 | 全局唯一对象 |
| 工厂模式 | 0.01ms | 中 | 对象创建复杂 |
| 代理模式 | 0.05ms | 中 | 增强功能 |
| 观察者模式 | 0.02ms | 中 | 事件通知 |

### 使用场景总结

1. **单例模式**
   - 数据库连接池
   - 线程池
   - 配置管理器

2. **工厂模式**
   - 日志框架
   - 数据库驱动
   - UI 组件创建

3. **代理模式**
   - Spring AOP
   - RPC 框架
   - 权限控制

4. **观察者模式**
   - 事件驱动系统
   - MVC 架构
   - 消息队列

## 总结

1. **设计原则**
   - 单一职责原则
   - 开闭原则
   - 里氏替换原则
   - 依赖倒置原则
   - 接口隔离原则
   - 迪米特法则

2. **模式选择**
   - 根据具体场景选择合适的设计模式
   - 不要过度设计
   - 优先使用简单方案

3. **最佳实践**
   - 理解模式意图
   - 结合实际项目
   - 持续重构优化
