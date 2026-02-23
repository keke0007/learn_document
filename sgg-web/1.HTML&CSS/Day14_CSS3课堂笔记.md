# Day14 CSS3 课堂笔记

## 1 回顾

```
1. 背景
   1.1 新增3个背景属性
       background-origin
       background-clip
       background-size
    1.2 复合属性
    1.3 多背景图

2. 边框
   2.1 边框圆角
       ① 设置单个角圆角
       ② 同时设置多个角圆角
   2.2 外轮廓
       outline-style outline-color outline-widht outline outline-offset

3. 文本样式
   text-align-last
   text-decoration-line
   text-decoration-style
   text-decoration-color
   text-decoration
   overflow-wrap
   white-space
   text-overflow
   text-shadow

4. 渐变
   4.1 线性渐变 linear-gradient()
   4.2 径向渐变 radial-grdient() 
   4.3 重复渐变 repeating-linear-gradient() repeating-radial-grdient() 

5. 滤镜
   filter: blur() / grayscale()

6. WEB字体
   6.1 @font-face
   6.2 定制字体
   6.3 字体图标
```





## 2 变换 transform

### 2.1 变换相关 CSS 属性

| CSS 属性名          | 含义                             | 值                                                           |
| ------------------- | -------------------------------- | ------------------------------------------------------------ |
| transform           | 设置变换方法                     | 变换方法                                                     |
| transform-origin    | 设置变换原点                     | 使用关键字设置。<br>使用坐标设置                             |
| transform-style     | 设置子元素的空间维度             | flat：子元素在平面空间中，默认值。<br>preserve-3d：子元素在3D空间中。 |
| perspective         | 设置观察者距离（透视距离、景深） | 长度                                                         |
| perspective-origin  | 设置观察者位置                   | 使用关键字设置。<br/>使用坐标设置。                          |
| backface-visibility | 设置元素背面是否可见             | visible：可见，默认值。<br>hidden：不可见。                  |

```
注意：行内元素设置变换无效!
```

```
需要设置给变换元素本身：	transform、transform-origin、backface-visibility
需要设置给变换元素的父元素： transform-style、perspective、perspetive-origin
```

```
变换原点如果只设置一个值，另一个值默认为center。
```

### 2.2 2D 变换的方法

#### ① 位移 translate 方法

```
translateX()		x方向位移
translateY()		y方向位移
translate()			同时设置x方向和y方向位置，需要两个值，如果只有一个值表示只进行x方向位移
```

**位移的变换方法参数的设置规则：**

```
使用长度作为位移方法的参数
如果使用百分比，x方向参照元素自身宽度，y方向参照元素自身高度
```

#### ② 缩放 scale 方法

```
scaleX()			x方向缩放
scaleY()			y方向缩放
scale()				同时设置x方向和y方向的缩放，需要两个值，如果只有一个值同时设置x方向和y方向
```

**缩放的变换方法参数的设置规则：**

```
使用数字设置缩放方法的参数
```

#### ③ 旋转 rotate 方法

```
rotate()			
```

**变换方法参数的设置规则：**

```
使用角度设置旋转
```

### 2.3 3D 变换的方法

#### ① 3D 位移

```
translateZ()		z轴方向位移
translate3D()		同时设置x方向、y方向、z方向的位移，必须三个值
```

#### ② 3D 缩放

```
scaleZ()		z轴方向方法
scale3D()       同时设置x方向、y方向、z方向的缩放，必须三个值
```

```
受限于平面的屏幕，3D缩放目前没有任何效果
```

#### ③ 3D 旋转

```
rotateX()		沿着x轴旋转
rotateY()		沿着y轴旋转
rotateZ()		远着z轴旋转，等同于2d旋转 rotate()
rotate3D()		沿着多个轴一起旋转
```

```css
rotate3D()	前三个参数对应x轴、y轴、z轴是否旋转，取值0和1； 第四个参数设置旋转角度
```



## 3 过渡 transition

