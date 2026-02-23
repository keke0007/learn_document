# Day20 Axios源码分析&自定义Axios

## 1 源码分析

### 1.1 源码目录结构

```
├── /dist/                     # 项目输出目录
├── /lib/                      # 项目源码目录
│ ├── adapters/                # 定义请求的适配器 xhr、http
│ │ ├── http.js                # 实现http适配器(包装http包)
│ │ └── xhr.js                 # 实现xhr适配器(包装xhr对象)
│ ├── cancel/                  # 定义取消功能
│ ├── core/                    # 一些核心功能
│ │ ├── Axios.js               # axios的核心主类
│ │ ├── dispatchRequest.js     # 用来调用http请求适配器方法发送请求的函数
│ │ ├── InterceptorManager.js  # 拦截器的管理器
│ │ └── settle.js              # 根据http响应状态，改变Promise的状态
│ ├── helpers/                 # 一些辅助方法
│ ├── defaults/                # axios的默认配置 
│ ├── axios.js                 # 对外暴露接口
│ └── utils.js                 # 公用工具
├── package.json               # 项目信息
├── index.d.ts                 # 配置TypeScript的声明文件
└── index.js                   # 入口文件
```

### 1.2 axios 运行流程图

![](./assets/flow.png)

### 1.3 拦截器原理图

![](./assets/interceptor.png)



## 2 自定义 axios

### 2.1 创建 axios 函数

**axios 函数本质不是 Axios 的实例，调用 axios 函数其实就是调用 Axios.prototype.request() **

```js
// 定义默认请求配置项
const defaults = {
    timeout: 0
};

// 核心类
class Axios {
    // 构造器方法
    constructor(instanceConfig) {
        this.defaults = instanceConfig;
    }

    // 发送请求的方法
    request() {
        console.log('request');
    }
}

function bind(fn, thisArg) {
    return function wrap() {
        // fn 就是 Axios.prototype.request
        // argments 是伪数组，成员是传递给 axios 函数的参数
        // 就是在调用 Axios.prototype.request， 并设置里面的this是Axios类的一个实例
        return fn.apply(thisArg, arguments)
    }
}

/**
 * 创建 axios 函数， axios函数本质不是 Axios 的实例
 * @param {Object} defaultConfig The default config for the instance
 * @returns {Function} 调用该函数就是调用Axios.prototype.request()
 */
function createInstance(defaultConfig) {
    // 实例化核心类型 得到实例
    const context = new Axios(defaultConfig);
    // 创建 axios 函数
    const instance = bind(Axios.prototype.request, context);
    // 返回
    return instance;
}

// 创建 axios
const axios = createInstance(defaults);

// 以模块的形式对外暴露
export default axios;
```



### 2.2 发送请求并返回 Promise

```
1. Axios.prototype.request 有一个或两个参数
2. 将发送请求时传入的配置对象和全局配置对象合并
3. 设置默认请求方式是 GET
4. 将发送请求的操作封装 dispatchRequest 函数中, 函数返回 Promise 对象
5. request 中调用 return dispathRequest()
```

