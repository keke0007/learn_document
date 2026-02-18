# 爬虫高级开发面试知识点总览

## 📚 目录

1. [爬虫基础](#1-爬虫基础)
2. [数据解析](#2-数据解析)
3. [反爬虫与应对](#3-反爬虫与应对)
4. [Scrapy 框架](#4-scrapy-框架)
5. [分布式爬虫](#5-分布式爬虫)
6. [性能优化](#6-性能优化)
7. [数据存储](#7-数据存储)
8. [法律法规](#8-法律法规)

---

## 1. 爬虫基础

### 1.1 HTTP 协议

**HTTP 请求方法**
- GET：获取资源
- POST：提交数据
- PUT：更新资源
- DELETE：删除资源

**请求头和响应头**
- User-Agent：用户代理
- Cookie：会话信息
- Content-Type：内容类型
- Status Code：状态码

### 1.2 请求库

**requests 库**
- GET 和 POST 请求
- Session 管理
- Cookie 处理
- 文件下载

**urllib 库**
- urllib.request
- urllib.parse
- urllib.error

**aiohttp 库**
- 异步 HTTP 请求
- 高并发支持

---

## 2. 数据解析

### 2.1 HTML 解析

**BeautifulSoup**
- 标签查找
- CSS 选择器
- 属性提取

**lxml**
- XPath 语法
- 高性能解析

**html.parser**
- Python 内置解析器
- 无需额外依赖

### 2.2 XPath 和 CSS 选择器

**XPath 语法**
- 路径表达式
- 条件筛选
- 函数使用

**CSS 选择器**
- 类选择器
- ID 选择器
- 属性选择器

### 2.3 正则表达式

**正则语法**
- 字符类
- 量词
- 分组

**常用模式**
- 邮箱匹配
- 手机号匹配
- URL 匹配

---

## 3. 反爬虫与应对

### 3.1 常见反爬虫机制

**User-Agent 检测**
- 识别爬虫请求
- 封禁特定 User-Agent

**IP 封禁**
- 限制请求频率
- 封禁异常 IP

**验证码**
- 图片验证码
- 滑动验证码
- 点选验证码

**JavaScript 渲染**
- 动态内容加载
- AJAX 请求

### 3.2 应对策略

**请求头伪装**
- 随机 User-Agent
- 完整请求头

**代理池**
- HTTP 代理
- SOCKS 代理
- 代理验证

**验证码识别**
- OCR 识别
- 打码平台
- 机器学习

**Selenium/Playwright**
- 浏览器自动化
- JavaScript 执行
- 页面渲染

---

## 4. Scrapy 框架

### 4.1 项目结构

```
project/
├── scrapy.cfg
└── project/
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders/
        └── example_spider.py
```

### 4.2 核心组件

**Spider**
- 定义爬取规则
- 数据提取
- 链接跟进

**Item**
- 数据结构定义
- 数据验证

**Pipeline**
- 数据处理
- 数据存储
- 数据清洗

**Middleware**
- 请求中间件
- 响应中间件
- 下载中间件

---

## 5. 分布式爬虫

### 5.1 Scrapy-Redis

**架构设计**
- Redis 作为任务队列
- 分布式去重
- 任务调度

**配置**
- SCHEDULER 设置
- DUPEFILTER 设置
- REDIS_URL 配置

### 5.2 任务调度

**任务分发**
- 任务队列管理
- 负载均衡
- 故障恢复

---

## 6. 性能优化

### 6.1 并发优化

**多线程爬虫**
- ThreadPoolExecutor
- 线程安全
- GIL 影响

**异步爬虫**
- asyncio
- aiohttp
- 协程池

### 6.2 资源优化

**连接池**
- HTTP 连接复用
- 连接数限制

**请求去重**
- URL 去重
- 内容去重

**缓存策略**
- 响应缓存
- 结果缓存

---

## 7. 数据存储

### 7.1 数据库存储

**MySQL**
- 关系型数据
- 事务支持

**MongoDB**
- 文档存储
- 灵活 schema

**Redis**
- 缓存
- 队列

### 7.2 文件存储

**JSON**
- 结构化数据
- 易于处理

**CSV**
- 表格数据
- Excel 兼容

---

## 8. 法律法规

### 8.1 合规要求

**robots.txt**
- 遵守爬取规则
- 尊重网站意愿

**服务条款**
- 阅读并遵守
- 避免违规

**数据使用**
- 合法使用数据
- 保护隐私

### 8.2 道德规范

**合理频率**
- 控制请求频率
- 避免服务器压力

**数据保护**
- 保护用户隐私
- 不泄露数据

---

## 📊 面试重点总结

### 高频面试题

1. **爬虫基础**
   - HTTP 协议
   - requests 库使用
   - Cookie 和 Session

2. **数据解析**
   - BeautifulSoup vs lxml
   - XPath vs CSS 选择器
   - 正则表达式

3. **反爬虫**
   - 常见反爬虫机制
   - 应对策略
   - 验证码识别

4. **Scrapy 框架**
   - 项目结构
   - Spider 编写
   - Pipeline 和 Middleware

5. **分布式爬虫**
   - Scrapy-Redis
   - 任务调度
   - 数据去重

6. **性能优化**
   - 并发优化
   - 资源优化
   - 缓存策略

### 手写代码题

1. **基础爬虫**
   - requests 请求
   - 数据解析
   - 文件下载

2. **反爬虫应对**
   - 代理池实现
   - 请求头伪装
   - Cookie 管理

3. **Scrapy 组件**
   - Spider 编写
   - Pipeline 实现
   - Middleware 编写

---

**最后更新：2026-01-26**
