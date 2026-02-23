# Day07 CSS 课堂笔记

## 1 回顾

```
1. 选择器
   1.1 基本选择器
   1.2 组合选择器
       后代元素选择器、子元素选择器、交集组合、并集组合
   1.3 伪类选择器
       :link :visited :hover :active
   1.4 选择器权重
       单个选择器权重
       组合选择器权重

2. 属性总结
   2.1 字体样式
       font-size、font-weight、font-style、font-family、font
   2.2 文字颜色
       color
   2.3 文本样式
       letter-spacing、word-spacing、text-decoration、text-indent、text-align
       vertical-align、line-height
   2.4 背景样式
       background-color、background-image、background-repeat
       background-position、background-attachment、background
   2.5 鼠标光标样式
   	   cursor: pointer、move
   2.6 列表样式
       list-style-type、list-style-positoin、list-style-image、list-style
   2.7 表格样式
       table-layout、border-spacing、border-collapse、caption-side、empty-cells
```



## 2 盒子模型 box model

### 2.1 盒子模型的组成

#### ① 盒子模型的相关概念

```
1. 将元素比作成一个盒子
2. 页面布局就是盒子的排列和堆砌
```

**内容（content）：** 内容是元素的核心区域，元素中的文本内容和后代元素都显示在内容上。

**内边距（padding）：** 内容与元素边界的距离。

**边框（border）：** 位于元素的边界上。

**外边距（margin）：** 在元素边界之外，是与相邻元素的距离。

#### ② 影响盒子大小的因素

```
盒子的总宽度 = 内容宽度 + 左右内边距 + 左右边框
盒子的总高度 = 内容高度 + 上下内边距 + 上下边框
```

### 2.2 盒子中的内容区域

#### ① 设置内容区域的宽高的 CSS 属性

| CSS 属性名 | 功能     | 属性值 |
| ---------- | -------- | ------ |
| width      | 宽度     | 长度   |
| max-width  | 最大宽度 | 长度   |
| min-width  | 最小宽度 | 长度   |
| height     | 高度     | 长度   |
| max-height | 最大高度 | 长度   |
| min-height | 最小高度 | 长度   |

> **注意：** 最大最小宽高一般不与固定宽高一同设置！

#### ③ 元素的默认宽高

**行内元素：**

```
默认宽度被内容撑开，没有内容就没有宽度
默认高度被内容撑开，没有内容也会有一个文字的高度
```

**行内块元素：**

```
默认宽度被内容撑开，没有内容就没有宽度
默认高度被内容撑开，没有内容就没有高度
```

**块级元素：**

```
默认宽度被内容撑开，没有内容就没有高度
```

```
默认总宽度 = 父元素内容宽度 - 自身的左右外边距
默认内容宽度 = 父元素内容宽度 - 自身的左右外边距 - 自身的左右内边距 - 自身的左右边框
```

### 2.3 盒子的内边距 padding

#### ① 相关 CSS 属性

| CSS 属性名     | 功能           | 属性值           |
| -------------- | -------------- | ---------------- |
| padding-left   | 左内边距       | 长度             |
| padding-right  | 右内边距       | 长度             |
| padding-top    | 上内边距       | 长度             |
| padding-bottom | 下内边距       | 长度             |
| padding        | 上下左右内边距 | 多个长度空格分隔 |

#### ② padding 设置规则

**padding 值设置的规则：**

```
1. 不能是负值
2. 使用百分比，上下左右内边距都参照父元素内容宽度
```

**padding 复合属性的设置规则：**

```css
/* 1个值: 上下左右 */
padding: 20px;
/* 2个值： 上下 左右*/
padding: 40px 30px;
/* 3个值： 上 左右 下*/
padding: 10px 20px 30px;
/* 4个值： 上 右 下 左*/
padding: 15px 25px 35px 45px;
```

**不同显示模式的元素设置内边距：**

```
1. 块级元素、行内块元素内边距可以完美设置
2. 行内元素，左右内边距可以完美设置，上下内边距效果不完美
```

### 2.4 边框 border

