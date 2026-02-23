Day15 DOM 课堂笔记

## 1 回顾

```
1 HTML DOM
 1.1 表单
 1.2 表格
 
2. 事件
2.1 监听事件三种方式
    ① 把事件作为HTML标签的属性
    ② 把事件作为元素对象的属性（方法）
    ③ 使用 addEventListener
2.2 解除事件的监听
    ① 第一种和第二种  元素对象.on事件名 = null;
    ② 第三种方式 元素对象.removeEventListener()
2.3 事件流
    捕获阶段
    目标阶段
    冒泡阶段
2.4 事件回调函数中的this
    指向监听事件的元素
```



## 2 常用事件总结

### 2.1 鼠标事件

```
click			单击				
dblclick		双击
contextmenu		右击，菜单事件		
mousedown		鼠标按键按下		
mouseup			鼠标按键抬起
mousemove		鼠标在元素上移动		
mouseover		鼠标进入元素
mouseout		鼠标离开元素
mouseenter		鼠标进入元素，用来代替 mouseover，后代元素不会冒泡		
mouseleave		鼠标离开元素，用来代替 mouseout，后代元素不会冒泡		
mousewheel		滚轮事件，用于	Chrome、Safari、Opear、Edge	
DOMMouseScroll	滚轮事件，用于 Firefox，只能通过 addEventListener 监听事件
```

**鼠标按键按下和抬起事件如何获取按的是哪个键？**

```
事件对象有button属性，值规则如下：
0	左键
1   滚轮键
2   右键
```

**鼠标移动事件中如何获取鼠标位置？**

```
通过事件对象获取鼠标光标的位置，具有如下属性：
offsetX / offsetY		获取鼠标在目标元素上的位置
clientX / clientY		获取鼠标在视口上的位置
pageX / pageY			获取鼠标在页面上的位置
screenX / screenY		获取鼠标在屏幕上的位置
```

**滚轮滚动事件兼容性处理：**

```js
// Chrome、Safari、Opear、IE
window.onmousewheel = wheelScrollFn;

// Firefox 浏览器
window.addEventListener('DOMMouseScroll', wheelScrollFn);

// 定义滚轮事件的回调函数
function wheelScrollFn(event) {
    if (event.wheelDelta) {
        // chrome、safari、ie 等
        if (event.wheelDelta < 0) {
            console.log('滚轮向下滚');
        } else {
            console.log('滚轮向上滚');
        }
    } else if (event.detail) {
        // firefox 浏览器
        if (event.detail > 0) {
            console.log('滚轮向下滚');
        } else {
            console.log('滚轮向上滚');
        }
    }
}
```

### 2.2 键盘事件

```
keydown		键盘按键按下
keyup		键盘按键抬起
keypress	键盘按键按下
```

**keypress 和 keydown 的区别：**

```
keypress：
控制按键不能触发，只有可输入字符按键才能触发
可以区分字母按键的大小写

keydown：
所有的按键按下都可以触发
无法区分字母按键的大小写
```

**哪些元素可以监听键盘事件？**

```
1. 表单控件元素，获取焦点之后按键盘
2. document对象
```

**如何获取按的是哪个键？**

```js
通过事件对象获取，键盘事件对象具有如下属性：
keyCode		获取所按按键对应的ascii码，是个数字
which		同keyCode
key			获取所按按键的名字，是个字符串
```

### 2.3 文档事件

```
load				文档加载完毕，需要监听到window或者body元素
DOMContentLoaded	文档加载完毕，需要监听到window或者body元素				
```

**load 事件与 DOMContentLoaded 事件的区别：**

```
load： 文档中所有的一切加载完毕，包括引用的外部文件
DOMContentLoaded： 文档中元素加载完毕，不包括引用的外部文件，只能使用addEventListener监听事件
```

### 2.4 表单事件

```
submit		表单提交的时候，需要监听到form元素上  
reset		表单重置的时候，需要监听到form元素上     
blur		失去焦点的时候，需要监听到表单控件元素			   
focus		获取焦点的时候，需要监听到表单控件元素		
select		里面的文字内容被选中的时候，需要监听到输入框或文本域元素上  
input		输入框内容改变，需要监听到输入框或文本域元素上     
change		监听到输入框元素，输入的内容改变且失去焦点
            监听到选择框元素，一改变就触发
```

### 2.5 图片事件

```
load		图片加载完毕
error		图片加载失败
```

### 2.6 过渡事件

```
transitionstart		过渡开始事件，过渡延迟之后触发
transitionrun 		过渡开始事件，过渡延迟之前触发
transitionend		过渡结束事件
```

### 2.7 动画事件

```
animationstart		动画开始事件，延迟之后触发
animationend		动画结束之后
animationiteration	动画每执行一次就触发一次
```

### 2.8 其他事件

```
scroll		滚动事件，需要监听给内容可以滚动的元素或者window
resize		视口尺寸改变事件， 需要监听给window
```





## 作业

```
1. 键盘事件控制元素位置移动
2. 轮播图
```











