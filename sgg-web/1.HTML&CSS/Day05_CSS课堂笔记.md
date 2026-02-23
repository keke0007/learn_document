# Day05 CSS 课堂笔记

## 1 回顾

```
1. HTML
   1.1 表单标签
       label
       fieldset legend
   1.2 iframe
   1.3 字符实体
       &nbsp;  &lt;  &gt;   &amp;
       &yen;  &copy;  &times;  &divide;
   1.4 全局属性
       title、lang、id、name、class、style
   1.5 meta 元信息
2. CSS
   2.1 在HTML中使用 CSS
       行内式、内嵌式、外链式
   2.2 CSS语法结构
       ① 内嵌式和外链式
         选择器、声明块、声明、CSS属性和它的值
       ② 行内式
   2.3 CSS层叠性
   2.4 注释
```



## 2 CSS 长度单位和颜色设置

### 2.1 CSS 中的长度单位

```
px 像素
em 字体大小的倍数
%  百分比
```

### 2.2 CSS 中的颜色设置方式

#### ① 使用颜色名表示颜色

常见的颜色名有：

```
red、orange、yellow、green、cyan、blue、purple、pink、deeppink、skyblue、greenyellow ...
```

#### ② rgb 方式表示颜色

```css
/*
    计算机三元色
    red         0~255   0%~100%
    green       0~255   0%~100%
    blue        0~255   0%~100%
*/
background: rgb(100, 200, 120);
background: rgb(255, 0, 0);
background: rgb(255, 0, 255);

/* 三个元色 取相同的数值  灰色 */
/* 数值越大颜色越浅，全是255是白色，数值越小颜色越深，全是0是黑色 */
background: rgb(255, 255, 255);
background: rgb(0, 0, 0);
background: rgb(100, 100, 100);
background: rgb(199, 199, 199);

/* 使用百分比 */
background: rgb(45%, 80%, 74%);
```

#### ③ hex 十六进制方式表示颜色

```css
/* 十六进制 原理同rgb一样 */

/* 
 十进制：    0 1 2 3 4 5 6 7 8 9 10 11 12 13 ... 19 20 21 ... 99 100 ...
 二进制：    0 1 10 11 100 101 110 111 1000 ...
 十六进制：  0 1 2 3 4 5 6 7 8 9 a b c d e f 10 11 ... 1f 20 21 ... ff 100 ...
*/

/* 
 十进制255 = 十六进制ff
 两位十六进制的数字可以表示一种原色，六位十六进制数字能够表示三元色
*/

/* 使用6位十六进制的数字表示颜色 每两位表示一个元色 */
background: #4fa8bb;
background: #0000ff;
background: #ababab;
background: #131313;

/* 表示一种元色的两个数字是相同的，且三组元色各自都是相同， 可以简写为3位十六进制数字 */
background: #a8c;  /* #aa88cc */
background: #bbb;  /* #bbbbbb */
background: #ab2233;  /* 不可简写 */
```





## 3 CSS 基本选择器

### 3.1 四种基本选择器

#### ① 标签名（元素名）选择器

```css
标签名 {}
```

#### ② 类名选择器

```css
.类名 {}
```

```
1. 多个元素可以设置相同的类名
2. 一个元素可以设置多个类名
```

#### ③ ID 选择器

```css
#ID名 {}
```

> 元素的ID名必须是唯一的！

#### ④ 全局（通配）选择器

```css
* {}
```

### 3.2 基本选择器之间的权重

```
1. ID选择器 > 类选择器 > 标签名选择器 > 全局选择器
2. 行内式大于所有的选择器
```



## 4 盒子模型（显示模式）

### 4.1 元素的显示模式

#### ① 块级元素 block

显示模式是块级的元素称为块级元素，特点：

```
1. 在页面中是一个块，能够独占一行
2. 可以设置宽度和高度
```

#### ② 行内元素 inline

显示模式是行内的元素称为行内元素，特点：

```
1. 显示在行内，不能独占一行
2. 无法设置宽度和高度
```

#### ③ 行内块元素 inline-block

显示模式是行内块的元素称为行内块元素，特点：

```
1. 显示在行内，不能独占一行
2. 可以设置宽度和高度
```

> 按照最早的标准，行内块元素也被当做行内元素！

### 4.2 HTML 元素的默认显示模式

#### ① 默认显示模式是 block 的元素：

```
排版标签： h1~h6、p、pre、hr、div
列表标签： ul、ol、li、dl、dt、dd
表单标签： form、option
```

#### ② 默认显示模式是 inline 的元素：

```
文本标签： em、strong、del、ins、sub、sup、span
超链接标签： a
表单标签： label
```

#### ③ 默认显示模式是 inline-block 的元素：

```
图片标签： img
表单标签： input、button、textarea、select
框架标签： iframe
```

### 4.3 修改元素的显示模式

