# Day04

## 1 ES6 回顾

```
1. let 和 const
2. 解构赋值
3. 字符串新增特性
4. 数值新增特性
   二进制和八进制表示方式
   Number的静态属性方法
   Math对象的属性方法
   数字分隔符
5. 函数新增特性
   参数默认值
   rest 参数
   箭头函数
   标签模板
   参数尾逗号
6. 数组新增特性
   扩展运算符
   Array的静态属性方法
   Array实例的属性方法
7. 对象新增特性
   属性简写、方法简写，表达式作为属性名
   super 关键字
   扩展运算符
   Object 的静态属性方法
8. class 语法
   class 定义类、 constructor 构造器方法
   私有属性
   静态方法
   class 继承、重写父类方法、super 
9. 新增运算符
10 新增对象类型
   Set、WeakSet、Map、WeakMap
11. 遍历器对象和可遍历对象
12. 生成器
```





## 2 ECMAScript 总结

### 2.1 ECMAScript 中的数据类型

**原始类型：** number、string、boolean、null、undefined、bigint、symbol 共 7 个。

**对象类型：** Array、Function、Object、Date、Set、WeakSet、Map、WeakMap ...

### 2.2 ECMAScript 中定义变量的方式

**共有 6 中定义变量的方式：**

```
var
function
let
const
class
import
```

**let、const、class、import 都是 ES6 新增的，具有如下特点：**

```
1. 不能重复声明
2. 不会提升
3. 全局变量不会作为全局对象的属性
4. 具有块级作用域
```

### 2.3 数组偏平化（拉平）

```js
// 第一种方式 使用递归函数遍历旧数组
function flatArray(arr) {
    // 创建新的空数组
    let newArr = [];
    // 使用循环结构遍历 arr
    for (var i = 0; i < arr.length; i ++) {
        // 判断当前的元素是否是数组
        if (arr[i] instanceof Array) {
            // 递归调用
            newArr = newArr.concat(flatArray(arr[i]));
        } else {
            // 将该元素添加到新数组中
            newArr.push(arr[i]);
        }
    }
    // 返回新数组
    return newArr;
}

// 第二种方式 缺点是里面的元素都会转为字符串
nums.join().split(',');

// 第三种方式 数组的flat方法
nums.flat(Infinity);
```

### 2.4 对象的浅拷贝

**数组的浅拷贝：**

```
1. [...arr] 扩展运算符
2. arr.concat() 返回新的数组
3. arr.slice()    返回新的数组，从头截取到尾
4. Array.from(arr) 返回新的数组
```

**对象的浅拷贝：**

```
1. {...obj} 扩展运算符
2. Object.assign({}, obj) 返回新对象，利用对象合并实现对象浅拷贝
```

### 2.5 对象的深拷贝

```js
// 1. 借助于JSON  无法拷贝方法，适合于纯数据对象
JSON.parse(JSON.stringify(obj));
```

```js
/**
 * 判断数据的类型
 * @params 要判断类型的数据
 * @returns string 数据的类型
*/
function getType(data) {
    const typeStr = Object.prototype.toString.call(data);
    return typeStr.slice(8, typeStr.length-1);
};

/**
 * 实现对象和数组的深拷贝
 * @params 要拷贝的数据
 * @returns 拷贝好的数据
*/
function deepClone(obj) {
    // 判断 obj 是 Object 类型还是 Array 类型
    let res;
    if (getType(obj) === 'Object') {
        res = {};
    } else if (getType(obj) === 'Array') {
        res = [];
    } else {
        return obj;
    }

    // 遍历 Object数据或者Array数据
    for (let i in obj) {
        // 将obj中中的成员添加到 res
        res[i] = deepClone(obj[i]);
    }

    // 返回res
    return res;
}
```





## 3 对象的属性特性

### 3.1 读取属性的特性

```
Object.getOwnPropertyDescriptor();		返回指定对象指定属性的描述特性
Object.getOwnPropertyDescriptors();		返回指定对象所有属性的描述特性
```

### 3.2 数据属性和访问器属性

