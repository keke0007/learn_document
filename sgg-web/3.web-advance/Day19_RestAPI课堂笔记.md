# Day19 REST API 课堂笔记

## 1 后端 API

### 1.1 非 REST(restless) API：地址一般不会重复

```
增加：POST http://127.0.0.1/news/create
删除：GET 	http://127.0.0.1/news/delete?id=12121
修改：POST http://127.0.0.1/news/modify
查找：GET	http://127.0.0.1/news/list
```

> 1. 不同的 URL 路径对应不同的 CURD 操作。
> 2. 请求方式一般只有GET、POST。

### 1.2 REST(restful) API：URL路径不变，改变的只是请求方式

```
Creae  增加：POST http://127.0.0.1/news
Delete 删除：DELETE http://127.0.0.1/news/id
Update 更新：PUT http://127.0.0.1/news
Read   读取：GET http://127.0.0.1/news
```

> 1. 所有的操作使用相同的 URL 路径，由请求方式决定哪一种操作
> 2. 请求方式会用到 GET、POST、PUT、DELETE 等



## 2 使用json-server搭建 restful API

### 2.1 json-server 是什么?

json-server 是用来快速搭建模拟的、 REST API 的工具包，可以搭建站点服务并提供数据的操作。可以作为前端工程师的开发测试工具。

在线文档: https://github.com/typicode/json-server

### 2.2 使用json-server 

**1 安装 Node**
由于json-server需要通过Node对其进行启动，所以首先要安装Node。

**2 全局安装 json-server**

```shell
npm install json-server -g
```

**3 检查是否安装成功**

```shell
json-server -v
```

**4 准备一份JSON文件: 内容必须是一个对象，不能是数组**

**5 启动**

```
json-server --watch json文件的地址 --port 6000 --host 127.0.0.1 --delay 2000
```

```
--watch:	可以省略，如果省略那么数据发生变化，站点服务不会及时响应。
--delay:	指定延长响应的时间 ，单位为毫秒。
--port:		指定端口号
--host:		指定主机名
```

### 2.3 使用浏览器访问测试

```
http://localhost:3000/scores
http://localhost:3000/scores/1
```

### 2.4 使用工具测试

**Postman：** https://www.postman.com

**Apipost：** https://www.apipost.cn

这两个工具都是用于测试后端 API 的软件，可以发送各种方式的 HTTP 请求。

### 2.5 json-server 后端服务的 API 规则

```
查询
GET http://localhost:6100/news
GET http://localhost:6100/news/2

增加
POST http://localhost:6100/news  需要请求体

修改
PUT	http://localhost:6100/news/2	整个修改
PATCH http://localhost:6100/news/2		修改单个数据中的属性

删除
DELETE http://localhost:6100/news/2
```



## 3 配置 hosts 文件

windows 系统的 hosts 文件一般位于 `C:\Windows\System32\drivers\etc\` 下， macos 系统的 host 文件一般位于 `/etc` 目录下。

hosts 文件的格式如下：

```config
127.0.0.1       localhost 
127.0.0.1       example.com
```

如上面的设置，当我们向 example.com 这个地址发送请求的时候，会映射到 127.0.0.1 这个 IP。