使用CSS属性 `display` 可以设置元素的显示模式，该属性的值如下：

```
inline
block
inline-block
```

```
按照最早的标准只有行内和块级，默认显示模式是行内块的元素，无法设置成真正的行内
```



## 5 CSS 属性总结

### 5.1 字体样式

| 属性名      | 作用             | 属性值                                                       |
| ----------- | ---------------- | ------------------------------------------------------------ |
| font-size   | 字体大小         | 长度                                                         |
| font-weight | 字体粗细         | normal：正常。<br>lighter：细。<br>bold：粗。<br>100~900数字：100~300是细体，400、500正常，600以及以上粗体 |
| font-style  | 斜体字           | normal：正常。<br>italic：斜体字。                           |
| font-family | 字体族科         | 字体名称、字体列表                                           |
| font        | 设置多种字体样式 | 多个值，使用空格分隔                                         |

#### ① 字体族科 font-family

**字体族科的设置：**

``` 
font-family: 字体名称；
font-family: "字体名称";  /* 如果字体名称中有空格，如 Microsoft YaHei 建议使用引号包裹*/
```

**设置字体列表：**

```css
font-family: arial, "Hiragino Sans GB", "Microsoft Yahei", 微软雅黑, 宋体, Tahoma, Arial, Helvetica, STHeiti;
font-family: "Microsoft YaHei", 微软雅黑, 宋体, sans-serif;
```

**衬线字体和非衬线字体：**

```
serif 表示衬线字体，笔画粗细不一致，如宋体、仿宋体、楷体等
sans-serif 表示非衬线字体，笔画粗细一致，如微软雅黑、黑体、Helvetica
```

#### ② 复合属性 font

```css
/* 最少两个值 字体大小 字体族科 */
font: 20px 宋体;
font: 20px "Microsoft YaHei",微软雅黑,宋体,sans-serif;

/* 粗体字 字体大小 字体族科  */
font: 800 16px "Microsoft YaHei",微软雅黑,宋体,sans-serif;

/* 斜体字 字体大小 字体族科  */
font: italic 16px "Microsoft YaHei",微软雅黑,宋体,sans-serif;

/* 又粗又斜 字体大小 字体族科  */
font: 800 italic 16px "Microsoft YaHei",微软雅黑,宋体,sans-serif;
font: italic italic 16px "Microsoft YaHei",微软雅黑,宋体,sans-serif;
```

#### ③ 子属性和复合属性的关系

```
1. 复合属性写在子属性的后面，前面的子属性全部失效，复合属性即使没写对应的值也会用默认值覆盖掉子属性
2. 子属性写在复合属性的后面，子属性会覆盖掉复合属性中与之对应的样式
```

### 5.2 文本颜色

| 属性名 | 作用         | 属性值 |
| ------ | ------------ | ------ |
| color  | 设置文字颜色 | 颜色   |

### 5.3 文本样式

| 属性名          | 作用                 | 属性值                                                       |
| --------------- | -------------------- | ------------------------------------------------------------ |
| letter-spacing  | 字间距               | 长度                                                         |
| word-spacing    | 词间距（中文无效果） | 长度                                                         |
| text-decoration | 文本修饰线           | none：无修饰线。<br>underline：下划线。<br>overline：上划线。<br>line-throuth：删除线 |
| text-indent     | 首行缩进             | 长度                                                         |
| text-align      | 文本水平对齐方式     | left：左对齐。<br>right：右对齐。<br>center：居中对齐        |
| vertical-align  | 与同行文本如何对齐   | baseline：基线对齐。<br>top：顶线对齐。<br>middle：中线对齐。<br>bottom：底线对齐。<br>sub：下标字。<br>super：上标字。<br>长度：元素底部与基线的距离 |
| line-height     |                      |                                                              |

#### ① vertical-align

```
1. 设置行内元素或行内块元素与同行文本如何对齐，如 基线对齐、顶线对齐、中线对齐、底线对齐等
2. 设置上标字和下标字
3. 设置单元格中内容的纵向对齐方式，只能用于 td、th
```

#### ② line-height 设置行高

**行高的概念：**

**使用行高实现元素中的一行文字垂直居中，满足以下条件：**

**line-height 是 font 的子属性：**



```
行高可选值：
1.normal：由浏览器根据文字大小决定的一个默认值。
2.像素（px）
3.数字：参考自身font-size的倍数（很常用。通常是1.5~2倍之间）
4.百分比：参考自身font-size的百分比。
备注：由于字体设计的原因，文字在一行中，并不是绝对垂直居中，若一行中都是文字，不会太影响观感。

注意：
1.行高过小：导致文字重叠，且最小值是0，不能为负数（负数会无效，默认为normal）。
2.行高是可以继承的。
3. 

```





## 作业

```
1. 课堂案例
2. google 字体设置
```







