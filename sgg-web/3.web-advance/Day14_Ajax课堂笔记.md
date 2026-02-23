# Day14  Ajax  课堂笔记

 Ajax 全称为 Asynchronous Javascript And XML，就是异步的 JavaScrript 和 XML。 

## 1 原生 Ajax — 使用 xhr 对象

### 1.1 基本使用流程

```js
 // 第一步 创建 XMLHttpRequest 对象
const xhr = new XMLHttpRequest();

// 第二步 监听接响应成功的事件
xhr.onload = () => {
    console.log('成功接收到后端的响应！');
    box.innerHTML += xhr.responseText + '<br>';
};


// 第三步 请求初始化
/*
   第一个参数 请求方式
   第二个参数 请求URL
   第三个参数 是否异步，默认异步
*/
xhr.open('GET', '/getData');

// 第四步 发送请求
/*
  参数可以设置请求体，没有请求可以不设置参数
*/
xhr.send();
```

### 1.2 发起请求携带数据

#### 1.4.1 通过 URL 携带数据

> 所有的请求方式都可以通过 URL 携带数据

```js
// 定义查询字符串
const qs = `username=${nameInp.value}&userpwd=${pwdInp.value}`;
// 请求初始化 将携带的数据以查询字符串的形式拼接到 URL 中
xhr.open('GET', '/addData?'+qs)
// 发送请求
xhr.send();
```

#### 1.2.2 通过请求体携带数据

> POST、PUT 等方式可以通过请求体携带数据

```js
// 定义查询字符串
const qs = `username=${nameInp.value}&userpwd=${pwdInp.value}`;

// 初始化
xhr.open('POST', '/addData');

// 设置请求头  请求头一定要在 open() 之后，send() 之前设置
// 通过请求头 Content-type，告知后端请求体的类型
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

// 发送请求，请求体必须是字符串
xhr.send(qs)
```

#### 1.2.3 请求体内容类型

##### text/plain

```
1. 默认的请求体类型，如果不设置请求头字段 Content-type，默认就是该种类型
2. 请求体只要是字符串就可以，后端不会做任何处理
```

**application/x-www-form-urlencoded**

```
1. 需要设置请求头 xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
2. 要求请求体是查询字符串，如 a=100&b=200
3. 点击提交按钮提交表单（非Ajax），如果 Method 是 Post，默认请求体内容就是 x-www-form-urlencoded
```

**application/json**

```
1. 设置设置请求头 xhr.setRequestHeader('Content-type', 'application/json');
2. 要求请求体是 json 格式的字符串
```

**multipart/form-data**

```
参加 FormData 小节
```

### 1.3 FormData

#### ① 使用 FormData 对象作为请求体

```
1. 请求体（send()的方法的参数）除了是字符串，也可以是 formData 对象
2. 如果请求体是 FormData 对象，浏览器会自动设置请求头字段 Content-type 为 multipart/form-data
```

```js
// 方式一 创建 空的 FormData，再添加数据，可以添加文件数据或者字符串数据
var fd = new FormData();
fd.append('message', msgInput.value);
fd.append('content', 'hello ajax');

// 方拾二 根据表单元素创建 FormData 会包含表单中所有的信息
var fd = new FormData(formElement);
```

#### ② FormData 对象的方法

```
append()
set()
delete()
get()
getAll()
```

#### ③ FormData 实现文件上传

```js
// 方式一 创建 空的 FormData，再添加数据，可以添加文件数据
var fd = new FormData();
fd.append('avator', avatorInput.files[0]);


// 方拾二 根据表单元素创建 FormData 会包含表单中所有的信息
var fd = new FormData(formElement);
```

### 1.4 读取响应报文

```js
// 响应行
xhr.status;			// 响应状态码
xhr.statusText;		// 响应状态描述

// 响应头
xhr.getResponseHeader('响应头字段');		// 获取指定字段的响应头的信息
xhr.getAllResponseHeaders();		   // 获取所有的响应头信息

// 响应体
xhr.responseText;		// 获取响应体体符串
xhr.response;			// 获取响应体字符串，如果响应体是特殊格式的字符串，会进行处理
```

### 1.5 响应 json 格式的数据

#### 1.5.1 服务端设置

