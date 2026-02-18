# Kubernetes 学习指南

## 📚 项目概述

本指南提供了完整的 Kubernetes 学习资源，包括基础知识、实战案例和验证数据，帮助你系统掌握 Kubernetes 容器编排技术。

---

## 📁 项目结构

```
kubernetes/
├── README.md                    # Kubernetes 知识点总览（详细文档）
├── GUIDE.md                     # 本指南文档（快速入门）
├── cases/                       # 实战案例目录
│   ├── basic_operations.md    # 案例1：基础操作
│   ├── deployment_service.md    # 案例2：Deployment 和 Service
│   ├── configmap_secret.md     # 案例3：ConfigMap 和 Secret
│   ├── storage_management.md  # 案例4：存储管理
│   └── full_application.md     # 案例5：完整应用部署
└── data/                        # 验证数据目录（YAML 配置文件）
    ├── pod-simple.yaml          # 简单 Pod
    ├── deployment.yaml          # Deployment
    ├── service-clusterip.yaml   # Service
    ├── configmap-literal.yaml   # ConfigMap
    ├── secret-opaque.yaml       # Secret
    ├── pv-hostpath.yaml         # PersistentVolume
    ├── pvc.yaml                 # PersistentVolumeClaim
    ├── namespace.yaml            # Namespace
    └── ...                      # 其他配置文件
```

---

## 🎯 学习路径

### 阶段一：Kubernetes 基础（3-4天）
1. **Kubernetes 基础概念**
   - 了解 Kubernetes 架构和组件
   - 理解 Pod、Node、Cluster 的概念
   - 掌握 kubectl 基本命令

2. **Pod 和容器**
   - Pod 定义和创建
   - 容器配置
   - Pod 生命周期

### 阶段二：工作负载管理（3-4天）
1. **Deployment 和 ReplicaSet**
   - Deployment 创建和管理
   - 副本扩展和收缩
   - 滚动更新和回滚

2. **Service 和 Ingress**
   - Service 类型和配置
   - 服务发现和负载均衡
   - Ingress 路由配置

### 阶段三：配置和存储（2-3天）
1. **ConfigMap 和 Secret**
   - 配置管理
   - 敏感信息管理
   - 环境变量和文件挂载

2. **存储管理**
   - PersistentVolume 和 PersistentVolumeClaim
   - StorageClass
   - 动态存储供应

### 阶段四：高级应用（3-5天）
1. **Namespace 和资源管理**
   - 命名空间管理
   - 资源配额和限制

2. **完整应用部署**
   - 多服务应用编排
   - 生产环境配置
   - 监控和日志

---

## 🚀 快速开始

### 前置要求

- Linux/macOS/Windows 系统
- kubectl 命令行工具
- Kubernetes 集群（本地或远程）

### 步骤1：安装 kubectl

#### Linux
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

#### macOS
```bash
brew install kubectl
```

#### Windows
```powershell
# 使用 Chocolatey
choco install kubernetes-cli
```

### 步骤2：配置集群连接

```bash
# 查看集群信息
kubectl cluster-info

# 查看节点
kubectl get nodes

# 查看所有资源
kubectl get all
```

### 步骤3：运行第一个 Pod

```bash
# 创建 Pod
kubectl create -f data/pod-simple.yaml

# 查看 Pod
kubectl get pods

# 查看 Pod 详情
kubectl describe pod nginx-pod

# 删除 Pod
kubectl delete pod nginx-pod
```

---

## 📖 核心知识点速查

### 1. 资源操作

| 操作 | 命令 | 说明 |
|------|------|------|
| **创建资源** | `kubectl create -f file.yaml` | 从文件创建 |
| **查看资源** | `kubectl get pods` | 查看资源列表 |
| **查看详情** | `kubectl describe pod name` | 查看详细信息 |
| **删除资源** | `kubectl delete pod name` | 删除资源 |
| **编辑资源** | `kubectl edit pod name` | 编辑资源 |

### 2. Pod 操作

| 操作 | 命令 | 说明 |
|------|------|------|
| **查看 Pod** | `kubectl get pods` | 查看 Pod 列表 |
| **查看日志** | `kubectl logs pod-name` | 查看 Pod 日志 |
| **进入 Pod** | `kubectl exec -it pod-name -- /bin/bash` | 进入 Pod |
| **执行命令** | `kubectl exec pod-name -- command` | 在 Pod 中执行命令 |

