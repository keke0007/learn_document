# Day08 Node&Npm 课堂笔记

## 回顾

```
1. commonJS
   1.1 模块中暴露数据
   	   module.exports
   	   exports
   1.2 如何导入模块（引用模块）
       require()  返回值就是模块暴露的数据
   1.3 模块文件的扩展名
       .js .json .node 其他 目录
       模块路径省略扩展名
       
2. esm
   2.1 暴露数据
       ① 暴露单个数据
       export defalut 数据;
       ② 暴露多个数据
         export 变量声明语句
         export 变量声明语句
         export 变量声明语句
         或者
         export {变量名,变量名,变量名,变量名}
    2.2 导入模块
        ① 如果模块暴露单个数据
          import 变量名 from '模块名'
        ② 如果模块暴露多个数据
          import {变量名,变量名} from ‘模块名’
          import * as 变量名 from ‘模块名’
     2.3 开启 esm 模块规则
         方式一： 脚本扩展改为 .mjs
         方式二： pakeage.json 配置 {"type":"module"}
         
  3. 模块的路径 文件的路径
     文件的路径，使用相对路径 参照命令行所在的目录
     模块的路径，使用相对路径 参照所在文件的目录，跟命令行所在目录无关！
     

```



## 2 NPM

### 2.1 NPM 的作用

通过 NPM 可以对 Node 的工具包进行搜索、下载、安装、删除、上传。借助别人写好的包，可以让我们的开发更加方便。

常见的使用场景有以下 3 种：

- 允许用户从NPM服务器下载别人编写的第三方包到本地使用。
- 允许用户从NPM服务器下载并安装别人编写的命令行程序到本地使用。 
- 允许用户将自己编写的包上传到NPM服务器供别人使用。

### 2.2 NPM 操作

```bash
# 查看版本
npm -v

# --------------------------------------------
# 初始化
npm init
# 快速初始化
npm init -y    
npm init --yes 

# --------------------------------------------
# 安装包
npm install 包名     # 默认添加到产品依赖  项目本身会用到的依赖
npm i 包名
npm install 包名 -D  # 添加到开发依赖  只有开发工程中会用到，项目本身用不到
npm i 包名 -D


# --------------------------------------------
# 全局安装  主要安装命令行工具
npm install 包名 -g
npm install 包名 --global

# --------------------------------------------
# 安装指定的版本
npm install 包名@版本号
npm install 包名@版本号 -g

# --------------------------------------------
# 删除包
npm remove 包名
npm remove 包名 -g

# --------------------------------------------
# 更新包
npm update 包名
npm update 包名 -g
# 查看哪些包可以更新
npm outdated
npm outdated -g

# --------------------------------------------
# 安装依赖
npm install   # 根据package.json 安装所需依赖
npm i

# --------------------------------------------
# 清除缓存
npm cache clean --force        # force 表示强制清除

```

### 2.3 package.json

```json
{
  "name": "01-project",		// 包名
  "version": "1.0.0",		// 版本
  "description": "",		// 描述信息
  "main": "index.js",	    // 入口文件
  "scripts": {				// 可执行的名
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",				// 作者信息
  "license": "ISC",			// 开源许可
  "dependencies": {			// 依赖信息
     "bootstrap": "^5.1.3",
     "jquery": "^3.6.0"
  }，
  "devDependencies": {		// 开发中的依赖
     "babel": "^6.23.0"
  }
}
```

**版本号信息：**

- "^3.0.0" ：锁定大版本，以后安装包的时候，保证包是3.x.x版本，x默认取最新的。
- "~3.1.x" ：锁定小版本，以后安装包的时候，保证包是3.1.x版本，x默认取最新的。
- "3.1.1" ：锁定完整版本，以后安装包的时候，保证包必须是3.1.1版本。

**package-lock.json 文件**

该文件记录包具体的版本信息，用于锁定版本。

**配置命令别名：**

配置 package.json 中的 `scripts` 属性：

```json
{
    "scripts": {
        "server": "node server.js",
        "start": "node index.js",
    },
}
```

配置完成之后，可以使用别名执行命令：`npm run server` 和 `npm run start`

### 2.4 模块的查找过程

