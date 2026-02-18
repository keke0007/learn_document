# Docker 学习知识点

## 目录
1. [Docker 基础概念](#1-docker-基础概念)
2. [镜像操作](#2-镜像操作)
3. [容器操作](#3-容器操作)
4. [Dockerfile](#4-dockerfile)
5. [Docker Compose](#5-docker-compose)
6. [网络管理](#6-网络管理)
7. [数据卷](#7-数据卷)
8. [镜像构建和发布](#8-镜像构建和发布)
9. [容器编排](#9-容器编排)
10. [案例与验证数据](#10-案例与验证数据)

---

## 1. Docker 基础概念

### 1.1 什么是 Docker
- Docker 是一个开源的应用容器引擎
- 基于容器技术，实现应用及其依赖的打包
- 轻量级、可移植、自包含的容器
- 一次构建，到处运行

### 1.2 Docker 核心概念
- **镜像（Image）**：只读的模板，用于创建容器
- **容器（Container）**：镜像的运行实例
- **仓库（Repository）**：集中存储镜像的地方
- **Dockerfile**：用于构建镜像的文本文件
- **Docker Compose**：多容器应用编排工具

### 1.3 Docker 架构
- **Docker Daemon**：Docker 守护进程
- **Docker Client**：Docker 客户端
- **Docker Registry**：镜像仓库（Docker Hub）
- **Docker Engine**：Docker 引擎

---

## 2. 镜像操作

### 2.1 镜像搜索和拉取
```bash
# 搜索镜像
docker search nginx

# 拉取镜像
docker pull nginx:latest
docker pull ubuntu:20.04

# 查看本地镜像
docker images
docker image ls
```

### 2.2 镜像管理
```bash
# 查看镜像详情
docker inspect nginx

# 删除镜像
docker rmi nginx
docker image rm nginx

# 清理未使用的镜像
docker image prune

# 导出镜像
docker save -o nginx.tar nginx:latest

# 导入镜像
docker load -i nginx.tar
```

### 2.3 镜像标签
```bash
# 给镜像打标签
docker tag nginx:latest mynginx:v1.0

# 查看镜像历史
docker history nginx
```

---

## 3. 容器操作

### 3.1 容器创建和启动
```bash
# 创建并启动容器
docker run -d --name mynginx nginx

# 交互式运行容器
docker run -it ubuntu:20.04 /bin/bash

# 指定端口映射
docker run -d -p 8080:80 --name mynginx nginx

# 挂载数据卷
docker run -d -v /host/path:/container/path nginx
```

### 3.2 容器管理
```bash
# 查看运行中的容器
docker ps

# 查看所有容器
docker ps -a

# 启动容器
docker start mynginx

# 停止容器
docker stop mynginx

# 重启容器
docker restart mynginx

# 删除容器
docker rm mynginx

# 强制删除运行中的容器
docker rm -f mynginx
```

### 3.3 容器交互
```bash
# 进入运行中的容器
docker exec -it mynginx /bin/bash

# 查看容器日志
docker logs mynginx
docker logs -f mynginx  # 实时查看

# 查看容器进程
docker top mynginx

# 查看容器资源使用
docker stats mynginx
```

---

## 4. Dockerfile

### 4.1 Dockerfile 指令
- **FROM**：指定基础镜像
- **RUN**：执行命令
- **COPY/ADD**：复制文件
- **WORKDIR**：设置工作目录
- **EXPOSE**：声明端口
- **ENV**：设置环境变量
- **CMD**：容器启动命令
- **ENTRYPOINT**：入口点
- **VOLUME**：数据卷
- **USER**：指定用户

### 4.2 Dockerfile 示例
```dockerfile
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y nginx
COPY index.html /var/www/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 4.3 构建镜像
```bash
# 构建镜像
docker build -t myapp:latest .

# 指定 Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .
```

---

## 5. Docker Compose

### 5.1 Compose 文件结构
```yaml
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
```

### 5.2 Compose 命令
```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs

# 构建并启动
docker-compose up --build
```

---

## 6. 网络管理

### 6.1 网络类型
- **bridge**：默认网络（桥接网络）
- **host**：主机网络
- **none**：无网络
- **overlay**：跨主机网络

### 6.2 网络操作
```bash
# 查看网络
docker network ls

# 创建网络
docker network create mynetwork

# 连接容器到网络
docker network connect mynetwork mycontainer

# 断开网络
docker network disconnect mynetwork mycontainer
```

---

## 7. 数据卷

### 7.1 数据卷类型
- **命名卷（Named Volume）**：Docker 管理
- **绑定挂载（Bind Mount）**：主机路径
- **匿名卷（Anonymous Volume）**：临时卷

### 7.2 数据卷操作
```bash
# 创建数据卷
docker volume create myvolume

# 查看数据卷
docker volume ls

# 查看数据卷详情
docker volume inspect myvolume

# 删除数据卷
docker volume rm myvolume

# 使用数据卷
docker run -v myvolume:/data nginx
```

---

## 8. 镜像构建和发布

### 8.1 构建镜像
```bash
# 基本构建
docker build -t myapp:latest .

# 多阶段构建
docker build -t myapp:latest -f Dockerfile.multistage .

# 构建参数
docker build --build-arg VERSION=1.0 -t myapp:1.0 .
```

### 8.2 发布镜像
```bash
# 登录 Docker Hub
docker login

# 推送镜像
docker push username/myapp:latest

# 标记并推送
docker tag myapp:latest username/myapp:latest
docker push username/myapp:latest
```

---

## 9. 容器编排

### 9.1 Docker Swarm
```bash
# 初始化 Swarm
docker swarm init

# 加入 Swarm
docker swarm join --token <token> <manager-ip>

# 创建服务
docker service create --replicas 3 nginx
```

### 9.2 Kubernetes（K8s）
- Pod、Service、Deployment
- ConfigMap、Secret
- Ingress、PersistentVolume

---

## 10. 案例与验证数据

详见以下文件：
- [案例1：基础操作](cases/basic_operations.md)
- [案例2：Dockerfile 构建](cases/dockerfile_build.md)
- [案例3：Docker Compose 应用](cases/docker_compose.md)
- [案例4：实际项目部署](cases/project_deployment.md)
- [验证数据文件](data/)