```js
// 定义默认请求配置项
const defaults = {
    timeout: 0
};

/**
 * 发送 ajax 请求
 * @param {object} config 请求配置项
 * @returns {Promise} 
 */
function dispatchRequest(config) {
    return new Promise((resolve, reject) => {
        // 创建 xhr 对象
        const xhr = new XMLHttpRequest();
        // 初始化
        xhr.open(config.method, config.url);
        // 发送
        xhr.send();

        // 监听成功响应
        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve('Success');
            } else {
                reject('Error');
            }
        }

        // 监听失败响应
        xhr.onerror = () => {
            reject('Error');
        }
    });
}

// 核心类
class Axios {
    // 构造器方法
    constructor(instanceConfig) {
        this.defaults = instanceConfig;
    }

    /**
     * 发送 ajax 请求
     * @param {String|Object} configOrUrl url或者请求配置对象
     * @param {?Object} config 请求配置对象，如果第一个参数已经是对象，不需要该参数
     * @returns {Promise} 
     */
    request(configOrUrl={}, config={}) {
        // 判断第一个参数是否是 url
        if (typeof configOrUrl === 'string') {
            config.url = configOrUrl
        } else {
            config = configOrUrl;
        }

        // 将传入的请求配置对象和全局请求配置对象合并
        config = Object.assign({}, this.defaults, config);

        // 设置默认请求方式是 GET
        config.method = (config.method || this.defaults.method || 'get').toUpperCase();
        
        // 调用函数发送请求
        return dispatchRequest.call(this, config);
    }
}

function bind(fn, thisArg) {
    return function wrap() {
        // fn 就是 Axios.prototype.request
        // argments 是伪数组，成员是传递给 axios 函数的参数
        // 就是在调用 Axios.prototype.request， 并设置里面的this是Axios类的一个实例
        return fn.apply(thisArg, arguments)
    }
}

/**
 * 创建 axios 函数， axios函数本质不是 Axios 的实例
 * @param {Object} defaultConfig The default config for the instance
 * @returns {Function} 调用该函数就是调用Axios.prototype.request()
 */
function createInstance(defaultConfig) {
    // 实例化核心类型 得到实例
    const context = new Axios(defaultConfig);
    // 创建 axios 函数
    const instance = bind(Axios.prototype.request, context);
    // 返回
    return instance;
}

// 创建 axios
const axios = createInstance(defaults);

// 以模块的形式对外暴露
export default axios;
```

### 2.3 请求配置项设置

```
1. baseURL  
2. params		 URL参数
3. responseType  响应类型
4. headers		 请求头
5. data			 请求体
6. 全局配置项
```

```js
// 定义默认请求配置项
const defaults = {
    timeout: 0,
    responseType: 'json'
};

/**
 * 发送 ajax 请求
 * @param {object} config 请求配置项
 * @returns {Promise} 
 */
function dispatchRequest(config) {
    return new Promise((resolve, reject) => {
        // 创建 xhr 对象
        const xhr = new XMLHttpRequest();
        // 设置响应类型
        xhr.responseType = config.responseType;
        
        // 初始化
        xhr.open(config.method, config.url);

        // 设置请求头 xhr.setRequestHeader(key, value)
        if (config.headers) {
            for (let key in config.headers) {
                xhr.setRequestHeader(key, config.headers[key]);
            }
        }

        // 设置请求体
        let body;
        // 只有允许的请求方法，才可以携带请求体
        if (['POST', 'PUT', 'PATCH'].includes(config.method)) {
            if (typeof config.data === 'string') {
                body = config.data;
                xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            } else if (Object.prototype.toString.call(config.data) === '[object Object]') {
                body = JSON.stringify(config.data);
                xhr.setRequestHeader('Content-type', 'application/json');
            } else {
                body = config.data;
            }
        }

        // 发送
        xhr.send(body);

        // 监听成功响应
        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve('Success');
            } else {
                reject('Error');
            }
        }

        // 监听失败响应
        xhr.onerror = () => {
            reject('Error');
        }
    });
}

// 核心类
class Axios {
    // 构造器方法
    constructor(instanceConfig) {
        this.defaults = instanceConfig;
    }

    /**
     * 发送 ajax 请求
     * @param {String|Object} configOrUrl url或者请求配置对象
     * @param {?Object} config 请求配置对象，如果第一个参数已经是对象，不需要该参数
     * @returns {Promise} 
     */
    request(configOrUrl={}, config={}) {
        // 判断第一个参数是否是 url
        if (typeof configOrUrl === 'string') {
            config.url = configOrUrl
        } else {
            config = configOrUrl;
        }

        // 将传入的请求配置对象和全局请求配置对象合并
        config = Object.assign({}, this.defaults, config);

        // 设置默认请求方式是 GET
        config.method = (config.method || this.defaults.method || 'get').toUpperCase();

        // 合并 baseURL 和 url
        if (config.baseURL && !config.url.startsWith('http://') && !config.url.startsWith('https://')) {
            config.url = config.baseURL + config.url;
        }

        // 将 searchParams 拼接到 url 后面
        if (config.params) {
            config.url += '?' + Object.entries(config.params).map(item=>item[0]+'='+item[1]).join('&');
        }
        
        // 调用函数发送请求
        return dispatchRequest.call(this, config);
    }
}

function bind(fn, thisArg) {
    return function wrap() {
        // fn 就是 Axios.prototype.request
        // argments 是伪数组，成员是传递给 axios 函数的参数
        // 就是在调用 Axios.prototype.request， 并设置里面的this是Axios类的一个实例
        return fn.apply(thisArg, arguments)
    }
}

/**
 * 创建 axios 函数， axios函数本质不是 Axios 的实例
 * @param {Object} defaultConfig The default config for the instance
 * @returns {Function} 调用该函数就是调用Axios.prototype.request()
 */
function createInstance(defaultConfig) {
    // 实例化核心类型 得到实例
    const context = new Axios(defaultConfig);
    // 创建 axios 函数
    const instance = bind(Axios.prototype.request, context);

    // 给 instance 设置全局配置接口
    instance.defaults = context.defaults;

    // 返回
    return instance;
}

// 创建 axios
const axios = createInstance(defaults);

// 以模块的形式对外暴露
export default axios;
```

