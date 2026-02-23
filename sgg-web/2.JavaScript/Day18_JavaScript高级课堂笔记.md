# Day18 JavaScript 高级课堂笔记

## 1 回顾

```
1. 垃圾回收
   引用计数
   标记清除

2. 函数高级
2.1 执行上下文对象
   ① 全局执行上下文对象和函数内执行上下文对象
   ② 执行栈
   ③ 执行上下文对象和作用域
2.2 闭包函数
   ① 闭包概念  
   ② 实现闭包
   ③ 闭包和作用域
   ④ 闭包和垃圾回收
   ⑤ 闭包应用
```



## 2 对象高级

### 2.1 原型链总结

#### ① 原型和构造函数

```
1. 构造函数.prototype 可以获取到该构造函数实例的原型
2. 构造函数相同的对象，原型也相同
```

#### ② `__proto__` 和 prototype 属性

```
1. 函数类型的对象
   __proto__ : 获取的是自己的原型  
   prototype: 获取的该构造函数的实例的原型

2. 其他类型的对象
   __proto__： 获取的是自己的原型
   没有 prototype 属性
```

#### ③  construct 属性

```
本身具有constructor属性的对象，会作为其他对象的原型，constructor的值就是其他对象的构造函数
```

#### ④ 原型链

```js
// 自定义的构造函数
function Foo() {}

// Foo 的两个实例
var f1 = new Foo();
var f2 = new Foo();

// Object的两个实例
var o1 = {};
var o2 = {};
```

```
f1、f2 -> Foo.prototype -> Object.prototype
o1、o2 -> Object.prototype
Foo、Object、Function -> Function.prototype -> Object.prototype
```

**特殊现象（不是规则，不要记，要理解）**

```
1. Object 的原型是 Function.prototype, Function.prototype 的构造函数是 Object
2. Function 的构造函数是 Function， 所以 Function.prototype === Function.__proto__
```





### 2.2 面向对象继承

#### ① 面向对象编程语言的继承规则

```php
// 父类（对应的就是js中的构造函数）
class Foo{
    private name;
    private age;
    public getInfo() {}
}

// 子类
class Product extends Foo {
    private address;
}

// 子类
class Shopcart extends Foo {
    
}
```

#### ② JS 中继承关系的特点（原型继承特点）

```
1. 对象可以继承它的原型上的属性
2. 对象的构造函数、它的原型的构造函数也可以描述成子类、父类的关系
```

```
1. 对象a的原型是对象b, 对象a的构造函数是子类，对象b的构造函数是父类
   子类的实例以父类的实例为原型
2. 一个对象只能有一个原型，原型可以作为多个对象的原型
   一个父类可以有多个子类， 一个子类只能有一个父类
```

#### ③ 实现JS中构造函数和构造函数之间继承(子类 父类)

**原理：**

```
1. 设置子类的实例的原型是父类的一个实例
2. 设置子类的实例的原型的 constructor 属性的值是子类
```

```js
function A(){}
function B(){}

// B作为子类 A作为父类 
// 设置B的实例的原型是 A的一个实例
B.prototype = new A();
// 设置 B.prptotype 的 constructor 属性
B.prototype.constructor = B;
```

```js
Array是子类 Object是父类
1. Array的实例的原型 是Object的一个实例
2. Array.prototype.constructor 是 Array
```

**实现：**

```js
 // 定义商品类 
function Product(price, nums) {
    // 给实例设置属性
    this.price = price;;
    this.nums = nums;
}
Product.prototype.discount = function(num) {
    this.price *= num;
};
Product.prototype.buy = function() {
    this.nums -= 1;
}

// 汽车类商品
function CarProduct(price, nums, speed) {
    // this.price = price;
    // this.nums = nums;
    // 将父类规定的属性添加到了 CarProduct 的实例上
    Product.call(this, price, nums);
    this.speed = speed;
}   
// 设置  CarProduct 的实例的原型是 Product 的一个实例
CarProduct.prototype = new Product();
// 设置 CarProduct 的实例的的原型的 constructor 属性的值是  CarProduct
CarProduct.prototype.constructor = CarProduct;
// 设置方法
CarProduct.prototype.driver = function() {
    console.log('这辆车可以被驾驶！');
}
```







## 3 单线程和事件轮询机制

### 3.1 进程和线程

```
进程：
    程序的一次执行, 它占有一片独有的内存空间

线程：
    CPU的基本调度单位, 是程序执行的一个完整流程


进程和线程：
  * 一个进程中一般至少有一个运行的线程: 主线程。
  * 一个进程中也可以同时运行多个线程, 我们会说程序是多线程运行的。
  * 一个进程内的数据可以供其中的多个线程直接共享。
  * 多个进程之间的数据是不能直接共享的。
```

### 3.2 JS 单线程运行

```
1. 如何证明JavaScript是单线程执行？
   设置了定时器，定时器的回调函数会等到主线程空闲且时间到执行；
   如果主线程没有空闲下来，即使定时器的时间到了，回调函数也不会执行（等到主线程空闲）。

2. 为什么JavaScript选择单线程？
   多线程会有线程调度以及线程开启关闭的开销
   JavaScript主要在浏览器端操作DOM完成特效，如果不是单线程，不好解决页面渲染的同步问题。
```

### 3.3 同步任务和异步任务

```
同步任务：
按照顺序，一步一步地执行，执行完上一个任务再执行下一个任务

异步任务：
需要满足条件且主线程空闲才可以执行，在等待异步任务满足条件的过程中，同步任务继续执行，  异步任务会在同步任务完成后执行
异步任务都是回调函数的形式， 回调函数不一定都是异步任务

JS中的异步任务有哪些：
1. 定时器的回调函数
2. DOM事件的回调函数
3. Ajax的回调函数
4. Promise的回调涵数
....
```

### 3.4 事件轮询机制

```
1、执行栈（调用栈）
   主线程里就是一个执行栈，所有的任务都要放入执行栈执行
    
2、异步任务管理模块
   判断异步任务是否满足了执行条件，分为：
   定时器管理模块
   DOM事件管理模块
   Ajax管理模块
   ...
   如果满足了异步任务管理模块，会将异步任务放入回调队列，等待执行

3. 回调队列
   队列是一种数据存储结构，特点是先进先出，后进后出
   回调队列存放等待执行的异步任务

4. 事件轮询模块
   时刻监听主线程（执行栈）是否空闲，一旦空闲，从回调队列中取出异步任务，放入主线程执行
```



## 4 JS 实现多线程（了解）

```
Worker 构造函数
Worker.prototype.postMessage()  向分线程发送数据
Worker.prototype.onmessage      监听分线程的消息
```

