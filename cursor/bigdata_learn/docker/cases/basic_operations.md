# 案例1：Docker 基础操作

## 案例描述
学习 Docker 的基本操作，包括镜像管理、容器操作等。

## 操作示例

### 1. 镜像操作 (image_operations.sh)
```bash
#!/bin/bash

echo "=== Docker 镜像操作示例 ==="

# ============================================
# 1. 搜索镜像
# ============================================

echo -e "\n1. 搜索 nginx 镜像"
docker search nginx | head -n 5

# ============================================
# 2. 拉取镜像
# ============================================

echo -e "\n2. 拉取 nginx 镜像"
docker pull nginx:latest

# ============================================
# 3. 查看本地镜像
# ============================================

echo -e "\n3. 查看本地镜像"
docker images

# ============================================
# 4. 查看镜像详情
# ============================================

echo -e "\n4. 查看 nginx 镜像详情"
docker inspect nginx:latest | head -n 20

# ============================================
# 5. 给镜像打标签
# ============================================

echo -e "\n5. 给镜像打标签"
docker tag nginx:latest mynginx:v1.0
docker images | grep nginx

# ============================================
# 6. 导出和导入镜像
# ============================================

echo -e "\n6. 导出镜像"
docker save -o nginx.tar nginx:latest
ls -lh nginx.tar

echo -e "\n7. 导入镜像"
docker load -i nginx.tar

# ============================================
# 8. 删除镜像
# ============================================

echo -e "\n8. 删除镜像"
docker rmi mynginx:v1.0
```

### 2. 容器操作 (container_operations.sh)
```bash
#!/bin/bash

echo "=== Docker 容器操作示例 ==="

# ============================================
# 1. 创建并启动容器
# ============================================

echo -e "\n1. 创建并启动 nginx 容器"
docker run -d --name mynginx -p 8080:80 nginx:latest

# ============================================
# 2. 查看运行中的容器
# ============================================

echo -e "\n2. 查看运行中的容器"
docker ps

# ============================================
# 3. 查看所有容器
# ============================================

echo -e "\n3. 查看所有容器"
docker ps -a

# ============================================
# 4. 查看容器日志
# ============================================

echo -e "\n4. 查看容器日志"
docker logs mynginx | head -n 5

# ============================================
# 5. 进入容器
# ============================================

echo -e "\n5. 进入容器（交互式）"
echo "执行: docker exec -it mynginx /bin/bash"

# ============================================
# 6. 查看容器资源使用
# ============================================

echo -e "\n6. 查看容器资源使用"
docker stats mynginx --no-stream

# ============================================
# 7. 停止容器
# ============================================

echo -e "\n7. 停止容器"
docker stop mynginx

# ============================================
# 8. 启动容器
# ============================================

echo -e "\n8. 启动容器"
docker start mynginx

# ============================================
# 9. 重启容器
# ============================================

echo -e "\n9. 重启容器"
docker restart mynginx

# ============================================
# 10. 删除容器
# ============================================

echo -e "\n10. 删除容器"
docker stop mynginx
docker rm mynginx
```

### 3. 数据卷操作 (volume_operations.sh)
```bash
#!/bin/bash

echo "=== Docker 数据卷操作示例 ==="

# ============================================
# 1. 创建数据卷
# ============================================

echo -e "\n1. 创建数据卷"
docker volume create mydata

# ============================================
# 2. 查看数据卷
# ============================================

echo -e "\n2. 查看数据卷列表"
docker volume ls

# ============================================
# 3. 查看数据卷详情
# ============================================

echo -e "\n3. 查看数据卷详情"
docker volume inspect mydata

# ============================================
# 4. 使用数据卷运行容器
# ============================================

echo -e "\n4. 使用数据卷运行容器"
docker run -d --name mynginx \
  -v mydata:/usr/share/nginx/html \
  nginx:latest

# ============================================
# 5. 绑定挂载
# ============================================

echo -e "\n5. 绑定挂载示例"
mkdir -p ./html
echo "<h1>Hello Docker</h1>" > ./html/index.html

docker run -d --name mynginx2 \
  -v $(pwd)/html:/usr/share/nginx/html \
  -p 8081:80 \
  nginx:latest

# ============================================
# 6. 清理
# ============================================

echo -e "\n6. 清理容器和数据卷"
docker stop mynginx mynginx2
docker rm mynginx mynginx2
docker volume rm mydata
```

### 4. 网络操作 (network_operations.sh)
```bash
#!/bin/bash

echo "=== Docker 网络操作示例 ==="

# ============================================
# 1. 查看网络
# ============================================

echo -e "\n1. 查看网络列表"
docker network ls

# ============================================
# 2. 创建网络
# ============================================

echo -e "\n2. 创建自定义网络"
docker network create mynetwork

# ============================================
# 3. 查看网络详情
# ============================================

echo -e "\n3. 查看网络详情"
docker network inspect mynetwork

# ============================================
# 4. 在指定网络中运行容器
# ============================================

echo -e "\n4. 在指定网络中运行容器"
docker run -d --name web1 --network mynetwork nginx:latest
docker run -d --name web2 --network mynetwork nginx:latest

# ============================================
# 5. 容器间通信
# ============================================

echo -e "\n5. 测试容器间通信"
docker exec web1 ping -c 2 web2

# ============================================
# 6. 连接容器到网络
# ============================================

echo -e "\n6. 连接现有容器到网络"
docker network connect mynetwork web1

# ============================================
# 7. 断开网络连接
# ============================================

echo -e "\n7. 断开网络连接"
docker network disconnect mynetwork web1

# ============================================
# 8. 清理
# ============================================

echo -e "\n8. 清理"
docker stop web1 web2
docker rm web1 web2
docker network rm mynetwork
```

## 运行方式

```bash
# 添加执行权限
chmod +x image_operations.sh container_operations.sh volume_operations.sh network_operations.sh

# 运行脚本
./image_operations.sh
./container_operations.sh
./volume_operations.sh
./network_operations.sh
```

## 预期结果

### 镜像操作输出
```
REPOSITORY    TAG       IMAGE ID       CREATED       SIZE
nginx         latest    xxx            xxx            xxx
mynginx       v1.0      xxx            xxx            xxx
```

### 容器操作输出
```
CONTAINER ID   IMAGE          COMMAND                  STATUS
xxx            nginx:latest   "nginx -g 'daemon off'"  Up 2 seconds
```

## 学习要点

1. **镜像管理**：搜索、拉取、查看、删除
2. **容器管理**：创建、启动、停止、删除
3. **数据卷**：创建、使用、绑定挂载
4. **网络管理**：创建网络、容器通信
5. **常用命令**：docker ps、docker logs、docker exec
