# Day11 Express 课堂笔记

## 回顾

```
1. 内置模块
   path url querystring fs

2. 自定义模块
   模块内部暴露数据
   导入模块

3. npm包管理工具

4. http协议

5. 内置 http 模块

6. express
   6.1 创建服务 启动服务
   6.2 路由
   6.3 请求对象和响应对象
```





## 1 中间件

Express 是一个自身功能极简，完全是由路由和中间件构成一个的 web 开发框架：从本质上来说，一个 Express 应用就是在调用各种中间件。

**中间件（Middleware）** 是一个**函数**，它可以接收参数 ：请求对象、 响应对象、 调用下一个中间件的函数。

中间件的功能包括：

- 执行任何代码。
- 修改请求和响应对象。
- 结束响应。
- 调用堆栈中的下一个中间件。

如果当前中间件没有结束响应，则必须调用 `next()` 方法将控制权交给下一个中间件，否则请求就会挂起。

### 1.1 应用级中间件

应用级中间件绑定在应用对象app上，中间件函数作为 app.use() 或者路由方法的回调函数。

```
1. 通过 app.use() 或者路由方法来绑定中间件
2. 路由方法的回调函数就是中间件
```

**定义访问日志中间件:**

1. 创建 accesslog.js，作为单独模块，定义中间件的代码

```js
const moment = require('moment');
const fs = require('fs');
const path = require('path');

module.exports = (req, res, next) => {
    // 从请求报文中获取信息
    const ip = req.ip.slice(7);
    const method = req.method;
    const url = req.url;
    const dt = moment().format('YYYY-MM-DD HH:mm:ss');
    
    // 拼接日志内容
    const logMsg = `${ip} ${dt} ${method} ${url}\n`;
    console.log(logMsg);

    // 写入文件
    fs.appendFile(path.resolve(__dirname, '../logs/access.log'), logMsg, err => {
        if (err) {
            throw err;
        }
        // 成功写入日志 放行
        next();
    });
};
```

2. 在应用的入口文件挂载中间件

```js
// 导入自定义中间件
const accessLog = require('./middleware/accesslog');

// 创建服务
const app = express();

// 在所有路由方法的前面
// 挂载访问日志中间件
app.use(accessLog);
```

### 1.2 错误处理中间件

> 错误处理中间件有 *4* 个参数，定义错误处理中间件时必须使用这 4 个参数。即使不需要 `next` 对象，也必须声明它，否则中间件会被识别为一个常规中间件，不能处理错误。
>
> 错误处理中间件需要挂载在所有路由和中间件的后面，如果路由回调函数或前面的中间件中出现错误，会自动进入错误处理中间件！

错误处理中间件和其他中间件定义类似，只是要使用 4 个参数，而不是 3 个，其写法如下： `(err, req, res, next)`。

```javascript
app.use(function(err, req, res, next) {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});
```

**定义一个错误处理中间件，响应500，且记录错误日志**

创建文件 catcherror.js，作为一个模块，代码如下：

```js
const moment = require('moment');
const fs = require('fs');
const path = require('path');

module.exports = (err, req, res, next) => {
    // 从请求报文中获取信息
    const ip = req.ip.slice(7);
    const method = req.method;
    const url = req.url;
    const dt = moment().format('YYYY-MM-DD HH:mm:ss');
    
    // 拼接日志内容
    const errMsg = `${ip} ${dt} ${method} ${url} \n ${err.stack} \n\n\n\n`;

    // 写入文件
    fs.appendFile(path.resolve(__dirname, '../logs/error.log'), errMsg, err => {
        if (err) {
            throw err;
        }
    });

    // 响应 500
    res.status(500).send('<h1>500 服务器出错！</h1>');
};
```

在应用的入口文件挂载中间件

```js
// 导入自定义中间件
const catchError = require('./middleware/catcherror');

// 创建服务
const app = express();

// 在所有路由方法的后面
// 挂载访问日志中间件
app.use(catchError);
```

### 1.3 路由级中间件

路由级中间件和应用级中间件一样，只是它绑定的对象为 `express.Router()`的返回值，路由级中间件可以实现路由的模块化。



## 2 express.Router 路由模块化

可使用 `express.Router` 类创建模块化、可挂载的路由系统。`Router` 实例是一个完整的中间件和路由系统，因此常称其为一个 `mini-app`。

下面的实例程序创建了一个路由模块，并加载了一个中间件，定义了一些路由，并且将它们挂载至应用的路径上。

**实现路由模块化：**

创建路由文件 index.js:

```js
// 导入模块
const express = require('express');

// 创建路由对象
const route = express.Router();

// 路由
route.get('/', (req, res) => {
    res.redirect('/index');
});

// 路由
route.get('/index', (req, res,next) => {
    res.send(`
    <h1>首页</h1>
    <hr>
    <a href="/login">登录</a>
    `);
});

// 将路由对象作为暴露数据
module.exports = route;


```

创建路由文件 login.js

```js
// 导入模块
const express = require('express');

// 创建路由对象
const route = express.Router();


// 路由
route.get('/', (req, res) => {
    res.send(`
    <h1>登录</h1>
    <hr>
    <form action="/login" method="post">
        <input placeholder="请输入用户名" type="text" name="username">
        <input placeholder="请输入密码" type="password" name="userpwd">
        <button>提交</button>
    </form>
    `);
});

// 路由
route.post('/', (req, res) => {
    res.send('<h2>提交成功！</h2>');
});

// 将路由对象作为暴露数据
module.exports = route;
```

在入口文件中，将路由文件挂载到应用上：

```js
// 导入路由模块
const indexRouter = require('./routes/index');
const loginRouter = require('./routes/login');

// 挂载路由模块
app.use(indexRouter);  //
app.use('/login', loginRouter);  // 挂载路由 指定路径
```





## 3 Express 使用模板引擎

### 3.1 模板引擎设置

```js
//1. 设置 express 所使用的模板引擎 会根据这里的设置自动引入模板引擎，无需再写 require()
app.set('view engine', 'ejs');

//2. 设置模板文件的存放目录
app.set('views', path.join(__dirname, 'pages'));
```

### 3.2 渲染

```js
app.get('/', function (req, res) {
  // 会在模板文件的存放目录中查找 index.ejs 文件
  res.render('index', { title: 'Hey', message: 'Hello there!'});
});
```

### 3.3 修改模板文件扩展名

```js
const ejs = require('ejs');

//1. 更改模板引擎名字为 html
app.engine('html', ejs.renderFile);
//2. 设置 express 所使用的模板引擎 
app.set('view engine', 'html');
//3. 设置模板文件的存放目录
app.set('views', path.join(__dirname, 'pages'));
```



## 4 EJS 模板引擎

执行语句

```ejs
<% code %>
```

```ejs
<% top.forEach(item => { %>
    <tr>
        <td><%= item.id %></td>
        <td><%= item.name %></td>
        <td><%= item.money %> 亿美元</td>
    </tr>
<% }) %>
```

输出转义的数据到模板上

```ejs
<%= code %>
```

```js
<p class="alert alert-warning">
    <%= Date.now() %> <br>
    <%= Math.random() %> <br>
    <%= 10 * 7 + 8 %> <br>
</p>
```

输出非转义的数据到模板上

```ejs
<%- code %>
```

```
<%= code %> 如果 code 的值中有html标签，会被转义成字符实体，原样显示
<%- code %> 如果 code 的值中有html标签，浏览器会解析处理
```



## 5 Express 项目生成器  express-generator 

**全局安装：**

```shell
npm install -g express-generator
```

**运行命令生成目录结构并指定模板引擎为 ejs：**

```shell
express --view=ejs
```

**安装依赖:**

```shell
npm install
```

**启动项目：**

```shell
npm start
```

> 注意不要直接运行入口文件！



## 6 记账本项目

```
第一步： 使用 express-generator 创建目录结构并安装依赖
	   express --view=ejs
	   npm install

第二步： 设计路由
      GET /  				    重定向到 /account
      GET /account			    展示账单列表
      GET /account/create       添加表单页面
      POST /account/create  	执行添加
      GET  /account/delete/:id  执行删除	
   
第三步： 模板和静态资源设置
	  1. 将账单相关模板文件放入 views 下的 account 目录中
	  2. 将模板所需要的css、js 放入静态资源目录 public
	  3. 路由回调函数渲染对应的模板
	  
第四步： 添加账单记录
      1. get  /account/create 
         给表单控件设置 name, 给 form 设置 method 和 action
      2. post /account/create  
         取出请求体
         使用 shortid 创建唯一 id
         将id和请求体里的数据添加到 lowdb 中（提取进行手动初始化）
         渲染 success 模板
         
第五步： 账单列表
       get /account
       1. 从lowdb中取出所有账单
       2. 渲染模板，向模板发送数据
       3. 在模板中展示数据
          遍历
          三元运算符
          双向分支
          
 第六步： 删除指定的账单
       1. 在列表页模板中设置超级链接，将id拼接到路径中
       2. get /account/delete/:id
          获取id
          根据id从lowdb中删除对应的记录
          渲染 success 模板
       
         
```