```js
require('模块名')
```

```js
1. 先确定模块名路径是不是以 ./ 或者 ../ 开头，如果不是就认为是内置模块或者第三方模块
2. 再确定有没有该内置模块，如果有该内置模块直接加载；如果没有该内置模块，判定为第三方模块
3. 第三方模块加载过程：
   ① 先从脚本本就所在的目录中查找有没有 node_modules 目录，如果有进入查找模块
   ② 如果脚本同级目录没有 node_modules 目录，去上级目录查找 node_modules 目录，如果有进入查找模块
   ③ 以此类推，一直查找到 根目录
```

### 2.4 远程仓库与 npm 一起使用 的工作流程

```
前提：
	仓库中将 node_modules 忽略，只同步 package.json

上班第一天：
	1. 从远程仓库克隆到本地
	2. 进入项目目录，运行 npm install 安装依赖
	3. 进行后续开发
	4. 下班之前推送
	
以后上班每一天：	
	1. 从远程仓库拉取
	2. 进入项目目录，运行 npm install 安装依赖 （同事可能会安装了新的依赖）
	3. 进行后续开发
	4. 下班之前推送
```

### 2.5 配置命令别名

配置 package.json 中的 `scripts` 属性：

```json
{
    "scripts": {
        "server": "node server.js",
        "start": "node index.js",
    },
}
```

配置完成之后，可以使用别名执行命令：

```bash
npm run server
npm run start
```

不过 `start` 别名比较特别，使用时可以省略 `run`

```bash
npm start
```

> 补充说明：
>
> - `npm start` 是项目中常用的一个命令，一般用来启动项目
> - `npm run` 有自动向上级目录查找的特性，跟 `require` 函数也一样
> - 对于陌生的项目，我们可以通过查看 `scripts` 属性来参考项目的一些操作



### 3.4 cnpm

使用国内的镜像作为 npm 源

方式一：全局安装 cnpm 命令，安装完成后使用 `cnpm ` 命令代替 `npm` 命令。

```bash
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

方式二：通过添加 `npm` 参数 `alias` 一个新命令，安装完成后使用 `cnpm ` 命令代替 `npm` 命令。

```bash
alias cnpm="npm --registry=https://registry.npm.taobao.org \
--cache=HOME/.npm/.cache/cnpm \
--disturl=https://npm.taobao.org/dist \
--userconfig=HOME/.cnpmrc"
```

方式三：把官方镜像地址修改为淘宝镜像地址，修改后继续使用 `npm 命令`。

```bash
# 设置为淘宝镜像
npm config set registry https://registry.npm.taobao.org

# 如果想改回官方镜像   
npm config set registry https://registry.npmjs.org/
```

> 修改了镜像地址之后，直接用 `npm` 命令就可以了。

### 3.5 yarn

yarn 命令是 facebook 退出的可以代替 npm 的命令行工具

yarn 相比于 npm 有几个特点：

- 本地缓存。安装过的包下次不会进行远程安装
- 并行下载。一次下载多个包，而 npm 是串行下载
- 精准的版本控制。保证每次安装跟上次都是一样的

### 3.6 cyarn

yarn 也可以使用淘宝镜像

```bash
npm install cyarn -g --registry "https://registry.npm.taobao.org"
```

### 3.7 npx

`npx` 是 `npm 5.2+` 版本中自带的一个命令行工具，用于执行依赖包中的可执行文件。它的作用是在不安装全局包的情况下，使用依赖包中的命令行工具。

举个例子，如果你想要使用 `create-react-app` 创建一个新的 React 应用程序，你可以使用以下命令：

```bash
npx create-react-app my-app
```



## 4 发布 npm 包

### 4.1 发布步骤

**第一步 本地开发好包内容**

1. `npm init` 进行初始化
2. 开发包的内容， `module.exports` 暴露数据

**第二步 注册账号并在命令行登录**

1.  npmjs.org 官网注册账号
2.  命令行登录账户  `npm login`

> 如果修改过官方的镜像地址，得改回来  `npm config set registry https://registry.npmjs.org/`

**第三步 发布**

1. 发布 `npm publish`

2. 如果要更新，先修改 package.json 中的版本号，再发布

