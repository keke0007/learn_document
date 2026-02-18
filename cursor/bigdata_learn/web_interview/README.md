# 前端高级开发面试知识点总览

## 📚 目录

1. [JavaScript 核心](#1-javascript-核心)
2. [Vue.js 框架](#2-vuejs-框架)
3. [React 框架](#3-react-框架)
4. [性能优化](#4-性能优化)
5. [浏览器原理](#5-浏览器原理)
6. [前端工程化](#6-前端工程化)
7. [TypeScript](#7-typescript)
8. [算法和数据结构](#8-算法和数据结构)

---

## 1. JavaScript 核心

### 1.1 闭包和作用域

**闭包定义**
- 函数能够访问其外部作用域的变量
- 即使外部函数执行完毕，内部函数仍能访问外部变量

**作用域类型**
- 全局作用域
- 函数作用域
- 块级作用域（ES6 let/const）

**应用场景**
- 模块化模式
- 私有变量
- 函数柯里化
- 事件处理

### 1.2 原型链和继承

**原型链机制**
- 每个对象都有 `__proto__` 属性
- 每个函数都有 `prototype` 属性
- 通过原型链实现继承

**继承方式**
- 原型链继承
- 构造函数继承
- 组合继承
- ES6 类继承

### 1.3 this 指向

**this 绑定规则**
- 默认绑定：全局对象（严格模式 undefined）
- 隐式绑定：调用对象
- 显式绑定：call/apply/bind
- new 绑定：新创建的对象

**箭头函数 this**
- 箭头函数没有自己的 this
- this 指向定义时的上下文

### 1.4 异步编程

**Promise**
- Promise 三种状态：pending、fulfilled、rejected
- Promise 链式调用
- Promise.all、Promise.race、Promise.allSettled

**async/await**
- async 函数返回 Promise
- await 等待 Promise 完成
- 错误处理使用 try/catch

**事件循环**
- 宏任务：setTimeout、setInterval、I/O
- 微任务：Promise.then、queueMicrotask
- 执行顺序：同步代码 -> 微任务 -> 宏任务

---

## 2. Vue.js 框架

### 2.1 响应式原理

**Vue 2（Object.defineProperty）**
- 通过 Object.defineProperty 劫持属性
- get 时收集依赖
- set 时触发更新
- 无法监听数组索引和 length 变化

**Vue 3（Proxy）**
- 使用 Proxy 代理整个对象
- 支持数组和对象的所有操作
- 性能更好，功能更强

### 2.2 虚拟 DOM

**虚拟 DOM 结构**
- 用 JavaScript 对象描述 DOM
- 减少直接操作 DOM
- 通过 diff 算法找出差异

**diff 算法**
- 同层比较，不跨层
- 通过 key 标识节点
- 只更新变化的节点

### 2.3 组件化

**组件通信**
- 父子：props / $emit
- 兄弟：事件总线 / Vuex
- 跨级：provide / inject

**插槽（Slots）**
- 默认插槽
- 具名插槽
- 作用域插槽

### 2.4 Vue 3 新特性

**Composition API**
- setup 函数
- ref、reactive
- computed、watch
- 生命周期钩子

**其他特性**
- Teleport：传送组件
- Suspense：异步组件
- Fragment：多根节点

---

## 3. React 框架

### 3.1 核心概念

**JSX**
- JavaScript 语法扩展
- 编译成 React.createElement
- 必须返回单个根元素（Fragment）

**虚拟 DOM**
- 用 JavaScript 对象描述 DOM
- 通过 diff 算法更新
- 提升性能

### 3.2 Fiber 架构

**Fiber 特点**
- 可中断的渲染
- 优先级调度
- 增量渲染
- 更好的用户体验

### 3.3 Hooks

**基础 Hooks**
- useState：状态管理
- useEffect：副作用处理
- useContext：上下文

**高级 Hooks**
- useMemo：缓存计算结果
- useCallback：缓存函数
- useRef：引用
- useReducer：状态管理

**自定义 Hooks**
- 封装逻辑复用
- 以 use 开头
- 可以调用其他 Hooks

### 3.4 性能优化

**React.memo**
- 浅比较 props
- 避免不必要的渲染

**useMemo / useCallback**
- 缓存计算结果和函数
- 减少重复计算

**代码分割**
- React.lazy
- Suspense
- 路由懒加载

---

## 4. 性能优化

### 4.1 代码层面

**防抖和节流**
- 防抖：延迟执行，适合搜索
- 节流：限制频率，适合滚动

**懒加载**
- 路由懒加载
- 组件懒加载
- 图片懒加载

**代码分割**
- Webpack splitChunks
- 动态 import
- Tree Shaking

### 4.2 资源优化

**图片优化**
- 使用 WebP 格式
- 响应式图片
- 图片压缩
- 懒加载

**资源压缩**
- Gzip 压缩
- 代码压缩
- CSS 压缩

**CDN 加速**
- 静态资源 CDN
- 减少请求时间

### 4.3 渲染优化

**虚拟滚动**
- 只渲染可见区域
- 适用于长列表

**骨架屏**
- 提升感知性能
- 改善用户体验

**预加载和预渲染**
- link rel="preload"
- link rel="prefetch"
- 预渲染关键页面

---

## 5. 浏览器原理

### 5.1 渲染机制

**渲染流程**
1. 解析 HTML：构建 DOM 树
2. 解析 CSS：构建 CSSOM 树
3. 合并：构建渲染树
4. 布局：计算元素位置
5. 绘制：填充像素
6. 合成：图层合成

**重排和重绘**
- 重排（Reflow）：改变布局
- 重绘（Repaint）：改变外观
- 避免频繁重排和重绘

### 5.2 网络协议

**HTTP/HTTPS**
- HTTP 1.1：持久连接
- HTTP 2：多路复用
- HTTPS：加密传输

**缓存机制**
- 强缓存：Cache-Control、Expires
- 协商缓存：ETag、Last-Modified

**WebSocket**
- 全双工通信
- 实时数据传输

### 5.3 浏览器存储

**Cookie**
- 4KB 大小限制
- 每次请求都会携带
- 可设置过期时间

**LocalStorage**
- 5-10MB 大小
- 持久化存储
- 同源策略

**SessionStorage**
- 会话级存储
- 关闭标签页清除

**IndexedDB**
- 大容量存储
- 异步 API
- 支持事务

---

## 6. 前端工程化

### 6.1 构建工具

**Webpack**
- 模块打包
- 代码分割
- 插件系统
- Loader 机制

**Vite**
- 快速开发服务器
- 基于 ES Module
- 生产环境 Rollup 打包

**Rollup**
- 库打包工具
- Tree Shaking
- 输出格式多样

### 6.2 代码质量

**ESLint**
- 代码检查
- 规则配置
- 自动修复

**Prettier**
- 代码格式化
- 统一风格

**TypeScript**
- 类型检查
- 增强 IDE 支持
- 减少错误

### 6.3 测试

**单元测试**
- Jest：测试框架
- Vitest：Vite 生态
- 测试覆盖率

**E2E 测试**
- Cypress
- Playwright
- Puppeteer

---

## 7. TypeScript

### 7.1 基础类型

**基本类型**
- number、string、boolean
- array、tuple
- enum、any、void

**高级类型**
- union、intersection
- 泛型
- 条件类型
- 映射类型

### 7.2 类型系统

**类型推断**
- 自动推断类型
- 上下文推断

**类型断言**
- as 语法
- <> 语法

**类型守卫**
- typeof
- instanceof
- in 操作符

---

## 8. 算法和数据结构

### 8.1 常见算法

**排序算法**
- 快速排序
- 归并排序
- 堆排序

**查找算法**
- 二分查找
- 哈希查找

**字符串算法**
- KMP 算法
- 正则表达式

### 8.2 数据结构

**数组和链表**
- 数组：随机访问快
- 链表：插入删除快

**栈和队列**
- 栈：LIFO
- 队列：FIFO

**树和图**
- 二叉树
- 图的遍历

---

## 📊 面试重点总结

### 高频面试题

1. **JavaScript 核心**
   - 闭包和作用域
   - 原型链和继承
   - this 指向
   - 事件循环

2. **框架原理**
   - Vue 响应式原理
   - React Fiber 架构
   - 虚拟 DOM 和 diff 算法

3. **性能优化**
   - 防抖和节流
   - 虚拟滚动
   - 代码分割
   - 缓存策略

4. **浏览器原理**
   - 渲染流程
   - 重排和重绘
   - HTTP 缓存

5. **工程化**
   - Webpack 原理
   - TypeScript
   - 测试框架

### 手写代码题

1. **工具函数**
   - 防抖和节流
   - 深拷贝
   - 数组扁平化
   - 函数柯里化

2. **Promise**
   - Promise 实现
   - Promise.all
   - Promise.race

3. **框架相关**
   - 响应式实现
   - 虚拟 DOM diff
   - 事件总线

---

**最后更新：2026-01-26**
