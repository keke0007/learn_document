# Day2 ES6+ 课堂笔记

## 1 回顾

```
1. let 和 const
   1.1 let 声明的变量
       ① 不能重复声明
       ② 不能提升
       ③ 全局变量不会作为全局对象的属性
       ④ 具有块级作用域
   1.2 const 
       创建值不能修改的变量，称为常量
       ① 不能重复声明
       ② 不能提升
       ③ 全局变量不会作为全局对象的属性
       ④ 具有块级作用域
    1.3 块级作用域
 
 2. 解构赋值
    2.1 数组解构赋值
    2.2 对象解构赋值
    
 3. 字符串新增特性
    3.1 模板字符串
        ``
        ① 模板字符串直接写换行
        ② 字符串中插入变量、表达式非常方便 ${}
    3.2 字符串对象新增方法
        includes()
        startsWith()
        endsWith()
        padStart()
        padEnd()
        trim()
        trimStart()
        trimEnd()
        replaceAll()
```



## 2 数值新增特性

### 2.1 新增的二进制和八进制表示方式

```js
// 八进制形式表示数字
0o105;

// 二进制形式表示数字
0b1010;
```

### 2.2 Number 构造函数本身新增的方法和属性

**ES5：**

```
Number.MAX_VALUE;
Number.MIN_VALUE;
```

**ES6+ (新)**

```
Number.MAX_SAFE_INTEGER			读取最大的安全整数
Number.MIN_SAFE_INTEGER			读取最小的安全整数
Number.EPSILION					两个数字间最小差值，就是JS的数字精度			

Number.isNaN()					同全局对象的 isNaN()		
Number.isFinite()				同全局对象的 isFinite()	
Number.parseInt()			    同全局对象的 parseInt()	
Number.parsetFloat()		    同全局对象的 parsetFloat()
Number.isInteger()				判断参数是否是整数，返回布尔值
Number.isSafeInteger()			判断参数是否是安全整数，返回布尔值
```

### 2.3 Math 对象新增方法

**ES5（旧）：**

```
Math.PI
Math.abs()
Math.sqrt()
Math.pow()
Math.floor()
Math,ceil()
Math.round()
Math.random()
Math.max()
Math.min()
```

**ES6+ (新)：**

```
Math.trunc()	截取数字中的整数部分	
Mthn.sign()		参数是整数返回1，参数是负数返回-1，参数是0返回0	
Math.cbrt()	    返回参数的立方根		
Math.hypot()    返回所有参数的平方和的平方根			
```

### 2.4 新增原始数据类型 bigint （ES2020）

**bigint 数据类型：**

```
1. bigint 是一种数据类型，属于原始类型。
2. 使用 typeof 判断，返回 bigint。
```

**bigint 类型的数据的表示方式：**

```js
// 十进制表示
45n;

// 前面可以加 -，不允许加 + 
-1231231231239182923n;

// 二进制、八进制、十六进制表示
0b101n;
0o75n;
0xab1n;
```

**bigint 类型的数据的特点：**

```
1. bigint 类型的数据不能与其他类型进行数学运算符
2. bigint 类型的数据和 number 类型的数据可以互相转换
3. bitint 只能表示整数
```

**bigint 类型的数据的作用：**

```
bigint 可以表示的数字范围没有限制，而且计算精度是精确的！
```

### 2.5 数字间隔符（ES2021）

允许数值直接量中间包含不连续`_` ，以提高可读性。分隔符不能在尾部和头部，只能在数字之间，只允许一个下划线作为数字分隔符，不可连续。分隔符不影响数值的类型转换值，也无法在字符串转数值时被识别。 

```js
123_0000;
12_0000_0000;
12_434_900;
```







## 3 函数新增特性

### 3.1 新增的函数参数默认值的设置方式

```js
function 函数名(参数1，参数2=默认值) {
    
}
```

### 3.2 rest 参数

**什么是 rest 参数：**

```
1. rest 参数（形式为 ...变量名），用于在函数中获取实参，用来代替 arguments 对象。
2. rest 参数必须放在其他形参的后面
```