### 4.2 发布全局命令

第一步 创建命令行执行的脚步文件，第一行代码写 `#!/usr/bin/env node`。

```js
#!/usr/bin/env node
/*
	这里是运行命令时候要执行的代码
*/
```

第二步 在 `package.json` 文件中配置 `bin` 字段

```js
"bin": {
     "命令名": "刚才创建的脚步文件路径"
}
```



# 5 HTTP 协议

HTTP（hypertext transport protocol）协议；中文叫 超文本传输协议，是一种基于TCP/IP的应用层通信协议吗，这个协议详细规定了 `浏览器` 和 万维网 `服务器` 之间互相通信的规则协议中主要规定了两个方面的内容:

- 客户端：用来向服务器发送数据，可以被称之为 请求报文
- 服务端：向客户端返回数据，可以被称之为 响应报文

### 5.1 请求报文

```
POST https://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/I5TOD9K40001899O/comments?ibc=newspc&_=1685348594866 HTTP/1.1
Host: comment.api.163.com
Connection: keep-alive
Content-Length: 342
sec-ch-ua: "Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"
Accept: application/json, text/plain, */*
Content-Type: application/x-www-form-urlencoded
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36
sec-ch-ua-platform: "Windows"
Origin: https://comment.tie.163.com
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://comment.tie.163.com/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,en-US;q=0.6
Cookie: nts_mail_user=fmuncle@163.com:-1:1; _n

content=%E7%89%9B%E9%80%BC%EF%BC%81%E8%B5%9E%EF%BC%81%E5%8E%89%E5%AE%B3%EF%BC%81&originalContent=牛逼！赞！厉害！&ntoken=2e4db38d-2dd8-4dc2-97f5-dd39e528794b&token=9ca17ae2e6ffcda170e2e6eeacf33af8acb7a9b63f91868aa2c54b878b9e86c5649cb5a1d1c83df38ebf8df52af0feaec3b92a869e97d9cc7ab89ca198e65b928f9fa6c55f909e00a8ea33ace7c087d972afb9ee9e
```

请求报文四部分组成： 请求行、请求头、空行、请求体

#### ① 请求行

**请求方式：** 包括 GET、POST、PUT 方式等，更多 https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods

**URL：** 统一资源定位符，确定具体请求的资源

**协议版本：** http1.1

#### ② 请求头

请求头是键值对结构，用于标记客户端相关的信息，更多请求头：https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers

#### ③ 空行

用于分隔请求头和请求体

#### ④ 请求体

向后端发送的数据，请求体可以为空

### 5.2 响应报文

```
HTTP/1.1 200 OK
Server: Tengine
Content-Type: text/html; charset=utf-8
Content-Length: 330076
Connection: keep-alive
Date: Mon, 29 May 2023 07:45:58 GMT
Last-Modified: Mon, 29 May 2023 07:45:01 GMT
Vary: Accept-Encoding
Expires: Mon, 29 May 2023 07:46:28 GMT
Cache-Control: no-cache,no-store,private
P3P: CP=CAO PSA OUR
Ali-Swift-Global-Savetime: 1685346358
Via: cache79.l2cn3036[47,47,200-0,M], cache24.l2cn3036[49,0], vcache1.cn4730[0,0,200-0,H], vcache1.cn4730[2,0]
Age: 29
X-Cache: HIT TCP_MEM_HIT dirn:10:364746730
X-Swift-SaveTime: Mon, 29 May 2023 07:45:58 GMT
X-Swift-CacheTime: 30
cdn-src-ip: 116.238.99.140
X-Cache-Remote: HIT
cdn-ip: 58.215.47.197
cdn-source: ali
cdn-user-ip: 116.238.99.140
x-server-ip: 58.215.47.197
Timing-Allow-Origin: *
EagleId: 3ad72f1516853463874755901e

响应体...
```

响应报文由四部分组成： 响应行、响应头、空行、响应体

#### ① 响应行

**协议版本：** HTTP/1,1

**响应状态码：** 200，标记响应状态，更多地响应状态码：https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status

**响应状态描述：** 与响应状态码对应

#### ② 响应头

键值对结构，标识服务端相关信息

