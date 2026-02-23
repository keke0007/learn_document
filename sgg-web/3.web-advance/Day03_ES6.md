# Day03 ES6 课堂笔记

## 复习

```
1. 数值新增特性
   1.1 二进制和八进制表示
   1.2 Number构造函数本身新增的属性方法
   1.3 Math对象新增的属性方法
   1.4 数字分隔符

2. 函数新增特性
   2.1 参数默认值
   2.2 reset 参数
   2.3 箭头函数
   2.4 参数为逗号

3. 数组新增特性
   2.1 扩展运算符
       将数组拆分成逗号分隔的参数序列
       从参数序列中获取到数组
   2.2 Array构造函数的属性方法
   2.3 Array实例的属性方法

4. 对象新增特性
   4.1 {}声明对象 属性简写
   4.2 {}声明对象 方法简写
   4.3 {}声明对象 表达式作为属性名
   4.4 super关键字
   4.5 扩展运算符
       将对象拆分为逗号分隔键值对序列
       从逗号分隔键值对序列获取到对象
   4.6 Object构造函数本身的属性方法
```





## 1 新增的运算符

| 运算符 | 运算符含义     | 操作数个数 | 操作数类型要求         | 组成的表达式的值的类型                   | 组成的表达式有无副作用 |
| ------ | -------------- | ---------- | ---------------------- | ---------------------------------------- | ---------------------- |
| **     | 指数运算符     | 2          | number                 | number                                   | 无                     |
| ?.     | 可选链运算符   | 2          | 无                     | undefined或其他                          | 无                     |
| ??     | 空值判断运算符 | 2          | 无                     | 多种                                     | 无                     |
| &&=    | 逻辑与赋值     | 2          | 左边操作数是变量的形式 | 左边操作数重新赋值之后的值作为表达式的值 | 有                     |
| \|\|=  | 逻辑或赋值     | 2          | 左边操作数是变量的形式 | 左边操作数重新赋值之后的值作为表达式的值 | 有                     |
| ??=    | 空值判断赋值   | 2          | 左边操作数是变量的形式 | 左边操作数重新赋值之后的值作为表达式的值 | 有                     |

### 1.1 指数运算符

```js
2 ** 10;  // 2 的 10 次方
89 ** 3;  // 89 的 3 次方
```

### 1.2 可选链运算符

`?.` 用于调用对象的属性方法，尤其适合链式调用，调用过程中一旦得到 undefined，直接结束（短路），并以undefined作为整个表达式的值。

```js
对象?.属性名
对象?.属性名?.属性名

对象.方法名?.()
```

### 1.3 空值判断运算符

如果第一个操作数是 null 或者 undefined，取第二个操作数作为表达式的值；如果第一个操作数不是 null 或者 undefined，取第一个操作数作为表达式的值，且不再执行第二个操作数。

```js
0 ?? 100;   // 0
false ?? 100; // false
null ?? 100; // 100
undefined ?? 100;  // 100
```

 ### 1.4 逻辑赋值运算符

```js
x &&= y;  // 相当于 x = x && y;
x ||= y;  // 相当于 x = x || y;
x ??= y;  // 相当于 x = x ?? y;
```





## 2 symbol 类型

```
1. symbol 使用原始类型，使用 typeof 判断返回 symbol
2. 使用 Symbol() 函数创建 sybol 类型的数据，Symbol() 只能调用不能实例化
3. 每使用 Symbol() 创建一个数据，都是独一无二（具有对象特性）
3. symbol 类型的数据可以用作属性名 （属性名可以是字符串或者symbol数据）
```





## 3 Class 语法

### 3.1 使用 Class 定义类（定义构造函数）

**语法：**

```js
class Product {
    // 给实例设置属性  属性会直接添加到实例本身
    name = '汽车';
    price = 121.23;

    // 给实例设置方法  简写方式 这些方法会添加到实例的原型上
    buy(n) {
        console.log(`购买了${n}件${this.name}`);
    };

    addShopcar() {
        console.log('将' + this.name + '加入购物车！');
    };
}

// 实例化
new Product();
```

**特点：**

```
1. 使用 class 关键字定义的类本质上仍然是构造函数，使用 typeof 判断返回 function
2. 使用 class 关键字定义的类（构造函数）不能被调用，只能被实例化
3. 在 class 里面使用简写方式为设置的方法，会添加到实例的原型的
4. 在 class 里面只能定义属性和方法，如果有其他代码可以在方法内部写
```

### 3.2 类中定义构造器方法

**语法：**

```js
class Product {
    // 给实例设置属性
    name;
    price;

    // 构造器方法
    constructor(name, price) {
        this.name = name;
        this.price = Math.max(price, 100);
        this.num = Math.random();
    };
}
```

**特点：**

```
1. 构造器方法在实例化的时候会自动执行
2. 构造函数方法通常用于给属性进行赋初始值，构造器方法中的this指向实例
```

### 3.3 私有属性

**语法：**