### 2.4 响应结果处理

```
成功的结果
{
	config
	data
	headers
	request
	status
	statusText
}

请求发送未成功的失败
{
    code: "ERR_NETWORK"
    config
    message: "ERR_NETWORK"
	name: "AxiosError"
	request
}

响应不正确，如404
{
    code: "ERR_BAD_REQUEST"
    config
    message: "Request failed with status code 404"
	name: "AxiosError"
	request
}
```

```js
// 定义默认请求配置项
const defaults = {
    timeout: 0,
    responseType: 'json'
};

/**
 * 发送 ajax 请求
 * @param {object} config 请求配置项
 * @returns {Promise} 
 */
function dispatchRequest(config) {
    return new Promise((resolve, reject) => {
        // 创建 xhr 对象
        const xhr = new XMLHttpRequest();
        // 设置响应类型
        xhr.responseType = config.responseType;
        
        // 初始化
        xhr.open(config.method, config.url);

        // 设置请求头 xhr.setRequestHeader(key, value)
        if (config.headers) {
            for (let key in config.headers) {
                xhr.setRequestHeader(key, config.headers[key]);
            }
        }

        // 设置 请求体
        let body;
        // 只有允许的请求方法，才可以携带请求体
        if (['POST', 'PUT', 'PATCH'].includes(config.method)) {
            if (typeof config.data === 'string') {
                body = config.data;
                xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            } else if (Object.prototype.toString.call(config.data) === '[object Object]') {
                body = JSON.stringify(config.data);
                xhr.setRequestHeader('Content-type', 'application/json');
            } else {
                body = config.data;
            }
        }

        // 发送
        xhr.send(body);

        // 监听成功响应
        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve({
                    config,
                    request: xhr,
                    data: xhr.response,
                    statsu: xhr.status,
                    statusText: xhr.statusText,
                    headers: xhr.getAllResponseHeaders().split('\r\n').filter(item=>item).map(item=>item.split(': ')).reduce((pre,item)=>({...pre, [item[0]]:item[1]}), {})
                });
            } else {
                reject({
                    code: "ERR_BAD_REQUEST",
                    config,
                    message: "Request failed with status code " + xhr.status,
                    name: "AxiosError",
                    request: xhr
                });
            }
        }

        // 监听失败响应
        xhr.onerror = () => {
            reject({
                code: "ERR_NETWORK",
                config,
                message: "ERR_NETWORK",
                name: "AxiosError",
                request: xhr
            });
        }
    });
}

// 核心类
class Axios {
    // 构造器方法
    constructor(instanceConfig) {
        this.defaults = instanceConfig;
    }

    /**
     * 发送 ajax 请求
     * @param {String|Object} configOrUrl url或者请求配置对象
     * @param {?Object} config 请求配置对象，如果第一个参数已经是对象，不需要该参数
     * @returns {Promise} 
     */
    request(configOrUrl={}, config={}) {
        // 判断第一个参数是否是 url
        if (typeof configOrUrl === 'string') {
            config.url = configOrUrl
        } else {
            config = configOrUrl;
        }

        // 将传入的请求配置对象和全局请求配置对象合并
        config = Object.assign({}, this.defaults, config);

        // 设置默认请求方式是 GET
        config.method = (config.method || this.defaults.method || 'get').toUpperCase();

        // 合并 baseURL 和 url
        if (config.baseURL && !config.url.startsWith('http://') && !config.url.startsWith('https://')) {
            config.url = config.baseURL + config.url;
        }

        // 将 searchParams 拼接到 url 后面
        if (config.params) {
            config.url += '?' + Object.entries(config.params).map(item=>item[0]+'='+item[1]).join('&');
        }
        
        // 调用函数发送请求
        return dispatchRequest.call(this, config);
    }
}

function bind(fn, thisArg) {
    return function wrap() {
        // fn 就是 Axios.prototype.request
        // argments 是伪数组，成员是传递给 axios 函数的参数
        // 就是在调用 Axios.prototype.request， 并设置里面的this是Axios类的一个实例
        return fn.apply(thisArg, arguments)
    }
}

/**
 * 创建 axios 函数， axios函数本质不是 Axios 的实例
 * @param {Object} defaultConfig The default config for the instance
 * @returns {Function} 调用该函数就是调用Axios.prototype.request()
 */
function createInstance(defaultConfig) {
    // 实例化核心类型 得到实例
    const context = new Axios(defaultConfig);
    // 创建 axios 函数
    const instance = bind(Axios.prototype.request, context);

    // 给 instance 设置全局配置接口
    instance.defaults = context.defaults;

    // 返回
    return instance;
}

// 创建 axios
const axios = createInstance(defaults);

// 以模块的形式对外暴露
export default axios;
```

