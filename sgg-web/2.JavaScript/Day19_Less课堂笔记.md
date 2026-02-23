# Day19 Less 课堂笔记

## 1 Less 的使用

### 1.1 使用 less.js 编译 less

```html
<style type="text/less">
        @fcolor: #900;
        @bcolor: #099;
        @len: 1000px;

        #box {
            width: @len;
            height: (@len/4);
            color: @fcolor;
            background: @bcolor;
            padding: 20px;
        }
</style>
<script src="./less.js"></script>
```

### 1.2 使用 vscode 插件自动编译 less

```
1. vscode 安装扩展 "Easy Less"
2. 创建扩展名是 .less 的文件，在文件中写 less 代码； Easy Less 会自动编译成同名的CSS； 每次保存都会自动编译。
3. html 中使用 link 引入 css 文件
```

## 2 Less 语法

### 2.1 Less 的注释

```less
/* 这是 CSS 注释,会原样编译到 CSS 中 */
// 这是 LESS 注释，不会编译到 CSS 中
```

 ### 2.2 Less 的变量

#### ① 定义变量

**定义变量的一般形式：**

```less
@变量名:值;

@len: 600px;
@master-red: #900;
@master-green: #080;
@sencond-red: #600;
```

**如果变量的值有特殊符号：**

```less
@变量名:~"值";

@min768: ~"min-width:768px";
@min992: ~"min-width:992px";
@sel02: ~".news li";
```

#### ② 使用变量

**将变量作为属性值使用（大部分应用场景）：**

```less
// 直接使用 @变量名
width: @len;
color: @master-green;
background: @master-red;
border: 1px solid @master-green;

@media (@min768) {
    .container {
        width: 100%;
    }
}
```

**将变量作为属性名或者选择器使用：**

```less
// @{变量名}

.box {
    // 变量作为属性名
    @{prop}: 10px 10px;
}

// 变量名作为选择器
@{sel01} {
    width: @len;
    height: (@len/2);
}
```

### 2.3 Less 混合 (mixins)

#### ① 混合

**定义混合：**

```less
.center-box01() {
    position: absolute;
    width: 400px;
    height: 300px;
    left: 50%;
    top: 50%;
    margin-left: -200px;
    margin-top: -150px;
}
```

**使用混合：**

```less
.item {
    // 调用混合
    .center-box01();
}

.news li {
    // 调用混合
    .center-box01();
    // 其他样式
    background: #900;
    border: 1px solid #999;
}
```

#### ② 带参数的混合

**定义带参数的混合：**

```less
// 定义混合 有参数
.center-box02(@width, @height) {
    position: absolute;
    width: @width;
    height: @height;
    left: 50%;
    top: 50%;
    margin-left: -(@width/2);
    margin-top: -(@height/2);
}
```

**使用有参数的混合：**

```js
// 调用有参数的混合 按照顺序传参数
.center-box02(600px,500px);

 // 调用有参数的混合 按照名字传参
.center-box02(@height:600px, @width:700px);
```

#### ③ 参数有默认值的混合

```less
// 定义混合 参数设置默认值
// 有默认值的参数在后面
// 可以按照顺序传参，也可以按照名字传参
.center-box03(@width, @height：800px) {
    position: absolute;
    width: @width;
    height: @height;
    left: 50%;
    top: 50%;
    margin-left: -(@width/2);
    margin-top: -(@height/2);
}

// 有默认值的参数在前面后面都可以
// 只能按照名字传参
.center-box04(@width：1200px, @height) {
    position: absolute;
    width: @width;
    height: @height;
    left: 50%;
    top: 50%;
    margin-left: -(@width/2);
    margin-top: -(@height/2);
}
```

#### ④ @arguments

```js
// @arguments 获取参数列表
.box-shadow(@x, @y, @b, @o, @color) {
    -webkit-box-shadow: @arguments;
    -moz-box-shadow: @arguments;
    -o-box-shadow: @arguments;
    box-shadow: @arguments;
}

.box {
    width: 400px;
    height: 300px;
    background: #900;
    .box-shadow(3px, 10px, 15px, 0px, #ccc);
}
```

### 2.4 Less 条件判断

```less
.triangle(@border-width, @color, @direction) when (@direction=up) {
    width: 0;
    height: 0;
    border-style: solid;
    border-width: @border-width;
    border-color: transparent transparent @color transparent;
}

.triangle(@border-width, @color, @direction) when (@direction=down) {
    width: 0;
    height: 0;
    border-style: solid;
    border-width: @border-width;
    border-color: @color transparent transparent transparent;
}
 
.triangle(@border-width, @color, @direction) when (@direction=left) {
    width: 0;
    height: 0;
    border-style: solid;
    border-width: @border-width;
    border-color: transparent @color transparent transparent;
}

.triangle(@border-width, @color, @direction) when (@direction=right) {
    width: 0;
    height: 0;
    border-style: solid;
    border-width: @border-width;
    border-color: transparent transparent transparent @color;
}
```

### 2.5 Less 导入

**导入 less 文件：**

```js
// 将 文件名.less 中的内容编译到 css 中
@import "文件名.less";

// 可以省略扩展名
@import "文件名"
```

**导入 css 文件**:

```less
// 原样编译到 css 中
@import "文件名.css";
```



### 2.6 Less 嵌套

#### ① 基本使用(层级选择器)

```less
.news {
    li {}
    >li {}
    +li {}
    ~li {}
}
```

**编译为：**

```css
.news {}
.news li {}
.news > li {}
.news + li {}
.news ~ li {}
```

#### ② & 符号应用（交集选择器组合）

```less
.item {
    &:hover {}
    &.active {}
}
```

**编译为：**

```css
.item {}
.item:hover {}
.item.active {}
```

#### ③ 媒体查询的嵌套

```less
.container {
    width: 100%;
    margin-left: auto;
    margin-right: auto;

    @media (min-width:768px) {
        width: 750px;
    }

    @media (min-width: 992px) {
        width: 970px;
    }

    @media (min-width: 1200px) {
        width: 1170px;
    }
}
```

**编译为：**

```css
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}
@media (min-width: 768px) {
  .container {
    width: 750px;
  }
}
@media (min-width: 992px) {
  .container {
    width: 970px;
  }
}
@media (min-width: 1200px) {
  .container {
    width: 1170px;
  }
}
```

#### ④ 混合和嵌套结合

```less
.clearfix() {
    &::after {
        content: "";
        display: block;
        clear:both;
    }
}
```

### 2.7 Less 运算符

```
1. Less 可以进行 +、-、*、/ 运算
2. 除运算需要使用小括号
3. 如果两个操作数单位不一致，结果使用第一个操作数的单位
   如果只有一个操作数有单位，结果就使用该单位
```

### 2.9 Less 函数

```
percentage()		计算百分比	
mod()				取余运算
lighten()			颜色调高亮度
darken()			颜色调低亮度
```

https://less.bootcss.com/functions/