```js
 // 定义类
class Product {
    // 给实例设置属性
    #name;
    #price;
    #num;

    // 构造器方法
    constructor(name, price) {
        this.#name = name;
        this.#price = Math.max(price, 100);
        this.#num = Math.random();
    };

    // 给实例设置方法
    buy(n) {
        console.log(`购买了${n}件${this.#name}`);
    };

    addShopcar() {
        console.log('将' + this.#name + '加入购物车！');
    };
}
```

**特点：**

```
1. 私有属性只能在类中的方法中通过this使用，在类的外部无法通过对象名使用
2. 私有属性需要在赋值前提前声明
```

### 3.4 静态方法

**语法：**

```js
  // 定义类
class Product {
    // 静态属性 静态属性语法还处提案借款
    static name = '小乐';

	// 静态属性
    static getInfo() {
        console.log('我是 Product 类中的静态方法');
    }
}

```

**特点：**

```
静态方法就是构造函数（类）自身的方法
```

### 3.4 继承

#### ① extends 关键字实现继承

**语法：**

```js
class 父类 {
    
}

class 子类 extends 父类 {
    
}
```

**特点：**

```
1. 一个父类可以被多个子类继承，一个子类只能继承一个父类
2. 子类的实例的原型会自动设置成父类的一个实例
   子类的实例的原型的 constructor 属性会自动指向子类
```

#### ② 方法和属性的重写

**语法：**

```js
class 父类 {
    name;
    price;
    say() {}
    eat() {}
}

class 子类 extends 父类 {
    name;
    say() {}
}

class 子类 extends 父类 {
  	constructor() {
        super();   // 将父类的构造器方法执行一次
    }
}
```

**特点：**

```
1. 子类中定义的属性和方法如果与父类中定义的属性或方法重名，子类中会重写继承下来的属性和方法
2. 如果子类中重写构造器方法，子类中构造器方法中必须先通过 super 关键字来调用父类的构造器方法，再进行其他操作
```

#### ③ super 关键字

super 关键字可以作为对象使用，也可以作为函数使用。

super 关键字作为对象使用，具有如下特点：

```
1. super 关键字写在使用 {} 声明对象时，里面简写形式的方法中
2. super 表示方法所属的对象的原型
```

super 关键字作为函数使用，具有如下特点：

```
1. 在子类的构造器方法中使用 super， 只能在构造器方法中使用，其他方法中不能使用。
2. 此时 super 表示父类的构造器方法， 子类若重写父类构造器方法，必须调用 super
3. 在子类的构造器方法中，要求 super 必须写在最前面
```

#### ④ 继承内置类（内置构造函数）

```js
 // 定义类 继承Array
class MyArray extends Array {
    #name;
    // 重写构造器方法
    constructor(name, ...args) {
        super(...args);
        this.#name = name;
    }
}
```



## 4 Set 和 Map

### 4.1 Set

#### ① Set 构造函数

Set 构造函数接收一个数组或者可遍历对象作为参数，该构造函数只能实例化，不能调用。

```js
const s1 = new Set();
const s2 = new Set([100,200,200,200,300,400,400,500, {name:'xiaole'},{name:'xiaole'}]);
const s3 = new Set('Hello World');
```

#### ② Set 的实例的属性方法

```
size
add()
delete()
has()
clear()
keys()
values()
entries()
forEach()
```

#### ③ Set 的应用

```
1. Set 中的成员不能重复，用来存储值不允许重复的集合
2. 实现数组的去重
```

### 4.2 WeakSet

WeakSet 结构与 Set 类似，也是不重复的值的集合。但是，它与 Set 有两个区别：

1）首先，WeakSet 的成员只能是对象类型的数据，而不能原始类型的数据。

2）WeakSet 不可遍历

#### ① WeakSet 构造函数

```js
 const ws = new WeakSet([new Number(100),msg, [10,20,30], {name:'小乐'}, msg]);
```

#### ② WeakSet 实例的方法

```
add()
delete()
has()
```

### 4.3 Map 

Map 结构类似于 Object 对象，有键值对组成的集合，不同的是， Map 中的键可以是任意类型的数据， 相比较 Object 对象中的键只能是字符串或symbol。

#### ① Map 构造函数

```js
 const arr = [10,20,30,40];
const user = {name:'小乐'};
const s = new Set(arr);

// 创建 Map 类型  Map 构造函数的参数必须是个二维数组
const m = new Map([
    [arr, arr],
    [user, '上海'],
    [s, ['司马姥姥', '欧阳姥姥']],
    ['address', '北京'],
    [100, 'helo world']
]);
```

#### ② Map 实例的属性方法

```
size

set()
get()
has()
delete()
clear()
keys()
values()
entries()
forEach()
```

### 4.4 WeakMap

WeakMap结构与Map结构类似，也是用于生成键值对的集合，WeakMap 与Map 的区别有两点：

1）WeakMap只接受对象类型的数据作为键名，不接受原始类型数据的值作为键名。

2）不可遍历。

#### ① WeakMap 构造函数

```js
const arr = [10,20,30,40];
const user = {name:'小乐'};
const s = new Set(arr);

