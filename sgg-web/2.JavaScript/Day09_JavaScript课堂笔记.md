# Day09 JavaScript 课堂笔记

## 1 回顾

```
1. Object 对象
   1.1 创建方式
   1.2 读写对象的属性
   1.3 遍历对象的属性
   1.4 in 运算符
   1.5 delete 运算符

2. 构造函数
   2.1 构造函数的概念 数据类型
       instanceof
       .constructor
   2.2 构造函数和对象的关系
   2.3 自定义构造函数
   2.4 实例化
       构造函数中的返回对实例化结果的影响
   2.5 构造函数和函数
   2.6 原始类型数据的对象特性
       
3. this
   3.1 this 是系统自动创建的只读变量，不同地方得到的值不同
   3.2 this 的取值
       ① 在函数外，全局下
       ② 在构造函数中  this的值是该构造函数实例化产生的对象
       ③ 在函数（方法）中
         谁掉用该函数，函数中的this就指向谁
    3.3 window
```





## 2 原型

### 2.1 原型的概念

```
1. 每个对象都有原型，原型也是个对象。
2. 对象可以使用原型上的属性（继承）。
```

### 2.2 如何获取对象的原型

**通过对象获取原型(隐式原型)：** 

```js
对象.__proto__
```

**通过对象的构造函数获取原型（显示原型）：**

```js
对象的构造函数.prototype
```

### 2.3 对象、构造函数、原型之间的关系

#### ① 对象和构造函数

```
1. 构造函数是对象的描述，对象是构造函数的实例
2、一个构造函数可以有无数个对象，一个对象只能有一个构造函数
```

#### ② 对象和原型

```
1. 每个对象都有原型，可以使用原型上的属性
2. 一个对象只能有一个原型，一个原型可以作为多个对象的原型。
```

#### ③ 构造函数和原型

```
1. 可以通过构造函数获取到对象的原型
2. 构造函数相同的对象，原型也是相同的； 相同数据类型的原型，原型相同。
```

### 2.4 自定义构造函数时原型的应用

```js
// 自定义构造函数
function User(name, age, address) {
    this.name = name;
    this.age = age;
    this.address = address;
}

// 将方法添加到 User的实例的原型
User.prototype.addShopcart = function(product) {
    console.log(this.name + '将' + product + '添加到购物车！');
};

User.prototype.buy = function(product) {
    console.log(this.name + '购买了' + product);
};
```

### 2.5 判断属性是否属于对象本身

```js
对象.hasOwnProperty('属性名');
```

```
只有属性在对象本身上才返回true，否则都是false（包括在原型不在本身）
```

### 2.6 创建对象的同时设置原型

```js
// 创建对象 原型是提取准备好的 实例化的时候将对象与原型关联
var obj1 = {};
console.log(obj1);
console.log('');


// 创建对象的同时 自己设置原型
var obj2 = Object.create([10,20,30,40]);
console.log(obj2);
console.log('');

// 创建对象的同时 自己设置原型
var obj3 = Object.create(new String('hello'));
console.log(obj3);
console.log('');


// 创建没有原型的对象
var obj4 = Object.create(null);
console.log(obj4);
```





## 3 原型链

### 3.1 原型链

```
每个对象都有原型，原型还是个对象，原型也有原型，原型的原型也有原型，组成了原型链
```

### 3.2 原型链的作用

```
1. 对象在查找找属性的时候，先从自身去找看有没有这个属性，如果有，直接使用这个属性的值。
2. 如果没有，会沿着原型链向上找，如果找到就使用这个属性的值且停止查找，如果没找到继续向上找直到原型链的终点。
3. 如果找到原型链的终点还没有找到，就返回 undefined 
```

### 3.3 原型链和构造函数

```
1. Object、Array、自定义函数等所有的函数 的原型是 Function.prototype, Function.prototype 的构造函数是 Object
2. Function.__proto__ 等于 Function.prototype, Function 的构造函数是自己
```

### 3.4 instanceof 和原型链

```
对象 instanceof 构造函数
```

```
第二个操作数是对象自己的构造函数成立； 第二个操作数是对象原型链上的某个对象的构造函数也成立
```

### 3.5 关于 constructor 属性

```js
默认情况：
假如对象a 的原型是 b
通常，a本身上没有 constructor属性； b 自身上会有 constructor 属性，但是给 a 准备的， 值是 a 的构造函数
所以：
a.constructor 获取的是 a 的构造函数
b.constructor 的值也是 a 的构造函数
```



## 4 值类型和引用类型

**值类型：**  

**引用类型：** 

**二者区别：**

```
1. 内存存储方式
   值类型： 
   引用类型： 

2. 赋值方式（传值方式）
   值类型： 
   引用类型：

3. 可变和不可变
   值类型： 
   引用类型： 

4. 判等方式
   值类型： 
   引用类型： 
```







## 作业

```
1. 原型链练习题
3. 画一画原型链的图
   Array、function Product() {}、Object、Function
   var arr = [];
   var p = new Product();

```