```js
function fn01(...args) {
    console.log(args);  // [100,200,250,'高小乐', true]
}
fn01(100,200,250,'高小乐', true);

function fn02(name, age, ...data) {
    console.log(name);
    console.log(age);
    console.log('rest参数：', data);  // ['司马姥姥', '欧阳姥姥', '爱新觉罗姥姥']
}

fn02('高小乐', 101, '司马姥姥', '欧阳姥姥', '爱新觉罗姥姥');
```

**rest 参数与 arguments 的区别：**

```
1. rest 参数得到是纯数组，arguments 获取的是伪数组
2. rest 参数的变量是自定义的，arguments 的名字是系统创建的
3. rest 参数获取没有形参与之对应的实参（剩下的实参）， arguments 获取所有的实参
```

### 3.3 箭头函数

箭头函数是一种声明函数的语法！

#### ① 箭头函数的语法

```js
// 1 使用箭头函数声明没有参数的函数
const fn01 = () => {};

// 2 使用箭头函数声明有参数的函数
const fn02 = (name, age) => {
    console.log(`我叫${name}，年龄${age}岁！`);
};

// 3 如果箭头函数的参数只有一个，可以省略小括号
const fn03 = num => {
    console.log(num * 2 + 100);
};

// 4 如果箭头函数的函数体只有一条语句，且是返回语句，可以省略大括号和return
/*
const fn04 = (n1,n2) => {
   return n1 * n2;
}
*/
const fn04 = (n1,n2) => n1 * n2;

// 5 大括号小括号都省略
/*
const fn05 = (item) => {
	return item * item;
}
*/
const fn05 = item => item * item;
```

#### ② 箭头函数的特点

```
1. 箭头函数中没有 arguments，可以使用 rest 参数
2. 箭头函数中没有 this，会使用上层作用域的 this，也无法通过 call和apply指定this。
3. 箭头函数不能用作构造函数，不能被 new
4. 箭头函数不能用作生成器函数
```

### 3.4 函数参数尾逗号（ES2017）

```js
function clownsEverywhere(param1,param2,) { 
}
clownsEverywhere('foo','bar',);
```

### 3.5 标签模板

函数调用和模板字符串结合使用，称为标签模板

```js
func``;   			 // 相当于 func([])
func`Hello World`;   // 相当于 func(['Hello World'])

const a = 100,b=200;
func`Hello ${a}World${b}`;  // 相当于 func(['Hello ', 'World', ''], 100, 200)
```



## 4 数组新增特性

### 4.1 扩展运算符

#### ① 把数组拆分为逗号分隔的参数序列

```
1. 用数组作为实参，给有多个形参的函数传参
2. 拷贝数组
3. 合并数组
4. 也可以将可遍历对象拆分为逗号分隔的参数序列，可以实现将伪数组转为纯数组
```

```js
// 将数组转为逗号分隔的参数序列
const nums = [1000,2000,3000,4000];
function func(n1,n2,n3,n4) {
}
func(nums);
func(...nums);   // 相当于 func(1000,2000,3000,4000)
func(...['刘姥姥', '司马姥姥', '欧阳姥姥']);   // 相当于 func('刘姥姥', '司马姥姥', '欧阳姥姥')

// 2 使用扩展运算符 复制数组
const arr01 = [100,200,300,400,500];
//const arr02 = arr01;      // arr01将地址传递给arr02，两个变量指向同一个数组
const arr02 = [...arr01];   // 使用[]创建新数组，将arr01转为参数序列放在新数组中

// 3 合并数组
const arr03 = [...nums, ...arr01, '刘姥姥'];

// 4. 也可以将可遍历对象转为逗号分隔的参数序列
// 将可遍历对象转为纯数组
const liBoxs = document.querySelectorAll('.news li');
const arr04 = [...liBoxs];
const arr05 = [...'Hello World'];
```

#### ② 把多个值合并到一个数组中（把参数序列变为数组）

```
1. rest 参数
2. 解构赋值中应用
```

```js
 // 1 rest 参数
function func(...args) {
    console.log(args);  // [100,200,300,400,500]
}
func(100,200,300,400,500);
console.log('');


// 2 解构赋值中的应用 
const [a1,a2,...a3] = ['刘姥姥','马姥姥', '司马姥姥', '欧阳姥姥', '爱新觉罗姥姥'];
console.log(a1);  // 刘姥姥
console.log(a2);  // 马姥姥
console.log(a3);  // ['司马姥姥', '欧阳姥姥', '爱新觉罗姥姥']
```