**更多响应头：**https://developer.mozilla.org/zh-CN/docs/Glossary/Response_header

#### ③ 空行

分隔响应头和响应体

#### ④  响应体

服务器向客户端发送的数据都在响应体中，如 html文件的内容、css文件的内容、js文件的内容等

### 5.3 URL

统一资源定位系统（uniform resource locator;URL）是因特网的万维网服务程序上用于指定信息位置的表示方法。

```
http://www.baidu.com:8080/home/msg/data/personalcontent?num=8&indextype=manht#logo
```

完整 URL 的组成部分：

- 协议 ，如 https、http。
- 主机名，一般使用 IP 地址或域名。
- 端口号 ，HTTP 的端口号为 80，HTTPS 的为 443
- 路径，上面 URL 中的路径部分为： `/home/msg/data/personalcontent`。
- 查询字符串，上面 URL 中的路径部分为：`num=8&indextype=manht`。
- 锚点，上面 URL 中的路径部分为：`#logo`

### 5.4 HTTP 响应状态码

状态码由三位数字组成，第一位数字表示响应的类型，常用的状态码有五大类如下所示：

- `1xx`：指示信息--表示请求已接收，继续处理。
- `2xx`：成功--表示请求已被成功接收、理解、接受。
- `3xx`：重定向--要完成请求必须进行更进一步的操作。
- `4xx`：客户端错误--请求有语法错误或请求无法实现。
- `5xx`：服务器端错误--服务器未能实现合法的请求。

常见状态代码、状态描述的说明如下。

- 200 OK：客户端请求成功。

- 400 Bad Request：客户端请求有语法错误，不能被服务器所理解。

- 401 Unauthorized：请求未经授权

- 403 Forbidden：服务器收到请求，但是拒绝提供服务。

- 404 Not Found：请求资源不存在，举个例子：输入了错误的URL。

- 500 Internal Server Error：服务器发生不可预期的错误。

- 503 Server Unavailable：服务器当前不能处理客户端的请求，一段时间后可能恢复正常

  



## 6 使用 node 创建 http 服务

### 6.1 创建服务

```js

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

### 6.2 获取请求报文信息

#### 获取请求行的信息

```js
request.httpVersion;		// 获取 http 版本
request.url;				// 获取请求的 url 地址
request.method;				// 获取请求方式（请求方法）
```

#### 获取请求头信息

```js
request.headers;			// 返回对象，包含请求报文中所有的请求头信息
request.headers.请求头名字；
```

#### 获取客户端 IP 地址

```js
request.socket.remoteAddress
```

#### 获取 URL 中的查询字符串

```js
const url = requeire('url');
url.parse(request.url, true).query;  // 返回一个对象
```

```
不论是 GET 请求是 POST 请求,URL 中都可以有查询字符串。
```

#### 获取请求体信息

```js
// request 本质上是一个可读流对象

// 定义变量 将请求体中读取的内容拼接到该变量
let reqBody = '';

// 分次从请求体中读取数据
req.on('data', chunk => {
    reqBody += chunk;
});

// 请求体内容读取结束
req.on('end', () => {
   	reqBody;  					 // 查询字符串
    querystring.parse(reqBody);   // 解析为对象
});
```

```
GET 请求方式没有请求体，POST 请求方式有请求体
```

### 6.3 设置响应报文

#### 设置响应行

```js
response.statusCode = 200;		// 设置响应状态码
response.statusMessage = 'OK';	// 设置响应状态描述
```

#### 设置响应头

```js
response.setHeader('响应头名字'， '响应头内容')
```

```js
// 同时设置 响应状态码、设置响应状态描述、响应头
response.writeHead(响应状态码, '响应状态描述', {
    '响应头名字' ：'响应头内容',
    '响应头名字' ：'响应头内容',
    '响应头名字' ：'响应头内容'
    ...
})
```

#### 设置响应体

```js
// resposne 本质上是一个可写流对象 可以通过 write 将内容写入流
response.write('内容');
response.write('内容');
response.write('内容');
response.write('内容');
```

#### 结束响应

```js
// 只用来结束响应
resposne.end();

// 设置响应体并结束响应
response.end('响应体内容');
```

