# Day16 CSS3 课堂笔记

## 1 回顾 

```
1. 多列布局
   1.1 设置给多列容器（包裹元素）
       column-count
       column-width
       columns
       column-gap
       column-rule-style
       column-rule-color
       column-rule-width
       column-rule
   1.2 设置给子元素
       column-span
       -webkit-column-break-before
       -webkit-column-break-after
       -webkit-column-break-inside
       
 2 伸缩盒布局（弹性盒、Flex）
   2.1 伸缩容器和伸缩项目
   2.2 主轴方向和换行方式
   2.3 主轴对齐
   2.4 侧轴对齐
       一行
       多行
   2.5 伸缩项目伸缩性
   2.6 伸缩项目排序
   2.7 伸缩项目单独设置侧轴对齐
   2.8 属性总结
       设置给伸缩容器：
       	display
       	flex-direction
       	flex-wrap
       	flex-flow
       	justify-content
       	align-items
       	align-content
       设置给伸缩项目
        flex-basis
        flex-grow
        flex-shrink
        flex: grow shrink basis
        order
        align-self
```



## 2 媒体查询和响应式布局

### 2.1 视口 viewport

#### ① 什么是视口

```
1. 视口是浏览器的可视区域
2. 视口是根元素的包含块
```

#### ② 移动端视口和PC端视口

```
PC端视口： 视口宽度默认等于屏幕宽度，不会进行缩放
移动端视口： 默认会进行缩放，视口宽度会缩放为980px
```

#### ③ 完美视口设置

**什么是完美视口：** 

```
视口宽度等于屏幕宽度不进行缩放就是完美视口！
```

**如何设置为完美视口：**

```html
PC端浏览器视口默认就是完美视口
移动端浏览器可以在网页中设置meta元信息实现完美视口
```

```html
<meta name="viewport" contnet="width=device-width,initical-scale=1.0">
```

### 2.2 媒体查询基本语法

#### ① 媒体类型

```
all
screen
print
speech	
```

```css
@media screen {
     h1 {
         text-align: center;
     }

     body {
         background: #099;
     }
}
```

#### ② 媒体特性

```
width			视口宽度
max-width		最大视口宽度
min-width		最小视口宽度

device-width		屏幕宽度
max-device-width	最大屏幕宽度
min-device-width	最小屏幕宽度
```

```css
@media (device-width:800px) {
      body {
          background: #900;
      }
}
```

#### ③ 运算符

```
only		仅仅，用于媒体特性
not			否定，用于媒体特性
and			并且
,			或者
```

```css
@media (min-width:600px) and (max-width:800px) {
     body {
         background: #900;
     }
}

@media (max-width:400px),(min-width:1000px) {
    body {
        background: #009;
    }
}
```

### 2.3 媒体查询在 CSS 中使用

#### ① 第一种使用方式： 媒体查询与CSS代码写在一起(推荐使用)

```css
body {
    margin: 0;
    background: #333;
}

h1 {
    text-align: center;
    font-size: 4em;
    color: #fff;
}

/* 视口宽度大于等于 1000px */
@media (min-width: 1000px) {
    body {
        background: #090;
    }
}

@media (min-width: 1000px) {
    h1 {
        text-decoration: wavy underline;
    }
}
```

#### ② 第二种使用方式:  link 标签的 media 属性 (不推荐)

```html
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="min1000.css" media="(min-width:1000px)">
```

### 2.4 响应式布局

#### ① 阈值（断点）

**常见方案一：**

```
640px
1080px
```

**常见方案二：**

```
768px
992px
1200px
```

#### ② 移动优先方案（媒体查询的设置）

```css
.container {
    width: 100%;
    height: 200px;
    background: #900;
}

/* 小屏幕 */
@media (min-width:768px) {
    .container {
        margin-left: auto;
        margin-right: auto;
        width: 750px;
        background: #090;
    }
}

/* 中等屏幕 */
@media (min-width: 992px) {
    .container {
        width: 970px;
        background: #099;
    }
}

/* 大屏幕 */
@media (min-width: 1200px) {
    .container {
        width: 1170px;
        background: #990;
    }
}
```

#### ③ 响应式图片

**方案一： 多个图片控制隐藏显示**