### 2.5 超时设置

```
{
    code: "ECONNABORTED"
    config
    message: "timeout of 2000ms exceeded"
	name: "AxiosError"
	request
}
```

```js
// 定义默认请求配置项
const defaults = {
    timeout: 0,
    responseType: 'json'
};

/**
 * 发送 ajax 请求
 * @param {object} config 请求配置项
 * @returns {Promise} 
 */
function dispatchRequest(config) {
    return new Promise((resolve, reject) => {
        // 创建 xhr 对象
        const xhr = new XMLHttpRequest();
        // 设置响应类型
        xhr.responseType = config.responseType;
        // 设置超时时间
        xhr.timeout = config.timeout;
        
        // 初始化
        xhr.open(config.method, config.url);

        // 设置请求头 xhr.setRequestHeader(key, value)
        if (config.headers) {
            for (let key in config.headers) {
                xhr.setRequestHeader(key, config.headers[key]);
            }
        }

        // 设置 请求体
        let body;
        // 只有允许的请求方法，才可以携带请求体
        if (['POST', 'PUT', 'PATCH'].includes(config.method)) {
            if (typeof config.data === 'string') {
                body = config.data;
                xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            } else if (Object.prototype.toString.call(config.data) === '[object Object]') {
                body = JSON.stringify(config.data);
                xhr.setRequestHeader('Content-type', 'application/json');
            } else {
                body = config.data;
            }
        }

        // 发送
        xhr.send(body);

        // 监听成功响应
        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                // console.log(xhr.getAllResponseHeaders().split('\r\n').filter(item=>item))

                // console.log(xhr.getAllResponseHeaders().split('\r\n').filter(item=>item).map(item=>item.split(': ')));

                // console.log(xhr.getAllResponseHeaders().split('\r\n').filter(item=>item).map(item=>item.split(': ')).reduce((pre,item)=>({...pre, [item[0]]:item[1]}), {}));

                resolve({
                    config,
                    request: xhr,
                    data: xhr.response,
                    statsu: xhr.status,
                    statusText: xhr.statusText,
                    headers: xhr.getAllResponseHeaders().split('\r\n').filter(item=>item).map(item=>item.split(': ')).reduce((pre,item)=>({...pre, [item[0]]:item[1]}), {})
                });
            } else {
                reject({
                    code: "ERR_BAD_REQUEST",
                    config,
                    message: "Request failed with status code " + xhr.status,
                    name: "AxiosError",
                    request: xhr
                });
            }
        }

        // 监听失败响应
        xhr.onerror = () => {
            reject({
                code: "ERR_NETWORK",
                config,
                message: "ERR_NETWORK",
                name: "AxiosError",
                request: xhr
            });
        }

        // 超时的事件
        xhr.ontimeout = () => {
            reject({
                code: "ECONNABORTED",
                config,
                message: `timeout of ${config.timeout}ms exceeded`,
                name: "AxiosError",
                request:xhr
            })
        }
    });
}

// 核心类
class Axios {
    // 构造器方法
    constructor(instanceConfig) {
        this.defaults = instanceConfig;
    }

    /**
     * 发送 ajax 请求
     * @param {String|Object} configOrUrl url或者请求配置对象
     * @param {?Object} config 请求配置对象，如果第一个参数已经是对象，不需要该参数
     * @returns {Promise} 
     */
    request(configOrUrl={}, config={}) {
        // 判断第一个参数是否是 url
        if (typeof configOrUrl === 'string') {
            config.url = configOrUrl
        } else {
            config = configOrUrl;
        }

        // 将传入的请求配置对象和全局请求配置对象合并
        config = Object.assign({}, this.defaults, config);

        // 设置默认请求方式是 GET
        config.method = (config.method || this.defaults.method || 'get').toUpperCase();

        // 合并 baseURL 和 url
        if (config.baseURL && !config.url.startsWith('http://') && !config.url.startsWith('https://')) {
            config.url = config.baseURL + config.url;
        }

        // 将 searchParams 拼接到 url 后面
        if (config.params) {
            config.url += '?' + Object.entries(config.params).map(item=>item[0]+'='+item[1]).join('&');
        }
        
        // 调用函数发送请求
        return dispatchRequest.call(this, config);
    }
}

function bind(fn, thisArg) {
    return function wrap() {
        // fn 就是 Axios.prototype.request
        // argments 是伪数组，成员是传递给 axios 函数的参数
        // 就是在调用 Axios.prototype.request， 并设置里面的this是Axios类的一个实例
        return fn.apply(thisArg, arguments)
    }
}

/**
 * 创建 axios 函数， axios函数本质不是 Axios 的实例
 * @param {Object} defaultConfig The default config for the instance
 * @returns {Function} 调用该函数就是调用Axios.prototype.request()
 */
function createInstance(defaultConfig) {
    // 实例化核心类型 得到实例
    const context = new Axios(defaultConfig);
    // 创建 axios 函数
    const instance = bind(Axios.prototype.request, context);

    // 给 instance 设置全局配置接口
    instance.defaults = context.defaults;

    // 返回
    return instance;
}

// 创建 axios
const axios = createInstance(defaults);

// 以模块的形式对外暴露
export default axios;
```



