# Day04 HTML&CSS 课堂笔记

## 1 回顾

```
1. 列表
   无序列表 ul li
   有序列表 ol li
   定义列表 dl dt dd
   
2. 表格
   2.1 表格结构
   2.2 table 标签属性： width、height、border、cellspacing、cellpadding
   2.3 单元格宽高
   2.4 单元格内容对齐方式  align、valign
   2.5 单元格跨行跨列  td、th属性： rowspan\colspan
   2.6 标签： table、caption、thead、tbody、tfoot、tr、td、th

3. 表单
   3.1 表单整体设置 form标签：action、target
   3.2 表单控件 9 中类型
      文本输入框、密码输入框、单选框、复选框、提交按钮、重置按钮、普通按钮、文本域、下拉选项
   3.3 表单控件属性
       name、value、disabled

```



## 2 表单

### 2.1 label 标签的使用

```html
<!-- 使用label关联描述文字和输入框 -->
<label for="usernameInp">用户名：</label>
<input type="text" id="usernameInp">

<!-- 使用label关联选择框 单选框、复选框 -->
<label>
    <input type="radio" name="gender">男
</label>
<label>
    <input type="radio" name="gender">女
</label>
```

### 2.2 fieldset 和 legend 标签（了解）

```html
<form>
    <fieldset>
        <legend>标题内容</legend>
        各种表单控件...
    </fieldset>
</form>
```

### 2.3 表单标签总结

| 标签名   | 语义和功能                         | 属性                                                         | 单标签和双标签 |
| -------- | ---------------------------------- | ------------------------------------------------------------ | -------------- |
| form     | 表单包裹元素                       | action：设置表单提交地址。<br>target：设置提交地址从那个窗口打开 | 双标签         |
| input    | 各种类型的表单控件                 | type：表单控件类型。<br>maxlength：最大可输入长度。<br>checked：设置默认选中。<br>name：表单控件标识。<br>value：表单控件的值。<br>disabled：设置为不可用。 | 单标签         |
| button   | 各种类型的按钮                     | type：按钮类型。<br>disabled：设置为不可用。                 | 双标签         |
| textarea | 文本域                             | rows: 默认显示的行数。<br>cols：默认显示的列数。<br>name：表单控件标识。<br/>disabled：设置为不可用。 | 双标签         |
| select   | 下拉选项包裹元素                   | name：表单控件标识。<br/>disabled：设置为不可用。            | 双标签         |
| option   | 下拉的选项                         | value：表单控件的值。<br/>selected：设置默认选中<br>disabled：设置为不可用。 | 双标签         |
| label    | 用于关联表单控件                   | for：表单控件的id                                            | 双标签         |
| fieldset | 设置外围的边框                     | 无                                                           | 双标签         |
| legend   | 设置表单标题<br>需要与fieldset配合 | 无                                                           | 双标签         |

```
input 标签的 type 属性值有 text、password、radio、checkbox、submit、reset、button， 默认值 text
button 标签的 type 属性值有 submit、reset、button，默认值 submit
```



## 3 内联框架标签

| 标签名 | 功能和语义                               | 属性                                                         | 单标签还是双标签 |
| ------ | ---------------------------------------- | ------------------------------------------------------------ | ---------------- |
| iframe | 内联框架<br>将各种类型的文件引入当前页面 | src: 设置目标文件地址。<br>frameborder：设置是否有边框，0表示没有，其他数字表示有。<br>width：设置宽度。<br>height：设置高度。 | 双标签           |



## 4 HTML 字符实体

```
&nbsp;			空格
&lt;			小于号 <
&gt;			大于号 >
&amp;           和好 &

&yen;			人民币符号
&copy;			版权符号
&times;			乘号
&divide;		除号
```

更多的字符实体，请参照：https://www.w3cschool.cn/htmltags/html-symbols.html



## 5 HTML 全局属性

全局属性指所有的标签都具有的属性，有如下全局属性：

