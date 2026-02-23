# Day10 Express 课堂笔记

## 总结

###  http 服务

```
1. 创建服务和启动服务
2. 从请求报文中获取数据
3. 设置响应报文
```

### GET 方式和 POST方式的区别：

```
1. get 方式一般用于从服务器获取数据； post 方式一般用于像服务器提交数据
2. get 方式的请求报文没有请求体； post 方式的请求报文中有请求体
3. post 方式更安全， get 方式通过url查询字符串向服务器传递数据，完全暴露； post 方式通过请求体传递数据，默认不可见的
4. get 方式传递数据受制于url的长度， post 方式传递数据理论上没有容量限制
```

### 实现静态资源托管服务

````
1. 根据url中的pathname，拼接静态资源文件在服务器上的路径
2. 读取静态资源文件，将文件内容作为响应体
   如果静态资源文件不存在，响应 404； 如果文件读取失败，响应 500
3. 浏览器会对中文路径编码，后端程序需要使用 decodeURI() 解码
4. 响应头中设置 Content-type 指定静态资源文件的 MIME 类型
````

#### MIME 文件类型

**媒体类型**（通常称为 **Multipurpose Internet Mail Extensions** 或 **MIME** 类型）是一种标准，用来表示文档、文件或字节流的性质和格式 。

服务器应该在响应头中设置 Content-type 指定响应内容的 MIME 类型。







## 1 Express 概述

### 1.1 什么是 Express

Express 是一个基于 Node.js 平台的极简、灵活的 web 应用开发框架，它提供一系列强大的特性，帮助你快速创建各种 Web 和移动设备应用。 Express 中的**路由**和**中间件**为我们的开发带来极大便利。

简单来说， Express 就是一个第三方模块，专门用来创建 HTTP服务。

### 1.2 相关网站

* 官网： http://expressjs.com/
* 中文网：https://www.expressjs.com.cn/
* Github: https://github.com/expressjs/express

### 1.3 安装 

```bash
npm install express;
```

### 1.4 基本使用

```js
// 导入模块
const path = require('path');
const express = require('express');

// 创建 express 应用
const app = express();


// 使用内置的中间件 express.static() 托管静态文件 指定静态文件所在的目录
app.use(express.static(path.join(__dirname, 'public')));

// 匹配 GET /index.html
app.get('/index', (request, response) => {
    response.send('<h1>首页</h1>');
});

// 匹配 GET /login
app.get('/login', (request, response) => {
    response.sendFile(path.join(__dirname, 'pages', 'login.html'));
});

// 匹配 POST /login
app.post('/login', (request, response) => {
    response.send('提交成功！');
});

// 启动 http 服务指定端口
app.listen(8080, () => {
    console.log('express server is running on :8080');
});

```



## 2 路由

### 2.1 路由方法

```
app.get()		
app.post()		
app.put()
app.head()
app.delete()
app.options()
app.trace()
app.connect()
app.all()		
```

> app.all 可以匹配所有的请求方式

### 2.2 路径匹配

```
1. URL 中的 pathname 需要与路由方法进行匹配，匹配成功才能执行对应的回调函数
2. URL 中只有 pathname 参与匹配，查询字符串会被剔除
```

```js
// 精确匹配，只能匹配 /home/index
app.get('/home/index', (req, res) => {
    res.send('<h1>这里是首页</h1>' + req.url);
});

// 字符串模糊匹配
// app.get('/home(ab)?', (req, res) => {
app.get('/admin/*', (req, res) => {
    res.send('<h1>这里是字符串的模糊匹配</h1>' + req.url);
});

// 正则模糊匹配
app.get(/\.html$/, (req, res) => {
    res.send('<h1>正则的模糊匹配成功！</h1>' + req.url);
});

// URL中带参数  /news/23112  /news/abab
app.get('/news/:id', (req, res) => {
    res.send('<h1>带参数的路径！</h1>' + req.params.id);
});


// 字符串的模糊匹配 * 表示任意数量的任意字符
// 写在最后，如果前面的路由都没有匹配到 设置 404 页面
app.all('*', (req, res) => {
    res.status(404).send('<h1>404 您要找的页面不存在！</h1>');
});
```

### 2.3 路由回调函数

```js
1. 路由方法可以设置回调函数，当url与该路由匹配的时候，调用回调函数，回调函数接收两个参数，分别请求对象和响应对象
2. 一个路由方法可以设置多个回调函数
```

### 2.4 app.route()

```js
app.route('/login')
    .get((request, response) => {
        response.sendFile(path.join(__dirname, 'pages', 'login.html'));
    })
    .post((request, response) => {
        response.send('提交成功！');
    });
```





