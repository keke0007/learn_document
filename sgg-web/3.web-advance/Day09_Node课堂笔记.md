# Day09 Node 课堂笔记

## 回顾

```
1. npm 包管理工具
   npm init
   
   npm install 
   inp i
   
   npm install 包名
   npm i 包名
  npm install 包名 -D
   npm i 包名 -D
   npm isntall 包名 -g
   npm i 包名 -g
   
   npm remove 包名
   
   npm update 包名
   npm outdated 包名
   
   npm cache clean --force
   
2. page.json
   入口文件
   script
   产品依赖
   开发依赖
   
3. cnpm yarn cyarn npx

4. 网络协议相关概念
   IP地址、域名
   端口号
   URL
   
5. HTTP协议
   5.1 请求报文
   	   请求行	请求方式、URL、协议版本
   	   请求头  键值对
   	   空行
   	   请求体  载荷
   
   5.2 响应报文
       响应行	响应状态码 响应状态描述 协议版本
       响应头  键值对
       空行
       响应体  给客户端的内容
  
```





## 1 http 服务

### 1.1 创建服务

写一个程序，该程序可以接收到客户端浏览器的请求，并能为客户端浏览器做出响应； 该程序是后端程序，运行在服务器上，需要 node 的支持。

```js
// 导入模块
const http = require('http');

/*
    1. 创建 http 服务的方法的参数是个回调函数
    2. 回调函数在接收到请求的时候自动执行
    3. 回调函数在执行的时候，接收到两个参数，分别是请求对象，响应对象
    4. createServer 方法返回一个对象
*/
const server = http.createServer((req, res) => {
    console.log('我接收到了一个请求！ 客户端IP：', req.socket.remoteAddress);
    // 设置响应
    res.end('<h1>Welcome to My WebSite</h1>');
});

// 启动服务 给http服务对象监听端口, 服务启动成功，回调函数就执行
// 端口号如果是 80，浏览器中的地址可以省略端口号
server.listen(8080, () => {
    console.log('http server is running on 8080');
});

// 第二个参数可以设置 ip
// server.listen(8080, '127.0.0.1', () => {
//     console.log('http server is running on 8080');
// });

/*
   注意：
   1. 修改代码之后，要重新启动服务，先 ctrl+c 结束，再重新运行
   2. 如果端口号被占用，可以换一个端口或者关闭占用端口的进程

*/
```

```
1. http 对象， 导入的 http 内置模块
2. http.Server 对象， http.createServer() 的返回值
3. http.clientRequest 对象， http.createServer() 的回调函数的第一个参数
4. http.serverResponse 对象， http.createServer() 的回调函数的第二个参数
```

**注意：如果启动服务的时候，报错提示端口被占用，可以采用下面两种方案来解决：**

1）给我们的程序换个端口

2）把占用端口的其他程序关闭

- windows cmd 命令行中运行命令 `netstat -ano | findstr 端口号` 来获取占用端口的程序的进程ID
- 资源管理器->详细信息，根据进程ID找到程序，右键选择结束任务。

### 1.2 获取请求报文信息

#### 获取请求行的信息

```js
请求对象.method
请求对象.url	获取到 url中的 pathname 部分和查询字符串部分，不包括协议、主机名、端口号、锚点
请求对象.httpVersion
```

#### 获取请求头信息

```js
请求对象.headers
```

#### 获取客户端 IP 地址

```js
请求对象.socket.remoteAddress
```

#### 获取 URL 中的查询字符串

```js
// 第一种方式 解析url
const url = require('url');

const urlInfo =  url.parse(req.url, true);
console.log(urlInfo.query);
```

```js
// 第二种方式 解析 url
const {URL} = require('url');

// 需要手动拼接成完整的url，否则会报错
const urlInfo = new URL('http://127.0.0.1/' + req.url);
console.log(urlInfo.searchParams);
// 使用 get 方法获取相应的信息
console.log(urlInfo.searchParams.get('a'));
console.log(urlInfo.searchParams.get('b'));
```

> get、post、put、delete 等所有的请求方式，都可以在url中拼接查询字符串！

#### 获取请求体信息

```js
 // 给请求对象监听 data 事件   请求对象本质上就是以读取流
req.on('data', chunk => {
    // += 会让 buffer 自动转为 string
    reqBody += chunk;
});

// 给请求对象监听 end 事件， 读取完毕触发该事件
req.on('end', () => {
  	reqBody;  // 是查询字符串格式，可以使用 querystring 模块处理成对象
});
```

