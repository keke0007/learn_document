# Day03 HTML 课堂笔记

## 1 回顾

```
1. 排版标签
   h1~h6
   p
   hr
   br
   pre
   div
2. 文本标签
   em
   strong
   ins
   del
   sup
   sub
   span
3. 图片标签
   img 属性 src、alt、width、height
4. 相对路径和绝对路径
   绝对路径： 网络绝对路径 、 计算机本地绝对路径
   相对路径： ./  ../
5. 超链接和锚点
   a 标签， 属性: href、target
```



## 2 列表

### 2.1 无序列表

```html
文字无序列表：
<ul>
      <li>HTML 超文本标记语言</li>
      <li>CSS 层叠样式表</li>
      <li>JavaScript 浏览器端脚本语言</li>
</ul>

超链接无序列表：
<ul>
     <li>
         <a href="#">感悟习近平主席俄罗斯之行的“历史逻辑”</a>
     </li>
     <li>
         <a href="#">携手向未来！习近平谈构建人类命运共同体</a>
     </li>
     <li>
         <a href="#">镜观·领航｜命运与共 携手建设更加美好的世界</a>
     </li>
     <li>
         <a href="#">总台“中国式现代化与世界新机遇”阿联酋专场研讨会在阿布扎比成功举办</a>
     </li>
</ul>

嵌套无序列表：
 <ul>
     <li>
         <a href="#">首页</a>
     </li>
     <li>
         <a href="#">论坛</a>
     </li>
     <li>
         <a href="#">关于我们</a>
         <ul>
             <li>
                 <a href="#">联系我们</a>
             </li>
             <li>
                 <a href="#">加入我们</a>
             </li>
             <li>
                 <a href="#">举报我们</a>
             </li>
         </ul>
     </li>
     <li>
         <a href="#">商城</a>
     </li>
     <li>
         <a href="#">博客</a>
     </li>
</ul>
```

> 无序列表可以用于表示一组相关的内容，如新闻列表、文章列表、商品列表、导航 等

### 2.2 有序列表

```html
<ol>
    <li>高小乐</li>
    <li>比尔盖茨</li>
    <li>巴菲特</li>
    <li>索罗斯</li>
    <li>马云</li>
</ol>
```

> 有序列表可以用于排序类的列表，如排行榜等。

### 2.3 定义列表

```html
<!-- 
	一个dt对应一个dd
-->
<dl>
    <dt>HTML</dt>
    <dd>超文本标记语言</dd>
    <dt>CSS</dt>
    <dd>层叠样式表</dd>
    <dt>JavaScript</dt>
    <dd>浏览器端脚本语言</dd>
</dl>

<!-- 
	一个dt对应多个dd 
-->
<dl>
    <dt>如何掌握一个HTML标签？</dt>
    <dd>该标签的语义功能</dd>
    <dd>该标签的属性以及属性值如何设置</dd>
    <dd>该标签是单标签还是双标签</dd>
</dl>
```

### 2.4 列表标签总结

| 标签名 | 功能和语义       | 属性 | 单标签还是双标签 |
| ------ | ---------------- | ---- | ---------------- |
| ul     | 无序列表包裹元素 |      | 双标签           |
| ol     | 有序列表包裹元素 |      | 双标签           |
| li     | 列表项           |      | 双标签           |
| dl     | 定义列表包裹元素 |      | 双标签           |
| dt     | 定义列表项标题   |      | 双标签           |
| dd     | 定义列表项描述   |      | 双标签           |

**注意：**

```
li 必须被 ul 或者 ol 直接包裹!
```





## 3 表格标签

### 3.1 表格的结构

```
table
	caption
	thead
		tr
			td/th
			....
		tr
		...
	tbody
		tr
			td/th
			...
		tr
		...
	tfoot
		tr
			td/th
			...
		tr
		...
```

```html
<table border="1">
    <!-- 表格标题 -->
    <caption>用户信息表</caption>
    <!-- 表格头 -->
    <thead>
        <tr>
            <th>序号</th>
            <th>姓名</th>
            <th>性别</th>
            <th>电话</th>
            <th>地址</th>
        </tr>
    </thead>
    <!-- 表格体 -->
    <tbody>
        <tr>
            <td>1</td>
            <td>曹操</td>
            <td>男</td>
            <td>13378652389</td>
            <td>上海市松江区</td>
        </tr>
        <tr>
            <td>2</td>
            <td>刘备</td>
            <td>男</td>
            <td>13378652388</td>
            <td>上海市浦东区</td>
        </tr>
        <tr>
            <td>3</td>
            <td>高小乐</td>
            <td>男</td>
            <td>13378652387</td>
            <td>上海市松江区</td>
        </tr>
        <tr>
            <td>4</td>
            <td>孙悟空</td>
            <td>男</td>
            <td>13378652386</td>
            <td>上海市黄浦区</td>
        </tr>
    </tbody>
    <!-- 表格脚 -->
    <tfoot></tfoot>
</table>
```

### 3.2 表格整体样式设置

给 table 标签设置如下属性：

```
width： 	设置宽度
height:  设置高度
cellspacing： 设置单元格之间的间距
cellpadding： 设置单元格内补白（边框与内容的间距）
border： 设置边框边框
```

### 3.3 设置单元格宽高

给 td、th 设置 width 和 height 属性：

```
给 td、th 设置 width 相当于设置列宽
给 td、th 设置 height 相当于设置行高 
```

给 tr 和 td 设置 height 有什么区别：

