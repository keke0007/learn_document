# Day15  Ajax  课堂笔记

## 总结

```
1. 基本使用流程
2. 发送请求
   2.1 通过URL携带数据
   2.2 通过请求体携带数据 -- 请求体是字符串
   2.3 通过请求体携带数据 -- 请求体是FormData
   2.4 设置请求头
3. 处理响应
   3.1 从响应报文中获取数据
   3.2 处理josn格式的响应体
   3.3 响应超时
4. 进度事件
5. 同步和异步
```



## 1 跨域

### 1.1 同源策略

* 同源策略是浏览器的一种安全策略。
* 同源策略要求 ajax 代码所在的页面URL中的 协议、域名、端口号与 ajax 请求的 URL 中  协议、域名、端口号保持一致
* 违反同源策略称为跨域， 实现跨域方案： **CORS**  **JSONP**

### 1.2  CORS 跨域资源共享

**1） CORS是什么？**

CORS（Cross-Origin Resource Sharing），跨域资源共享。CORS是官方的跨域解决方案，它的特点是不需要在客户端做任何特殊的操作，完全在服务器中进行处理，支持 GET、POST 等所有的请求方式。

**2）CORS怎么工作的？**

CORS 后端是通过设置一个响应头 `Access-Control-Allow-Origin` 来告诉浏览器，该请求允许跨域，浏览器收到该响应以后就会对响应放行。

### 1.3  JSONP

**1） 什么是JSONP ?**

JSONP(JSON with Padding)，是一个非官方的跨域解决方案，纯粹凭借程序员的聪明才智开发出来，只支持 GET 请求方式。

在网页有一些标签天生具有跨域能力，比如：img link iframe script，JSONP就是利用 script 标签的跨域能力来发送请求的。

**2）JSONP 使用步骤**

```js
// 1.动态的创建一个script标签
var script = document.createElement("script");

// 2.设置script的 src
script.src = "http://localhost:3000/testAJAX?callback=abc";

// 3. 定义函数
function abc(data) {
    alert(data.name);
};

// 4.将script添加到 body 中,会发送请求
document.body.appendChild(script);

// 5. 将 script 从 body 中删除
document.body.removeChild(script);
```

**3）服务端的处理**

服务端需要将 js 代码作为响应体：

```j's
var callback = req.query.callback;
var obj = {
  name:"孙悟空",
  age:18
}
res.send(callback+"("+JSON.stringify(obj)+")");
```



## 2 封装一个 Ajax 函数

```js
/*  
            选项：
            url： 请求地址
            method： 请求方式，默认值 GET
            headers: 请求头，默认值 {}
            body： 请求体
            dataType: 响应体类型
            success: 成功的回调
            error: 失败的回调
*/
function ajax(options) {
    // 从 options 取出相关的选项
    const {url, method='GET', headers={}, body, dataType, success=()=>{}, error=()=>{}} = options;

    // 创建 xhr 对象
    const xhr = new XMLHttpRequest();

    // 如果指定了 dataType
    if (dataType) {
        xhr.responseType = dataType;
    }

    // 监听响应成功的事件
    xhr.onload = () => {
        if (xhr.status === 200) {
            success(xhr.response);
        } else {
            error();
        }
    }

    // 监听响应失败的事件
    xhr.onerror = error;

    // 请求初始化
    xhr.open(method, url);

    // 设置请求头
    for (let key in headers) {
        xhr.setRequestHeader(key, headers[key]);
    }

    // 发送
    xhr.send(body);


}
```



## 3 Ajax 记账本

### 3.1 数据请求API

```
获取指定用户的账单： GET  	/api/account/用户ID
给指定用户添加账单： POST 	/api/account/用户ID
删除账单：		  DELETE   /api/account/账单ID
```

### 3.2 流程

```
1. 发起请求获取该用户的账单信息
2. 添加账单
   ① 点击按钮 弹出表单
   ② 填写表单点击提交按钮，监听了表单提交事件，自己处理，阻止默认提交
   ③ 提交事件触发之后，使用formdata获取表单的内容，formdata作为请求体，发送请求
   ④ 当后端确定添加成功之后，重新请求数据，清空原来的，添加新的
3. 删除账单
   ① 事件委托给删除按钮监听事件，提前使用自定义属性保存账单ID
   ② 点击删除按钮之后，发送请求删除
   ③ 确定后端删除成功之后，删除元素
   
```



