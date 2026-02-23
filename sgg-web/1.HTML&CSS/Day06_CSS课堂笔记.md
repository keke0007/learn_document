# Day06 CSS 课堂笔记

## 1 回顾

```
1. 长度单位和颜色设置方式
   长度单位： px、em、%
   颜色设置方式：颜色名、rgb()、HEX

2. CSS基本选择器
   ID选择器
   类名选择器
   标签名选择器
   全局选择器

3. 显示模式
   inline、block、inline-block
   display

4. 属性总结
   4.1 字体样式
       font-size、font-weight、font-style、font-family、font
   4.2 文字颜色
       color
   4.3 文本样式
       letter-spacing、word-spacing、text-indent、text-decoration、text-align
       vertical-align

```







## 2 CSS 常用属性

### 2.1 文本样式

| 属性名          | 作用                 | 属性值                                                       |
| --------------- | -------------------- | ------------------------------------------------------------ |
| letter-spacing  | 字间距               | 长度                                                         |
| word-spacing    | 词间距（中文无效果） | 长度                                                         |
| text-decoration | 文本修饰线           | none：无修饰线。<br>underline：下划线。<br>overline：上划线。<br>line-throuth：删除线 |
| text-indent     | 首行缩进             | 长度                                                         |
| text-align      | 文本水平对齐方式     | left：左对齐。<br>right：右对齐。<br>center：居中对齐        |
| vertical-align  | 与同行文本如何对齐   | baseline：基线对齐。<br>top：顶线对齐。<br>middle：中线对齐。<br>bottom：底线对齐。<br>sub：下标字。<br>super：上标字。<br>长度：元素底部与基线的距离 |
| line-height     | 行高                 | 长度                                                         |

#### ① vertical-align

```
1. 设置行内元素或行内块元素与同行文本如何对齐，如 基线对齐、顶线对齐、中线对齐、底线对齐等
2. 设置上标字和下标字
3. 设置单元格中内容的纵向对齐方式，只能用于 td、th
```

#### ② line-height 设置行高

**行高的概念：**

```
1. 上一行文字中线与下一行文字中线的距离称为行高
2. 上一行文字底线与下一行文字顶线的距离称为行距，调整行高大小，行距受到影响
```

> 第一行文字中线与元素顶部距离是行高一半，最后一行文字中线与元素底部距离是行高一半！

**使用行高实现元素中的一行文字垂直居中，满足以下条件：**

```
1. 只有一行文字
2. 设置行高与高度一致
```

**line-height 是 font 的子属性：**

```css
 /* 将行高写在font复合属性中 */
font: bold 14px/30px 'Microsoft YaHei';
font: bold 14px/3 'Microsoft YaHei';  /* 此时 3 表示字体大小的倍数，相当于em */
```

### 2.2 背景样式

| 属性名                | 作用                 | 属性值                                                       |
| --------------------- | -------------------- | ------------------------------------------------------------ |
| background-color      | 背景颜色             | 颜色                                                         |
| background-image      | 设置背景图像地址     | url(地址)                                                    |
| background-repeat     | 设置背景图像重复方式 | repeat：重复。<br>repeat-x：横向重复。<br>repeat-y：纵向重复。<br>no-repeat：不重复。 |
| background-position   | 设置背景图像位置     | 关键字。<br>两个长度表示的坐标。<br>百分比                   |
| background-attachment | 背景图像固定         | scroll：随元素滚动，默认值。<br>fixed：固定。                |
| background            | 背景复合属性         | 多个值使用空格分隔                                           |

#### ① 背景颜色

```
1. 元素默认背景颜色是透明,background-color的默认值是 transparent（透明）
2. 给 body 设置背景色就是给整个页面设置背景色
```

#### ① 设置背景图像的位置 background-position

**使用关键字设置属性值：**

```css
/* 
    x轴位置：left right center
    y轴位置：top bottom center
*/
/* 使用两个值 */
background-position: left top;
background-position: right bottom;
background-position: right center;
background-position: right top;
/* 使用一个值  另一个值默认center*/
background-position: left;   /* left center */
background-position: bottom; /* center bottom */
background-position: center; /* center center */
```

**通过指定坐标（用长度）设置属性值：**

```css
/* 使用坐标设置背景图像位置 */
/* 设置的是图像的左上角位置 */
/* 使用两个长度（px、em） 分别是x坐标 y 坐标 */
background-position: 0 0;
background-position: 100px 20px;
background-position: 520px 320px;
background-position: -100px 100px;
/* 只设置一个长度， 被认为是x坐标 y轴位置默认取center */
background-position: 100px;
/* 长度表示的坐标和关键字混搭 */
background-position: right -50px;
background-position: 100px bottom;
```

**使用百分比设置属性值：**

