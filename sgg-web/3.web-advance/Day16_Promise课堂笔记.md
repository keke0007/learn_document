# Day 16 Promise 课堂笔记

## 回顾

```
1. XMLHttpRequest 对象
   1.1 ajax 基本流程步骤
   1.2 发送请求
       ① url 携带参数
       ② 请求体 字符串 
       ② 请求体 FormData
   1.3 处理响应
   1.4 响应超时
   1.5 进度事件
   1.6 同步和异步

2. 同源策略
   打开页面的URL和ajax请求的URL 协议、域名（ip地址）、端口 必须相同
   2.1 跨域方案一： 后端做出响应的时候，设置响应头
   2.2 跨域方案二： josnp

3. 封装 ajax 函数
4. ajax记账本
```







## 1 Promise 概述

Promise 是异步编程的一种解决方法，比传统的方式更加高效、友好！Promise 是 ES6 新增的语法。

使用 Promise 语法需要创建一个 promise 对象，promise 对象中包含一个异步操作， 可以通过实例化 Promise 构造函数来创造 promise 对象。

promise 对象具有三种状态：

1. pending 状态， 进行中， 刚创建的 promise 对象就处于 pending 状态。
2. resolved（fulfilled） 状态，已成功， 内部的异步操作执行成功，promise 对象的状态由 pending -> resolved
3. rejected 状态，已失败。 内部的异步操作执行失败，promise 对象的状态由 pending -> rejected

当 promise 的状态发生改变，就再也不会变了！



## 2 Promise 基本语法

#### ① 使用 Promise 构造函数创建 promise 对象

```js
 new Promise((res, rej) => {
     console.log('第一个参数：', res);
     console.log('第二个参数：', rej);
 });
```

```js
1. 实例化 Promise 类，需要传一个回调函数作为参数
2. Promise 类的回调函数（参数），在实例化 Promise 的时候会自动调用，是同步任务
3. Promise 类的回调函数（参数），在被调用的时候，会接收两个参数，两个参数都是函数
```

#### ② 修改 promise 对象的状态

```js
new Promise((resolve, reject) => {
    // 调用第一个参数 该promise对象的状态改为 resolved（fulfilled）
    // 可以传个参数作为 PromiseResult
    // resolve('hello');
    // resolve({status:'OK', msg: 'success'});

    // 调用第二个参数， 该promise对象的状态改为 rejected
    // 可以传个参数作为 PromiseResult
    // reject();
    reject([10,20,30,40]);
});
```

```
1. 调用 Promise 类回调函数的第一个参数，该 promise 对象改为 resolve(fulfilled)状态，可以传个参数作为 PromiseResult
2. 调用 Promise 类回调函数的第二个参数，该 promise 对象改为 rejected 状态，可以传个参数作为 PromiseResult
3.promise 类回调函数中抛出异常promise对象改为rejected状态，值是异常信息
3. promise 对象的状态一旦改变，就无法再修改

```

#### ③ 为 promise 对象设置回调函数

```js
promise对象.then(res => {
    // 如果promise对象是成功状态，执行该回调函数
    // res 可以获取 PromiseResult
}, err => {
    // 如果promise对象是失败状态，执行该回调函数
    // res 可以获取 PromiseResult
});
```

```
1. promise对象的then方法第第一个参数（回调函数），状态变为成功会执行，可以通过形参得到 PromiseResult
2. promise对象的then方法第第二个参数（回调函数），状态变为失败会执行，可以通过形参得到 PromiseResult
3. then 方法的两个回调函数都是异步执行！
```



## 3 Promise 实例的方法

### 3.1 then 方法

#### ① 参数

```
1. 第一个参数，是一个回调函数，当promise对象的状态改为成功的时候，会被调用，并接收到参数 PromiseResult
2. 第一个参数，是一个回调函数，当promise对象的状态改为失败的时候，会被调用，并接收到参数 PromiseResult
```

#### ② 返回值

