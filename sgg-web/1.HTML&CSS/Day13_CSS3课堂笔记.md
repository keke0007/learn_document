

# Day13 CSS3 课堂笔记

## 1 回顾

```
1. CSS3 选择器
   1.1 基本选择器（6个）
   1.2 层级选择器（4个）
       后代元素、子元素、相邻兄弟、通用兄弟
   1.3 属性选择器（5个）
       [attr] [attr="val"] [attr^="val"] [attr$="val"] [attr*="val"]
   1.4 伪类选择器（23个）
       ① 动态伪类（5个）
         :link :visited :hover :active :focus
       ② 目标伪类（1个）
         :target
       ③ 语言伪类（1个）
         :lang()
       ④ UI元素伪类（表单伪类）（3个）
         :enabled :disabled :checked
       ⑤ 结构伪类（12个）
         child系列
         of-type系列
         :root :empty
       ⑤ 否定伪类(1个)
         :not(选择器)
     1.5 伪元素选择器
         ::first-letter ::first-line  ::before ::after ::placeholder ::selection
     1.6 权重
         ID > 类、伪类、属性 > 标签名、伪元素
 
2. 新增的盒子相关样式
   ① display
   ② box-sizing： content-box/border-box
   ③ box-shadow
   ④ opacity
   ⑤ 粘连定位 position: sticky
```



## 2 CSS3 新增背景属性

**旧标准已有的背景属性：**

```
background-color
background-image
background-repeat
background-position
background-attachment
```

### 2.1 新增属性

#### ① background-origin

该属性可以设置背景图像定位的原点，属性值如下：

```
padding-box		原点在内边距上左上角，默认值
border-box		原点在边框上左上角
content-box		原点在内容上左上角
```

#### ② background-clip

该属性可以设置背景图像的显示区域，属性值如下：

```
border-box		显示在边框以及以内，默认值
padding-box		显示在内边距以及以内
content-box		显示在内容区域
text			指显示在文本上，chrome浏览器需要私有前缀
```

#### ③ background-size 

该属性可以设置背景图像的尺寸，属性值设置规则如下：

```
1. 设置两个长度，分别表示背景图像的宽度和高度
2. 设置一个长度，表示背景图像的宽度，高度根据比例自动计算
3. 关键字 contain 表示背景图像尺寸自动适配元素，优先保证背景图像显示完整
4. 关键字 cover 表示背景图像尺寸自动适配元素，优先保证元素上铺满该背景图，可能造成背景图像显示不完整。
```

### 2.2 background 复合属性

```
1. content-box/padding-box/border-box 这样的值在复合属性中设置一个，同时设置 origin 和 clip
   这样的值如果设置了两个，第一个是 origin 第二个是 clip
2. background-size 的值必须写在 position 的后面,使用 / 分隔
```

```css
/* content-box 同时设置了 origin 和 clip */
background: url(../images/jd001.jpg) content-box;

/* origin的值是content-box， clip的值是padding-box */
background: url(../images/jd001.jpg) content-box padding-box;

/*  position 的值是 0 0， size 的值是 500px 100px */
background: url(../images/jd001.jpg) content-box padding-box 0 0/500px 100px;
```

### 2.3 多背景图

```css
background-color: #ccc;
background-image: url(../images/bg-tl.png), url(../images/bg-tr.png);
background-repeat: no-repeat;
background-position: left top, right top;

background: url(../images/bg-tl.png) no-repeat left top, 
            url(../images/bg-tr.png) no-repeat right top,
            url(../images/bg-bl.png) no-repeat left bottom,
            url(../images/bg-br.png) no-repeat right bottom,
            url(../images/bg05.jpg) center/cover;
```

> 如果位置重合，先写的背景图像会显示在上层！



## 3 CSS3 新增边框属性

### 3.1 边框圆角

| CSS 属性名                 | 含义       | 值                  |
| -------------------------- | ---------- | ------------------- |
| border-top-left-radius     | 左上角圆角 | 1~2个长度           |
| border-top-right-radius    | 右上角圆角 | 1~2个长度           |
| border-bottom-left-radius  | 左下角圆角 | 1~2个长度           |
| border-bottom-right-radius | 右下角圆角 | 1~2个长度           |
| border-radius              | 多个角圆角 | 1~4个长度/1~4个长度 |

