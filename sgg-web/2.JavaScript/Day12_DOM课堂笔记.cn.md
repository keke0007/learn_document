# Day12 JavaScript DOM 课堂笔记

## 回顾 BOM 

浏览器对象模型

```
1. window
   name
   innerWidth
   innerHeight
   alert()
   confirm()
   prompt()
   open()
   close()
   scrollTo()
   scrollBy()
   setInterval()
   clearInterval()
   setTimeout()
   clearTimeout()

2. location
   href
   protocol
   hostname
   port
   host
   pathname
   hash
   search
   reload()
   assign()
   replace()

3. history
   length
   back()
   forward()
   go()

4. navigator
   userAgent

5. screen
   width
   height
```



## 1 DOM 介绍

**<font color="red">MDN 文档对象模型手册</font>：**https://developer.mozilla.org/zh-CN/docs/Web/API/Document_Object_Model

### 1.1 五大节点(Node)类型 

```
document 	文档类型的节点
element		元素类型的节点
attribute	属性类型的节点
text		文本类型的节点
comment		注释类型的节点
```

### 1.2 节点的属性

所有的节点对象具有以下三个属性：

```
nodeName		节点名称，元素节点的节点名称是标签名
nodeValue		节点值
nodeType		节点类型 文档:9; 元素：1； 属性：2； 文本：3；  注释：8
```



## 2 获取元素

#### ① 通过 ID 名

```js
document.getElementById('ID名')
```

```
1. 返回符合条件的元素对象
2. 如果获取不到元素，返回 null
```

#### ② 通过标签名

```js
// 从文档中获取所有指定标签名的元素
document.getElementsByTagName('标签名');

// 从某个元素的后代中获取所有指定标签名的元素
元素.getElementsByTagName('标签名');
```

```
1. 返回的是一个 HTMLCollection 对象，是一个伪数组，里面的成员是元素对象
2. 如果没有符合条件的元素，同样返回 HTMLCollection 对象，是个空集合
```

#### ③ 通过类名（了解，IE8 + 支持）

```js
// 从文档中获取所有指定类名的元素
document.getElementsByClassName('标签名');

// 从某个元素的后代中获取所有指定类名的元素
元素.getElementsByClassName('标签名');
```

```
1. 返回的是一个 HTMLCollection 对象，是一个伪数组，里面的成员是元素对象
2. 如果没有符合条件的元素，同样返回 HTMLCollection 对象，是个空集合
```

#### ④ 通过 name 属性值 （了解）

```js
// 只要 document 才有 getElementsByName 方法
document.getElementsByName('name属性值');
```

```
1. 返回的是一个 NodeList 对象，是一个伪数组，里面的成员是元素对象
2. 如果没有符合条件的元素，同样返回 NodeList 对象，是个空集合
```

#### ⑤ 使用 CSS 选择器获取元素 (推荐)

```js
// 从整个文档中获取
document.querySelector('CSS选择器')
document.querySelectorAll('CSS选择器')

// 从指定元素的后代中获取
元素.querySelector('CSS选择器')
元素.querySelectorAll('CSS选择器')
```

```
1. querySelector() 返回符合选择器条件的第一个元素，没有符合条件的元素返回 null
2. querySelectorAll() 返回所有符合选择器条件的元素组成的集合，是 NodeList 对象，是伪数组。
```

#### ⑥ 快捷方式获取元素

```js
document.body				获取到body元素
document.head				获取到head元素
document.documentElement	获取到html元素（根元素）
document.all				获取本文档中所有的元素组成的集合
```

**使用 document.all 判断是否是 IE 浏览器：**

```js
if (document.all) {
     // IE10以及以下的浏览器
     document.write('您使用的是IE浏览器！');
 } else {
     // IE11、EDGE、Chrome、Firefox、Safari 等等
     document.write('您使用的不是IE浏览器！');
 }
```



## 3 文档结构（根据元素关系获取元素）

```
children				获取所有的子元素，是一个 HTMLCollection 类型的对象
firstElementChild		获取第一个子元素
lastElementChild		获取最后一个子元素

parentElement			获取父元素

previousElementSibling	获取紧邻的前面的一个兄弟元素
nextElementSibling		获取紧邻的后面的一个兄弟元素
```



## 4 元素的属性操作

### 4.1 读写内置属性

```
元素对象.属性名;
元素对象.属性名 = 新值;
```

```js
1. 标准中所规定的标签上的属性会映射成js元素对象上的属性，称为内置属性
2. html标签中不需要设置值的属性，对应的js元素对象的属性值是布尔值
```

### 4.2 读写设置在标签代码上的属性

```js
元素对象.getAttribute('属性名');		// 读取设置在标签代码上的属性（不区分内置属性和自定义属性）
元素对象.setAttribute('属性名', '值'); // 将属性值设置在标签的文档结构中，如果不存在属性会添加
```

### 4.3 `data-*` 形式的自定义属性

```html
<img data-loadpic="" data-home-address="">
```

```js
imgEle.dataset.loadpic;  // 可读可写
imgEle.dataset.homeAddress; // 可读可写 自动转为小驼峰
```



## 5 元素的样式的操作

### 5.1 读写行内样式

```js
// 只能读取设置在行内的样式
元素对象.style.属性名;
元素对象.style.color;
元素对象.style.backgroundColor;

// 设置样式 如果行内设置过修改，如果行内没有添加
元素对象.style.属性名 = 新值;
元素对象.style.color = '#f00';
元素对象.style.backgroundColor = '#099';
```

### 5.2 读取计算样式

**计算样式：** 最终作用在元素上的样式，即使没有设置也有默认样式。只能读取不能设置。

```js
// 返回由计算样式组成的对象
getComputedStyle(元素);

var computedStyle = getComputedStyle(box);
console.log(computedStyle.background);
console.log(computedStyle.backgroundColor);

console.log(getComputedStyle(box).backgroundColor);
console.log(getComputedStyle(box).fontSize);
```

### 5.3 操作元素的类名

#### ① className

```
元素对象.className 对应标签上的 class 属性
```

#### ② classList

```
元素对象.classList 可以得到管理类名的对象，该对象有如下方法：
add()		添加一个类名
remove()    删除一个类名
contains()	判断是否包含指定的类名
toggle()	切换类名，如果存在类名删除，如果没有类名添加
```



## 作业

```
1. 实现反选
2. 复选框全选
3. 春节倒计时
```