### 4.2 Array 构造函数本身新增的属性方法

```
Array.of()			创建新的数组，参数作为数组中的元素
Array.from()		将可遍历对象或伪数组转为纯数组
```

### 4.3 Array 的实例新增的属性方法

**ES5（旧方法）：**

```
修改器方法：
push()
pop()
shift()
unshift()
splice()
sort()
reverse()

访问器方法：
concat()
join()
slice()
forEach()
filter()
map()
every()
some()
reduce()
reduceRight()
indexOf()
lastIndexOf()
```

**ES6+（新方法）：**

```
find()				返回第一个满足条件的元素，参数是回调函数
findIndex()			返回第一个满足条件的元素的索引，参数是回调函数
fill()				使用固定的值替换到原来的元素值，修改器方法		
keys()				返回遍历器对象
values()			返回遍历器对象
entries()			返回遍历器对象
flat()				实现数组扁平化，参数用数字指定层级，可以用Infinity
flatMap()			先对数组map，再进行深度是1的flat，
includes()			判断是否包含指定的元素，返回布尔值
at()				根据索引读取元素，可以使用负数，负数表示倒数第几个
```



## 5 对象新增特性

### 5.1 属性简写

使用变量表示属性值，属性名和变量名是同名的，可以简写。

```js
const username = '高小乐', age = 19, address = '上海';
function say() {
    console.log('say function');
}

const user = {
    username,
    age,
    address,
    say
};
```

### 5.2 方法简写

```js
const obj = {
    say() {
        console.log('say');
    },
    drink() {
        console.log('drink');
    }
}
```

### 5.3 声明对象时用表达式作为属性名

```js
const prop = 'homeAddress';
const obj = {
    [10+10]: '高小乐',   // 属性名是 20
    [prop]: '北京',      // 属性名是 homeAddress
}
```

### 5.4 super 关键字

```
1. this 指向调用该方法的对象； super 指向方法所属的对象的原型
2. super 的指向与谁调用该方法无关，只与定义方法时所在的对象的有关
3. super 只能在简写的对象方法中使用，其他形式的方法一律报错！
```

```js
{
    drink() {
        super;
    }
    eat: function() {
        super; // 报错
    },
    say: ()=>{
        super; // 报错
    }
}
```

### 5.5 对象的扩展运算符 (ES2018)

#### ① 把对象拆分为逗号隔开的键值对序列

```js
 const user = {
     name: '高小乐',
     age: 45,
     address: '上海',
     say() {},
     drink() {}
 };

// 对象的拷贝
const user01 = {...user};  // 相当于 {name: '高小乐', age: 45, address: '上海', say:function(){}, drink:function(){}}


// 对象的合并
const user02 = {homeAddress:'北京', schollAddress:'广州', address:'纽约'};
const user03 = {...user, ...user02};
```

#### ② 把键值对序列合并到一个对象中

```js
// 用于对象的解构赋值
const {age,address,...data} = user03;
console.log(data);  
// {name: '高小乐', homeAddress: '北京', schollAddress: '广州', say: ƒ, drink: ƒ}drink: ƒ drink()homeAddress: "北京"name: "高小乐"say: ƒ say()schollAddress: "广州"[[Prototype]]: Object
```

### 5.6 Object 构造函数本身新增的方法

```
Object.is()		          		对两个参数进行判等，返回布尔值  
Object.assign()	
Object.keys()					返回由对象的属性名组成的数组
Object.values()					返回由对象的属性值组成的数组
Object.entries()				返回由对象的属性名和属性值组成的数组，是二维数组
Object.fromEntries()			是 entries()	的逆运算，返回对象
Object.getPrototypeOf()			返回对象的原型
Object.setPrototypeof() 		修改对象的原型
Object.getOwnPropertyDescriptors()	返回该对象所有属性的描述信息
Object.hasOwn()					判断属性是否属于对象自身
```

```js
Object.is(100, 100);  // true
Object.is(100, '100'); // false
Object.is(NaN, NaN);  // true
Object.is(+0, -0);   // false
+0 === -0;			 // true
```











