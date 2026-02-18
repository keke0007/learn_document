# 案例4：实际项目部署

## 案例描述
学习使用 Docker 部署实际项目，包括应用构建、数据库配置、反向代理等。

## 项目结构

```
project/
├── docker-compose.yml
├── Dockerfile
├── nginx/
│   └── nginx.conf
├── app/
│   ├── app.py
│   └── requirements.txt
└── init/
    └── init.sql
```

## 完整部署示例

### 1. Docker Compose 配置 (docker-compose.yml)
```yaml
version: '3.8'

services:
  # 应用服务
  app:
    build:
      context: ./app
      dockerfile: Dockerfile
    container_name: myapp
    environment:
      - DATABASE_URL=mysql://user:pass@db:3306/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    networks:
      - app-network
    restart: unless-stopped

  # 数据库服务
  db:
    image: mysql:5.7
    container_name: mydb
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: userpass
    volumes:
      - db-data:/var/lib/mysql
      - ./init/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    networks:
      - app-network
    restart: unless-stopped

  # Redis 服务
  redis:
    image: redis:6-alpine
    container_name: myredis
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    networks:
      - app-network
    restart: unless-stopped

  # Nginx 反向代理
  nginx:
    image: nginx:alpine
    container_name: mynginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - app
    networks:
      - app-network
    restart: unless-stopped

volumes:
  db-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

### 2. 应用 Dockerfile (app/Dockerfile)
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# 启动应用
CMD ["python", "app.py"]
```

### 3. Python 应用 (app/app.py)
```python
from flask import Flask, jsonify
import mysql.connector
import redis
import os

app = Flask(__name__)

# 数据库配置
db_config = {
    'host': os.getenv('DATABASE_URL', 'localhost').split('@')[1].split(':')[0] if '@' in os.getenv('DATABASE_URL', '') else 'db',
    'user': 'user',
    'password': 'pass',
    'database': 'mydb'
}

# Redis 配置
redis_client = redis.Redis(
    host=os.getenv('REDIS_URL', 'redis://redis:6379').split('://')[1].split(':')[0] if '://' in os.getenv('REDIS_URL', '') else 'redis',
    port=6379,
    decode_responses=True
)

@app.route('/')
def index():
    return jsonify({
        'message': 'Hello from Docker!',
        'status': 'running'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/users')
def get_users():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'users': users})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cache/<key>')
def get_cache(key):
    value = redis_client.get(key)
    if value:
        return jsonify({'key': key, 'value': value})
    return jsonify({'key': key, 'value': None}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### 4. 依赖文件 (app/requirements.txt)
```
Flask==2.3.0
mysql-connector-python==8.1.0
redis==4.6.0
requests==2.31.0
```

### 5. Nginx 配置 (nginx/nginx.conf)
```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:5000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /health {
            proxy_pass http://app/health;
        }
    }
}
```

### 6. 数据库初始化 (init/init.sql)
```sql
-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入测试数据
INSERT INTO users (name, email) VALUES
('张三', 'zhangsan@example.com'),
('李四', 'lisi@example.com'),
('王五', 'wangwu@example.com');
```

### 7. 部署脚本 (deploy.sh)
```bash
#!/bin/bash

echo "=== Docker 项目部署 ==="

# ============================================
# 1. 构建并启动服务
# ============================================

echo -e "\n1. 构建并启动服务"
docker-compose up -d --build

# ============================================
# 2. 等待服务启动
# ============================================

echo -e "\n2. 等待服务启动..."
sleep 10

# ============================================
# 3. 检查服务状态
# ============================================

echo -e "\n3. 检查服务状态"
docker-compose ps

# ============================================
# 4. 查看服务日志
# ============================================

echo -e "\n4. 查看应用日志"
docker-compose logs app --tail=20

# ============================================
# 5. 测试应用
# ============================================

echo -e "\n5. 测试应用"
curl http://localhost/
curl http://localhost/health
curl http://localhost/users

# ============================================
# 6. 查看资源使用
# ============================================

echo -e "\n6. 查看资源使用"
docker stats --no-stream
```

### 8. 清理脚本 (cleanup.sh)
```bash
#!/bin/bash

echo "=== 清理 Docker 资源 ==="

# ============================================
# 1. 停止并删除容器
# ============================================

echo -e "\n1. 停止并删除容器"
docker-compose down

# ============================================
# 2. 删除数据卷（可选）
# ============================================

read -p "是否删除数据卷? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose down -v
    echo "数据卷已删除"
fi

# ============================================
# 3. 清理未使用的资源
# ============================================

echo -e "\n2. 清理未使用的资源"
docker system prune -f
```

## 运行方式

```bash
# 创建项目目录结构
mkdir -p project/{app,nginx,init}

# 添加执行权限
chmod +x deploy.sh cleanup.sh

# 部署项目
./deploy.sh

# 清理项目
./cleanup.sh
```

## 预期结果

### 服务状态
```
NAME      COMMAND                  STATUS
myapp     "python app.py"          Up 2 seconds
mydb      "docker-entrypoint.sh"   Up 2 seconds
myredis   "redis-server"           Up 2 seconds
mynginx   "nginx -g 'daemon off'"  Up 2 seconds
```

### 测试结果
```json
{
  "message": "Hello from Docker!",
  "status": "running"
}
```

## 学习要点

1. **多服务编排**：Web、数据库、缓存、反向代理
2. **服务依赖**：depends_on、网络配置
3. **数据持久化**：数据卷、初始化脚本
4. **环境变量**：配置管理
5. **健康检查**：服务监控
6. **反向代理**：Nginx 配置
7. **部署流程**：构建、启动、测试、清理
