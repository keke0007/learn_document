# Day10 JavaScript  内置对象（内置构造函数）

内置对象的在线文档（MDN）：

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects

## 1 Boolean

```js
// 1. 直接量方式
true;
false;

// 2. Boolean 函数方式
Boolean(true);
Boolean(false);

// 3. Boolan 构造函数方式  默认对象状态
new Boolean(true);
new Boolean(false);
```



## 2 Number

#### ① 实例的属性和方法

```
toFixed()	返回指定小数位数的数字，不写参数返回整数（四舍五入）
toString()  返回指定进制形式的字符串，参数2~36
```

#### ② 构造函数本身的属性和方法

``` 
Number.MAX_VALUE	js中可以表示的最大的数字
Number.MIN_VALUE    js中可以表示的最小的正数
```



## 3 String

#### ① 实例的属性和方法

```
length			读取字符串长度，字符个数

charAt()		返回指定位置的字符，参数是指定的索引
indexOf()		返回指定的内容在字符串中第一次出现的位置（索引），参数就是指定的内容
lastIndexOf()   返回指定的内容在字符串中最后一次出现的位置（索引），参数就是指定的内容
slice()			截取字符串并返回，参数指定开始位置和结束位置（结束位置字符不包括在内），不设置第二个参数截				 取到最后
substring()		截取字符串并返回，规则同上
substr()		截取字符串并返回，参数指定开始位置和截取长度，不设置第二个参数截取到最后
split()			分隔字符串返回数组，参数指定分隔符
toUpperCase()	将字符串所有字母转为大写并返回，不需要参数
toLowerCase()   将字符串所有字母转为小写并返回，不需要参数
chatCodeAt()	返回指定位置的字符的unicode编码，，参数是指定的索引
```

#### ② 构造函数本身的属性和方法

```
String.fromCharCode()		返回指定unicode编码对应的字符，参数指定unicode编码是个数字
```



## 4 Math

Math 就是系统定义好的对象，是一个 Object 的实例

```
Math.PI			圆周率
Math.abs()		返回绝对值
Math.pow()		返回次方数，两个参数
Math.sqrt()		返回平方根
Math.floor()	返回整数，向下取整
Math.ceil()		返回整数，向上取整
Math.round()	返回整数，四舍五入
Math.max()		返回参数中最大的，参数数量可以是任意个
Math.min()		返回参数中最小的，参数数量可以是任意个
Math.random()	返回一个随机数，范围是0到1,0可能会被取到，1不可能。
```

**取随机整数： 0 ~ n**

```js
Math.floor(Math.random() * (n+1))
```

**取随机整数： m ~ n**

```js
Math.floor(Math.random() * (n-m+1)) + m;
```



## 5 Date

#### ① 实例化日期时间对象

```js
// 实例化日期时间对象  不写参数包含当前的日期时间
var d1 = new Date();

// 实例化日期时间对象  指定日期时间
var d2 = new Date('December 17, 1995 03:24:00');

// 实例化日期时间对象  指定日期时间
var d3 = new Date('2008-09-12T10:06:45');

// 实例化日期时间对象  指定日期时间
var d4 = new Date(1949,9,1,10,0,12);
var d5 = new Date(1997,6);
var d6 = new Date(1997,6,10,8);

// 实例化日期对象 指定日期时间 参数是unix时间戳(1970.1.1 00:00:00 距离目标日期的毫秒数)
var d7 = new Date(360000000000);
```

#### ② 实例的属性和方法

```
getFullYear()		获取年，公元纪年
getMonth()			获取月，月的取值0~11
getDate()			获取每月第几天
getDay()			获取每周第几天
getHours()			获取时
getMinutes()		获取分
getSeconds()		获取秒
getMilliseconds()	获取毫秒
getUTC...			获取零时区的年月日时分秒...
getTime()			获取时间戳，从1970-01-01 00:00:00 距离日期时间对象的毫秒数

set...				设置日期时间
setUTC...			设置零时区日期时间
setTime()			设置时间戳
```

#### ③ 构造函数本身的属性和方法

```
Date.now()			获取此时此刻的时间戳，没有参数
Date.UTC()			获取指定日期的时间戳，用2~6个数字表示年月日时间秒
```



## 6 Array

#### ① 实例的属性

```
length			获取数组的长度，元素的个数
```

#### ② 实例的访问器方法

执行完方法后，结算结果以返回值给出，而调用方法的对象本身不会被修改

```
concat()		将多个数组连接成一个，返回连接好的数组，参数是数组，可以是任意个
slice()			截取数组中一部分返回新数组，指定开始位置和结束位置
join()			将数组中所有的元素合并成一个字符串并返回，参数指定分隔符，默认是逗号
indexOf()		返回指定元素在数组第一次出现的位置，不存在返回-1
lastIndexOf()   返回指定元素在数组最后一次出现的位置，不存在返回-1
forEach()		遍历数组，没有返回值
filter()		返回由复合条件的元素组成的新数组，如果回调函数返回true，与之对应的元素表示复合条件
map()			返回由回调函数的返回值组成的新数组，新数组长度与原数组一致
every()			只有每个回调函数都返回true，every方法才返回true，否则every方法返回true
some()			只有有一个回调函数返回true，some方法就返回true		
reduce()		用于累计运算，最后一次回调函数的返回值作为reduce方法的返回值
reduceRight()	reduce()从左到右遍历，reduceRight从右到左遍历
```

#### ③ 实例的修改器方法

执行完方法后，调用该方法的对象本身会被修改，修改器方式是数组所独有的

```
push()			在数组的后面添加元素，返回添加元素后数组的长度
unshift()		在数组的前面添加元素，返回添加元素后数组的长度
pop()			删除最后一个元素，返回被删除的元素
shift()			删除第一元素，返回被删除的元素
splice()		替换指定位置指定数量元素，返回数组，数组中被删除掉的元素
sort()			数组排序，返回排好序的数组
reverse()		翻转数组，返回翻转好的数组
```













## 作业

```
1. 封装函数
   'get-element-by-id' 转为 'getElementById'
   'set-name-by-class-name' 转为 'setNameByClassName'
   
2. 封装函数
   实现翻转字符串，  请用上数组的 reverse 方法

3. 封装函数，参数是数组，返回值是随机取出来的元素
   定义数组 ['刘姥姥', '牛姥姥', '司马姥姥', '欧阳姥姥', '独孤姥姥', '令狐姥姥', '东方姥姥'];
   随机取出数组中的元素


4. 输出当前日期时间，时间格式如下 “2021-03-04 19:02:56” （字符串拼接）

```











