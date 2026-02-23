# Day12 CSS3 课堂笔记

## 回顾

```
1. HTML5
   1.1 新增标签
       排版布局： header、footer、nav、section、aside、article、main、figure、figcaption
       状态： meter progress
       详情： details summary
       注音： ruby rt
       文本： mark
   1.2 表单新增功能
       表单控件新增属性： placeholder、rquired、autofocus、autocomplete、form
       新增表单控件类型： email、number、url、tel、search
                       range、color
                       date、month、week、time、datetime-local
       form标签新增属性： novalidate
       搜索框下拉提示： datalist
   1.3 音视频
       video、audio、source
   1.4 全局属性
       全局属性： hidden
       a标签新增属性： download 
       
2. CSS3 基本语法
   2.1 浏览器私有前缀
   2.2 新增长度单位： rem、vw、vh、vmax、vmin
   2.3 新增颜色设置方式： rgba()、hsl()、hsla()
```



## 1 CSS3 选择器

### 1.1 基本选择器（6个）

#### ① 标签名选择器

```css
标签名 {}
```

#### ② 类名选择器

```css
.类名 {}
```

#### ③ ID 选择器

```css
#ID名 {}
```

#### ④ 全局选择器

```css
* {}
```

#### ⑤ 交集选择器（选择器的组合形式）

```css
选择器1选择器2 { }
```

#### ⑥ 并集选择器（选择器的组合形式）

```css
选择器1，选择器2 {}
```

### 1.2 层级选择器（4个）

#### ① 后代元素选择器

```css
选择器1 选择器2 {}
```

#### ② 子元素选择器

```css
选择器1 > 选择器2 {}
```

#### ③ 相邻兄弟元素选择器

```css
选择器1 + 选择器2 {}
```

#### ④ 通用兄弟元素选择器

```css
选择器1 ~ 选择器2 {}
```

### 1.3 属性选择器（5个）

```
[attr]			  选择包含属性名attr的元素
[attr=“val”]  	  选择属性attr的值是val的元素
[attr^="val"]     选择属性attr的值以val开头的元素
[attr$="val"]     选择属性attr的值以val结尾的元素
[attr*="val"]     选择属性attr的值包含val的元素
```

> 属性选择器如果与其他选择器进行交集组合，通常写在其他选择器的后面
>
> ```css
> img[alt] {}
> .item[title] {}
> ```

### 1.4 伪类选择器（23个）

#### ① 动态伪类选择器（5个）

```
:link
:visited
:hover
:active	
:focus		选择获取到焦点的元素
```

#### ② 目标伪类选择器（1个）

```
:target		选择到当前锚点所对应的元素
```

#### ③ 语言伪类选择器 (1个，了解)

```css
:lang(语言)
```

```
问答： :lang(zh-CN) 和 [lang="zh-CN"] 什么区别？
答案： :lang(zh-CN） 所选择到的元素中可以自己不设置 lang 属性，会继承祖先元素的语言设置
	  [lang="zh-CN"] 所选择到元素，必须元素自身设置了 lang 属性。
```

#### ④ UI元素伪类选择器（3个）

```
:enabled		可用的表单控件
:disabled		不可用的表单控件
:checked		被选中的表单控件（单选框、复选框、下拉选项）
```

#### ⑤ 结构伪类选择器（12个）

```
:frist-child			在兄弟元素中排名第一
:last-child				在兄弟元素汇总的排名最后
:nth-child(n)			在兄弟元素中排名第n个
:nth-last-child(n)		在兄弟元素中排名倒数第n个
:only-child				没有兄弟元素

:first-of-type			在同标签名的兄弟元素中排名第一
:last-of-type			在同标签名的兄弟元素中排名最后
:nth-of-type(n)			在同标签名的兄弟元素中排名第n个
:nth-last-of-type(n)	在同标签名的兄弟元素中排名倒数第n个
:only-of-type			没有同标签名的兄弟元素

:root					根元素
:empty					没有文本内容也没有后代元素
```

```css
:nth-child(odd)        奇数行
:nth-child(even)       偶数行
:nth-of-type(2n-1)	   奇数行
:nth-of-type(2n)	   偶数行
:nth-of-type(3n)	   排号是3的倍数
```

####  ⑥ 否定伪类选择器（1个）

```css
:not(选择器) 			 选择不满足括号中选择器的元素
```

### 1.5 伪元素选择器（6个）

```
::first-letter / :first-letter	选择元素中的第一个文字
::first-line / :first-line		选择元素中的第一行文字
::before / :before				给元素动态添加子元素，放在第一个位置
::after / :after				给元素动态添加子元素，放在最后一个位置
::placeholder					选择输入框、文本域中placeholder中的文字
::selction						选择被鼠标选中的文字
```

> `::before`和`::after` 选择器后面的声明块中必须设置 `content` 属性！

### 1.6 选择器的优先级（权重）

```
1. ID选择器 > 类选择器、伪类选择器、属性选择器 > 标签名选择器、伪元素选择器 > 全局选择器
2. !important > 行内式 > 任何选择器
   注意：!important 可以无限提高某个属性的权重
```

https://flukeout.github.io/



## 2 CSS3 新增盒子相关样式

#### ① display 介绍

display 属性拥有更多的值，可以让任何元素设置任何样式。

#### ② box-sizing 属性

通过该属性可以调整元素宽高的设置规则：

```
content-box		width和height设置的内容宽高，默认值
border-box		width和height设置的总宽总高，也称为怪异模式
```

#### ③ 盒子阴影 box-shadow

```css
box-shadow: x偏移 y偏移 模糊值 外延值 颜色 内阴影;
```

```css
/* 设置阴影的偏移位置 x方向 y方向 */
box-shadow: 10px 5px;

/* 设置阴影的 偏移位置 颜色 */
box-shadow: -5px 10px #ccc;
box-shadow: #099 -5px -10px;

 /* 设置阴影的模糊值 */
box-shadow: 5px 5px 10px;
/* 设置阴影的模糊值 颜色 */
box-shadow: 5px 5px 10px #ccc;
box-shadow: rgba(0,0,0,.3) 5px 5px 10px;
/* 阴影不偏移 靠模糊值向四周扩散 */
box-shadow: 0 0 15px #000;

/* 设置外延值 */
box-shadow: 3px 3px 5px 1px #080;

/* 设置内阴影 */
box-shadow: 10px 10px inset;
box-shadow: -10px 10px inset;
box-shadow: inset -10px -10px #000;

/* 多阴影 */
box-shadow: 5px 0 5px #f00,
            0 5px 5px #080,
            -5px 0 5px #088,
            0 -5px 5px #880;
```

#### ④ 不透明度 opacity

给元素设置 `opacity` 属性可以让元素整体半透明，该属性的值取 0 到 1之间的小数，数字越大越不透明，1表示完全不透明，0表示完全透明。

#### ⑤ 粘连定位

给元素设置 `position:sticky;` 该元素粘连定位，当页面滚动，该元素顶部触碰到视口顶部的时候，会固定定位在那个位置。







## 作业

```
1. 属性选择器应用： 根据 href 属性值的结尾，设置背景图
2. :target 应用： 实现点击图片切换效果
3. :checked： 实现点击图片切换效果
4. 阴影作业：鼠标悬停加阴影
```