### 2.6 取消请求

```
取消请求的步骤：
1. 提前定义变量用于存储取消函数
2. 请求配置中 设置 cancelToken, 它的值是 axios.CancelToken 的实例， 是一个 Promise 对象，将能够改变该 Promise状态的函数赋值给前面的变量
3. 需要的时候调用取消函数， 本质上改变Promise对象状态，状态一改，执行取消
注意： axios.isCancel(error) 判断错误是否是因为取消请求
```

```js
{
    code: "ERR_CANCELED"
    message: "canceled"
    name: "CanceledError"
}
```

```
执行流程：(调用了取消函数之后 发生了什么)
1. 调用取消函数
2. config.cancelToken 状态改变
3. 执行了 then 中的回调，回调里 xhr.abort
4. xhr.onabort 事件触发
```

```js
// 定义默认请求配置项
const defaults = {
    timeout: 0,
    responseType: 'json'
};

/**
 * 发送 ajax 请求
 * @param {object} config 请求配置项
 * @returns {Promise} 
 */
function dispatchRequest(config) {
    return new Promise((resolve, reject) => {
        // 创建 xhr 对象
        const xhr = new XMLHttpRequest();
        // 设置响应类型
        xhr.responseType = config.responseType;
        // 设置超时时间
        xhr.timeout = config.timeout;
        
        // 初始化
        xhr.open(config.method, config.url);

        // 设置请求头 xhr.setRequestHeader(key, value)
        if (config.headers) {
            for (let key in config.headers) {
                xhr.setRequestHeader(key, config.headers[key]);
            }
        }

        // 设置 请求体
        let body;
        // 只有允许的请求方法，才可以携带请求体
        if (['POST', 'PUT', 'PATCH'].includes(config.method)) {
            if (typeof config.data === 'string') {
                body = config.data;
                xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            } else if (Object.prototype.toString.call(config.data) === '[object Object]') {
                body = JSON.stringify(config.data);
                xhr.setRequestHeader('Content-type', 'application/json');
            } else {
                body = config.data;
            }
        }

        // 设置取消请求的Promise对象状态改变
        config.cancelToken.then(() => {
            xhr.abort(); // 取消请求
        })

        // 发送
        xhr.send(body);

        // 监听成功响应
        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                // console.log(xhr.getAllResponseHeaders().split('\r\n').filter(item=>item))

                // console.log(xhr.getAllResponseHeaders().split('\r\n').filter(item=>item).map(item=>item.split(': ')));

                // console.log(xhr.getAllResponseHeaders().split('\r\n').filter(item=>item).map(item=>item.split(': ')).reduce((pre,item)=>({...pre, [item[0]]:item[1]}), {}));

                resolve({
                    config,
                    request: xhr,
                    data: xhr.response,
                    statsu: xhr.status,
                    statusText: xhr.statusText,
                    headers: xhr.getAllResponseHeaders().split('\r\n').filter(item=>item).map(item=>item.split(': ')).reduce((pre,item)=>({...pre, [item[0]]:item[1]}), {})
                });
            } else {
                reject({
                    code: "ERR_BAD_REQUEST",
                    config,
                    message: "Request failed with status code " + xhr.status,
                    name: "AxiosError",
                    request: xhr
                });
            }
        }

        // 监听失败响应
        xhr.onerror = () => {
            reject({
                code: "ERR_NETWORK",
                config,
                message: "ERR_NETWORK",
                name: "AxiosError",
                request: xhr
            });
        }

        // 超时的事件
        xhr.ontimeout = () => {
            reject({
                code: "ECONNABORTED",
                config,
                message: `timeout of ${config.timeout}ms exceeded`,
                name: "AxiosError",
                request:xhr
            })
        }

        // 监听取消请求的事件
        xhr.onabort = () => {
            reject({
                code: "ERR_CANCELED",
                message: "canceled",
                name: "CanceledError"
            })
        }
    });
}

// 核心类
class Axios {
    // 构造器方法
    constructor(instanceConfig) {
        this.defaults = instanceConfig;
    }

    /**
     * 发送 ajax 请求
     * @param {String|Object} configOrUrl url或者请求配置对象
     * @param {?Object} config 请求配置对象，如果第一个参数已经是对象，不需要该参数
     * @returns {Promise} 
     */
    request(configOrUrl={}, config={}) {
        // 判断第一个参数是否是 url
        if (typeof configOrUrl === 'string') {
            config.url = configOrUrl
        } else {
            config = configOrUrl;
        }

        // 将传入的请求配置对象和全局请求配置对象合并
        config = Object.assign({}, this.defaults, config);

        // 设置默认请求方式是 GET
        config.method = (config.method || this.defaults.method || 'get').toUpperCase();

        // 合并 baseURL 和 url
        if (config.baseURL && !config.url.startsWith('http://') && !config.url.startsWith('https://')) {
            config.url = config.baseURL + config.url;
        }

        // 将 searchParams 拼接到 url 后面
        if (config.params) {
            config.url += '?' + Object.entries(config.params).map(item=>item[0]+'='+item[1]).join('&');
        }
        
        // 调用函数发送请求
        return dispatchRequest.call(this, config);
    }
}

function bind(fn, thisArg) {
    return function wrap() {
        // fn 就是 Axios.prototype.request
        // argments 是伪数组，成员是传递给 axios 函数的参数
        // 就是在调用 Axios.prototype.request， 并设置里面的this是Axios类的一个实例
        return fn.apply(thisArg, arguments)
    }
}

/**
 * 创建 axios 函数， axios函数本质不是 Axios 的实例
 * @param {Object} defaultConfig The default config for the instance
 * @returns {Function} 调用该函数就是调用Axios.prototype.request()
 */
function createInstance(defaultConfig) {
    // 实例化核心类型 得到实例
    const context = new Axios(defaultConfig);
    // 创建 axios 函数
    const instance = bind(Axios.prototype.request, context);

    // 给 instance 设置全局配置接口
    instance.defaults = context.defaults;

    // 返回
    return instance;
}

// 创建 axios
const axios = createInstance(defaults);

// 给 axios 设置属性
axios.CancelToken = Promise;
axios.isCancel = (err) => {
    return err.code === "ERR_CANCELED";
}

// 以模块的形式对外暴露
export default axios;
```