`then()` 方法的返回值是一个 Promise 对象，该 Promise 对象的状态取决于 `then()` 方法回调函数的返回值（then 可以设置两个回调函数，哪个回调函数执行就取决于谁）

`then()` 方法回调函数的返回值对 `then()` 方法返回的 Promise 对象的影响，如下：

```
1. 情况一，回调函数没有返回值, then()返回的Promise对象改为成功状态，PromiseResult是undefined
2. 情况二：返回非Promise类型的对象或原始类型数据，then()返回的Promise对象改为成功状态，PromiseResult是该回调的返回值
3. 情况三：返回Promise对象， then()返回的Promise对象与该回调返回的Promise对象，状态和PromiseResult保持一致
4. 情况四：出现代码运行错误,  then()返回的Promise对象,状态改为失败，PromiseResult是错误对象
```

#### ③ 链式调用

由于 then() 方法返回的仍然是一个 promise 对象，所以支持链式调用，then() 的链式调用可以解决**回调地狱**的问题。 

```js
promise对象
.then(val => {}, reason => {})
.then(val => {}, reason => {})
.then(val => {}, reason => {})
.then(val => {}, reason => {})
.then(val => {}, reason => {})
```

### 3.2 catch 方法

#### ① 参数

需要一个回调函数作为参数，Promise对象的状态改为失败的的时候，执行该回调函数。

#### ② then 和 catch 可以配合使用

```js
promise对象
.then(value => {
    console.log('成功！', value);
})
.catch(reason => {
    console.log('失败！', reason);
})
```

#### ③ 返回值

catch() 返回 promise 对象，promise 对象的状态由回调函数的返回值决定，与 then() 方法相同

#### ③ 异常穿透

```js
promise对象
.then(val => {})
.then(val => {})
.then(val => {})
.then(val => {})
.then(val => {})
.catch(reason => {})
```

### 3.3 finally

finally() 也需要设置一个回调函数作为参数，不论 promise 对象是什么状态，都一定会执行，可以与 then() catch() 一起使用：

```js
promise对象
.then(value => {
     console.log('成功！', value);
 })
.catch(reason => {
     console.log('失败！', reason);
 })
.finally( () => {
     console.log('finally');
 });
```



## 4 Promise 构造函数本身的方法

### 4.1 Promise.resolve()

#### ①  功能

该方法返回一个 promise 对象， 状态由参数决定。

#### ② 根据参数不同返回的 Promise 对象的状态也不同：

1) 情况一： 没有参数，返回的 promise 对象状态会变为成功，PromiseResult 是 undefined

2) 情况二： 参数是除了 Promise 对象和 thenable 对象以外的其他对象或原始类型数据 ，返回的 promise 对象状态会变为成功，PromiseResult 是参数

3) 情况三：参数是一个 promise 对象，该参数直接作为 resolve() 方法的返回值

```js
 const p1 = new Promise((resolve, reject) => {
     const randNum = Math.random();
     if ( randNum>= .5) {
         // 设置为成功状态
         resolve(randNum);
     } else {
         // 设置为失败的状态
         reject(randNum);
     }
 });

const p = Promise.resolve(p1);  // 等价于 const p = p1;
```

 4) 情况四：参数是一个 thenable 对象, 具有 then 方法的对象称为 thenable 对象， then 方法接收两个参数，调用第一个参数，设置为成功状态，调用第二个参数设置为失败状态 

```js
// 创建一个 thenable 对象
const obj = {
    then(res, rej) {
        const randNum = Math.floor(Math.random() * 10);
        if ( randNum>= 5) {
            // 设置为成功状态
            res(randNum);
        } else {
            // 设置为失败的状态
            rej(randNum);
        }
    }
}

const p = Promise.resolve(obj);
```

### 4.2 Promise.reject()

返回一个 失败状态的 Promise 对象，参数作为 PromiseResult。



### 4.3 Promise.all()

### 4.4 Promise.race()

### 4.5 Promise.allSettled()






