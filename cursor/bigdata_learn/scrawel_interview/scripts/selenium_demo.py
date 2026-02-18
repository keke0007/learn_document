"""
Selenium 示例
演示浏览器自动化的使用
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# 1. 基础使用
def basic_selenium():
    driver = webdriver.Chrome()
    try:
        driver.get('https://www.example.com')
        print(f"Page title: {driver.title}")
    finally:
        driver.quit()

# 2. 配置 Chrome 选项
def create_driver():
    options = Options()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    
    driver = webdriver.Chrome(options=options)
    return driver

# 3. 元素定位
def element_location():
    driver = webdriver.Chrome()
    try:
        driver.get('https://www.example.com')
        
        # ID 定位
        element = driver.find_element(By.ID, "element-id")
        
        # 类名定位
        elements = driver.find_elements(By.CLASS_NAME, "class-name")
        
        # CSS 选择器
        element = driver.find_element(By.CSS_SELECTOR, "div.content")
        
        # XPath
        element = driver.find_element(By.XPATH, "//div[@class='content']")
    finally:
        driver.quit()

# 4. 等待元素
def wait_for_element():
    driver = webdriver.Chrome()
    try:
        driver.get('https://www.example.com')
        
        # 显式等待
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "element-id"))
        )
        
        # 等待元素可点击
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button-id"))
        )
        element.click()
    finally:
        driver.quit()

# 5. 执行 JavaScript
def execute_javascript():
    driver = webdriver.Chrome()
    try:
        driver.get('https://www.example.com')
        
        # 滚动到底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # 获取页面高度
        height = driver.execute_script("return document.body.scrollHeight")
        print(f"Page height: {height}")
        
        # 修改元素属性
        driver.execute_script("arguments[0].style.display = 'none';", element)
    finally:
        driver.quit()

# 6. 表单操作
def form_operation():
    driver = webdriver.Chrome()
    try:
        driver.get('https://www.example.com/login')
        
        # 输入文本
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys("user")
        
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("pass")
        
        # 提交表单
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()
        
        # 或者按回车
        password_input.send_keys(Keys.RETURN)
    finally:
        driver.quit()

# 7. 获取页面信息
def get_page_info():
    driver = webdriver.Chrome()
    try:
        driver.get('https://www.example.com')
        
        # 获取页面标题
        title = driver.title
        print(f"Title: {title}")
        
        # 获取当前 URL
        url = driver.current_url
        print(f"URL: {url}")
        
        # 获取页面源码
        html = driver.page_source
        
        # 获取 Cookie
        cookies = driver.get_cookies()
        print(f"Cookies: {cookies}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=== 基础使用 ===")
    # basic_selenium()
    
    print("=== 元素定位 ===")
    # element_location()
    
    print("=== 等待元素 ===")
    # wait_for_element()
    
    print("=== 执行 JavaScript ===")
    # execute_javascript()
    
    print("=== 表单操作 ===")
    # form_operation()
    
    print("=== 获取页面信息 ===")
    # get_page_info()