对象的属性可以分为**数据属性**和**访问器属性**，它们的描述特性是不同的。

#### ① 数据属性

数据属性包含一个数据值的位置，我们定义对象时设置的属性都是**数据属性**。

数据属性有如下 4 个特性：

1）`Configurable`：可配置性，表示能否通过 delete 删除属性，能否修改属性的特性，能否把属性修改为访问器属性，默认值为 true。

2）`Enumerable`：可枚举性，表示能否通过 for-in 循环返回，默认值为 true。

3）`Writable`：可写性，表示能否修改属性的值，默认值为 true。

4）`Value`：值，这个属性的数据值。读取属性值的时候，从这个位置读；写入属性值的时候，把新值保存在这个位置。默认值为 undefined。

**可以通过下面方式设置属性的特性：**

```js
var person = {}; 
Object.defineProperty(person, "name", { 
 writable: false, 
 value: "Nicholas" 
});
```

#### ② 访问器属性

访问器属性不包含数据值；它们包含一对儿 getter 和 setter 函数。在读取访问器属性时，会调用 getter 函数，这个函数负责返回有效的值；在写入访问器属性时，会调用 setter 函数并传入新值，这个函数负责决定如何处理数据。

访问器属性有如下 4 个特性：

1）`Configurable`：表示能否通过 delete 删除属性从而重新定义属性，能否修改属性的特性，或者能否把属性修改为数据属性。

2）`Enumerable`：表示能否通过 for-in 循环返回属性。

3）`Get`：在读取属性时调用的函数。默认值为 undefined。

4）`Set`：在写入属性时调用的函数。默认值为 undefined。

**可以通过如下方式为对象设置访问器属性：**

```js
var book = { 
 _year: 2004, 
 edition: 1 
}; 
Object.defineProperty(book, "year", { 
 get: function(){ 
   return this._year; 
 }, 
 set: function(newValue){ 
   if (newValue > 2004) { 
     this._year = newValue; 
     this.edition += newValue - 2004; 
   } 
 } 
});
```

### 3.3 定义多个属性

`Object.defineProperties()` 这个方法可以通过描述符一次定义多个属性。

```js
var book = {}; 
Object.defineProperties(book, { 
 _year: { 
     value: 2004 
 }, 
 edition: { 
     value: 1 
 }, 
 year: { 
     get: function(){ 
         return this._year; 
     }, 
     set: function(newValue){ 
         if (newValue > 2004) { 
             this._year = newValue; 
             this.edition += newValue - 2004; 
         } 
     } 
 } 
});
```

`Object.create()` 可以在创建新对象的同时，给对象添加属性并设置特性：

```js
Object.create(Objec.prototype, {
   // foo 是一个常规数据属性
   foo: {
    writable: true,
    configurable: true,
    value: "hello",
  },
  // bar 是一个访问器属性
  bar: {
    configurable: false,
    get() {
      return 10;
    },
    set(value) {
      console.log("Setting `o.bar` to", value);
    },
});
```

### 3.4 Class 语法

```js
//定义类
class Person {
  //定义属性
  #firstName = '尼古拉斯';
  #lastName = '赵四';

  //当获取fullName属性值的时候 自动调用
  get fullName() {
    return this.#firstName + '·' + #this.lastName;
  }

  //当设置fullName属性值的时候 自动调用  接受一个参数，是要给fullName属性设置的新值
  set fullName(val) {
    this.#firstName = val.split('·')[0];
    this.#lastName = val.split('·')[1];
  }
}
```

### 3.5 对象的封闭和冻结

#### ① 封闭对象

 对象封闭之后，阻止添加新属性并将所有现有属性标记为不可配置。

```
Object.seal()		封闭对象
Object.isSealed()	判断对象是否被封闭
```

#### ② 冻结对象

对象冻结之后，阻止添加新属性并将所有现有属性标记为不可配置，不能修改已有属性的值，该对象的原型也不能被修改。 

```
Object.freeze()		冻结对象
Object.isFrozen()	判断对象是否被冻结
```