```
id		唯一标识，可以用作锚点名、可以用作css选择器
name	设置名称标识，对于表单控件用处较大
class	设置类名，用于css选择器
style	用于直接设置css样式
title	设置提示文字，鼠标悬浮在元素上会显示
lang	设置语言，英文：en; 中文：zh-CN
```

语言参考代码：https://www.w3school.com.cn/tags/html_ref_language_codes.asp



## 6 meta 元信息

```html
<!-- 字符集编码 -->
<meta charset="UTF-8">
<meta http-equiv="content-type" content="text/html;charset=utf-8">

<!-- 网页关键字 -->
<meta name="keywords" content="8-12个以英文逗号隔开的单词/词语">

<!-- 网页描述信息 -->
<meta name="description" content="80字以内的一段话，与网站内容相关">

<!-- 设置完美视口 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- 设置网页刷新 -->
<!-- <meta http-equiv="refresh" content="3"> -->
<!-- 定时跳转 -->
<meta http-equiv="refresh" content="10,url=http://www.atguigu.com">
<title>Document</title>
```



## 7 CSS 的基本语法

### 7.1 HTML 和 CSS 的关系

```
1. HTML 实现页面结构，CSS 实现页面样式
2. CSS 样式需要作用在 HTML 元素上
```

### 7.2 HTML 元素树（元素和元素之间的关系）

```
父元素
祖先元素
子元素
后代元素
兄弟元素		具体相同父元素的才是兄弟元素
```

### 7.3 在 HTML 中使用 CSS

#### ① 行内式

```html
<标签 style="CSS代码...;"></标签>
```

#### ② 内嵌式

```html
<style>
	CSS 代码...
</style>
```

```
style 标签放在页面的任意位置都可以生效，建议放在 head 中！
```

#### ③ 外链式

```html
<link rel="stylesheet" href="CSS文件地址">
```

```
link 标签放在页面的任意位置都可以生效，建议放在 head 中！
```

### 7.4 CSS 基本语法结构

**选择器：** 用于选择要设置样式的元素。

**声明块：** 选择器后面的大括号，声明块由多条声明组成。

**声明：** 每条声明以分号结尾，声明由CSS属性和它的值组成。

#### ① 内嵌式和外链式的语法结构

```css
选择器 {
    属性名:值;
    属性名:值;
    属性名:值;
    属性名:值;
	....
}
```

#### ② 行内式的语法结构

```html
<标签名 style="属性名:值; 属性名:值; 属性名:值; 属性名:值;..."></标签名>
```

#### ③ 注意区分HTML 属性 和 CSS 属性

```html
<!-- 使用HTML属性设置图片尺寸 -->
<img src="./images/小乐出浴图.jpg" alt="小乐出狱" width="400" height="300">

<!-- 使用CSS属性设置图片尺寸 -->
<img src="./images/小乐出浴图.jpg" alt="小乐出狱" style="width:400px;height:300px">
```

### 7.5 CSS 的层叠性

```
不同方式、不同选择器所设置的样式都会层叠在该元素上
```

### 7.6 CSS 注释

```css
/* CSS 注释 */
/* 
    CSS 注释
    CSS 注释
    CSS 注释
    CSS 注释
*/
```





## 附录 VsCode 的使用

#### 使用方式

```
整个目录拖进vsode
在vscode里面新建文件和目录
```

#### 相关设置

```
自动保存：  设置 -> Auto Save
字体大小：  设置 -> Font Size
目录结构缩进距离： 设置 ->  Tree: Indent
合并单个目录结构： 设置 ->  Compact Folders  去掉前面的√
颜色主题
文件图标主题
```

#### 快捷键

```
代码自动格式化： alt + shift + f
复制当前行到下一行： 连续按 ctrl+c ctrl+v
```

#### Emmet 快捷键

```
!
标签名+tab
```

更多Emmet快捷键： https://docs.emmet.io/abbreviations/syntax/

```
设置语言为zh-CN
设置 -> Emmet: Variables 点击添加项 选择 lang 值 zh-CN
```

#### 常用扩展

```
Chinese (Simplified) (简体中文) Language Pack for Visual Studio Code
open in browser
Live Server
Chinese Lorem
```







## 作业