// 创建 WeakMap 类型  WeakMap 构造函数的参数必须是个二维数组
const wm = new WeakMap([
    [arr, arr],
    [user, '上海'],
    [s, ['司马姥姥', '欧阳姥姥']],
    [{}, '北京'],
    [new Number(100), 'helo world']
]);
```

#### ② WeakMap 实例的方法

```
set()
get()
delete()
has()
```



## 5 遍历器 iterator

### 5.1 iterator 遍历器对象

**什么是遍历器对象？**

iterator(遍历器对象)是一种接口，为各种不同的数据提供统一的访问机制，任何数据只要部署了 iterator 接口就可以进行遍历操作。

**遍历器对象的特点？**

```
1. 每个遍历器都有一个 next() 方法
2. 遍历器对象内部存在一个指针，初始指向遍历器对象中的第一个数据，调用 next（） 会取出当前指针指向的数据，并且指针下移。
3. 每次调用 next() 方法，返回对象，对象中包含 value 属性 和 done 属性， value 属性就是当前指针指向的数据的值，done 属性是一个布尔值，表示是否结束遍历。
```

**得到遍历器对象的方法：**

```
数组实例： keys() values() entries()
Set实例： keys() values() entries()
Map实例： keys() values() entries()
...
```

### 5.2 iterable 可遍历对象

#### ① 什么是可遍历对象

```
1. 把部署了 iterator 接口（遍历器接口）的数据类型称为 iterable (可遍历对象)
2. iterator 接口部署在了可遍历对象的 Symbol.iterator 属性上，该属性是一个方法，这个方法返回一个遍历器对象
```

#### ② 内置的可遍历对象

```
Array 的实例
Set 的实例
Map 的实例
字符串
arguments
NodeList

HTMLCollection
....
```

#### ③  哪些情况会调用可遍历对象的遍历器接口

```
1. 使用 for of 遍历可遍历对象
2. 数组的解构赋值，所有可遍历对象都可以被解构
3. Array.from() 该方法可以把可遍历对象转为数组
4. 使用扩展运算符将可遍历对象分割为逗号隔开的参数序列
5. Set 构造函数的参数，要求是可遍历对象
6. WeakSet 构造函数的参数，要求是可遍历对象
7. Map 构造函数的参数，要求是可遍历对象
9. WeakMap 构造函数的参数，要求是可遍历对象
9. Promise.all() 的参数
10. Promise.race() 的参数
....
```

#### ④ 可遍历对象（iterable）和遍历器对象（iterator）的关系

```
1. 所有的遍历器对象都是可遍历的，可遍历对象不是遍历器对象。
2. 所有的可遍历对象都可以通过遍历器接口获取到与之对应的遍历器。
```

#### ⑤ 可遍历对象（iterable）和伪数组的关系

```
1. 伪数组指的是像数组一样具有索引结构，由多个数据组成的不是数组的数据类型
2. 可遍历对象指的是部署了遍历器接口的对象
3. 二者是完全不同的两个概念， String、Arguments、NodeList、HTMLCollection 既是伪数组又是可遍历对象； Set、Map 不是伪数组是可遍历对象。
```

### 5.3 for ... of

```
所有的可遍历对象（包括遍历器对象）都可以使用 for of 进行遍历。
```



## 6 生成器 generator

### 6.1 什么是生成器

```
1. 能够创建遍历器的函数称为生成器函数（generator）
2. 可遍历对象的遍历器接口（Symbol.iterator 属性的值）就是一个生成器函数
```

### 6.2 如何自定义生成器

```js
function* 生成器名字() {
    
}
```

### 6.3 yield 关键字

```js
function* 生成器名字（） {
	yield 值;
    yield 值;
    yield 值;
    yield 值;
    yield 值;
}
```

```
1. yield 关键字只能在生成器函数中使用
2. 调用生成器函数得到遍历器对象之后，调用遍历器对象的next()方法，得到yield 后面的数据，作为next()返回对象的value属性的值
3. 调用生成器函数的时候，只会得到一个遍历器对象，不会执行生成器中的语句； 只有调用遍历器对象的 next()方法的时候，才会执行生成器中的语句，执行到 yield 会停下来，再调用 next() ，再执行到下一次 yield
4. 生成器中的 return，可以结束遍历器的遍历
```

### 6.4 利用生成器给对象部署 iterator 接口（自定义可遍历对象）

```js
const obj = {
    name: '高小乐',
    age: 18,
    address: '上海',
    users: ['刘姥姥', '马姥姥', '欧阳姥姥', '司马姥姥'],
    say: ()=>{}
};


// 给 obj 部署一个遍历器接口
obj[Symbol.iterator] = function*(){
    for (let i in obj) {
        yield [i, this[i]];
    }
};
```



