# Day15 CSS3 课堂笔记

## 1 回顾

```
1. tranform 变换（变形）
   1.2 变换方法
       2D变换：translateX() translateY() translate() scaleX() scaleY() scale() rotate()
       3D变换：translateZ() translate3D() rotateX() rotateY() rotateZ() rotate3D()
   1.3 css属性
       需要给变换的元素： transform、transform-origin、backface-visibility
       需要给变换的元素的父元素：transform-style、perspective、perspective-origin

2. transition 过渡
   transition-duration
   transition-delay
   trnasition-property
   trnasition-timing-funciton
   transition
  
3. animation 动画
   3.1 关键帧
   3.2 css属性
       animation-name
       animation-duration
       animation-delay
       animatino-timing-function
       animation-iteration-count
       animation-direction
       animation-play-state
       animation-fill-mode
       animation
```



## 2 多列布局

#### ① 设置给包裹元素的 CSS 属性（共 8 个属性）

| CSS 属性名        | 含义               | 值              |
| ----------------- | ------------------ | --------------- |
| column-count      | 列数               | 数字            |
| column-width      | 列宽               | 长度            |
| columns           | 同时设置列数和列宽 | 空格分隔两个值  |
| column-gap        | 列间距             | 长度            |
| column-rule-style | 列分隔线风格       | 同 border-style |
| column-rule-color | 列分隔线颜色       | 颜色            |
| column-rule-width | 列分隔线宽度       | 长度            |
| column-rule       | 列分隔线复合属性   | 空格分隔两个值  |

**column-count 和 column-width：**

```
哪个属性分出来的列数少，就按照哪一个。
```

#### ② 设置给子元素的 CSS 属性（共 4 个属性）

| CSS 属性名                          | 含义                 | 值                                                           |
| ----------------------------------- | -------------------- | ------------------------------------------------------------ |
| column-span                         | 跨列                 | none：不跨列，默认值。<br>all：跨所有列                      |
| -webkit-column-break-before（了解） | 设置元素前面是否断列 | auto：自动，默认值。<br>always：必须断列。<br>avoid：必须不断列。 |
| -webkit-column-break-after（了解）  | 设置元素后面是否断列 | auto：自动，默认值。<br/>always：必须断列。<br/>avoid：必须不断列。 |
| -webkit-column-break-inside（了解） | 设置元素内部是否断列 | auto：自动，默认值。<br/>avoid：必须不断列。                 |



## 3 伸缩盒布局 Flex

### 3.1 伸缩容器和伸缩项目

#### ① 概念定义

**伸缩容器：**  元素设置 `display:flex`或者`display:inline-flex`，该元素就称为伸缩容器。

**伸缩项目：**  伸缩容器的**子元素**称为伸缩项目。

#### ② 伸缩项目的特点

```
1. 伸缩项目沿主轴排列（主轴默认横向），不会脱离文档流
2. 不论元素原来的显示模式是什么，变为伸缩项目之后，具有自己的显示特点：
   ① 不存在外边距的塌陷和合并，默认宽高被内容撑开
   ② 宽高内外边距都可以设置，不会被父元素当成文本
```

### 3.2 设置主轴方向和换行方式

**主轴：** 伸缩项目沿着主轴排列，主轴的默认方向是从左到右。

**侧轴：** 与主轴垂直的是侧轴。

#### ① 设置主轴方向

给伸缩容器设置CSS属性 `flex-direction` 可以修改主轴方向，该属性的值如下：

```
row				水平从左到右
row-reverse		水平从右到左
column			竖直从上到下
column-reverse	竖直从下到上
```

#### ② 设置换行方式

给伸缩容器设置CSS属性`flex-wrap` 可以修改换行方式，该属性值如下：

```
nowrap			不换行
wrap			自动换行
wrap-reverse	换行并翻转
```

#### ③ 同时设置主轴方向和换行方式

`flex-flow` 可以同时设置主轴方向和换行方式，是 `flex-direction` 和 `flex-wrap` 的复合属性。

### 3.3 设置伸缩项目在主轴上的对齐方式

给伸缩容器设置CSS属`justify-content`，可以调整伸缩项目在主轴上的对齐方式，该属性的值如下：

```
flex-start				主轴起点对齐，默认值
flex-end				主轴终点对齐
center					居中对齐
space-between			两端对齐，两端无间距
space-around			两端间距是中间间距一半
space-evenly			两端间距与中间间距相等
```

### 3.4 设置伸缩项目在侧轴上的对齐方式

#### ① 一条主轴线（伸缩项目在主轴上不换行）

给伸缩容器设置CSS属性 `align-items`， 该属性的值如下：

```
stretch		伸缩项目在侧轴方向拉伸（前提：不设置侧轴方向对应的长度）
flex-start	侧轴起点
flex-end	侧轴终点
center		居中
baseline	基线
```

