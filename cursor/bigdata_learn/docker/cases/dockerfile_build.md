# 案例2：Dockerfile 构建

## 案例描述
学习使用 Dockerfile 构建自定义镜像，包括基础镜像、应用部署等。

## Dockerfile 示例

### 1. 简单 Web 应用 (Dockerfile.web)
```dockerfile
# 使用官方 Nginx 作为基础镜像
FROM nginx:latest

# 设置维护者信息
LABEL maintainer="your-email@example.com"

# 复制自定义 HTML 文件
COPY html/index.html /usr/share/nginx/html/

# 暴露端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
```

### 2. Python 应用 (Dockerfile.python)
```dockerfile
# 使用 Python 官方镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app.py .

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 启动应用
CMD ["python", "app.py"]
```

### 3. Node.js 应用 (Dockerfile.node)
```dockerfile
# 使用 Node.js 官方镜像
FROM node:16-alpine

# 设置工作目录
WORKDIR /app

# 复制 package.json
COPY package*.json ./

# 安装依赖
RUN npm install --production

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 3000

# 启动应用
CMD ["node", "server.js"]
```

### 4. 多阶段构建 (Dockerfile.multistage)
```dockerfile
# 第一阶段：构建阶段
FROM node:16 AS builder

WORKDIR /app

# 复制依赖文件
COPY package*.json ./
RUN npm install

# 复制源代码并构建
COPY . .
RUN npm run build

# 第二阶段：运行阶段
FROM nginx:alpine

# 从构建阶段复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 5. 完整应用示例 (Dockerfile.complete)
```dockerfile
# 基础镜像
FROM ubuntu:20.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV APP_HOME=/app

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR $APP_HOME

# 复制应用文件
COPY app/ $APP_HOME/

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser $APP_HOME

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/health || exit 1

# 启动命令
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
```

## 构建脚本

### 构建脚本 (build.sh)
```bash
#!/bin/bash

echo "=== Docker 镜像构建示例 ==="

# ============================================
# 1. 构建简单 Web 应用
# ============================================

echo -e "\n1. 构建 Web 应用镜像"
docker build -f Dockerfile.web -t myweb:latest .

# ============================================
# 2. 构建 Python 应用
# ============================================

echo -e "\n2. 构建 Python 应用镜像"
docker build -f Dockerfile.python -t mypython:latest .

# ============================================
# 3. 构建 Node.js 应用
# ============================================

echo -e "\n3. 构建 Node.js 应用镜像"
docker build -f Dockerfile.node -t mynode:latest .

# ============================================
# 4. 多阶段构建
# ============================================

echo -e "\n4. 多阶段构建"
docker build -f Dockerfile.multistage -t myapp:prod .

# ============================================
# 5. 查看构建的镜像
# ============================================

echo -e "\n5. 查看构建的镜像"
docker images | grep -E "myweb|mypython|mynode|myapp"

# ============================================
# 6. 运行构建的镜像
# ============================================

echo -e "\n6. 运行 Web 应用"
docker run -d -p 8080:80 --name myweb myweb:latest

# ============================================
# 7. 测试应用
# ============================================

echo -e "\n7. 测试应用"
sleep 2
curl http://localhost:8080

# ============================================
# 8. 清理
# ============================================

echo -e "\n8. 清理"
docker stop myweb
docker rm myweb
```

## 应用代码示例

### Python 应用 (app.py)
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Docker!'

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Node.js 应用 (server.js)
```javascript
const http = require('http');

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Hello from Docker!\n');
});

server.listen(3000, '0.0.0.0', () => {
    console.log('Server running on port 3000');
});
```

### HTML 文件 (html/index.html)
```html
<!DOCTYPE html>
<html>
<head>
    <title>Docker Web App</title>
</head>
<body>
    <h1>Hello from Docker!</h1>
    <p>This is a simple web application running in a Docker container.</p>
</body>
</html>
```

## 运行方式

```bash
# 创建必要的目录和文件
mkdir -p html app

# 添加执行权限
chmod +x build.sh

# 运行构建脚本
./build.sh
```

## 预期结果

### 构建输出
```
Step 1/5 : FROM nginx:latest
 ---> xxx
Step 2/5 : COPY html/index.html /usr/share/nginx/html/
 ---> xxx
...
Successfully built xxx
Successfully tagged myweb:latest
```

### 运行测试
```
Hello from Docker!
```

## 学习要点

1. **Dockerfile 指令**：FROM、RUN、COPY、WORKDIR、EXPOSE、CMD
2. **多阶段构建**：减少镜像大小
3. **最佳实践**：使用非 root 用户、健康检查
4. **构建优化**：缓存利用、层合并
5. **应用部署**：不同语言应用的容器化
