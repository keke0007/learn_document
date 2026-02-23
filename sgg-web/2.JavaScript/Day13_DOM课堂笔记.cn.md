# Day13 DOM 课堂笔记

## 1 回顾 

```
1. 节点
   document、元素、属性、文本、注释

2. 获取元素
   ① 通过ID  document.getElementById()
   ② 通过标签名  document.getElementsByTagName() / 元素..getElementsByTagName()
   ③ 通过类名
   ③ 通过name属性
   ⑤ 使用CSS选择器  querySelector() / querySelectorAll();  文档、元素都有这两个方法
   ④ 快捷方法 document.documentElement、document.body、body.head、document.all

3. 文档结构 根据关系获取元素
   children
   firstElementChild
   lastElementChild
   parentElement
   previousElementSibling
   nextElementSibling

4. 元素的属性操作
   4.1 读写内置属性  元素对象.属性名
   4.2 元素对象.setAttribute() / 元素对象.getAttribute()
   4.3 读写data-形式的自定义属性  元素对象.dataset.属性名
   
5. 元素的样式操作
   5.1 读写行内样式  元素对象.style.属性名
   5.2 读取计算样式  getComputedStyle(元素对象).属性名
   5.2 操作类名
       元素对象.className
       元素对象.classList   add() remove() toggle() contains()
 
```



## 2 读写元素的文本内容（可读可写）

```
元素对象.innerHTML		读写内部的html代码和文本内容
元素对象.outerHTML		读写包括元素自身在内的html代码和文本内容
元素对象.innerText		读写内部的文本内容，会剔除掉标签
元素对象.textContent	读写内部的文本内容，会剔除掉标签，读取的值保留空格
```



## 3 读取元素的尺寸（只读）

```
元素对象.offfsetWidth / 元素对象.offfsetHeight	获取元素的总宽总高
元素对象.clientWidth / 元素对象.clientHeight    获取元素宽高，内容+内边距
元素对象.scrollWidth / 元素对象.scrollHeight	获取元素宽高，client加上溢出的部分

元素对象.getBoundingClientRect() 返回对象，对象包含元素的位置和尺寸信心，对象有如下属性：
元素对象.getBoundingClientRect().width	 同offsetWidth
元素对象.getBoundingClientRect().height  同offsetHeihgt
```

**获取视口的尺寸：**

```js
// 会包括滚动条本身的宽度
window.innerWidth
window.innerHeight

// 不会包括滚动条本身的宽度
document.documentElenment.clientWidth
document.documentElenment.clientHeight
```



## 4 读取元素的位置 （只读）

```
元素对象.offsetLeft / 元素对象.offsetTop	获取元素在第一个定位的祖先元素上的位置（祖先元素没有定位的，										   参照页面）
元素对象.clientLeft / 元素对象.clientTop    获取元素的左边框宽度、上边框宽度

元素对象.getBoundingClientRect() 返回对象，对象包含元素的位置和尺寸信心，对象有如下属性：
    left		读取元素在视口上到位置x坐标
    top			读取元素在视口上到位置y坐标
    x			同 left
    y			共 top
    right		元素右边的x坐标
    bottom		元素底部的y坐标
```



## 5 读写元素中内容滚动的位置（可读可写）

```
scrollLeft		内容在元素中向左滚动的距离
scrollTop		内容在元素中向上滚动的距离
```

> **注意：** 需要设置元素 overflow 的值不是 visible.

**读写整个页面在视口中滚动的位置：**

```js
document.documentElement.scrollLeft
document.documentElement.scrollTop
```





## 6 元素节点的添加/删除/替换/克隆

### 6.1 创建元素节点

```js
document.createElement('标签名');
```

### 6.2 添加子节点

```js
父元素.appendChild(新元素);
父元素.insertBefore(新元素， 旧元素);
```

### 6.3 删除子节点

```js
父元素.removeChild(要删除元素);
```

### 6.4 替换子节点

```js
父元素.replaceChild(新元素， 旧元素);
```

### 6.5 克隆节点

```js
元素.cloneNode(true)  返回克隆后的元素 参数设置为true表示元素和里面的内容一起克隆
```



## 7 document 对象

document 表示整个文档，document 是 html 元素的父节点，document 是 window 的一个属性，document 对象具有如下属性方法：

```
documentElement		获取html根元素
body				获取body元素
head				获取head元素
all					获取到所有的元素组成的集合
title				读写标题栏标题
cookie				读写cookie信息

createElement()		
getElementById()
getElementsByTagName()
getElementsByClassName()
getElementsByName()
querySelector()
querySelectorAll()
```





## 作业

```
1. 随机点名器
2. 选项卡效果
3. 优化图片延迟加载
4. 实现图片无缝滚动
```