设置响应头，告知浏览器响应体的内容类型是 json 格式

```
Content-type: application/json;charset=utf-8
```

#### 1.5.2 客户端处理接收到的 json 数据

##### ① 方式一 使用 JSON.parse

```js
// 监听响应结束的回调函数、
xhr.onload = function() {
    // 将响应体中 json 格式的字符串处理成对象
    var resData = JSON.parse(xhr.responseText);
}
```

##### ② 方式二 设置 xhr.responseType 属性 ，通过 xhr.response获取 

```js
xhr.responseType = 'json';
xhr.onload = function() {
    xhr.response;		// 直接得到处理好的对象
}
```

### 1.6 响应超时

#### 1.6.1 方案一 兼容方案（了解）

```js
// 发送请求
xhr.send();

// 发送请求之后，设置单次定时，如果时间到了还没有接收到响应，中断请求
setTimeout(function(){
    // 判断如果没有响应结束
    if (xhr.readyState !== 4) {
        xhr.abort();  // 中断请求
        alert('请求超时！');
    }
}, 5000);
```

#### 1.6.2 案二 XHR2 方案

```js
 // 监听响应超时的事件
xhr.ontimeout = function(){
    alert('响应超时！');
}

// 请求初始话
xhr.open('GET', '/getInfo');

// 发送请求之前设置超时时间
xhr.timeout = 5000;

// 发送
xhr.send();
```

### 1.6 HTTP 进度事件

#### 1.6.1 进度相关事件

```
readystatechange	触发至少 4 次
loadstart			开始请求的时候触发，此时 readyState 的值是 1
load				响应结束的时候触发，此时 readyState 的值是 4，请求成功触发
error				请求失败触发，应用层面的错误也算是请求成功（如 404错误），只有网络错误才算请求失败
loadend				响应结束之后触发，不论请求是否成功都会触发
progress			开始接收响应内容之后，被触发多次，该事件的回调函数可以获取一个 progressEvent 对象
```

> **相关事件的触发顺序：** loadstart、progress（可能会触发多次）、 load/error、loadend

#### 1.6.2 ProgressEvent 事件对象

progress 事件的回调函数可以获取一个 progressEvent 对象，该对象有如下属性：

```
loaded		表示当前已经下载的字节数
total		表示响应内容的总长度
```

### 1.7 异步请求和同步请求

**两者区别：**

```
1. 异步请求，请求发送之后，其他同步操作继续执行； 当获取响应之后触发回调函数，回调函数进入回调队列等待主线程空闲执行
2. 同步请求，请求发送之后，其他的同步操作必须等到，响应结束之后才能继续执行
```

**如何发送同步请求：**

```
open() 方法的第三个参数是布尔值，true 表示异步请求，false 表示同步请求，默认值是 true。
```

## 1.8 总结

```
1. 设置请求报文
   请求体：字符串、formData
   请求体字符串三种格式： 无格式、querystring、json

2. 解析响应报文
   响应状态码  响应状态描述
   响应体
   响应体是json格式的字符串
   设置响应超时
   

3. 监听进度事件
   readystatechange
   loadstart  
   progress
   load
   error
   loadend

```





## 2 XMLHttpRequest 对象总结

#### ① XHR 对象概述

1）XMLHttpRequest 对象简称 **XHR** 对象。

2）XMLHttpRequest 对象提供了对 HTTP 协议的完全的访问，包括做出 POST 和 HEAD 请求以及普通的 GET 请求的能力。

3）XMLHttpRequest 可以同步或异步地返回 Web 服务器的响应，并且能够以文本或者一个 DOM 文档的形式返回内容。

4）尽管名为 XMLHttpRequest，它并不限于和 XML 文档一起使用，它可以接收任何形式的文本文档。

#### ② 创建 XHR 对象

使用构造函数 XMLHttpRequest 就可以创建一个 XHR 对象。

```js
const xhr = new XMLHttpRequest()；
```

注意：在古老的 IE 浏览器中（如：IE6），需要使用其他方式来创建 XHR 对象。

```js
// IE5、IE6
let xhr = new ActiveXObject("Microsoft.XMLHTTP");
```

#### ③ XHR 对象的属性

