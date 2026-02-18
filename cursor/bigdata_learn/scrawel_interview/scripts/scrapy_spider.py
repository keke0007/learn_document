"""
Scrapy Spider 示例
演示 Scrapy 爬虫的编写
"""

import scrapy

# 基础 Spider
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

# Item 定义
class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()

# 使用 Item 的 Spider
class ArticleSpider(scrapy.Spider):
    name = 'article'
    start_urls = ['https://www.example.com/articles']
    
    def parse(self, response):
        item = ArticleItem()
        item['title'] = response.css('h1::text').get()
        item['content'] = response.css('div.content::text').get()
        item['author'] = response.css('span.author::text').get()
        item['publish_time'] = response.css('time::attr(datetime)').get()
        item['tags'] = response.css('a.tag::text').getall()
        item['url'] = response.url
        yield item
        
        # 翻页
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

# Pipeline 示例
class JsonPipeline:
    def open_spider(self, spider):
        import json
        self.file = open('items.json', 'w')
    
    def close_spider(self, spider):
        self.file.close()
    
    def process_item(self, item, spider):
        import json
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

# 运行示例（需要在 Scrapy 项目中运行）
# scrapy crawl example
