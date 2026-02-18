"""
requests 库示例
演示 HTTP 请求的各种用法
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 1. 基础 GET 请求
def basic_get():
    response = requests.get('https://www.example.com')
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Content: {response.text[:100]}")

# 2. 带参数的 GET 请求
def get_with_params():
    params = {
        'page': 1,
        'size': 10,
        'keyword': 'python'
    }
    response = requests.get('https://www.example.com/search', params=params)
    print(f"URL: {response.url}")

# 3. POST 请求
def post_request():
    data = {
        'username': 'user',
        'password': 'pass'
    }
    response = requests.post('https://www.example.com/login', data=data)
    print(f"Status Code: {response.status_code}")

# 4. JSON POST 请求
def post_json():
    json_data = {
        'name': 'test',
        'age': 25
    }
    response = requests.post('https://www.example.com/api', json=json_data)
    print(response.json())

# 5. 设置请求头
def request_with_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Referer': 'https://www.example.com'
    }
    response = requests.get('https://www.example.com', headers=headers)
    print(f"Status Code: {response.status_code}")

# 6. 使用 Session
def session_example():
    session = requests.Session()
    
    # 设置通用请求头
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    })
    
    # 登录
    login_data = {
        'username': 'user',
        'password': 'pass'
    }
    response = session.post('https://www.example.com/login', data=login_data)
    
    # 使用 Session 访问需要登录的页面
    response = session.get('https://www.example.com/profile')
    print(response.text)

# 7. Cookie 处理
def cookie_example():
    session = requests.Session()
    
    # 设置 Cookie
    session.cookies.set('session_id', 'abc123')
    session.cookies.set('user_id', '456')
    
    # 获取 Cookie
    response = session.get('https://www.example.com')
    print(session.cookies.get_dict())

# 8. 文件下载
def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {save_path}")

# 9. 重试机制
def create_session_with_retry():
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

# 10. 超时设置
def request_with_timeout():
    try:
        response = requests.get('https://www.example.com', timeout=(5, 10))
        print(response.status_code)
    except requests.exceptions.Timeout:
        print("Request timeout")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    print("=== 基础 GET 请求 ===")
    # basic_get()
    
    print("=== 带参数的 GET 请求 ===")
    # get_with_params()
    
    print("=== POST 请求 ===")
    # post_request()
    
    print("=== JSON POST 请求 ===")
    # post_json()
    
    print("=== 设置请求头 ===")
    # request_with_headers()
    
    print("=== 使用 Session ===")
    # session_example()
    
    print("=== Cookie 处理 ===")
    # cookie_example()
    
    print("=== 文件下载 ===")
    # download_file('https://example.com/image.jpg', 'image.jpg')
    
    print("=== 重试机制 ===")
    session = create_session_with_retry()
    # response = session.get('https://www.example.com')
    
    print("=== 超时设置 ===")
    # request_with_timeout()