### 3. Deployment 操作

| 操作 | 命令 | 说明 |
|------|------|------|
| **扩展副本** | `kubectl scale deployment name --replicas=5` | 扩展副本数 |
| **更新镜像** | `kubectl set image deployment/name nginx=nginx:1.20` | 更新镜像 |
| **查看状态** | `kubectl rollout status deployment/name` | 查看更新状态 |
| **回滚** | `kubectl rollout undo deployment/name` | 回滚到上一版本 |

### 4. 常用资源类型

| 资源类型 | 缩写 | 说明 |
|---------|------|------|
| **Pod** | `po` | Pod |
| **Deployment** | `deploy` | 部署 |
| **Service** | `svc` | 服务 |
| **ConfigMap** | `cm` | 配置映射 |
| **Secret** | - | 密钥 |
| **PersistentVolume** | `pv` | 持久卷 |
| **PersistentVolumeClaim** | `pvc` | 持久卷声明 |
| **Namespace** | `ns` | 命名空间 |

---

## 💡 实战案例概览

### 案例1：基础操作
**学习目标**：掌握 Kubernetes 的基本操作

**涉及知识点**：
- Pod 创建和管理
- 容器配置
- 资源查看和删除
- Pod 交互

**典型操作**：
- 创建简单 Pod
- 多容器 Pod
- Pod 环境变量
- Pod 卷挂载

### 案例2：Deployment 和 Service
**学习目标**：掌握工作负载管理

**涉及知识点**：
- Deployment 创建和管理
- 副本扩展和滚动更新
- Service 类型和配置
- Ingress 路由

**典型操作**：
- 创建 Deployment
- 扩展和更新 Deployment
- 创建 Service
- 配置 Ingress

### 案例3：ConfigMap 和 Secret
**学习目标**：掌握配置和敏感信息管理

**涉及知识点**：
- ConfigMap 创建和使用
- Secret 创建和使用
- 环境变量注入
- 文件挂载

**典型操作**：
- 创建 ConfigMap
- 创建 Secret
- 在 Pod 中使用配置
- 更新配置

### 案例4：存储管理
**学习目标**：掌握存储管理

**涉及知识点**：
- PersistentVolume 创建
- PersistentVolumeClaim 创建
- StorageClass 配置
- 动态存储供应

**典型操作**：
- 创建 PV 和 PVC
- Pod 使用存储
- 动态存储供应
- 存储管理

### 案例5：完整应用部署
**学习目标**：部署完整的应用

**涉及知识点**：
- 多服务编排
- Namespace 管理
- 配置和存储整合
- 完整部署流程

**典型操作**：
- 创建 Namespace
- 部署多服务应用
- 配置 Service 和 Ingress
- 应用验证

---

## 📊 数据说明

### YAML 配置文件

| 文件名 | 资源类型 | 说明 |
|--------|---------|------|
| pod-simple.yaml | Pod | 简单 Pod 示例 |
| deployment.yaml | Deployment | Deployment 示例 |
| service-clusterip.yaml | Service | ClusterIP Service |
| configmap-literal.yaml | ConfigMap | ConfigMap 示例 |
| secret-opaque.yaml | Secret | Secret 示例 |
| pv-hostpath.yaml | PersistentVolume | PV 示例 |
| pvc.yaml | PersistentVolumeClaim | PVC 示例 |
| namespace.yaml | Namespace | Namespace 示例 |

### 完整应用配置

| 文件 | 说明 |
|------|------|
| deployment-web.yaml | Web 服务部署 |
| deployment-api.yaml | API 服务部署 |
| deployment-db.yaml | 数据库部署 |
| service-*.yaml | 各种服务配置 |
| configmap-app.yaml | 应用配置 |
| secret-db.yaml | 数据库密钥 |
| ingress-app.yaml | Ingress 配置 |

---

## 🔧 使用技巧

### 1. kubectl 别名

```bash
# 设置常用别名
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgd='kubectl get deployments'
alias kgs='kubectl get services'
alias kd='kubectl describe'
alias kl='kubectl logs'
```

### 2. 资源查看技巧

