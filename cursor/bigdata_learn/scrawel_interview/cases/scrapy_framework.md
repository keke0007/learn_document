# Scrapy 框架案例

## 案例概述

本案例通过实际代码演示 Scrapy 框架的使用，包括 Spider 编写、Item 定义、Pipeline 处理等。

## 知识点

1. **Scrapy 基础**
   - 项目结构
   - Spider 编写
   - Item 定义

2. **Pipeline 和 Middleware**
   - 数据处理 Pipeline
   - 请求中间件
   - 响应中间件

3. **高级特性**
   - 增量爬取
   - 去重策略
   - 数据存储

## 案例代码

### 案例1：基础 Spider

```python
import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['https://www.example.com']
    
    def parse(self, response):
        # 提取数据
        title = response.css('h1::text').get()
        content = response.css('div.content::text').get()
        
        yield {
            'title': title,
            'content': content,
            'url': response.url
        }
        
        # 跟进链接
        links = response.css('a::attr(href)').getall()
        for link in links:
            yield response.follow(link, self.parse)
```

### 案例2：Item 定义

```python
import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()

# 在 Spider 中使用
class ArticleSpider(scrapy.Spider):
    name = 'article'
    
    def parse(self, response):
        item = ArticleItem()
        item['title'] = response.css('h1::text').get()
        item['content'] = response.css('div.content::text').get()
        item['url'] = response.url
        yield item
```

### 案例3：Pipeline 处理

```python
import json
import pymongo

class JsonPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w')
    
    def close_spider(self, spider):
        self.file.close()
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        self.db[spider.name].insert_one(dict(item))
        return item
```

### 案例4：Middleware 使用

```python
import random
from scrapy import signals

class UserAgentMiddleware:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        ]
    
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)
        return None

class ProxyMiddleware:
    def __init__(self):
        self.proxies = [
            'http://proxy1.example.com:8080',
            'http://proxy2.example.com:8080'
        ]
    
    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy
        return None
```

### 案例5：增量爬取

```python
import scrapy
import hashlib

class IncrementalSpider(scrapy.Spider):
    name = 'incremental'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_urls = set()
    
    def parse(self, response):
        # 生成 URL 的哈希值
        url_hash = hashlib.md5(response.url.encode()).hexdigest()
        
        # 检查是否已爬取
        if url_hash in self.seen_urls:
            self.logger.info(f"Skip duplicate: {response.url}")
            return
        
        self.seen_urls.add(url_hash)
        
        # 提取数据
        yield {
            'title': response.css('h1::text').get(),
            'url': response.url
        }
```

## 验证数据

### Scrapy 性能

| 场景 | 普通爬虫 | Scrapy | 提升 |
|-----|---------|--------|------|
| 1000个页面 | 500s | 50s | 90% |
| 数据存储 | 手动处理 | 自动Pipeline | 效率提升 |
| 去重 | 手动实现 | 内置去重 | 更可靠 |

## 总结

1. **Scrapy 优势**
   - 高性能
   - 内置去重
   - 灵活的 Pipeline
   - 强大的中间件

2. **最佳实践**
   - 合理使用 Item
   - 编写高效的 Pipeline
   - 配置合适的并发数
   - 使用中间件处理反爬虫
