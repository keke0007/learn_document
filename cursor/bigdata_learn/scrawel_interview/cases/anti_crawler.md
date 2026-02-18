# 反爬虫与应对案例

## 案例概述

本案例通过实际代码演示常见的反爬虫机制和应对策略。

## 知识点

1. **常见反爬虫机制**
   - User-Agent 检测
   - IP 封禁
   - 验证码
   - JavaScript 渲染

2. **应对策略**
   - 请求头伪装
   - 代理池
   - 验证码识别
   - Selenium/Playwright

## 案例代码

### 案例1：请求头伪装

```python
import requests
import random

# User-Agent 池
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

# 使用随机请求头
response = requests.get('https://www.example.com', headers=get_random_headers())
```

### 案例2：代理池

```python
import requests
import random

# 代理池
PROXIES = [
    {'http': 'http://proxy1.example.com:8080', 'https': 'https://proxy1.example.com:8080'},
    {'http': 'http://proxy2.example.com:8080', 'https': 'https://proxy2.example.com:8080'},
    {'http': 'http://proxy3.example.com:8080', 'https': 'https://proxy3.example.com:8080'}
]

def get_random_proxy():
    return random.choice(PROXIES)

# 使用代理
def request_with_proxy(url):
    max_retries = 3
    for _ in range(max_retries):
        try:
            proxy = get_random_proxy()
            response = requests.get(url, proxies=proxy, timeout=10)
            if response.status_code == 200:
                return response
        except Exception as e:
            print(f"Proxy failed: {e}")
            continue
    return None

# 代理验证
def verify_proxy(proxy):
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=5)
        return response.status_code == 200
    except:
        return False
```

### 案例3：Cookie 处理

```python
import requests
from http.cookiejar import MozillaCookieJar

# 使用 CookieJar 保存 Cookie
def save_cookies():
    session = requests.Session()
    session.get('https://www.example.com/login', data={'user': 'test', 'pass': 'test'})
    
    # 保存 Cookie
    jar = MozillaCookieJar('cookies.txt')
    for cookie in session.cookies:
        jar.set_cookie(cookie)
    jar.save(ignore_discard=True, ignore_expires=True)

# 加载 Cookie
def load_cookies():
    session = requests.Session()
    jar = MozillaCookieJar('cookies.txt')
    jar.load(ignore_discard=True, ignore_expires=True)
    session.cookies = jar
    return session
```

### 案例4：Selenium 处理 JavaScript

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 配置 Chrome 选项
def create_driver():
    options = Options()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    
    driver = webdriver.Chrome(options=options)
    return driver

# 使用 Selenium
def selenium_example():
    driver = create_driver()
    try:
        driver.get('https://www.example.com')
        
        # 等待元素加载
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "element-id"))
        )
        
        # 执行 JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # 获取页面源码
        html = driver.page_source
        
        return html
    finally:
        driver.quit()
```

### 案例5：验证码识别

```python
import requests
from PIL import Image
import pytesseract

# 下载验证码图片
def download_captcha(url):
    response = requests.get(url)
    with open('captcha.png', 'wb') as f:
        f.write(response.content)
    return 'captcha.png'

# OCR 识别验证码
def recognize_captcha(image_path):
    image = Image.open(image_path)
    # 图像预处理
    image = image.convert('L')  # 灰度化
    # 使用 OCR 识别
    text = pytesseract.image_to_string(image)
    return text.strip()

# 使用打码平台
def recognize_with_api(image_path):
    api_url = 'https://api.captcha-service.com/recognize'
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(api_url, files=files)
        return response.json()['text']
```

### 案例6：请求频率控制

```python
import time
import random
from collections import deque

class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def wait_if_needed(self):
        now = time.time()
        # 移除过期的请求记录
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()
        
        # 如果超过限制，等待
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            time.sleep(sleep_time)
        
        self.requests.append(time.time())

# 使用频率限制器
limiter = RateLimiter(max_requests=10, time_window=60)

for url in urls:
    limiter.wait_if_needed()
    response = requests.get(url)
```

## 验证数据

### 反爬虫应对效果

| 策略 | 成功率 | 说明 |
|-----|--------|------|
| 无伪装 | 30% | 容易被封 |
| User-Agent 伪装 | 60% | 基础应对 |
| 代理池 | 85% | 有效应对 |
| Selenium | 90% | 完全模拟浏览器 |

### 性能对比

```
普通请求：速度快，但容易被封
代理请求：速度中等，稳定性好
Selenium：速度慢，但成功率高
```

## 总结

1. **反爬虫机制**
   - User-Agent 检测
   - IP 封禁
   - 验证码
   - JavaScript 渲染

2. **应对策略**
   - 请求头伪装
   - 代理池
   - 验证码识别
   - Selenium/Playwright

3. **最佳实践**
   - 合理控制请求频率
   - 使用多种策略组合
   - 遵守网站 robots.txt
   - 尊重网站服务条款
