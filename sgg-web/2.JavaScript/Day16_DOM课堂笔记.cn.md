# Day16 DOM 课堂笔记

## 1 回顾

```
1. 鼠标事件
   click
   dblclick
   contextmenu
   mousedown
   mouseup
   mousemove
   mouseenter mouseover
   mouseleave mouseout
   mousewheel DOMMouseScroll

2. 键盘事件
   keydown
   keyup
   keypress

3. 文档事件
   load
   DOMContentLoaded

4. 表单事件
   submit
   reset
   focus
   blur
   select
   input
   change

5. 图片事件
   load
   error

6. 过渡事件
   transitionstart
   transitionend
   transitionrun

7. 动画事件
   animationstart
   animationend
   animationiteration

8. 其他事件
   scroll
   resize
```



## 2 Event 对象

### 2.1 获取 Event 对象

```
给事件的回调函数设置形参，自动获取到事件对象
```

### 2.2 鼠标事件对象 MouseEvent 的属性和方法

```
button				按键值， 0表示左键，1表示滚轮键，2表示右键
offsetX / offsetY   获取鼠标在目标元素上的位置
clientX / clientY	获取鼠标在视口上的位置
pageX / pageY		获取鼠标在页面上的位置	
screenX / screenY	获取鼠标在屏幕上的位置
```

 ### 2.3 键盘事件对象 KeyborardEvent 的属性和方法

```
keyCode		获取按键对应的ascii码，是个数字
which		同keyCode
key			获取按键的名字，是个字符串
```

### 2.4 所有类型的事件对象都有的属性和方法

```
type		获取事件名
timeStamp	获取事件触发时的时间戳（从页面打开的那一刻开始算）
target		获取目标元素

stopPropagation()	阻止事件冒泡
preventDefault()	阻止浏览器默认行为
```

### 2.5 阻止事件冒泡

```js
事件对象.stopPropagation()
```

### 2.6  浏览器的默认行为

#### ① 浏览器有哪些默认行为

```
1. 点击超链接跳转
2. 点提交按钮会按回车键表单可以提交； 点重置按钮表单重置
3. 鼠标右键弹出系统菜单
4. 滚动滚轮页面滚动
...
```

#### ② 阻止浏览器默认行为

```
1. 事件对象.preventDefault()
2. 如果是第二种事件监听方式， return false 也可以阻止浏览器默认行为
```

### 2.7 事件委托（事件委派）

**事件委托的原理：**

```
1. 将事件监听到某个祖先元素
2. 在事件的回调函数进行判断， 只有目标元素是指定的元素才进行相应的操作
   可以使用 event.target 获取目标元素，类名、标签名都可以作为判断依据
```

**事件委托能解决什么问题？**

```
1. 让新增加的元素也具有事件
2. 如果需要给大量的元素监听事件，使用事件委托可以提升效率，减少内存
```



## 3 DOM 对象深入分析

### 3.1 元素对象的原型链关系(了解)

```
div元素对象 -> HTMLDivElement.prototype -> HTMlElement.prototype -> Element.prototype -> Node.prototype -> EventTarget.prototype -> Object.prototype
```

### 3.2 事件对象的原型链关系(了解)

以鼠标事件对象为例：

```
鼠标事件对象 -> MouseEvent.prototype -> UIEvent.prototype -> Event.prototype -> Object.prototype
```

### 3.3 HTMLCollection 和 NodeList 的区别

#### ① HTMLCollection 对象

```
1. 能够返回HTMLCollection 对象的属性和方法： getElementsByTagName()、getElementsByClassName()、children
2. HTMLCollection 对象的成员只能是元素类型对象 
3. 没有 forEach 方法
4. 是动态的集合，如果文档中新增了满足条件的元素，集合会自动更新
```

#### ② NodeList

```
1. 能够返回 NodeList 对象的属性和方法： querySelectorAll()、getElementsByName()、childNodes
2. NodeList 对象的成员可以是节点类型的对象（包括元素类型、document 等）
3. 具有 forEach 方法
4. 静态的集合
```







## 作业

```
1. 滑动效果轮播图
```









