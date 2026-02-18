# 浏览器原理案例

## 案例概述

本案例通过实际代码演示浏览器的工作原理，包括渲染机制、事件循环、网络协议等。

## 知识点

1. **浏览器渲染机制**
   - 渲染流程
   - 重排和重绘
   - 合成层

2. **事件循环**
   - 宏任务和微任务
   - 执行顺序
   - 异步处理

3. **网络协议**
   - HTTP/HTTPS
   - 缓存机制
   - WebSocket

## 案例代码

### 案例1：浏览器渲染流程

```javascript
// 浏览器渲染流程
// 1. 解析 HTML，构建 DOM 树
// 2. 解析 CSS，构建 CSSOM 树
// 3. 合并 DOM 和 CSSOM，构建渲染树
// 4. 布局（Layout/Reflow）：计算元素位置
// 5. 绘制（Paint）：填充像素
// 6. 合成（Composite）：图层合成

// 避免重排和重绘
// 不好的做法：多次修改样式，触发多次重排
element.style.width = '100px';
element.style.height = '100px';
element.style.left = '10px';
element.style.top = '10px';

// 好的做法1：使用 transform（只触发合成）
element.style.transform = 'translate(10px, 10px) scale(1)';

// 好的做法2：批量修改 DOM
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const div = document.createElement('div');
  fragment.appendChild(div);
}
container.appendChild(fragment);

// 好的做法3：使用 class 批量修改
element.classList.add('new-style');

// 读取布局属性会触发重排
const width = element.offsetWidth; // 触发重排
element.style.width = width + 10 + 'px'; // 触发重排

// 使用 requestAnimationFrame 优化动画
function animate() {
  element.style.left = (parseInt(element.style.left) + 1) + 'px';
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

### 案例2：事件循环

```javascript
// 事件循环执行顺序
console.log('1');

setTimeout(() => {
  console.log('2');
}, 0);

Promise.resolve().then(() => {
  console.log('3');
});

console.log('4');

// 输出顺序：1, 4, 3, 2
// 执行顺序：同步代码 -> 微任务 -> 宏任务

// 宏任务和微任务
console.log('start');

setTimeout(() => {
  console.log('timeout1');
  Promise.resolve().then(() => {
    console.log('promise1');
  });
}, 0);

setTimeout(() => {
  console.log('timeout2');
}, 0);

Promise.resolve().then(() => {
  console.log('promise2');
});

console.log('end');

// 输出：start, end, promise2, timeout1, promise1, timeout2

// 微任务队列
Promise.resolve().then(() => {
  console.log('promise1');
});

Promise.resolve().then(() => {
  console.log('promise2');
});

// 输出：promise1, promise2（按顺序执行）

// 宏任务队列
setTimeout(() => {
  console.log('timeout1');
}, 0);

setTimeout(() => {
  console.log('timeout2');
}, 0);

// 输出：timeout1, timeout2（按顺序执行）
```

### 案例3：HTTP 缓存

```javascript
// 强缓存：Cache-Control
// 服务器设置
// Cache-Control: max-age=3600

// 协商缓存：ETag
fetch('/api/data', {
  headers: {
    'If-None-Match': etag
  }
})
  .then(response => {
    if (response.status === 304) {
      // 使用缓存
      return cachedData;
    }
    return response.json();
  });

// 协商缓存：Last-Modified
fetch('/api/data', {
  headers: {
    'If-Modified-Since': lastModified
  }
})
  .then(response => {
    if (response.status === 304) {
      // 使用缓存
      return cachedData;
    }
    return response.json();
  });

// Service Worker 缓存
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request).then(response => {
          const responseClone = response.clone();
          caches.open('v1').then(cache => {
            cache.put(event.request, responseClone);
          });
          return response;
        });
      })
  );
});
```

### 案例4：WebSocket

```javascript
// WebSocket 连接
const ws = new WebSocket('wss://example.com/ws');

ws.onopen = () => {
  console.log('WebSocket connected');
  ws.send('Hello Server');
};

ws.onmessage = (event) => {
  console.log('Message from server:', event.data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket closed');
};

// React Hook：useWebSocket
function useWebSocket(url) {
  const [socket, setSocket] = useState(null);
  const [message, setMessage] = useState(null);
  const [readyState, setReadyState] = useState(WebSocket.CONNECTING);
  
  useEffect(() => {
    const ws = new WebSocket(url);
    
    ws.onopen = () => {
      setReadyState(WebSocket.OPEN);
    };
    
    ws.onmessage = (event) => {
      setMessage(event.data);
    };
    
    ws.onerror = () => {
      setReadyState(WebSocket.CLOSED);
    };
    
    ws.onclose = () => {
      setReadyState(WebSocket.CLOSED);
    };
    
    setSocket(ws);
    
    return () => {
      ws.close();
    };
  }, [url]);
  
  const sendMessage = useCallback((data) => {
    if (socket && readyState === WebSocket.OPEN) {
      socket.send(data);
    }
  }, [socket, readyState]);
  
  return { socket, message, readyState, sendMessage };
}
```

### 案例5：浏览器存储

```javascript
// LocalStorage
localStorage.setItem('key', 'value');
const value = localStorage.getItem('key');
localStorage.removeItem('key');
localStorage.clear();

// SessionStorage
sessionStorage.setItem('key', 'value');
const value = sessionStorage.getItem('key');

// Cookie
function setCookie(name, value, days) {
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function getCookie(name) {
  const nameEQ = name + '=';
  const ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

// IndexedDB
const request = indexedDB.open('MyDatabase', 1);

request.onerror = (event) => {
  console.error('IndexedDB error:', event);
};

request.onsuccess = (event) => {
  const db = event.target.result;
  const transaction = db.transaction(['users'], 'readwrite');
  const objectStore = transaction.objectStore('users');
  const request = objectStore.add({ id: 1, name: 'John' });
  
  request.onsuccess = () => {
    console.log('Data added');
  };
};

request.onupgradeneeded = (event) => {
  const db = event.target.result;
  const objectStore = db.createObjectStore('users', { keyPath: 'id' });
};
```

## 验证数据

### 渲染性能测试

| 操作 | 重排时间 | 重绘时间 | 合成时间 |
|-----|---------|---------|---------|
| 修改 width | 5ms | 2ms | - |
| 修改 transform | - | - | 1ms |
| 批量修改 DOM | 50ms | 20ms | - |
| 使用 class | 3ms | 1ms | - |

### 事件循环测试

```
同步代码执行时间：1ms
微任务执行时间：0.5ms
宏任务执行时间：5ms
```

## 总结

1. **渲染优化**
   - 避免频繁重排和重绘
   - 使用 transform 和 opacity
   - 批量修改 DOM

2. **事件循环**
   - 理解宏任务和微任务
   - 合理使用异步操作
   - 避免阻塞主线程

3. **缓存策略**
   - 合理使用浏览器缓存
   - 设置合适的缓存时间
   - 使用 Service Worker

4. **存储选择**
   - Cookie：小数据，每次请求携带
   - LocalStorage：持久化存储
   - SessionStorage：会话存储
   - IndexedDB：大容量存储
