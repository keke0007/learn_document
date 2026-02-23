# Day19 Axios 课堂笔记

## 1 Axios 概述

### 1.1 axios 是什么?

Axios 是前端最流行的 ajax 请求库 ，没有之一，react、vue官方都推荐使用 的 Ajax 请求库。

官方网站：https://axios-http.com

仓库地址：https://github.com/axios/axios

中文文档：https://axios-http.com/zh/docs/intro

### 1.2 axios特点

```
1. 基于 XMLHttpRequest + Promise 的异步的 Ajax 请求库
2. 浏览器端、Node端都可以使用
3. 支持请求和响应拦截器
4. 支持请求取消 
5. 批量发送多个请求
6. 支持请求与响应的数据转换（二次封装）
```



## 2 axios 的安装使用

### 2.1 浏览器中使用

下载后在页面引入或者直接使用 CDN

```html
<script src="axios脚本文件地址"></script>
```

```html
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
```

### 2.2 Node 中使用

**安装**

```bash
npm install axios
```

**代码中引入模块**

```js
const axios = require(‘axios’)
```



## 3 axios 基本使用

```js
// axios 设置请求配置项
axios({
    method: 'GET',
    url: 'http://127.0.0.1/server',
    其他请求配置项...
})
.then(成功回调， 失败回调);

// axios 第一个参数是URL，第二个参数是请求配置项
axios('http://127.0.0.1/server', {
    method: 'GET',
    其他请求配置项...
})
.then(成功回调， 失败回调);

// 请求方法别名
axios
.get('http://127.0.0.1/server', {请求配置项...})
.then(成功回调， 失败回调);

axios
.post('http://127.0.0.1/server', {请求体}, {请求配置项...})
.then(成功回调， 失败回调);
```

* axios(config): 通用/最本质的发送意类型请求的方式。
* axios(url[, config]): 第一个参数是地址，第二个参数是配置项。

* axios.request(config): 等同于axios(config)  （了解）
* axios.get(url[, config]): 发get请求
* axios.delete(url[, config]): 发delete请求
* axios.post(url[, data, config]): 发post请求
* axios.put(url[, data, config]): 发put请求
* axios.patch(url[, data[, config]]) 发送patch请求



## 4 axios 请求配置项

### 4.1 常用的请求配置项

```js
{
 	// `url` 是用于请求的服务器 URL
  	url: '/user',

  	// `method` 是创建请求时使用的方法
  	method: 'get', // default

  	// `baseURL` 将自动加在 `url` 前面，除非 `url` 是一个绝对 URL。
  	// 它可以通过设置一个 `baseURL` 便于为 axios 实例的方法传递相对 URL
  	baseURL: 'https://some-domain.com/api/',
        
    // `headers` 是即将被发送的请求头
  	headers: {
        'Content-type': 'appliation/json'
    },
    
    // `params` 是即将与请求一起发送的 URL 参数
    // 必须是一个无格式对象(plain object)或 URLSearchParams 对象
    params: {
       ID: 12345
    },
      
    // `data` 是作为请求主体被发送的数据
    // 只适用于这些请求方法 'PUT', 'POST', 和 'PATCH'
    // 在没有设置 `transformRequest` 时，必须是以下类型之一：
    // - string, plain object, ArrayBuffer, ArrayBufferView, URLSearchParams
    // - 浏览器专属：FormData, File, Blob
    // - Node 专属： Stream
    data: {
       firstName: 'Fred'
    },

     // `timeout` 指定请求超时的毫秒数(0 表示无超时时间)
     // 如果请求话费了超过 `timeout` 的时间，请求将被中断
     timeout: 1000,
         
     // `responseType` 表示服务器响应的数据类型，可以是 'arraybuffer', 'blob', 'document', 'json', 'text', 'stream'
  	 responseType: 'json', // default
}
```

> **注意：** 更多的请求配置项见附录

### 4.2 每次发送请求时设置配置项

```js
axios({
    配置项
    ...
});

axios(url, {
    配置项
   	...
});

axios.request(url, {
    配置项
    ...
});

axios.get(url, {
    配置项
    ...
});

axios.post(url, data, {
    配置项
    ...
})
```

### 4.3 设置全局配置项

 设置全局配置项，将被应用到每一个要求。 

```js
axios.defaults.baseURL = "http://api.example.com";
axios.defaults.timeout = 2000;
axios.defaults.headers = {
    token:"abc"
}
```



## 5 响应结构

```js
{
  // `data` 由服务器提供的响应体
  data: {},

  // `status` 来自服务器响应的 HTTP 状态码
  status: 200,

  // `statusText` 来自服务器响应的 HTTP 状态信息
  statusText: 'OK',

  // `headers` 服务器响应的头
  headers: {},

   // `config` 是为请求提供的配置信息
  config: {},
 // 'request'
  // `request` is the request that generated this response
  // It is the last ClientRequest instance in node.js (in redirects)
  // and an XMLHttpRequest instance the browser
  request: {}
}
```



## 6 创建 axios 实例