> 只有 post、put 等请求方式才能有请求体，get 、delete 等方式没有请求体！

### 1.3 设置响应报文

#### 设置响应行

```js
响应对象.statusCode = 响应状态码
响应对象.statusMessage = 响应状态描述
```

#### 设置响应头

```js
响应对象.setHeader('键', '值');
```

```js
// 同时设置 响应状态码 响应状态描述 响应头
响应对象.writeHead(响应状态码, '响应状态描述', {
    '键':'值',
    '键':'值',
    '键':'值',
})
```

#### 设置响应体

```js
响应对象.write('内容')；
响应对象.write('内容')；
响应对象.write('内容')；
```

#### 结束响应

```js
// 结束响应
响应对象.end();

// 向响应体写入内容并结束响应
响应对象.end('<hr><h2>结束<h2>');
```





## 2 http 服务案例

### 2.1 根据路径不同做出不同响应

```js
/*
    http://127.0.0.1:8080/           首页
    http://127.0.0.1:8080/login      登录页    
    http://127.0.0.1:8080/register    注册页
    其他                              404
*/
// 导入模块
const http = require('http');
const url = require('url');

// 创建服务
const server = http.createServer((req, res) => {
    // 获取到 url 中的路径名部分
    const pathname = url.parse(req.url).pathname;

    // 根据路径名不同做出不同的响应
    switch (pathname) {
        case '/':
        case '/index':
            res.setHeader('Content-type', 'text/html;charset=utf-8');
            res.end('<h1>首页</h1><hr><a href="/login">登录</a> <a href="/register">注册</a>');
            break;
        case '/login':
            res.setHeader('Content-type', 'text/html;charset=utf-8');
            res.end('<h1>登录</h1>');  
            break;
        case '/register':
            res.setHeader('Content-type', 'text/html;charset=utf-8');
            res.end('<h1>注册</h1>');  
            break;
        default:
            res.writeHead(404, 'Not Found', {
                'Content-type': 'text/html;charset=utf-8'
            });
            res.end('<h1>404 您访问的页面不存在的！</h1><a href="/">返回首页</a>');
    }
});

// 启动服务
server.listen(8080, () => {
    console.log('http server is runing on 8080');
});
```

### 2.2 根据请求方式不同做出不同的响应

```js
/*
    所有请求方式 / 或者 /index    响应首页
    get方式 /login          加载登录页面
    post方式 /login         执行登录
    其他路径             404
*/


// 导入模块
const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');
const qs = require('querystring');

// 创建服务
const server = http.createServer((req, res) => {
    // 获取到 url 中的路径名部分
    const pathname = url.parse(req.url).pathname;

    // 根据路径和请求方式判断 做出不同的响应
    if (pathname === '/' || pathname === '/index') {
        const resBody = `
        <h1>首页</h1>
        <hr>
        <a href="/login">登录</a>
        `;
        res.writeHead(200, 'OK', {
            'Content-type': 'text/html;charset=utf-8'
        });
        res.end(resBody);
    } else if (pathname === '/login' && req.method === 'GET') {
        // 读取文件 login.html
        fs.readFile(path.resolve(__dirname, './login.html'), (err,data) => {
            if (err) {
                res.writeHead(500, 'Internal Server Error', {
                    'Content-type': 'text/html;charset=utf-8'
                });
                res.end('<h1>500 服务器错误！</h1>');
            } else {
                res.end(data);
            }
        });
    } else if (pathname === '/login' && req.method === 'POST') {
        // 接收表单提交的数据
        let reqBody = '';
        req.on('data', chunk => {
            reqBody += chunk;
        });
        // 读取请求体完毕
        req.on('end', () => {
            // 解析请求体
            const body = qs.parse(reqBody);
            
            // 定义响应内容
            let resBody = '';
            // 执行模拟登录
            if (body.username === 'admin' && body.pwd === '123456') {
                // 登录成功
                resBody = '<p>登录成功！ <a href="/">返回首页</a></p>';
            } else {
                // 登录失败
                resBody = '<p>登录失败！ <a href="/login">重新登录</a></p>';
            }

            // 作出响应
            res.writeHead(200, 'OK', {
                'Content-type': 'text/html;charset=utf-8'
            });
            res.end(resBody);

        });
    } else {
        res.writeHead(404, 'Not Found', {
            'Content-type': 'text/html;charset=utf-8'
        });
        res.end('<h1>404 页面不存在！</h1>');
    }


});

// 启动服务
server.listen(8080, () => {
    console.log('http server is runing on 8080');
});

```

### 2.3 静态文件服务器