#### ② 多条主轴线 （伸缩项目在主轴上发生换行）

给伸缩容器设置CSS属性 `align-content`， 该属性的值如下：

```
stretch					伸缩项目在侧轴方向拉伸,默认
flex-start				侧轴起点对齐，默认值
flex-end				侧轴终点对齐
center					居中对齐
space-between			两端对齐，两端无间距
space-around			两端间距是中间间距一半
space-evenly			两端间距与中间间距相等
```

### 3.5 伸缩项目的伸缩性

#### ① 伸缩项目在主轴上的长度 flex-basis

如果设置了 flex-basis，伸缩项目在主轴上的长度就按照 flex-basis， 与主轴方向对应的 width 或者 heihgt 将不生效。

flex-basis 的默认值是 auto，表示 flex-basis 不起作用，主轴方向的长度仍然按照 width 或者 height 的设置。

#### ② 扩展比率 flex-grow

**伸缩项目扩展的前提：**

```
1. 伸缩容器在主轴方向有富余的空间
2. 伸缩项目的扩展比率flex-grow不能是0
```

**伸缩项目扩展的规则：**

```css
			  原来的主轴长度  扩展比率    瓜分比重
.item01         100            1        1/10     100+400*1/10即100+40
.item02         200            6        6/10     100+400*6/10即200+240
.item03         300            3        3/10     100+400*3/10即300+120

富余空间： 400
分母： 1+6+3=10
```

#### ③ 收缩比率 flex-shrink

**伸缩项目收缩的前提：**

```
1. 伸缩容器在主轴上的长度不够，小于所有伸缩项目的主轴长度和
2. 不能换行
3. 伸缩项目的收缩比率不能是0，默认值是 1
```

**伸缩项目收缩的规则：**

```css
			原来的主轴长度    收缩比率    瓜分比重
.item01         100            5        500/1700     100-100*5/17
.item02         200            3        600/1700     200-100*6/17
.item03         300            2        600/1700     300-100*6/17

亏空长度： 100
分母：    100*5 + 200*3 + 300*2 = 1700 
```

#### ④ flex 复合属性

```css
flex: grow shrink basis
```

```css
flex: 1 1 0;
flex: 0 0 auto;
flex: 0 1 auto;
```

- 如果缩写为 `flex: 1` , 则其计算值为 `1 1 0%`
- 如果缩写 `flex: auto` , 则其计算值为 `1 1 auto`
- 如果`flex: none` , 则其计算值为`0 0 auto`
- 如果 `flex: 0 auto` 或者 `flex: initial` , 则其计算值为`0 1 auto`，即 flex 初始值

### 3.6 伸缩项目排序

给伸缩项目设置 `order` 属性，属性值是数字，值越大排序越靠后，可以是负值。

### 3.7 单独设置伸缩项目在侧轴上的对齐方式

给伸缩项目设置 `align-self` ，该属性的值：

```
auto： 	   按照伸缩容器 align-items 的设置,默认值
stretch		伸缩项目在侧轴方向拉伸
flex-start	侧轴起点
flex-end	侧轴终点
center		居中
baseline	基线
```

### 3.8 伸缩盒相关 CSS 属性总结

#### ① 设置给伸缩容器的属性

| CSS 属性名      | 含义                         | 值                                                           |
| --------------- | ---------------------------- | ------------------------------------------------------------ |
| display         | 设置伸缩容器                 | flex<br>inline-flex                                          |
| flex-direction  | 主轴方向                     | row<br>row-reverse<br>column<br>column-reverse               |
| flex-wrap       | 换行方式                     | nowrap<br>wrap<br>wrap-reverse                               |
| flex-flow       | 同时设置主轴方向和换行方式   |                                                              |
| justify-content | 主轴上的对齐方式             | flex-start<br>flex-end<br>center<br>space-between<br>space-around<br>space-evenly |
| align-items     | 侧轴上的对齐方式             | stretch<br>flex-start<br>flex-end<br>center<br>baseline      |
| align-content   | 侧轴上的对齐方式（发生换行） | stretch<br>flex-start<br/>flex-end<br/>center<br/>space-between<br/>space-around<br/>space-evenly |

#### ② 设置给伸缩项目的属性

| CSS 属性名  | 含义               | 值            |
| ----------- | ------------------ | ------------- |
| flex-basis  | 伸缩项目的主轴长度 | auto，长度    |
| flex-grow   | 扩展比率           | 数字，默认值0 |
| flex-shrink | 收缩比率           | 数字，默认值1 |
| flex        | 复合属性           |               |
| order       | 排序               | 数字          |
| align-self  | 单独设置侧轴对齐   |               |



## 作业

```
1. 等分布局
2. Flex布局页面
```