**单个圆角属性值的设置规则：**

```
1. 设置一个长度，同时设置 x 半径和 y 半径
2. 设置两个长度，第一个是 x 半径，第二个是 y 半径
```

**复合属性的使用：**

```css
/* 每个角x半径和y半径一致 */
/* 同时设置4个角 */
border-radius: 20px;
/* 左上和右下  左下和右上 */
border-radius: 10px 100px;
/* 左上 左下和右上 右下 */
border-radius: 10px 100px 50px;
/* 左上 右上 右下 左下 */
border-radius: 10px 30px 50px 80px;
```

```css
/*每个角 x 半径 和 y 半径不一定一致 */

/* 
	/ 左边都是 x 半径，可以写 1 ~ 4 个长度， 
	/ 右边都是 y 半径，可以写 1 ~ 4 个长度， 
	两边长度的数量不要求一致，各自计算各自的。
*/

/* 分被设置 x 半径和 y 半径 */
border-radius: 100px / 10px;

/*  
	左上和右下x半径:100px; 左下和右上x半径:30px /  左上y半径:10px; 左下和右上y半径:40px; 右下y半	径:50px  
*/
/* 左上:100px 10px;  右上:30px 40px;  右下:100px 50px; 左下:30px 40px */
border-radius: 100px 30px / 10px 40px 50px;
```

### 3.2 外轮廓

| CSS 属性名     | 含义                                  | 值                 |
| -------------- | ------------------------------------- | ------------------ |
| outline-style  | 外轮廓风格                            | 同border-style     |
| outline-width  | 外轮廓宽度                            | 长度               |
| outline-color  | 外轮廓颜色                            | 颜色               |
| outline        | 复合属性                              | 多个值使用空格分隔 |
| outline-offset | 与边框的距离<br>不是 outline 的子属性 | 长度，可以是负值   |

**外轮廓与边框的区别：**

```
外轮廓不是盒子的一部分，不影响元素的尺寸和位置！
```



## 4 CSS3 新增文本属性

| CSS 属性名                | 含义                     | 值                                                           |
| ------------------------- | ------------------------ | ------------------------------------------------------------ |
| text-align-last           | 最后一行文本水平对齐方式 | start：靠文字起始方向对齐，默认自。<br>end：靠文字结束方向对齐。<br>left：靠左对齐。<br>right：靠右对齐。<br>center：居中对齐。<br>justify：两端对齐。 |
| text-decoration-line      | 文本修饰线的类型         | none：无。<br>underline：下划线。<br>overline：上划线。<br>line-throuth：删除线。 |
| text-decoration-style     | 文本修饰线风格           | solid：实线。<br>dashed：虚线。<br>dotted：点线。<br>double：双实线。<br>wavy：波浪线。 |
| text-decoration-color     | 文本修饰线颜色           | 颜色                                                         |
| text-decoration           | 文本修饰线复合属性       | 多个值使用空格分隔                                           |
| word-wrap / overflow-wrap | 是否允许单词内部断行     | normal：不允许。<br>break-wrod：允许。                       |
| white-space               | 文本显示格式             | normal：默认值。<br>pre：原格式显示。<br>pre-wrap：pre基础上+自动换行。<br>pre-line：normal基础上+识别换行符。<br>nowrap：强制显示成一行 |
| text-overflow             | 溢出文本显示省略号       | clip：默认值。<br>ellipsis：显示省略号。                     |
| text-shadow               | 文本阴影                 | 阴影偏移、模糊值、颜色                                       |

**单行长文本显示省略号：**

```
1. 强制将文字显示在一行中
2. 设置溢出部分隐藏
3. 设置溢出文本显示成省略号
```

```css
 /* 将文本强制显示到一行 */
white-space: nowrap;
/* 溢出部分隐藏 */
overflow: hidden;
/* 显示省略号 */
text-overflow: ellipsis;
```

**text-shadow 文本阴影的设置规则：**

```
可以设置阴影偏移位置、阴影模糊值和阴影颜色
```

