## Fetch

Fetch 被设计用来取代 XMLHttpRequest，它提供了许多与 XMLHttpRequest 相同的功能，但被设计成更具可扩展性和高效性。

### 1 fetch 方法返回一个 Promise 对象

```js
fetch('http://example.com/movies.json')
.then(response => response.json())
.then(data => console.log(data));
```

### 2 fetch 设置请求配置项

```js
 fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify(data) // body data type must match "Content-Type" header
 });
```

更多选项： https://developer.mozilla.org/zh-CN/docs/Web/API/fetch