## 3 请求对象和响应对象

### 3.1 请求对象

request 对象是路由回调函数中的第一个参数，代表了用户发送给服务器的请求信息，通过 request 对象可以读取用户发送的请求包括 URL 地址中的查询字符串中的参数，和 post 请求的请求体中的参数。

#### 获取客户端 IP

```js
request.ip
```

#### 获取请求头

```js
request.get('请求头key');
```

#### 查询字符串信息

```js
request.query;  // 获取一个对象
```

#### 路径中的参数信息

```js
// 路径中的参数信息 代替 查询字符串  匹配 /news/20342323/a12.shtml
app.get('/news/:date/:id.shtml', (request, response) => {
    const data = `
    <h1>news</h1>
    <p>date： ${request.params.date}</p>
    <p>id： ${request.params.id}</p>
    `;
    console.log(request.params);  // 对象 date 和 id 是属性名
    response.send(data);
})
```

#### 获取请求体

```
request.body 必须经过中间件的处理才能获取到请求体数据解析成的对象，否则只能得到 undefined
```

```js
const bodyParser = require('body-parser');

// 创建 express 应用
const app = express();

// 使用 body-parser 解析请求体内容
app.use(bodyParser.urlencoded({ extended: false }));

app.post('/login', (request, response) => {
    console.log(request.body);  // 对象
    response.send('提交成功！');
});
```

### 3.2 响应对象

response 对象是路由回调函数中的第二个参数，代表了服务器发送给用户的响应信息，通过 response 对象可以设置响应报文中的各个内容，包括响应头和响应体。

#### 设置响应状态码

```js
response.status(404);
```

#### 设置响应头

```js
response.set('响应头key', '值');
```

#### 设置响应体

```
response.end()
response.send()				比起 end() 可以自动添加 Content-type 响应头
response.sendFile(文件地址)	  将文件中的内容读取作为响应体
response.download(文件地址)	  将文件下载
response.json()				将对象转为json字符串，进行响应
response.jsonp()			将对象转为jsonp调用形式，进行响应
response.render()			渲染模板
```

#### 重定向

```
response.redirect()			重定向
```



## 4 中间件

Express 是一个自身功能极简，完全是由路由和中间件构成一个的 web 开发框架：从本质上来说，一个 Express 应用就是在调用各种中间件。

**中间件（Middleware）** 是一个**函数**，它可以接收参数 请求对象（req)）, 响应对象（ res）, 和 web 应用中处于请求-响应循环流程中的中间件，一般被命名为 `next` 的变量。

中间件的功能包括：

- 执行任何代码。
- 修改请求和响应对象。
- 终结请求-响应循环。
- 调用堆栈中的下一个中间件。

如果当前中间件没有终结请求-响应循环，则必须调用 `next()` 方法将控制权交给下一个中间件，否则请求就会挂起。

### 4.1 应用级中间件

应用级中间件绑定在应用对象app上。中间件函数作为 app.use() 或者路由方法的回调函数。

```
1. 通过 app.use() 或者路由方法来绑定中间件
2. 路由方法的回调函数本质上就是中间件
```

### 4.2 路由级中间件

路由级中间件和应用级中间件一样，只是它绑定的对象为 `express.Router()`的返回值。

### 4.3 错误处理中间件

> 错误处理中间件有 *4* 个参数，定义错误处理中间件时必须使用这 4 个参数。即使不需要 `next` 对象，也必须在签名中声明它，否则中间件会被识别为一个常规中间件，不能处理

错误处理中间件和其他中间件定义类似，只是要使用 4 个参数，而不是 3 个，其写法如下： `(err, req, res, next)`。

```javascript
app.use(function(err, req, res, next) {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});
```

## 5 express.Router

可使用 `express.Router` 类创建模块化、可挂载的路由句柄。`Router` 实例是一个完整的中间件和路由系统，因此常称其为一个 “mini-app”。

下面的实例程序创建了一个路由模块，并加载了一个中间件，定义了一些路由，并且将它们挂载至应用的路径上。

在 app 目录下创建名为 `birds.js` 的文件，内容如下：

```javascript
var express = require('express');
var router = express.Router();

// 该路由使用的中间件
router.use(function timeLog(req, res, next) {
  console.log('Time: ', Date.now());
  next();
});
// 定义网站主页的路由
router.get('/', function(req, res) {
  res.send('Birds home page');
});
// 定义 about 页面的路由
router.get('/about', function(req, res) {
  res.send('About birds');
});

module.exports = router;
```

然后在入口文件中加载路由模块：

```javascript
var birds = require('./birds');
...
app.use(birds);
```

## 6 模板引擎