| 属性名       | 含义                                                         |
| ------------ | ------------------------------------------------------------ |
| readyState   | 返回一个数字，表示请求的状态：<br>0 -- UNSET -- XHR对象已创建或已被 abort() 方法重置。 <br>1 -- OPENDED -- `open()` 方法已经被调用。<br>2 -- HEADERS_RECEIVED -- `send()` 方法已经被调用，并且响应头和响应状态已经可获得。 <br>3 -- LOADING -- 下载中， `responseText` 属性已经包含部分数据。 <br>4 -- DONE -- 所有响应数据接收完毕。 |
| status       | 响应状态码，如 404、200 等。                                 |
| statusText   | 响应状态码的文本描述，如 200 对应的是 “OK”。                 |
| responseXML  | 接收格式为 XML 的响应数据，返回一个 document 对象。          |
| responseText | 获取响应文本，返回一个字符串。                               |
| responseType | 用于设置响应内容的类型 *xhr2*                                |
| response     | 返回的类型取决于 responseType 的设置。 *xhr2*                |
| timeout      | 设置超时时间。*xhr2*                                         |

#### ④ XHR 对象的方法

| 方法名                  | 含义                                                         |
| ----------------------- | ------------------------------------------------------------ |
| open()                  | 初始化 HTTP 请求，用来指定请求方式和 URL。 `xhr.open(method, url, [async], [user], [password])` |
| send()                  | 发送 HTTP 请求，参数可以设置请求体，没有请求体无需设置参数。 |
| setRequestHeader()      | 设置 HTTP 请求头的值。必须在 `open()` 之后、`send()` 之前调用。 |
| abort()                 | 如果请求已被发出，则立刻中止请求。                           |
| getAllResponseHeaders() | 以字符串形式返回所有的响应头。                               |
| getResponseHeader()     | 返回指定的响应头。                                           |

#### ⑤ XHR 对象的事件

| 事件名           | 含义                                                         |
| ---------------- | ------------------------------------------------------------ |
| readystatechange | readyState 属性值发生变化触发该事件。                        |
| abort            | 请求终止时触发。                                             |
| error            | 请求遇到错误时触发。**注意**，只有发生了网络层级别的异常才会触发此事件。 |
| loadstart        | 接收到响应数据时触发。 *xhr2*                                |
| load             | 请求成功完成时触发。*xhr2*                                   |
| loadend          | 当请求结束时触发, 无论请求成功 ( `load`) 还是失败 (`abor` 或 `error`)。*xhr2* |
| progress         | 当请求接收到更多数据时，周期性地触发。*xhr2*                 |
| timeout          | 在预设时间内没有接收到响应时触发。*xhr2*                     |











## 3 跨域

### 3.1 同源策略

* 同源策略是浏览器的一种安全策略。
* 要求 ajax 代码所在的页面URL中的 协议、域名、端口号与 ajax 请求的 URL 中  协议、域名、端口号保持一致
* 解决同源策略，进行跨域： **CORS**  **JSONP**

### 3.2  CORS 跨域资源共享

```
在服务端进行设置
添加一个响应头，设置允许的 域名

Access-Control-Allow-Origin: http://localhost:8080   
# 允许前面页面的域名是http://localhost:8080，才能跨域

Access-Control-Allow-Origin：*
# 允许所有的域名都可以跨域
```

### 3.3  JSONP

#### 实现思路

```
实现基础：
	利用 script 标签也可以发送请求，天然支持跨域， script 会把响应到的内容作为 js 代码执行

实现步骤：（前端）
	1. 创建 script 标签
	2. 指定 script 标签的 src 属性值，src 的属性值就是请求地址， 把函数名通过url中的查询字符串传给后端
	3. 把 script 标签添加到 body 中
	4. 再把 script 标签从 body 中移除
	5. 定义获取数据的函数，该函数会被后端响应的内容调用，把数据传进来
	注意： 在 script 添加到 body 中的瞬间，发起请求，接收响应，调用了函数
	
	
实现步骤：（后端）
	1. 从 url 中的查询字符串里取出函数名
	2. 响应体内容是 js 代码，调用函数的js代码，把数据变为json格式作为函数的参数
	3. 做出响应

```

#### JSONP 缺点

```
只支持 GET 请求
```


