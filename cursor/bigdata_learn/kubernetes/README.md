# Kubernetes 学习知识点

## 目录
1. [Kubernetes 基础概念](#1-kubernetes-基础概念)
2. [Pod 和容器](#2-pod-和容器)
3. [Deployment 和 ReplicaSet](#3-deployment-和-replicaset)
4. [Service](#4-service)
5. [Ingress](#5-ingress)
6. [ConfigMap 和 Secret](#6-configmap-和-secret)
7. [存储管理](#7-存储管理)
8. [Namespace](#8-namespace)
9. [资源管理](#9-资源管理)
10. [滚动更新和回滚](#10-滚动更新和回滚)
11. [案例与验证数据](#11-案例与验证数据)

---

## 1. Kubernetes 基础概念

### 1.1 什么是 Kubernetes
- Kubernetes（K8s）是一个开源的容器编排平台
- 自动化容器的部署、扩展和管理
- 支持多主机、多容器应用
- 提供服务发现、负载均衡、自动扩缩容等功能

### 1.2 Kubernetes 架构
- **Master 节点**：控制平面
  - API Server：API 服务器
  - etcd：键值存储
  - Scheduler：调度器
  - Controller Manager：控制器管理器
- **Node 节点**：工作节点
  - kubelet：节点代理
  - kube-proxy：网络代理
  - Container Runtime：容器运行时

### 1.3 核心概念
- **Pod**：最小的部署单元，包含一个或多个容器
- **Node**：工作节点，运行 Pod
- **Cluster**：集群，由 Master 和 Node 组成
- **Namespace**：命名空间，资源隔离

---

## 2. Pod 和容器

### 2.1 Pod 定义
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
```

### 2.2 Pod 操作
```bash
# 创建 Pod
kubectl create -f pod.yaml

# 查看 Pod
kubectl get pods
kubectl get pod my-pod

# 查看 Pod 详情
kubectl describe pod my-pod

# 删除 Pod
kubectl delete pod my-pod
```

### 2.3 容器配置
- **镜像**：image
- **端口**：ports
- **环境变量**：env
- **资源限制**：resources
- **卷挂载**：volumeMounts

---

## 3. Deployment 和 ReplicaSet

### 3.1 Deployment 定义
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: nginx
        image: nginx:latest
```

### 3.2 Deployment 操作
```bash
# 创建 Deployment
kubectl create -f deployment.yaml

# 查看 Deployment
kubectl get deployments

# 扩展 Deployment
kubectl scale deployment my-deployment --replicas=5

# 更新 Deployment
kubectl set image deployment/my-deployment nginx=nginx:1.20

# 查看滚动更新状态
kubectl rollout status deployment/my-deployment
```

### 3.3 ReplicaSet
- Deployment 管理 ReplicaSet
- ReplicaSet 确保 Pod 副本数
- 自动创建和删除 Pod

---

## 4. Service

### 4.1 Service 类型
- **ClusterIP**：集群内部访问（默认）
- **NodePort**：节点端口访问
- **LoadBalancer**：负载均衡器
- **ExternalName**：外部名称

### 4.2 Service 定义
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

### 4.3 Service 操作
```bash
# 创建 Service
kubectl create -f service.yaml

# 查看 Service
kubectl get services

# 查看 Service 详情
kubectl describe service my-service
```

---

## 5. Ingress

### 5.1 Ingress 定义
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

### 5.2 Ingress Controller
- Nginx Ingress Controller
- Traefik
- Istio Gateway

---

## 6. ConfigMap 和 Secret

### 6.1 ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  config.properties: |
    key1=value1
    key2=value2
```

### 6.2 Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  username: YWRtaW4=  # base64编码
  password: cGFzc3dvcmQ=
```

### 6.3 使用 ConfigMap 和 Secret
```yaml
spec:
  containers:
  - name: app
    envFrom:
    - configMapRef:
        name: my-config
    - secretRef:
        name: my-secret
```

---

## 7. 存储管理

### 7.1 PersistentVolume (PV)
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  hostPath:
    path: /data
```

### 7.2 PersistentVolumeClaim (PVC)
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: local-storage
```

### 7.3 使用存储
```yaml
spec:
  containers:
  - name: app
    volumeMounts:
    - name: storage
      mountPath: /data
  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: my-pvc
```

---

## 8. Namespace

### 8.1 Namespace 操作
```bash
# 创建 Namespace
kubectl create namespace my-namespace

# 查看 Namespace
kubectl get namespaces

# 在 Namespace 中创建资源
kubectl create -f pod.yaml -n my-namespace

# 删除 Namespace
kubectl delete namespace my-namespace
```

### 8.2 默认 Namespace
- **default**：默认命名空间
- **kube-system**：系统组件
- **kube-public**：公共资源

---

## 9. 资源管理

### 9.1 资源请求和限制
```yaml
spec:
  containers:
  - name: app
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### 9.2 ResourceQuota
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: my-quota
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
```

---

## 10. 滚动更新和回滚

### 10.1 滚动更新
```bash
# 更新镜像
kubectl set image deployment/my-deployment nginx=nginx:1.20

# 查看更新状态
kubectl rollout status deployment/my-deployment

# 查看更新历史
kubectl rollout history deployment/my-deployment
```

### 10.2 回滚
```bash
# 回滚到上一个版本
kubectl rollout undo deployment/my-deployment

# 回滚到指定版本
kubectl rollout undo deployment/my-deployment --to-revision=2
```

---

## 11. 案例与验证数据

详见以下文件：
- [案例1：基础操作](cases/basic_operations.md)
- [案例2：Deployment 和 Service](cases/deployment_service.md)
- [案例3：ConfigMap 和 Secret](cases/configmap_secret.md)
- [案例4：存储管理](cases/storage_management.md)
- [案例5：完整应用部署](cases/full_application.md)
- [验证数据文件](data/)
