# Docker 学习指南

## 📚 项目概述

本指南提供了完整的 Docker 学习资源，包括基础知识、实战案例和验证数据，帮助你系统掌握 Docker 容器化技术。

---

## 📁 项目结构

```
docker/
├── README.md                    # Docker 知识点总览（详细文档）
├── GUIDE.md                     # 本指南文档（快速入门）
├── cases/                       # 实战案例目录
│   ├── basic_operations.md     # 案例1：基础操作
│   ├── dockerfile_build.md     # 案例2：Dockerfile 构建
│   ├── docker_compose.md       # 案例3：Docker Compose 应用
│   └── project_deployment.md   # 案例4：实际项目部署
├── data/                        # 验证数据目录
│   ├── html/                   # HTML 文件
│   ├── app/                    # 应用代码
│   └── init/                   # 初始化脚本
└── scripts/                     # 脚本和配置文件
    ├── dockerfile.web          # Web 应用 Dockerfile
    ├── dockerfile.python       # Python 应用 Dockerfile
    ├── docker-compose.simple.yml
    └── docker-compose.web-db.yml
```

---

## 🎯 学习路径

### 阶段一：Docker 基础（2-3天）
1. **Docker 基础概念**
   - 了解 Docker 的作用和优势
   - 理解镜像、容器、仓库的概念
   - 掌握 Docker 的基本命令

2. **镜像和容器操作**
   - 镜像搜索、拉取、管理
   - 容器创建、启动、停止
   - 容器交互和日志查看

### 阶段二：Dockerfile（2-3天）
1. **Dockerfile 编写**
   - Dockerfile 指令学习
   - 构建自定义镜像
   - 多阶段构建

2. **镜像优化**
   - 减少镜像大小
   - 构建缓存优化
   - 最佳实践

### 阶段三：Docker Compose（2-3天）
1. **Compose 基础**
   - Compose 文件编写
   - 多容器应用编排
   - 服务依赖和网络

2. **实际应用**
   - Web + 数据库部署
   - 完整应用栈部署
   - 开发/生产环境配置

### 阶段四：高级应用（3-4天）
1. **网络和数据管理**
   - 网络配置
   - 数据卷管理
   - 持久化存储

2. **生产部署**
   - 镜像发布
   - 容器编排
   - 监控和日志

---

## 🚀 快速开始

### 前置要求

- Linux/Windows/macOS 系统
- Docker Engine 20.10+
- Docker Compose 1.29+（可选）

### 步骤1：安装 Docker

#### Linux
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker
```

#### Windows/macOS
- 下载并安装 Docker Desktop
- 启动 Docker Desktop

### 步骤2：验证安装

```bash
# 查看 Docker 版本
docker --version
docker-compose --version

# 运行测试容器
docker run hello-world
```

### 步骤3：运行第一个容器

```bash
# 运行 Nginx 容器
docker run -d -p 8080:80 --name mynginx nginx

# 访问 http://localhost:8080
# 停止并删除容器
docker stop mynginx
docker rm mynginx
```

---

## 📖 核心知识点速查

### 1. 镜像操作

| 操作 | 命令 | 说明 |
|------|------|------|
| **搜索镜像** | `docker search nginx` | 搜索镜像 |
| **拉取镜像** | `docker pull nginx` | 拉取镜像 |
| **查看镜像** | `docker images` | 查看本地镜像 |
| **删除镜像** | `docker rmi nginx` | 删除镜像 |
| **构建镜像** | `docker build -t myapp .` | 构建镜像 |

### 2. 容器操作

| 操作 | 命令 | 说明 |
|------|------|------|
| **运行容器** | `docker run nginx` | 运行容器 |
| **后台运行** | `docker run -d nginx` | 后台运行 |
| **端口映射** | `docker run -p 8080:80 nginx` | 端口映射 |
| **查看容器** | `docker ps` | 查看运行中的容器 |
| **停止容器** | `docker stop container` | 停止容器 |
| **删除容器** | `docker rm container` | 删除容器 |

### 3. Dockerfile 指令

| 指令 | 说明 | 示例 |
|------|------|------|
| **FROM** | 基础镜像 | `FROM ubuntu:20.04` |
| **RUN** | 执行命令 | `RUN apt-get update` |
| **COPY** | 复制文件 | `COPY app.py /app/` |
| **WORKDIR** | 工作目录 | `WORKDIR /app` |
| **EXPOSE** | 暴露端口 | `EXPOSE 80` |
| **CMD** | 启动命令 | `CMD ["python", "app.py"]` |

### 4. Docker Compose

| 操作 | 命令 | 说明 |
|------|------|------|
| **启动服务** | `docker-compose up -d` | 后台启动 |
| **停止服务** | `docker-compose down` | 停止服务 |
| **查看状态** | `docker-compose ps` | 查看状态 |
| **查看日志** | `docker-compose logs` | 查看日志 |
| **构建并启动** | `docker-compose up --build` | 构建并启动 |

---

## 💡 实战案例概览

### 案例1：基础操作
**学习目标**：掌握 Docker 的基本操作

**涉及知识点**：
- 镜像搜索、拉取、管理
- 容器创建、启动、停止
- 数据卷操作
- 网络管理

**典型操作**：
- 镜像拉取和管理
- 容器生命周期管理
- 数据持久化
- 容器网络配置

### 案例2：Dockerfile 构建
**学习目标**：使用 Dockerfile 构建自定义镜像

**涉及知识点**：
- Dockerfile 指令
- 镜像构建
- 多阶段构建
- 最佳实践

**典型操作**：
- 编写 Dockerfile
- 构建 Web 应用镜像
- 构建 Python/Node.js 应用镜像
- 多阶段构建优化

### 案例3：Docker Compose 应用
**学习目标**：使用 Compose 编排多容器应用

**涉及知识点**：
- Compose 文件编写
- 多服务编排
- 服务依赖
- 数据卷和网络

**典型操作**：
- Web + 数据库部署
- 完整应用栈部署
- 开发环境配置
- 服务扩展

### 案例4：实际项目部署
**学习目标**：部署完整的实际项目

**涉及知识点**：
- 项目结构设计
- 多服务协调
- 反向代理配置
- 数据初始化
- 部署流程

**典型操作**：
- 完整项目容器化
- 数据库和缓存配置
- Nginx 反向代理
- 健康检查和监控

---

## 📊 数据说明

### 数据文件结构

| 目录/文件 | 说明 | 用途 |
|----------|------|------|
| html/index.html | HTML 页面 | Web 应用示例 |
| app/app.py | Python 应用 | Flask 应用示例 |
| app/requirements.txt | Python 依赖 | 应用依赖 |
| init/init.sql | SQL 脚本 | 数据库初始化 |

### 配置文件

| 文件 | 说明 | 用途 |
|------|------|------|
| dockerfile.web | Web 应用 Dockerfile | 构建 Web 镜像 |
| dockerfile.python | Python 应用 Dockerfile | 构建 Python 镜像 |
| docker-compose.simple.yml | 简单 Compose 配置 | 单服务示例 |
| docker-compose.web-db.yml | Web+DB Compose 配置 | 多服务示例 |

---

## 🔧 使用技巧

### 1. 镜像优化

```bash
# 使用多阶段构建减少镜像大小
FROM node:16 AS builder
# 构建阶段
FROM nginx:alpine
# 运行阶段，只复制构建产物
```

### 2. 数据持久化

```bash
# 使用命名卷
docker volume create mydata
docker run -v mydata:/data nginx