```css
/* 
    元素和图像各自创建一个坐标系
    原点在各自的左上角，x轴从左到右，y轴从上到下
    根据百分比从元素上找到坐标点，根据百分比从图像上找到坐标点，两点重合
*/
/* 两个百分比 */
background-position: 0% 0%;
background-position: 50% 50%;
background-position: 20% 10%;
background-position: 100% 100%;
/* 百分比和其他混搭 */
background-position: 100% 100px;
background-position: left 100%;
/* 值使用一个百分比 被认为x方向位置，另一个方向默认center */
background-position: 10%;
```

**background-position 的两个子属性：**

```
background-position-x	设置x位置
background-position-y   设置y位置
```

#### ② 背景图像固定 background-attachment

```
如果设置 background-attachment 为 fixed， 背景图像定位的坐标原点是视口的左上角
背景图像只能显示图像与元素位置重合的位置
```

#### ③ 背景复合属性 background

```
任何子属性的值都可以作为background的值，没有数量要去，没有顺序要求
```

### 2.3 鼠标光标样式

| 属性名 | 作用         | 属性值                              |
| ------ | ------------ | ----------------------------------- |
| cursor | 设置鼠标光标 | pointer：小手。<br>move：移动图标。 |

```css
/* 自定义鼠标光标 */
cursor: url(../images/arrow03.png),pointer;
```

### 2.4 列表样式

| 属性名              | 作用               | 属性值                                    |
| ------------------- | ------------------ | ----------------------------------------- |
| list-style-type     | 设置列表项图标     | none：无                                  |
| list-style-position | 设置列表项图标位置 | outside：在li外面。<br>inside：在li里面。 |
| list-style-image    | 自定义列表项图标   | url(图片地址)                             |
| list-style          | 复合属性           | 多个值使用空格分隔                        |

> **注意：** 只有 ul、ol、li 这些标签设置列表样式才有效果！

### 2.5 表格样式

| 属性名          | 作用                         | 属性值                               |
| --------------- | ---------------------------- | ------------------------------------ |
| table-layout    | 设置列宽固定                 | auto：默认值。<br>fixed：固定。      |
| border-spacing  | 设置单元格之间的距离         | 长度                                 |
| border-collapse | 合并单元格边框               | separate：默认值。<br>collapse：合并 |
| caption-side    | 标题位置                     | top：表格上面。<br>bottom：表格下面  |
| empty-cells     | 没有内容的单元格显示还是隐藏 | show：显示，默认值。<br>hide：隐藏   |

> **注意：** 表格相关的属性只能设置到 table 标签上才生效！



## 3 CSS 选择器

### 3.1 基本选择器

#### ① ID 选择器

```css
#ID名 {}
```

#### ② 类选择器

```css
.类名 {}
```

#### ③ 标签名选择器

```css
标签名 {}
```

#### ④ 全局选择器

```js
* {}
```

### 3.2 组合选择器

#### ① 后代元素选择器

```css
选择器1 选择器2 {}
```

#### ② 子元素选择器

```css
选择器1 > 选择器2 {}
```

#### ③ 交集选择器

```css
选择器1选择器2 {}

.item.active {}
.active.item {}
div.item {}
```

#### ④ 并集选择器

```css
选择器1, 选择器2 {}
```

### 3.3 伪类选择器

```
:link			选择未访问过的超链接
:visited		选择已访问过的超链接
:hover			鼠标悬停在元素上
:active			鼠标悬停在元素上且鼠标按键按下不抬起
```

```
多个伪类选择器一起使用，请按照 :link、:visited、:hover、:active 顺序书写 (love hate 记忆法)
```

### 3.4 选择器权重（优先级）

#### ① 单个选择器之间的权重

```
ID选择器 > 类选择器、伪类选择器 > 标签名选择器 > 全局选择器
```

#### ② 组合选择器优先级比较规则

```
1. 两个组合选择器，先比较ID的数量，数量多者权重高，比较结束
2. ID数量无法分胜负，比较类、伪类的数量，数量多者权重高，比较结束
3. 类、伪类的数量无法分胜负，比较标签名的数量，数量多者权重高， 比较结束
4. 两个选择器权重一致，后面覆盖前面
```

> **组合： ** 并集选择器的组合，各自计算各自的权重，不会放在一起计算。





## 作业

```
1. 实现背景图片固定案例(交)
   https://example.fuming.site/HTML&CSS/04-%E8%83%8C%E6%99%AF%E5%9B%BE%E5%9B%BA%E5%AE%9A.html
   
2. 列表效果案例（交）
   https://example.fuming.site/HTML&CSS/05-%E5%88%97%E8%A1%A8.html
   ul，ol 自带40px左内边距 padding-left
```







 
