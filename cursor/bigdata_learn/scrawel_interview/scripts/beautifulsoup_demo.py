"""
BeautifulSoup 示例
演示 HTML 解析的各种方法
"""

from bs4 import BeautifulSoup
import requests

html = """
<html>
<head><title>Example</title></head>
<body>
    <div class="content">
        <h1>Title</h1>
        <p class="text">Paragraph 1</p>
        <p class="text">Paragraph 2</p>
        <a href="https://example.com">Link</a>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
    </div>
</body>
</html>
"""

# 1. 基础解析
def basic_parsing():
    soup = BeautifulSoup(html, 'lxml')
    
    # 查找单个标签
    title = soup.find('title')
    print(f"Title: {title.text}")
    
    # 查找所有标签
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        print(f"Paragraph: {p.text}")

# 2. CSS 选择器
def css_selector():
    soup = BeautifulSoup(html, 'lxml')
    
    # 类选择器
    divs = soup.select('div.content')
    print(f"Divs: {len(divs)}")
    
    # 属性选择器
    links = soup.select('a[href]')
    for link in links:
        print(f"Link: {link.get('href')}")
    
    # 组合选择器
    items = soup.select('div.content > p.text')
    for item in items:
        print(f"Item: {item.text}")

# 3. 属性提取
def attribute_extraction():
    soup = BeautifulSoup(html, 'lxml')
    
    # 获取属性
    link = soup.find('a')
    href = link.get('href')
    text = link.get_text()
    print(f"Link: {text} -> {href}")

# 4. 嵌套查找
def nested_search():
    soup = BeautifulSoup(html, 'lxml')
    
    content_div = soup.find('div', class_='content')
    items = content_div.find_all('p')
    for item in items:
        print(f"Item: {item.text}")

# 5. 文本提取
def text_extraction():
    soup = BeautifulSoup(html, 'lxml')
    
    # 获取文本
    text = soup.get_text()
    print(f"All text: {text[:50]}...")
    
    # 获取单个元素文本
    title = soup.find('h1')
    print(f"Title text: {title.get_text(strip=True)}")

# 6. 实际网页解析
def parse_real_website():
    response = requests.get('https://www.example.com')
    soup = BeautifulSoup(response.text, 'lxml')
    
    # 提取标题
    title = soup.find('title')
    print(f"Page title: {title.text if title else 'Not found'}")
    
    # 提取所有链接
    links = soup.find_all('a', href=True)
    for link in links[:5]:  # 只显示前5个
        print(f"Link: {link.get('href')}")

if __name__ == "__main__":
    print("=== 基础解析 ===")
    basic_parsing()
    print()
    
    print("=== CSS 选择器 ===")
    css_selector()
    print()
    
    print("=== 属性提取 ===")
    attribute_extraction()
    print()
    
    print("=== 嵌套查找 ===")
    nested_search()
    print()
    
    print("=== 文本提取 ===")
    text_extraction()
    print()
    
    print("=== 实际网页解析 ===")
    # parse_real_website()
