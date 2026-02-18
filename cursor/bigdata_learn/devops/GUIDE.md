# Java 服务 Linux 环境 DevOps 开发部署学习指南

## 📚 项目概述

本指南提供了完整的基于 Java 服务在 Linux 环境下的 DevOps 开发部署学习资源，包括 CI/CD、容器化、监控、自动化运维等核心知识点、实战案例和验证数据。

---

## 📁 项目结构

```
devops/
├── GUIDE.md                     # 本指南文档（快速入门）
├── README.md                    # DevOps 知识点总览（详细文档）
├── cases/                       # 实战案例目录
│   ├── linux_basics.md         # 案例1：Linux 基础
│   ├── java_deployment.md      # 案例2：Java 服务部署
│   ├── docker_kubernetes.md    # 案例3：Docker 和 Kubernetes
│   ├── cicd_pipeline.md         # 案例4：CI/CD 流水线
│   ├── monitoring_logging.md    # 案例5：监控和日志
│   └── automation.md            # 案例6：自动化运维
├── data/                        # 验证数据目录
│   ├── deployment_config.json   # 部署配置
│   ├── performance_metrics.json # 性能指标
│   └── deployment_log.txt       # 部署日志
└── scripts/                     # 脚本目录
    ├── deploy.sh               # 部署脚本
    ├── docker-compose.yml      # Docker Compose 配置
    ├── jenkinsfile.groovy      # Jenkins 流水线
    └── monitoring.sh           # 监控脚本
```

---

## 🎯 学习路径

### 阶段一：Linux 基础（5-7天）
1. **Linux 系统管理**
   - 文件系统操作
   - 用户和权限管理
   - 进程和服务管理
   - 网络配置

2. **Shell 脚本**
   - Bash 基础
   - 脚本编写
   - 自动化任务

### 阶段二：Java 服务部署（7-10天）
1. **Java 环境配置**
   - JDK 安装和配置
   - JVM 参数调优
   - 环境变量设置

2. **服务部署**
   - Spring Boot 应用部署
   - Tomcat/Jetty 部署
   - 服务启动和停止
   - 健康检查

### 阶段三：容器化部署（7-10天）
1. **Docker**
   - Dockerfile 编写
   - 镜像构建和推送
   - Docker Compose
   - 容器编排

2. **Kubernetes**
   - K8s 基础概念
   - Pod、Service、Deployment
   - ConfigMap 和 Secret
   - 服务发现和负载均衡

### 阶段四：CI/CD 流水线（7-10天）
1. **CI/CD 工具**
   - Jenkins
   - GitLab CI/CD
   - GitHub Actions
   - 流水线设计

2. **自动化部署**
   - 代码构建
   - 自动化测试
   - 自动部署
   - 回滚策略

### 阶段五：监控和日志（5-7天）
1. **监控系统**
   - Prometheus
   - Grafana
   - 指标收集
   - 告警配置

2. **日志管理**
   - ELK Stack
   - 日志收集
   - 日志分析
   - 日志聚合

### 阶段六：自动化运维（5-7天）
1. **配置管理**
   - Ansible
   - 自动化配置
   - 批量操作

2. **基础设施即代码**
   - Terraform
   - 资源管理
   - 环境一致性

---

## 📖 核心知识点详解

### 1. Linux 基础

#### 知识点概述
Linux 是 DevOps 的基础平台，掌握 Linux 系统管理是必备技能。

#### 常用命令

**文件操作**
```bash
# 文件查看
cat file.txt
less file.txt
tail -f log.txt

# 文件操作
cp source dest
mv old new
rm -rf directory
chmod 755 file.sh
chown user:group file
```

**进程管理**
```bash
# 进程查看
ps aux
ps -ef
top
htop

# 进程管理
kill -9 PID
killall process_name
nohup command &

# 服务管理（systemd）
systemctl start service
systemctl stop service
systemctl restart service
systemctl status service
systemctl enable service
```

**网络管理**
```bash
# 网络配置
ifconfig
ip addr
netstat -tulpn
ss -tulpn

# 防火墙
firewall-cmd --list-all
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --reload
```

#### 案例代码

```bash
# deploy.sh
#!/bin/bash

# 变量定义
APP_NAME="myapp"
APP_HOME="/opt/apps/${APP_NAME}"
JAR_FILE="${APP_NAME}.jar"
PID_FILE="/var/run/${APP_NAME}.pid"

# 函数：启动服务
start_service() {
    if [ -f "$PID_FILE" ]; then
        echo "Service is already running"
        return 1
    fi
    
    echo "Starting ${APP_NAME}..."
    nohup java -jar ${APP_HOME}/${JAR_FILE} > ${APP_HOME}/logs/app.log 2>&1 &
    echo $! > $PID_FILE
    echo "Service started with PID $(cat $PID_FILE)"
}

# 函数：停止服务
stop_service() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Service is not running"
        return 1
    fi
    
    PID=$(cat $PID_FILE)
    echo "Stopping ${APP_NAME} (PID: $PID)..."
    kill $PID
    
    # 等待进程结束
    for i in {1..10}; do
        if ! ps -p $PID > /dev/null; then
            rm -f $PID_FILE
            echo "Service stopped"
            return 0
        fi
        sleep 1
    done
    
    # 强制杀死
    kill -9 $PID
    rm -f $PID_FILE
    echo "Service force stopped"
}

# 函数：重启服务
restart_service() {
    stop_service
    sleep 2
    start_service
}

# 主逻辑
case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat $PID_FILE)
            if ps -p $PID > /dev/null; then
                echo "Service is running (PID: $PID)"
            else
                echo "Service is not running (stale PID file)"
            fi
        else
            echo "Service is not running"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
```

