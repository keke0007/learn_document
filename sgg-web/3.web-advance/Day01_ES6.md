# Day01 ES6+ 课堂笔记

官方地址：https://www.ecma-international.org/technical-committees/tc39/

铭哥教程：https://learn.fuming.site/front-end/es6/

阮一峰教程：https://es6.ruanyifeng.com/



## 1 let 和 const 关键字

### 1.1 let 关键字

**let 关键字的作用：** 

```\
用于创建变量，代替 var 关键字
```

**let 关键字声明的变量与 var 关键字声明的变量有哪些区别：**

```
1. let 创建的变量不能重复声明
2. let 创建的变量不会提升
3. let 创建的全局变量不是全局对象的属性
4. let 创建的变量除了具有全局作用域、函数内作用域，还具备块级作用域
```

### 1.2 const 关键字

**const 关键字的作用：**

```
用于创建变量，const 创建的变量值不能修改，const 创建的变量也可以称为常量
```

**const 声明的变量与 let 声明的变量的区别：**

```
let 声明的变量，不能重复声明，但可以修改值
const 声明的变量，不能重复声明，也不能修改值
```

**const 声明的变量也具备 let 声明的变量的 4 个特点：**

```
1. const 创建的变量不能重复声明
2. const 创建的变量不会提升
3. const 创建的全局变量不是全局对象的属性
4. const 创建的变量除了具有全局作用域、函数内作用域，还具备块级作用域
```

### 1.3 块级作用域

```
产生块级作用域的情况？
① 大括号中let声明的变量
② 分支结构中
② 循环结构中
```





## 2 解构赋值 （Destructuring assignment） 

```
1. 解构赋值是指按照一定模式，从数组和对象中提取值，对变量进行赋值，或函数传参
2. 等号的右边需要写数组或者对象（可以是任何形式，变量、直接量、表达式）
   等号的左边要求将变量写在数组或者或者对象结构中，并不是真正的数组或对象。
```

### 2.1 数组的解构赋值

```
数组解构赋值根据索引进行匹配
可以解构纯数组，也可以解构伪数组（arguments、string、arguments、NodeList 等）
```

```js
// 1. 声明多个变量并赋值
const num = Math.random();
let [v1,v2,v3,v4,v5] = [100,200,{name:'小乐',age:100},function(){alert('ok');}, num];

// 2. 同时修改多个变量的值
const data = ['司马姥姥', '欧阳姥姥', '东方姥姥', '西门姥姥'];
[v1,v2,v3,v4] = data;

// 3. 使用解构赋值 交换两个变量的值
[v1,v2] = [v2,v1];

// 4. 解构赋值用于函数传参  所谓传参就是实参赋值给形参
function func([name1,name2,name3]) {
    console.log(name1 + '和' + name2 + '以及' + name3 + '是好朋友！');
}
func(['小明', '小刚', '小红']);
func(data);


// 5. 两边的数组结构不完全一致
let [a1,a2,a3] = [100,200,300,400,500];
[a1,a2,a3] = ['刘姥姥', '马姥姥'];  // 重新赋值
console.log(a1);   // 刘姥姥
console.log(a2);   // 马姥姥
console.log(a3);   // undefiend


// 6. 解构赋值 左侧的变量可以指定默认值
// const [c1,c2,c3=250] = [100,200,300];
// const [c1,c2,c3=250] = [100,200];
const [c1,c2,c3=250] = [100];



// 7. 解构格式复杂的数组；
// 同一个数组可以进行多种形式的解构
var arr = [
    100,
    ['高小乐', 199],
    [
        100,
        [10, 20]
    ]
];
const [a, [b, c], [d, [e, f]]] = arr;
const [d1,d2,d3] = arr;


// 8. 伪数组也可以被解构
const msg = 'Hello 高小乐';
const btns = document.querySelectorAll('.btns button');
const [s1,s2,s3,s4] = msg;
const [btn1,btn2,btn3] = btns;
```

### 2.2 对象的解构赋值

```
对象解构赋值根据属性名进行匹配
一切皆对象，所有类型的数据都可以进行对象结构
```

```js
// 1. 对象的解构赋值 按照属性名进行匹配
let {name: username, address, num: age} = {name:'高小乐', address:[10,20,30,40], num:{name:'老乐',age:20}};

const user = {name:'Jack',address:'上海',length:1000};
const {name: u, address: a, num: b} = user;


// 2. 对象的结构赋值简写 左边： 属性名与变量名一致
// {num01:num01, num02:num02, num03:num03} = {num01:1000, num02:2000, num03:3000};
const {num01, num02, num03} = {num01:1000, num02:2000, num03:3000};


// 3. 对象的解构赋值 用于函数传参
function func({content,length,delay}) {
    console.log(content, length, delay);
}
const options = {content:'box', delay:2000, duration:3000};
func(options);


// 4. 对象解构赋值，可以设置默认值 
const {n1:n1, n2:n2=250, n3=350, n4} = {n1:100, n3:300};


// 5. 对于复杂一些对象 进行解构 （按照属性名进行解构， 变量位于属性值的位置）
const obj = {
    email: 'xiaole@qq.com',
    nums: [100, 200],
    prop: {
        content: 'Hello ES6'
    }
};
const {email, nums:[nu01, nu02], prop: {content}} = obj; 
const {email: em, nums: nus, prop:props} = obj;


// 6. 一切皆对象 对象的解构赋值可以解构一切数据
const {length, push, map} = [10,20,30,40,50];
const {length:len, indexOf, forEach} = 'Hello 小乐';
const {PI} = Math;
```



## 3 字符串新增特性

### 3.1 模板字符串

**什么是模板字符串？**

```
使用反引号表示的字符串
```

**相对于使用单引号或双引号定义的字符串，模板字符串有如下特点：**

```
1. 模板字符串中可以直接写换行
2. 模板字符串通过 ${} 可以直接插入变量后者表达式
```

### 3.2 字符串实例新增方法

**ES5 方法：**

```
charAt()
charCodeAt()
indexOf()
lastIndexOf()
slice()
substring()
substr()
toLowerCase()
toUpperCalse()
split()
search()
match()
replace()
```

**ES6 + 方法：**

```
repeat()		字符串重复，返回新字符串
includes()		判断是否包含某个值，返回布尔值
startsWith()	判断是否以某个值开始，返回布尔值
endsWith()		判断是否以某个值结尾，返回布尔值
trim()			去掉两端的空格
trimStart()		去掉前面的空格（ES2019）
trimEnd()		去掉后面的空格（ES2019）
padStart()		字符串填充，填充到前面（ES2017）
padEnd()		字符串填充，填充到后面（ES2017）
replaceAll()	替换字符串中指定内容，替换所有（ES2021）
```







## 4 数值新增特性

### 4.1 新增的二进制和八进制表示方式

```js

```

### 4.2 Number 构造函数本身新增的方法和属性

**ES5：**

```

```

**ES6+ (新)**

```

```

### 4.3 Math 新增方法

**ES5（旧）：**

```

```

**ES6+ (新)：**

```

```

### 4.4 指数运算符 ** （ES2016）

```js

```

### 4.5 新增原始数据类型 bigint （ES2020）

**bigint 数据类型：**

```

```

**bigint 类型的数据的表示方式：**

```js

```

**bigint 类型的数据的特点：**

```

```

**bigint 类型的数据的作用：**

```

```

### 4.6 数字间隔符（ES2021）

```js

```



