| CSS 属性名                                                   | 功能                     | 属性值                                                       |
| ------------------------------------------------------------ | ------------------------ | ------------------------------------------------------------ |
| border-style                                                 | 边框风格                 | none：无风格。<br>solid：实线。<br>dashed：虚线。<br>dotted：点线。<br>double：双实线。 |
| border-color                                                 | 边框颜色                 | 颜色，默认值是文字颜色                                       |
| border-width                                                 | 边框宽度                 | 长度，默认值是3px                                            |
| border                                                       | 同时设置风格、颜色、宽度 | 多个值使用空格分隔                                           |
| border-left-style<br>border-left-color<br>border-left-width<br>border-left<br><br>border-right-style<br/>border-right-color<br/>border-right-width<br/>border-right<br><br>border-top-style<br/>border-top-color<br/>border-top-width<br/>border-top<br/><br/>border-bottom-style<br/>border-bottom-color<br/>border-bottom-width<br/>border-bottom |                          |                                                              |

```css
border的子属性有： border-style、border-color、border-width

border-left 的子属性： bordre-left-style、border-left-color、border-left-width
border-right border-top border-bottom 各种具有子属性

border-style 的子属性： border-left-style、border-right-style、border-top-style、border-bottom-style
border-color、border-width 各种具有子属性
```

### 2.5 外边距 margin

```
1. 外边距是元素与相邻兄弟元素的距离，如果没有相邻兄弟元素就是与父元素内容边界的距离
2. 左外边距和上外边距主要影响自己的位置，右外边距和下外边距主要影响相邻兄弟元素的位置
```

#### ① 相关 css 属性

| CSS 属性名    | 功能           | 属性值           |
| ------------- | -------------- | ---------------- |
| margin-left   | 左外边距       | 长度             |
| margin-right  | 右外边距       | 长度             |
| margin-top    | 上外边距       | 长度             |
| margin-bottom | 下外边距       | 长度             |
| margin        | 外边距复合属性 | 多个长度空格分隔 |

#### ② margin 设置规则

**margin 值设置的规则：**

```
1. 使用百分比，上下左右内边距都参照父元素内容宽度
2. 外边距可以是负值
3. 块级元素左右外边距都设置为 auto，该元素在父元素中横向居中
```

**margin 复合属性的设置规则：**

```
1个值： 上下左右
2个值： 上下 左右
3个置： 上 左右 下
4个值： 上 右 下 左
```

**不同显示模式的元素设置外边距：**

```
1. 块级元素、行内块元素外边距可以完美设置
2. 行内元素，只能设置左右外边距，上下外边距设置无效
```

#### ③ margin 塌陷

**什么是 margin 塌陷？**

```
1. 最上面元素的上外边距、最下面元素的下外边距会塌陷到父元素
2. 外边距塌陷只会发生在块级元素上
```

**如何解决 margin 塌陷？**

```
- 方案一： 父元素设置边框
- 方案二： 父元素设置内边距
- 方案三： 父元素开启BFC，设置 overflow:hidden;
```

#### ④ margin 合并

**什么是 margin 合并？**

```
1. 上面兄弟元素的下外边距会与下面兄弟元素的上外边距合并，两者之间距离取较大的外边距
2. 外边距合并只会发生在块级元素上
```

**如何解决 margin 合并？**

```
不用解决
```

### 2.6 内容溢出

| CSS 属性名 | 功能                      | 属性值                                                       |
| ---------- | ------------------------- | ------------------------------------------------------------ |
| overflow   | 设置溢出内容的显示方式    | visible：显示，默认值。<br>hidden：隐藏。<br>scroll：滚动条。<br>auto：自动。 |
| overflow-x | x轴方向溢出内容的显示方式 | 同上                                                         |
| overflow-y | y轴方向溢出内容的显示方式 | 同上                                                         |

**auto 和 scroll 的区别：**

```
1. scroll 不论内容是否会溢出，都有滚动条
2. auto 只有内容溢出才会显示滚动条
```

### 2.7 隐藏元素

```
1. 设置 visibility:hidden;   元素隐藏但是占据位置
2. 设置 display:none;  元素彻底隐藏，不占据位置
```



## 3 样式继承和自带样式

### 3.1 样式继承

**哪些样式可以被后代元素继承：**

```
1. 字体样式 font-size、font-weight、font-style font-family、font
2. 文字颜色 color
3. 文本样式 letter-spacing、word-spacing、text-decoration、text-indent、text-align、line-height （vertical-align 不可以被继承）
```

### 3.2 自带样式（用户代理样式）

```
标题h1~h6 自带 font-size、font-weight、上下外边距
p 自带 上下外边距
em 自带 font-style
strong 自带 font-weight
a 自带 color、text-decoration、cursor
ul、ol 自带 padding-left、上下外边距
...
```

### 3.3 继承的样式、自带的样式、直接设置的样式

```
直接设置的样式 > 自带的样式 > 继承的样式
```





## 作业

```
1. 导航条
2. 安装标记工具 markman
```















