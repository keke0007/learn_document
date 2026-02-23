# Day14 DOM 课堂笔记

## 1 回顾 元素操作

```
1. 属性操作
   1.1 读写内置属性
   1.2 getAttribute() setAttribute()
   1.3 data-形式的自定义属性

2. 样式操作
   2.1 读写行内样式
   2.2 读取计算样式
   2.3 类名操作
       className 内置属性
       classList add() remove() toggle() contains()

3. 读写元素的内容(可读可写)
   innerHTML
   outerHTML
   innerText
   textContent

4. 读取元素的尺寸(只读)
   offsetWidth / offsetHeight
   clientWidth / clientHeight
   scrollWidth / scrollHeight
   getBoundingClientRect()  width height

5. 读取元素的位置(只读)
   offsetLet / offstTop
   clientLeft / clientTop
   getBoundingClientRect()   left top x y right bottom

6. 读写元素中内容滚动的位置（可读可写）
   scorllLeft
   scrollTop

7. 元素的创建、添加、删除、替换、克隆
   7.1 创建元素
       document.createElement()
   7.2 添加元素
      父元素.appendChild(新元素)
      父元素.insertBefore(新元素，旧元素)
   7.3 删除元素
      父元素.removeChild(元素)
   7.4 替换元素
      父元素.replaceChild(新元素， 旧元素)
   7.5 克隆元素
      元素.cloneNode(true)

```



## 2 HTML DOM

### 2.1 表单相关元素

#### ① form 元素

```
length		获取该表单中表单控件的数量
elements    获取该表单中表单控件元素的集合

submit()	执行该方法表单会提交
reset()     执行该方法表单会重置
```

#### ② 文本输入框类和文本域（input 和 textarea）

```
blur()		执行该方法会失去焦点
focus()		执行该方法会获取焦点
select()	执行该方法会选中里面的文字
```

#### ③ select 元素

```
length				获取到选项的数量
options				获取到所有选项元素的集合
selectedIndex		获取当前被选中的选项的索引

add(option元素)		添加一个新的选项
remove(选项的索引)	  删除指定索引的选项
blur()				 执行该方法会失去焦点
focus()				 执行该方法会获取焦点
```

**快速创建 option 元素的方式：**

```js
new Option('内容'， 'value值')
```

### 3.2 表格相关元素 

#### ① table 元素

```
rows			获取所有行元素的集合

insertRow(索引)	添加一行，如果不设置参数添加到最后
deleteRow(索引)	删除一行
```

#### ② tableRow 元素（tr 元素）

```
rowIndex		本行的索引
cells			获取本行中单元格元素的集合

insertCell(索引)	添加一个单元格，，如果不设置参数添加到最后
deleteCell(索引)	删除一个单元格
```

#### ③ tableCell 元素 （td 或 th）

```
cellIndex		本单元格的索引（同一行内）
```

### 3.3 快速创建 img 元素

```js
new Image();
new Image(width, height);
```







## 3 事件

### 3.1 事件监听

#### ① 给元素监听事件的三种方式

**第一种方式： 事件作为HTML标签的属性：**

```html
<标签名 on事件名="代码..."></标签名>
```

```
相同的事件如果设置多次，只有前面的生效！
```

**第二种方式： 事件作为元素对象的方法：**

```js
元素对象.on事件名 = 回调函数;
```

```
相同的事件如果设置多次，最后面的生效！
```

**第三种方式：使用 addEventListenrer 方法：**

```js
元素对象.addEventListener('事件名', 回调函数);
```

```
相同的事件如果设置多次，都可以生效！
```

#### ② 解除事件的监听

**第一种和第二种方式监听的事件：**

```js
元素对象.on事件名 = null;
```

**第三种方式监听的事件：**

```js
元素对象.removeEventListener('事件名', 函数名);
```

### 3.2 事件流

事件触发的过程分为三个阶段：

**捕获阶段：** 从 window、document 、html 开始层层向下，直到找到具体发生了事件动作的元素，该元素称为目标元素。

**目标阶段：** 找到目标元素的那一刻，标志着捕获阶段的结束，冒泡阶段的开始。

**冒泡阶段：** 从目标元素开始，层层向上，直到 html、document、window， 事件的回调函数默认在冒泡阶段执行。

> 注意：事件流也可以只分为捕获阶段和冒泡阶段。
>
> 注意： addEventListener 设置第三个参数为 true，该事件会在捕获阶段触发！

### 3.3 事件的回调函数中 this 的指向

```
this 指向事件监听的元素！
```