---

### 2. Java 服务部署

#### 知识点概述
Java 服务部署需要考虑 JVM 参数、环境配置、健康检查等。

#### JVM 参数调优

```bash
# JVM 参数示例
java -Xms2g \
     -Xmx4g \
     -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=200 \
     -XX:+HeapDumpOnOutOfMemoryError \
     -XX:HeapDumpPath=/opt/logs/heapdump.hprof \
     -Dspring.profiles.active=prod \
     -jar app.jar
```

#### Spring Boot 部署

```bash
# 生产环境启动脚本
#!/bin/bash

JAVA_OPTS="-Xms2g -Xmx4g -XX:+UseG1GC"
SPRING_OPTS="--spring.profiles.active=prod"
APP_JAR="app.jar"

java $JAVA_OPTS -jar $APP_JAR $SPRING_OPTS
```

#### 验证数据

**性能测试结果：**
```
默认 JVM 参数：GC 时间 500ms，吞吐量 80%
优化后 JVM 参数：GC 时间 200ms，吞吐量 95%
```

---

### 3. Docker 和 Kubernetes

#### 知识点概述
容器化部署是现代 DevOps 的标准实践。

#### Dockerfile 示例

```dockerfile
# Dockerfile
FROM openjdk:11-jre-slim

WORKDIR /app

# 复制应用文件
COPY target/app.jar app.jar

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# 启动命令
ENTRYPOINT ["java", "-jar", "app.jar"]
```

#### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - DB_HOST=db
    depends_on:
      - db
    restart: unless-stopped
  
  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpass
      - MYSQL_DATABASE=appdb
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

#### Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: java-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: java-app
  template:
    metadata:
      labels:
        app: java-app
    spec:
      containers:
      - name: app
        image: myregistry/java-app:latest
        ports:
        - containerPort: 8080
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "prod"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /actuator/health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /actuator/health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: java-app-service
spec:
  selector:
    app: java-app
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

---

### 4. CI/CD 流水线

#### 知识点概述
CI/CD 实现自动化构建、测试和部署。

#### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        IMAGE_NAME = 'java-app'
        KUBERNETES_NAMESPACE = 'production'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }
        
        stage('Test') {
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    sh "docker build -t ${imageTag} ."
                    sh "docker push ${imageTag}"
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                        kubectl set image deployment/java-app \
                        app=${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} \
                        -n ${KUBERNETES_NAMESPACE}
                        kubectl rollout status deployment/java-app -n ${KUBERNETES_NAMESPACE}
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
            // 回滚逻辑
        }
    }
}
```

---

### 5. 监控和日志

#### 知识点概述
监控和日志是保障服务稳定运行的关键。

#### Prometheus 配置

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'java-app'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['app:8080']
```

#### 日志收集脚本

```bash
# log_collector.sh
#!/bin/bash

LOG_DIR="/opt/logs"
ARCHIVE_DIR="/opt/logs/archive"
DATE=$(date +%Y%m%d)

# 归档日志
find $LOG_DIR -name "*.log" -mtime +7 -exec gzip {} \;
find $LOG_DIR -name "*.log.gz" -exec mv {} $ARCHIVE_DIR/ \;

# 清理旧日志（保留30天）
find $ARCHIVE_DIR -name "*.log.gz" -mtime +30 -delete
```

---

## 📊 面试重点总结

### 高频面试题

1. **Linux 系统管理**
   - 进程管理
   - 服务管理
   - 网络配置
   - 权限管理

2. **Java 部署**
   - JVM 参数调优
   - 服务启动脚本
   - 健康检查
   - 性能优化

3. **容器化**
   - Dockerfile 编写
   - Docker Compose
   - Kubernetes 部署
   - 服务编排

4. **CI/CD**
   - 流水线设计
   - 自动化部署
   - 回滚策略
   - 环境管理

5. **监控和日志**
   - 监控指标
   - 告警配置
   - 日志收集
   - 性能分析

### 学习建议

1. **理论与实践结合**
   - 理解概念后，通过实际操作验证
   - 搭建实验环境练习

2. **循序渐进**
   - 先掌握基础，再深入高级特性
   - 每个知识点都要有实际操作

3. **持续练习**
   - 定期回顾知识点
   - 参与实际项目实践
   - 关注 DevOps 最佳实践

4. **面试准备**
   - 准备项目经验描述
   - 准备技术难点和解决方案
   - 准备故障处理案例

---

## 🔧 工具推荐

### 开发工具
- **IDE**：IntelliJ IDEA、VS Code
- **版本控制**：Git
- **构建工具**：Maven、Gradle

### DevOps 工具
- **CI/CD**：Jenkins、GitLab CI、GitHub Actions
- **容器化**：Docker、Kubernetes
- **监控**：Prometheus、Grafana
- **日志**：ELK Stack、Loki
- **配置管理**：Ansible、Terraform

---

## 📚 参考资源

### 官方文档
1. **Docker 官方文档**：https://docs.docker.com/
2. **Kubernetes 官方文档**：https://kubernetes.io/docs/
3. **Jenkins 官方文档**：https://www.jenkins.io/doc/

### 在线资源
1. **DevOps 最佳实践**：https://www.devops.com/
2. **Kubernetes 教程**：https://kubernetes.io/docs/tutorials/

---

## ✅ 学习检查清单

- [ ] 掌握 Linux 系统管理
- [ ] 熟悉 Java 服务部署
- [ ] 理解 Docker 和 Kubernetes
- [ ] 能够设计 CI/CD 流水线
- [ ] 熟悉监控和日志系统
- [ ] 掌握自动化运维工具
- [ ] 具备故障处理能力
- [ ] 了解性能优化方法

---

**最后更新：2026-01-26**