# 使用绑定挂载（开发环境）
docker run -v $(pwd)/data:/data nginx
```

### 3. 常见问题

**问题1：端口被占用**
```bash
# 查看端口占用
netstat -tuln | grep 8080

# 使用其他端口
docker run -p 8081:80 nginx
```

**问题2：容器无法启动**
```bash
# 查看容器日志
docker logs container_name

# 交互式运行调试
docker run -it nginx /bin/bash
```

**问题3：镜像构建失败**
```bash
# 查看构建过程
docker build --progress=plain -t myapp .

# 使用缓存构建
docker build --no-cache -t myapp .
```

---

## 📝 学习建议

### 初学者
1. 从基础命令开始，逐步学习
2. 多动手实践，运行示例容器
3. 理解镜像和容器的关系
4. 学会查看文档和日志

### 进阶学习
1. 学习 Dockerfile 编写
2. 掌握 Docker Compose 编排
3. 学习镜像优化技巧
4. 理解容器网络和数据管理

### 实践建议
1. **动手实践**：不要只看文档，要实际运行容器
2. **理解原理**：了解 Docker 的工作原理
3. **最佳实践**：学习 Docker 的最佳实践
4. **生产部署**：学习生产环境的部署方法

---

## 🔗 相关资源

### 官方文档
- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [Docker Hub](https://hub.docker.com/)

### 推荐阅读
- `README.md` - 详细的知识点文档
- `cases/` - 四个实战案例的详细说明
- Docker 最佳实践指南

### 扩展学习
- Kubernetes 容器编排
- Docker Swarm 集群管理
- 容器安全
- CI/CD 集成

---

## ✅ 学习检查清单

完成以下任务，确保掌握 Docker 核心技能：

### 基础操作
- [ ] 能够搜索和拉取镜像
- [ ] 能够创建和运行容器
- [ ] 能够管理容器生命周期
- [ ] 能够使用数据卷

### 进阶操作
- [ ] 能够编写 Dockerfile
- [ ] 能够构建自定义镜像
- [ ] 能够使用 Docker Compose
- [ ] 能够配置容器网络

### 实战能力
- [ ] 完成案例1的所有操作
- [ ] 完成案例2的镜像构建
- [ ] 完成案例3的 Compose 应用
- [ ] 完成案例4的项目部署
- [ ] 能够独立容器化应用

---

## 🎓 学习成果

完成本指南的学习后，你将能够：
- ✅ 熟练使用 Docker 进行容器化
- ✅ 掌握镜像和容器的操作
- ✅ 能够编写 Dockerfile 构建镜像
- ✅ 能够使用 Docker Compose 编排应用
- ✅ 理解 Docker 的网络和数据管理
- ✅ 具备部署容器化应用的能力

**祝你学习愉快！** 🚀

---

## 📌 快速参考

### 常用命令

```bash
# 查看 Docker 信息
docker info
docker version

# 查看运行中的容器
docker ps

# 查看所有容器
docker ps -a

# 查看镜像
docker images

# 查看日志
docker logs container_name

# 进入容器
docker exec -it container_name /bin/bash

# 清理资源
docker system prune -a
```

### Docker Compose 命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 扩展服务
docker-compose up -d --scale web=3
```