```bash
# 查看所有命名空间的资源
kubectl get pods --all-namespaces

# 按标签筛选
kubectl get pods -l app=nginx

# 输出 YAML 格式
kubectl get pod name -o yaml

# 输出 JSON 格式
kubectl get pod name -o json
```

### 3. 常见问题

**问题1：Pod 一直 Pending**
```bash
# 查看 Pod 事件
kubectl describe pod pod-name

# 查看节点资源
kubectl top nodes
```

**问题2：Pod 一直 CrashLoopBackOff**
```bash
# 查看 Pod 日志
kubectl logs pod-name

# 查看前一个容器的日志
kubectl logs pod-name --previous
```

**问题3：Service 无法访问**
```bash
# 查看 Service 和 Endpoints
kubectl get svc,endpoints

# 查看 Service 详情
kubectl describe service service-name
```

---

## 📝 学习建议

### 初学者
1. 从基础概念开始，理解 Kubernetes 架构
2. 多动手实践，创建和操作资源
3. 理解 YAML 配置文件结构
4. 学会查看日志和事件排查问题

### 进阶学习
1. 学习 Deployment 和 Service 的深入使用
2. 掌握 ConfigMap 和 Secret 管理
3. 学习存储管理和动态供应
4. 理解 Kubernetes 的网络模型

### 实践建议
1. **动手实践**：不要只看文档，要实际操作集群
2. **理解原理**：了解 Kubernetes 的工作原理
3. **最佳实践**：学习 Kubernetes 的最佳实践
4. **生产部署**：学习生产环境的部署方法

---

## 🔗 相关资源

### 官方文档
- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [kubectl 命令参考](https://kubernetes.io/docs/reference/kubectl/)
- [Kubernetes API 参考](https://kubernetes.io/docs/reference/kubernetes-api/)

### 推荐阅读
- `README.md` - 详细的知识点文档
- `cases/` - 五个实战案例的详细说明
- Kubernetes 最佳实践指南

### 扩展学习
- Kubernetes 网络深入
- Kubernetes 安全
- Helm 包管理
- Operator 开发
- 集群运维

---

## ✅ 学习检查清单

完成以下任务，确保掌握 Kubernetes 核心技能：

### 基础操作
- [ ] 能够创建和管理 Pod
- [ ] 能够创建和管理 Deployment
- [ ] 能够创建和管理 Service
- [ ] 能够使用 kubectl 基本命令

### 进阶操作
- [ ] 能够使用 ConfigMap 和 Secret
- [ ] 能够管理存储（PV/PVC）
- [ ] 能够配置 Ingress
- [ ] 能够进行滚动更新和回滚

### 实战能力
- [ ] 完成案例1的所有操作
- [ ] 完成案例2的所有操作
- [ ] 完成案例3的所有操作
- [ ] 完成案例4的所有操作
- [ ] 完成案例5的完整部署
- [ ] 能够独立部署应用

---

## 🎓 学习成果

完成本指南的学习后，你将能够：
- ✅ 熟练使用 Kubernetes 进行容器编排
- ✅ 掌握 Pod、Deployment、Service 等核心资源
- ✅ 能够管理配置和存储
- ✅ 理解 Kubernetes 的网络和存储模型
- ✅ 具备部署和管理生产应用的能力
- ✅ 掌握 Kubernetes 的最佳实践

**祝你学习愉快！** 🚀

---

## 📌 快速参考

### 常用命令

```bash
# 查看集群信息
kubectl cluster-info

# 查看节点
kubectl get nodes

# 查看所有资源
kubectl get all

# 查看特定资源
kubectl get pods,services,deployments

# 查看资源详情
kubectl describe pod pod-name

# 查看日志
kubectl logs pod-name -f

# 进入 Pod
kubectl exec -it pod-name -- /bin/bash

# 应用 YAML 文件
kubectl apply -f file.yaml

# 删除资源
kubectl delete -f file.yaml
```

### 常用缩写

```bash
# 资源类型缩写
kubectl get po,deploy,svc,cm,secret,pv,pvc,ns
```

### 调试技巧

```bash
# 查看事件
kubectl get events --sort-by=.metadata.creationTimestamp

# 查看资源使用
kubectl top pods
kubectl top nodes

# 端口转发（调试）
kubectl port-forward pod/pod-name 8080:80
```