```css
/* 阴影偏移 */
text-shadow: 3px 3px; 
/* 阴影偏移 颜色 */
text-shadow: 4px 4px #999;
text-shadow: #900 4px 4px;
/* 阴影模糊值 */
text-shadow: 3px 3px 5px;
text-shadow: 3px 3px 15px rgba(0,0,0,.5);

/* 多阴影 */
text-shadow: 1px 1px #bbb, 
            2px 2px #aaa, 
            3px 3px #999,
            4px 4px #888,
            5px 5px #777,
            6px 6px #666;
```



## 5 CSS3 渐变

渐变是一个值，要作为一个图片被使用，可以使用渐变作为值的属性有 `background-image`、`list-style-image` 等。

### 5.1 线性渐变

```
linear-gradient(渐变方向，颜色列表)
```

```
1. 渐变方向
   ① 使用关键字，如 to bottom、to left、to top bottom、to right top ...
   ② 使用角度，取值 0 ~ 360，角度单位是deg

2. 颜色列表
   每个颜色之间使用逗号分隔
   每个颜色可以指定颜色位置，如果不指定位置，多个颜色位置平均分布
```

### 5.2 径向渐变（了解）

```
radial-gradient(半径 at 圆心位置，颜色列表)
```

### 5.3 重复渐变

```
repeating-linear-gradient()    重复线性渐变
repeating-radial-gradient()	   重复径向渐变
```



## 6 Filter 滤镜

```css
filter: 滤镜函数(参数);
```

| 滤镜函数      | 描述                                                         |
| :------------ | :----------------------------------------------------------- |
| blur()        | 设置模糊，值是长度，值越大越模糊，百分比无效。               |
| brightness()  | 设置亮度，值是数字或者百分比，0全黑，1无效果，可以比1大，默认1。 |
| saturate()    | 设置饱和度，值是数字或者百分比，0完全不包含，1无效果，可以比1大，默认1。 |
| contrast()    | 设置对比度，值是0~1之间的数字或者百分比，0全灰，1无效果，可以比1大，默认1。 |
| grayscale()   | 设置灰度，使用0~1之间的数字或百分比，值越大灰度越高，0无效果，1灰度最高，默认0 |
| sepia()       | 设置深褐色度，使用0~1之间的数字或百分比，值越大深褐色度越高，0无效果，1灰度最高，默认0 |
| hue-rotate()  | 设置色相旋转，值是0~360deg之间的角度                         |
| invert()      | 设置反转，使用0~1之间的数字或百分比，0无效果，1彻底反转，默认0 |
| opacity()     | 设置不透明度，使用0~1之间的数字或百分比，0完全不透明，1彻底透明，默认0 |
| drop-shadow() | 设置阴影，需要设置偏移位置、模糊值、颜色                     |
| url()         | 使用svg设置滤镜                                              |

```
blur()				模糊
grayscale()			灰度
```



## 7 WEB 字体

### 7.1 web 字体基本语法

```css
/* 声明 web 字体 */
@font-face {
    font-family: 'diyfont';
    src: url('diyfont.eot'); /* IE9兼容模式 */
    src: url('diyfont.eot?#iefix') format('embedded-opentype'), /* IE9 - */
         url('diyfont.woff') format('woff'), /* chrome、firefox opera  safari  IE9+ 最佳格式 */
         url('diyfont.ttf') format('truetype'), /* chrome、firefox、opera、Safari, Android, iOS 4.2+ IE9+*/
         url('diyfont.svg#fontname') format('svg'); /* iOS 4.1- */
}


/* 使用 web 字体 */
.box {
    font-family: "diyfont";
}
```

**字体格式的转换工具：**

- https://www.fontsquirrel.com/tools/webfont-generator FontSquirrel在线工具
- https://www.fontke.com/tool/fontface/ 字客网

**字体定制工具：**

- https://www.iconfont.cn/webfont?spm=a313x.7781068.0.d81ec59f2#!/webfont/index 阿里Web字体
- http://www.youziku.com/ 字体库网站
- https://www.ziti163.com/webfont/create.aspx 字体网

### 7.2 字体图标

#### ① 阿里图标

地址：  http://www.iconfont.cn/

#### ② font-awesome

地址：http://fontawesome.dashgame.com/

#### ③ 字体图标制作工具 icoMoon

地址： http://icomoon.io/app/#/select









## 作业

```
1. 渐变文字
2. 发廊灯 黑白条纹
```