```css
<!--html样式-->
.small-logo {
     display: block;
}

.middle-logo {
    display: none;
}

.large-logo {
    display: none;
}

@media (min-width: 640px) {
     .small-logo {
         display: none;
     }

     .middle-logo {
         display: block;
     }

     .large-logo {
         display: none;
     }
}

@media (min-width: 1024px) {
    .small-logo {
        display: none;
    }

    .middle-logo {
        display: none;
    }

    .large-logo {
        display: block;
    }
}
```

**方案二： 背景图**

```css
/*css样式*/
.logo {        
    background-image: url(./images/Brand-S.png);
}

@media (min-width: 640px) {
    .logo {
        background-image: url(./images/Brand-M.png);
    }
}

@media (min-width: 1024px) {
     .logo {
         background-image: url(./images/Brand-L.png);
     }
}

```

**方案三 使用 picture 标签**

```html
<!-- （html样式）哪个source先满足条件就先加载哪个图片，后面的将不再加载 -->
<picture>
    <source srcset="./images/Banner-S.png" media="(max-width:640px)">
    <source srcset="./images/Banner-M.png" media="(max-width:1024px)">
    <img src="./images/Banner-L.png" alt="">
</picture>
```

**方案四 使用 img 标签的 srcset 属性**

```html
<img srcset="./images/Banner-S.png 640w,
             ./images/Banner-M.png 1024w, 
             ./images/Banner-L.png 1440w"
     src="./images/Banner-L.png" 
     alt="">
注：图片地址后面的长度是图片的宽度，不是视口的宽度，父元素此时默认100%，与视口同宽，视口小于640时，选择小图，以此类推。  src="./images/Banner-L.png"表示默认情况下（即大于1440时），也用大图，防止用户屏幕过大。
```

#### ④ 响应式导航





## 3 BFC

### 3.1 什么是 BFC

**Block Formatting Context** 简称 **BFC**，中文翻译为 **块级格式上下文**。

#### ① W3C 中对 BFC 的定义

Floats, absolutely positioned elements, block containers (such as inline-blocks, table-cells, and table-captions) that are not block boxes, and block boxes with 'overflow' other than 'visible' (except when that value has been propagated to the viewport) establish new block formatting contexts for their contents.

> **译文：**
>
> 浮动、绝对定位元素、不是块盒子的块容器(如inline-blocks、table-cells和table-captions)，以及`overflow`属性的值除`visible`以外的块盒(除非该值已传播到视口)，将为其内容建立新的块格式化上下文。

https://www.w3.org/TR/CSS22/visuren.html#block-formatting

#### ② MDN 上对 BFC 的定义

A **block formatting context** is a part of a visual CSS rendering of a web page. It's the region in which the layout of block boxes occurs and in which floats interact with other elements.

> **译文：**
>
> **块格式化上下文（Block Formatting Context，BFC）** 是Web页面的可视CSS渲染的一部分，是块盒子的布局过程发生的区域，也是浮动元素与其他元素交互的区域。

https://developer.mozilla.org/en-US/docs/Web/Guide/CSS/Block_formatting_context

https://developer.mozilla.org/zh-CN/docs/Web/Guide/CSS/Block_formatting_context

#### ③ 到底什么是 BFC 

首先，BFC 的意思是 **Block Formatting Context** ，即**块级格式上下文**。 然后，当元素满足了某些条件，我们认为该元素创建了 **BFC**。 创建了 BFC 的元素我们可以把他看做是一个独立的容器，容器内的元素不论如何布局都不会影响到外面。

### 3.2 创建 BFC 的方式

- 根元素。
- 浮动元素。
- 绝对定位或固定定位的元素。
- 行内块元素。
- 表格单元格（th、td）、表格行（tr）、表格标题（caption）、table、thead、tbody、tfoot。
- `overflow` 的值不为 `visible` 的块元素。
- 伸缩项目。
- 多列容器。
- `column-span` 为 `all` 的元素始终会创建一个新的BFC，即使该元素没有包裹在一个多列容器中。

### 3.3 创建 BFC 可以解决的问题

#### ① 清除子元素浮动的影响

给浮动元素的父元素创建 BFC，清除掉子元素浮动的影响。

#### ② 解决外边距塌陷

给父元素创建 BFC，第一个和最后一个子元素的外边距不会塌陷。





## 作业

```

```