### 2.9 get()、post() 方法

```
1. 将 Axios 实例（context）上的属性都添加到 axios 上
2. 将 Axios 实例原型（Axios.prototype）上的方法都添加到 axios 上
```

```js
// 定义默认请求配置项
const defaults = {
    timeout: 0,
    responseType: 'json'
};

/**
 * 发送 ajax 请求
 * @param {object} config 请求配置项
 * @returns {Promise} 
 */
function dispatchRequest(config) {
    return new Promise((resolve, reject) => {
        // 创建 xhr 对象
        const xhr = new XMLHttpRequest();
        // 设置响应类型
        xhr.responseType = config.responseType;
        // 设置超时时间
        xhr.timeout = config.timeout;
        
        // 初始化
        xhr.open(config.method, config.url);

        // 设置请求头 xhr.setRequestHeader(key, value)
        if (config.headers) {
            for (let key in config.headers) {
                xhr.setRequestHeader(key, config.headers[key]);
            }
        }

        // 设置 请求体
        let body;
        // 只有允许的请求方法，才可以携带请求体
        if (['POST', 'PUT', 'PATCH'].includes(config.method)) {
            if (typeof config.data === 'string') {
                body = config.data;
                xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            } else if (Object.prototype.toString.call(config.data) === '[object Object]') {
                body = JSON.stringify(config.data);
                xhr.setRequestHeader('Content-type', 'application/json');
            } else {
                body = config.data;
            }
        }

        // 设置取消请求的Promise对象状态改变
        if (config.cancelToken) {
            config.cancelToken.then(() => {
                xhr.abort(); // 取消请求
            });
        }
    

        // 发送
        xhr.send(body);

        // 监听成功响应
        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve({
                    config,
                    request: xhr,
                    data: xhr.response,
                    statsu: xhr.status,
                    statusText: xhr.statusText,
                    headers: xhr.getAllResponseHeaders().split('\r\n').filter(item=>item).map(item=>item.split(': ')).reduce((pre,item)=>({...pre, [item[0]]:item[1]}), {})
                });
            } else {
                reject({
                    code: "ERR_BAD_REQUEST",
                    config,
                    message: "Request failed with status code " + xhr.status,
                    name: "AxiosError",
                    request: xhr
                });
            }
        }

        // 监听失败响应
        xhr.onerror = () => {
            reject({
                code: "ERR_NETWORK",
                config,
                message: "ERR_NETWORK",
                name: "AxiosError",
                request: xhr
            });
        }

        // 超时的事件
        xhr.ontimeout = () => {
            reject({
                code: "ECONNABORTED",
                config,
                message: `timeout of ${config.timeout}ms exceeded`,
                name: "AxiosError",
                request:xhr
            })
        }

        // 监听取消请求的事件
        xhr.onabort = () => {
            reject({
                code: "ERR_CANCELED",
                message: "canceled",
                name: "CanceledError"
            })
        }
    });
}

// 核心类
class Axios {
    // 构造器方法
    constructor(instanceConfig) {
        this.defaults = instanceConfig;
    }

    /**
     * 发送 ajax 请求
     * @param {String|Object} configOrUrl url或者请求配置对象
     * @param {?Object} config 请求配置对象，如果第一个参数已经是对象，不需要该参数
     * @returns {Promise} 
     */
    request(configOrUrl={}, config={}) {
        // 判断第一个参数是否是 url
        if (typeof configOrUrl === 'string') {
            config.url = configOrUrl
        } else {
            config = configOrUrl;
        }

        // 将传入的请求配置对象和全局请求配置对象合并
        config = Object.assign({}, this.defaults, config);

        // 设置默认请求方式是 GET
        config.method = (config.method || this.defaults.method || 'get').toUpperCase();

        // 合并 baseURL 和 url
        if (config.baseURL && !config.url.startsWith('http://') && !config.url.startsWith('https://')) {
            config.url = config.baseURL + config.url;
        }

        // 将 searchParams 拼接到 url 后面
        if (config.params) {
            config.url += '?' + Object.entries(config.params).map(item=>item[0]+'='+item[1]).join('&');
        }
        
        // 调用函数发送请求
        return dispatchRequest.call(this, config);
    }

    get(url, config={}) {
        return this.request(url, {
            ...config,
            method: 'GET'
        });
    }

    post(url, data, config={}) {
        return this.request(url, {
            ...config,
            data,
            method: 'POST'
        });
    }
    
}

function bind(fn, thisArg) {
    return function wrap() {
        // fn 就是 Axios.prototype.request
        // argments 是伪数组，成员是传递给 axios 函数的参数
        // 就是在调用 Axios.prototype.request， 并设置里面的this是Axios类的一个实例
        return fn.apply(thisArg, arguments)
    }
}

/**
 * 创建 axios 函数， axios函数本质不是 Axios 的实例
 * @param {Object} defaultConfig The default config for the instance
 * @returns {Function} 调用该函数就是调用Axios.prototype.request()
 */
function createInstance(defaultConfig) {
    // 实例化核心类型 得到实例
    const context = new Axios(defaultConfig);
    // 创建 axios 函数
    const instance = bind(Axios.prototype.request, context);

    // 给 instance 设置全局配置接口
    // instance.defaults = context.defaults;

    // 将 Axios 实例自身的所有属性都添加到 axios 上
    for (let key in context) {
        instance[key] = context[key];
    }

    // 将 Axios 实例的原型上所有属性都添加到 axios 上
    //console.log(Axios.prototype.request);
    Object.getOwnPropertyNames(Axios.prototype).forEach(key => {
        instance[key] = Axios.prototype[key].bind(context);
    });

    // 返回
    return instance;
}

// 创建 axios
const axios = createInstance(defaults);

// 给 axios 设置属性
axios.CancelToken = Promise;
axios.isCancel = (err) => {
    return err.code === "ERR_CANCELED";
}

// 以模块的形式对外暴露
export default axios;
```





### 2.8 实现拦截器