```
1. 根据指定配置创建一个自定义的 axios 实例, 每个自定义的 axios 实例都有自己的配置。
2.  axios 实例只是没有取消请求和批量发请求的方法, 其它所有方法与默认 axios 本身是一样的。
3. 为什么要设计这个语法?
   (1) 需求: 项目中有部分接口需要的配置与另一部分接口需要的配置不太一样, 如何处理
   (2) 解决: 创建 2 个自定义 axios 新实例, 每个都有自己特有的配置, 分别应用到不同要求的接口请求中
```

```js
const instance = axios.create({
  baseURL: 'https://example.com/api/',
  timeout: 1000,
});

instance.get(url).then(res => {
    console.log(res);
});
```



## 7 拦截器

在请求或响应被 `then` 或 `catch` 处理前拦截它们。

```js
// 添加请求拦截器
axios.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么
    return config;
  }, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
  });

// 添加响应拦截器
axios.interceptors.response.use(function (response) {
    // 对响应数据做点什么
    return response;
  }, function (error) {
    // 对响应错误做点什么
    return Promise.reject(error);
  });
```

如果你想在稍后移除拦截器，可以这样：

```js
// 定义拦截器的时候使用变量记录拦截器的唯一标识
const reqInterceptor = axios.interceptors.request.use(function () {/*...*/});
const resInterceptor = axios.interceptors.response.use(function () {/*...*/});
// 根据唯一标识移除拦截器
axios.interceptors.request.eject(reqInterceptor);
axios.interceptors.response.eject(resInterceptor);
```

可以为自定义 axios 实例添加拦截器

```js
const instance = axios.create();
instance.interceptors.request.use(function () {/*...*/});
```

调用 axios() 并不是立即发送 ajax 请求, 而是需要经历一个较长的流程

```
1. 流程: 请求拦截器2 -> 请求拦截器1 -> 发ajax请求 -> 响应拦截器1 -> 响应拦截器2 -> 请求的回调
2. 注意: 此流程是通过 Promise 串连起来的, 请求拦截器传递的是 config, 响应拦截器传递的是 response
```



## 8 取消请求

**基本流程：**

```
1. 请求配置项中配置 cancelToken 对象
2. 用变量保存用于取消请求的 cancel 函数
3. 在后面特定时机调用 cancel 函数实现取消请求
4. 在错误回调中判断如果 error 是 cancel, 做相应处理
```

**具体实现：**

```js
// 定义变量用于保存 cancel 函数
let cancel = null;

axios({
    method: "GET",
    url:'api.emaple.com',
    // 配置取消请求的选项
    cancelToken: new axios.CancelToken(cb => {
        cancel = cb;
    })
})
.then(response => {
    console.log(response);
})
.catch(err => {
    console.log(err);
    console.log(axios.isCancel(err));// 判断错误信息是否由取消请求触发的
});

// 如果需要取消，只需调用 cancel 函数
cancel();
```



## 9 批量发送请求(批量处理响应)

```js
const r1 = axios.get("http://127.0.0.1:3000/computers/1");
const r2 = axios.get("http://127.0.0.1:3000/computers/2");
const r3 = axios.get("http://127.0.0.1:3000/computers/3");

axios
.all([r1,r2,r3])
.then(axios.spread((s1,s2,s3) => {
    console.log(s1,s2,s3);
}))
.catch(err => {
    console.log(err);
})
```



## [附录] axios 方法总结

* axios(config): 通用/最本质的发任意类型请求的方式。
* axios(url[, config]): 第一个参数是地址，第二个参数是配置项。
* axios.request(config): 等同于axios(config) 
* axios.get(url[, config]): 发get请求
* axios.delete(url[, config]): 发delete请求
* axios.post(url[, data, config]): 发post请求
* axios.put(url[, data, config]): 发put请求
* axios.patch(url[, data, config]): 发put请求
* axios.defaults.xxx: 请求的默认全局配置
* axios.interceptors.request.use(): 添加请求拦截器
* axios.interceptors.response.use(): 添加响应拦截器
* axios.create([config]): 创建一个新的axios实例。
* axios.CancelToken(): 用于创建取消请求的token对象
* axios.isCancel(): 是否是一个取消请求的错误
* axios.all(promises): 用于批量执行多个异步请求
* axios.spread(): 用来指定接收所有成功数据的回调函数的方法

![](assets/axios-function.png)



## [附录] 请求配置项

