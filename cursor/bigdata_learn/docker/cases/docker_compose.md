# 案例3：Docker Compose 应用

## 案例描述
学习使用 Docker Compose 编排多容器应用，包括 Web 应用、数据库、缓存等。

## Compose 文件示例

### 1. 简单 Web 应用 (docker-compose.simple.yml)
```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    restart: unless-stopped
```

### 2. Web + 数据库 (docker-compose.web-db.yml)
```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: userpass
    volumes:
      - db-data:/var/lib/mysql
    networks:
      - app-network
    restart: unless-stopped

volumes:
  db-data:

networks:
  app-network:
    driver: bridge
```

### 3. 完整应用栈 (docker-compose.full.yml)
```yaml
version: '3.8'

services:
  # Web 前端
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:5000
    depends_on:
      - backend
    networks:
      - app-network

  # 后端 API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=mysql://user:pass@db:3306/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    networks:
      - app-network

  # 数据库
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: userpass
    volumes:
      - db-data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    restart: unless-stopped

  # Redis 缓存
  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - app-network
    restart: unless-stopped

  # Nginx 反向代理
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
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

### 4. 开发环境配置 (docker-compose.dev.yml)
```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres-data:
```

## 操作脚本

### Compose 操作脚本 (compose_operations.sh)
```bash
#!/bin/bash

echo "=== Docker Compose 操作示例 ==="

# ============================================
# 1. 启动服务
# ============================================

echo -e "\n1. 启动服务"
docker-compose -f docker-compose.web-db.yml up -d

# ============================================
# 2. 查看服务状态
# ============================================

echo -e "\n2. 查看服务状态"
docker-compose -f docker-compose.web-db.yml ps

# ============================================
# 3. 查看服务日志
# ============================================

echo -e "\n3. 查看服务日志"
docker-compose -f docker-compose.web-db.yml logs --tail=10

# ============================================
# 4. 查看特定服务日志
# ============================================

echo -e "\n4. 查看 Web 服务日志"
docker-compose -f docker-compose.web-db.yml logs web

# ============================================
# 5. 扩展服务
# ============================================

echo -e "\n5. 扩展 Web 服务到 3 个实例"
docker-compose -f docker-compose.web-db.yml up -d --scale web=3

# ============================================
# 6. 重启服务
# ============================================

echo -e "\n6. 重启 Web 服务"
docker-compose -f docker-compose.web-db.yml restart web

# ============================================
# 7. 停止服务
# ============================================

echo -e "\n7. 停止服务"
docker-compose -f docker-compose.web-db.yml stop

# ============================================
# 8. 启动服务
# ============================================

echo -e "\n8. 启动服务"
docker-compose -f docker-compose.web-db.yml start

# ============================================
# 9. 删除服务
# ============================================

echo -e "\n9. 删除服务（保留数据卷）"
docker-compose -f docker-compose.web-db.yml down

# ============================================
# 10. 删除服务和数据卷
# ============================================

echo -e "\n10. 删除服务和数据卷"
docker-compose -f docker-compose.web-db.yml down -v
```

## 配置文件示例

### Nginx 配置 (nginx.conf)
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:5000;
    }

    upstream frontend {
        server frontend:3000;
    }

    server {
        listen 80;

        location /api {
            proxy_pass http://backend;
        }

        location / {
            proxy_pass http://frontend;
        }
    }
}
```

### 数据库初始化脚本 (init.sql)
```sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES
('张三', 'zhangsan@example.com'),
('李四', 'lisi@example.com');
```

## 运行方式

```bash
# 创建必要的目录
mkdir -p html frontend backend

# 添加执行权限
chmod +x compose_operations.sh

# 启动服务
docker-compose -f docker-compose.web-db.yml up -d

# 查看服务状态
docker-compose -f docker-compose.web-db.yml ps

# 停止服务
docker-compose -f docker-compose.web-db.yml down
```

## 预期结果

### 服务状态
```
NAME                COMMAND                  STATUS
web_web_1           "nginx -g 'daemon off'"  Up 2 seconds
web_db_1            "docker-entrypoint.sh"   Up 2 seconds
```

### 服务日志
```
web_1  | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty
db_1   | 2024-01-15 10:00:00 [Note] mysqld: ready for connections
```

## 学习要点

1. **Compose 文件结构**：services、volumes、networks
2. **服务依赖**：depends_on、networks
3. **数据持久化**：volumes、命名卷
4. **环境变量**：environment、env_file
5. **服务扩展**：scale、负载均衡
6. **多环境配置**：dev、prod 环境分离