### 3.1 过渡相关 CSS 属性

| CSS 属性名                 | 含义                 | 值                                                           |
| -------------------------- | -------------------- | ------------------------------------------------------------ |
| transition-duration        | 过渡持续时间         | 时间单位：s、ms                                              |
| transition-delay           | 过渡延迟时间         | 时间单位：s、ms                                              |
| transition-property        | 设置哪些样式可以过渡 | all：能过渡都过渡，默认值<br>指定属性名，多个使用逗号分隔。  |
| transition-timing-function | 过渡的运动曲线       | 曲线运动、分步运动                                           |
| transition                 | 过渡复合属性         | 多个值使用空格分隔<br>一个时间表示持续时间<br>两个时间，第一个持续，第二个延迟 |

**哪些 CSS 属性可以过渡？**

```
1. 属性值是长度，如 width、height、padding、margin、border-width、background-position 等
2. 属性值是颜色，如 color、background-color、border-color 等
3. 属性值是数字，如 z-index、opacity 等
4. 变换 transform、滤镜 filter 
```

**什么时候设置过渡相关的属性 transition**

```
在样式变化之前就将过渡相关属性设置好！
```

**transition-timing-function 设置过渡运动曲线：**

```
ease			平滑运动，先加速后减速，默认值
linear			匀速运动
ease-in			加速运动
ease-out		减速运动
ease-in-out 	先加速后减速
cubic-bezier() 	贝塞尔曲线
steps()			分步运动，第一个参数必须为正整数，指定函数的步数。第二个参数取值可以是start或end，指定每			  	一步的值发生变化的时间点。第二个参数是可选的，默认值为end。 
step-start		steps(1, start)
step-end		steps(1, end)
```

**贝塞尔曲线在线工具：**

 https://cubic-bezier.com

### 3.2 触发过渡的条件

```
1. CSS 伪类选择器， :hover、:active、:focus、:checked 等
2. CSS 媒体查询
3. JavaScript 事件
```



## 4 动画 animation

### 4.1 关键帧

```css
@keyframes 关键帧名字 {
    from {}
    to {}
}

@keyframes 关键帧名字 {
    0% {}
    100% {}
}

@keyframes 关键帧名字 {
    from {}
    40%{}
    80%{}
    to {}
}

@keyframes 关键帧名字 {
    100% {}
}
```

**关键帧与元素的关系：**

```
1. 一个元素可以设置多个关键帧
2. 一个关键帧也可以设置给多个元素
```

### 4.2 动画相关 CSS 属性

| CSS 属性名                | 含义                   | 值                                                           |
| ------------------------- | ---------------------- | ------------------------------------------------------------ |
| animation-name            | 设置关键帧             | 关键字名字，多个使用逗号分隔                                 |
| animation-duration        | 动画持续时间           | 时间单位：s、ms                                              |
| animation-delay           | 动画延迟时间           | 时间单位：s、ms                                              |
| animation-timing-function | 动画运动曲线           | 曲线运动、分步运动                                           |
| animation-iteration-count | 动画执行次数           | 数字，infinite表示无限次                                     |
| animation-direction       | 动画运动方向           | normal：默认值。<br>reverse：反向。<br>alternate：交替运动。<br>alternate-reverse：反向交替。 |
| animation-play-state      | 动画运动状态           | running：正在运动。<br>paused：暂停运动                      |
| animation-fill-mode       | 动画开始前和结束后状态 | none：默认值。<br>forwards：结束后处于结束帧样式。<br>backwards：开始前处于起始帧样式。<br>both：同时设置forwards和backwards |
| animation                 | 动画复合属性           | 多个值使用空格分隔<br/>一个时间表示持续时间<br/>两个时间，第一个持续，第二个延迟 |



## 作业

```
1. 过渡：幽灵按钮
2. 过渡：第二个过渡案例
3. 动画：自行车手
4. 动画：loading动画
5. 3D变换： 立方体（选做）
```