```js
{
   // `url` 是用于请求的服务器 URL
  url: '/user',

  // `method` 是创建请求时使用的方法
  method: 'get', // default

  // `baseURL` 将自动加在 `url` 前面，除非 `url` 是一个绝对 URL。
  // 它可以通过设置一个 `baseURL` 便于为 axios 实例的方法传递相对 URL
  baseURL: 'https://some-domain.com/api/',

  // `transformRequest` 允许在向服务器发送前，修改请求数据
  // 只能用在 'PUT', 'POST' 和 'PATCH' 这几个请求方法
  // 后面数组中的函数必须返回一个字符串，或 ArrayBuffer，或 Stream
  transformRequest: [function (data, headers) {
    // 对 data 进行任意转换处理
    return data;
  }],

  // `transformResponse` 在传递给 then/catch 前，允许修改响应数据
  transformResponse: [function (data) {
    // 对 data 进行任意转换处理
    return data;
  }],

  // `headers` 是即将被发送的请求头
  headers: {'X-Requested-With': 'XMLHttpRequest'},

  // `params` 是即将与请求一起发送的 URL 参数
  // 必须是一个无格式对象(plain object)或 URLSearchParams 对象
  params: {
    ID: 12345
  },

   // `paramsSerializer` 是一个负责 `params` 序列化的函数
  // (e.g. https://www.npmjs.com/package/qs, http://api.jquery.com/jquery.param/)
  paramsSerializer: function(params) {
    return Qs.stringify(params, {arrayFormat: 'brackets'})
  },

  // `data` 是作为请求主体被发送的数据
  // 只适用于这些请求方法 'PUT', 'POST', 和 'PATCH'
  // 在没有设置 `transformRequest` 时，必须是以下类型之一：
  // - string, plain object, ArrayBuffer, ArrayBufferView, URLSearchParams
  // - 浏览器专属：FormData, File, Blob
  // - Node 专属： Stream
  data: {
    firstName: 'Fred'
  },

  // `timeout` 指定请求超时的毫秒数(0 表示无超时时间)
  // 如果请求话费了超过 `timeout` 的时间，请求将被中断
  timeout: 1000,

   // `withCredentials` 表示跨域请求时是否需要使用凭证
  withCredentials: false, // default

  // `adapter` 允许自定义处理请求，以使测试更轻松
  // 返回一个 promise 并应用一个有效的响应 (查阅 [response docs](#response-api)).
  adapter: function (config) {
    /* ... */
  },

 // `auth` 表示应该使用 HTTP 基础验证，并提供凭据
  // 这将设置一个 `Authorization` 头，覆写掉现有的任意使用 `headers` 设置的自定义 `Authorization`头
  auth: {
    username: 'janedoe',
    password: 's00pers3cret'
  },

   // `responseType` 表示服务器响应的数据类型，可以是 'arraybuffer', 'blob', 'document', 'json', 'text', 'stream'
  responseType: 'json', // default

  // `responseEncoding` indicates encoding to use for decoding responses
  // Note: Ignored for `responseType` of 'stream' or client-side requests
  responseEncoding: 'utf8', // default

   // `xsrfCookieName` 是用作 xsrf token 的值的cookie的名称
  xsrfCookieName: 'XSRF-TOKEN', // default

  // `xsrfHeaderName` is the name of the http header that carries the xsrf token value
  xsrfHeaderName: 'X-XSRF-TOKEN', // default

   // `onUploadProgress` 允许为上传处理进度事件
  onUploadProgress: function (progressEvent) {
    // Do whatever you want with the native progress event
  },

  // `onDownloadProgress` 允许为下载处理进度事件
  onDownloadProgress: function (progressEvent) {
    // 对原生进度事件的处理
  },

   // `maxContentLength` 定义允许的响应内容的最大尺寸
  maxContentLength: 2000,

  // `validateStatus` 定义对于给定的HTTP 响应状态码是 resolve 或 reject  promise 。如果 `validateStatus` 返回 `true` (或者设置为 `null` 或 `undefined`)，promise 将被 resolve; 否则，promise 将被 rejecte
  validateStatus: function (status) {
    return status >= 200 && status < 300; // default
  },

  // `maxRedirects` 定义在 node.js 中 follow 的最大重定向数目
  // 如果设置为0，将不会 follow 任何重定向
  maxRedirects: 5, // default

  // `socketPath` defines a UNIX Socket to be used in node.js.
  // e.g. '/var/run/docker.sock' to send requests to the docker daemon.
  // Only either `socketPath` or `proxy` can be specified.
  // If both are specified, `socketPath` is used.
  socketPath: null, // default

  // `httpAgent` 和 `httpsAgent` 分别在 node.js 中用于定义在执行 http 和 https 时使用的自定义代理。允许像这样配置选项：
  // `keepAlive` 默认没有启用
  httpAgent: new http.Agent({ keepAlive: true }),
  httpsAgent: new https.Agent({ keepAlive: true }),

  // 'proxy' 定义代理服务器的主机名称和端口
  // `auth` 表示 HTTP 基础验证应当用于连接代理，并提供凭据
  // 这将会设置一个 `Proxy-Authorization` 头，覆写掉已有的通过使用 `header` 设置的自定义 `Proxy-Authorization` 头。
  proxy: {
    host: '127.0.0.1',
    port: 9000,
    auth: {
      username: 'mikeymike',
      password: 'rapunz3l'
    }
  },

  // `cancelToken` 指定用于取消请求的 cancel token
  // （查看后面的 Cancellation 这节了解更多）
  cancelToken: new CancelToken(function (cancel) {
  })
}
```