```
给 th、td 设置height，实际行高会在设置的高度的基础上加上上下的 cellpadding
给 tr 设置 height 就是总行高
```

### 3.4 设置单元格中内容对齐方式

**设置单元格内容横向对齐方式：**

```
给 thead、tbody、tfoot 设置 align 属性，属性的值： left、right、center，所包裹的单元格都会生效
给 tr 设置 align 属性，属性的值： left、right、center，所包裹的单元格都会生效
给 td、th 设置 align 属性，属性的值： left、right、center，本单元格会生效
```

**设置单元格内容纵向对齐方式：**

```
给 thead、tbody、tfoot 设置 valign 属性，属性的值： top、bottom、middle，所包裹的单元格都会生效
给 tr 设置 valign 属性，属性的值： top、bottom、middle，所包裹的单元格都会生效
给td、th 设置 valign 属性，属性的值： top、bottom、middle，本单元格会生效
```

### 3.5 单元格跨行和跨列（重要）

给 td、th 设置属性：

```
rowspan： 设置所跨行数
colspan： 设置所跨列数
```

### 3.5 表格标签总结

| 标签名  | 功能和语义   | 属性                                                         | 单标签还是双标签 |
| ------- | ------------ | ------------------------------------------------------------ | ---------------- |
| table   | 表格包裹元素 | width<br>height<br>cellspacing<br>cellpadding<br>border      | 双标签           |
| caption | 表格标题     |                                                              | 双标签           |
| thead   | 表格头       | align<br>valign                                              | 双标签           |
| tbody   | 表格体       | align<br/>valign                                             | 双标签           |
| tfoot   | 表格脚       | align<br/>valign                                             | 双标签           |
| tr      | 行           | height<br>align<br/>valign                                   | 双标签           |
| td      | 单元格       | width<br>height<br>align<br/>valign<br>colspan<br>rowspan    | 双标签           |
| th      | 表头单元格   | width<br/>height<br/>align<br/>valign<br/>colspan<br/>rowspan | 双标签           |



## 4 表单

### 4.1 表单总体设置

```html
<form action="http://www.baidu.com/s" target="_blank">
     <input type="text" name="wd">
     <button>搜索</button>
</form>
```

### 4.2 表单控件

#### ① 文本输入框

```html
<input type="text"> <br>

<!-- type 属性的默认值就是 text -->
<input> <br>

<!-- maxlength 可以限制最大输入长度 -->
<input type="text" maxlength="10">
```

#### ② 密码输入框

```html
<input type="password"> <br>
<input type="password" maxlength="6">
```

#### ③ 单选框

```html
 <input type="radio" name="gender">男
<input type="radio" name="gender">女
<input type="radio" name="gender" checked>其他
```

```
1. 多个单选框要实现单选效果，需要设置相同的 name 属性值
2. 设置 checked 属性可以实现默认选中，该属性不需要值 
```

#### ④ 复选框

```html
<input type="checkbox">唱
<input type="checkbox">跳
<input type="checkbox" checked>RAP
<input type="checkbox">打篮球
<input type="checkbox" checked>敲代码
```

```
设置 checked 属性可以实现默认选中，该属性不需要值 
```

#### ⑤ 提交按钮

```html
<input type="submit">
<input type="submit" value="免费注册">
<button type="submit">提交</button>
<button>登录</button>
```

#### ⑥ 重置按钮

```html
<input type="reset">
<button type="reset">重置</button>
```

#### ⑦ 普通按钮

```html
<input type="button" value="普通按钮01">
<button type="button">普通按钮02</button>
```

#### ⑧ 文本域

```html
<textarea rows="10" cols="60"></textarea>
```

```
rows 设置默认显示的行数，影响高度
cols 设置默认显示的列数，影响宽度
```

#### ⑨ 下拉选项

```html
<select>
    <option>江苏省</option>
    <option>安徽省</option>
    <option>河南省</option>
    <option selected>新疆维吾尔自治区</option>
    <option>内蒙古自治区</option>
    <option>广西壮族自治区</option>
</select>
```

```
默认选中的是第一个选项，可以使用 selected 设置默认选项
```

### 4.3 表单控件的属性

#### ① name 属性

```
1. name 用于给表单控件设置标识，与后端对应
2. 多个单选框要实现单选效果需要设置相同的 name
3. 下拉选项需要将 name 设置到 select 上
4. 提交按钮、重置按钮、普通按钮不要设置 name 属性
```

#### ② value 属性

```
1. 文本输入框、密码输入框，value 可以设置默认显示的内容
2. 单选框、复选框，value 设置真正提交的数据
3. input 实现的提交按钮、重置按钮、普通按钮，value 设置按钮上的文字
4. button 和 textarea 不需要 value
5. 下拉选项option可以使用value设置真正提交的数据，如果没有设置value，双标签中的文字作为提交的数据
```

#### ③ disabled 属性

```
1. 表单控件设置 disabled 属性将变为不可用
2. disabled 属性不需要值
3. select 设置disable 属性整个下拉选项不可用；option 设置 disabled 属性该选项不可选。
```





## 作业

```
1. 课堂案例
2. 表格
3. 表单
```











### 4.4 label 标签的使用

### 4.5 表单标签总结

| 标签名 | 语义和功能 | 属性 | 单标签和双标签 |
| ------ | ---------- | ---- | -------------- |
|        |            |      |                |
|        |            |      |                |
|        |            |      |                |
|        |            |      |                |
|        |            |      |                |
|        |            |      |                |
|        |            |      |                |





