# 案例1：Kubernetes 基础操作

## 案例描述
学习 Kubernetes 的基本操作，包括 Pod 创建、查看、删除等。

## YAML 配置文件

### 1. 简单 Pod (pod-simple.yaml)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
    version: v1
spec:
  containers:
  - name: nginx-container
    image: nginx:latest
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### 2. 多容器 Pod (pod-multi-container.yaml)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
  labels:
    app: multi-app
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
  - name: redis
    image: redis:alpine
    ports:
    - containerPort: 6379
```

### 3. Pod 带环境变量 (pod-with-env.yaml)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-env
spec:
  containers:
  - name: app
    image: nginx:latest
    env:
    - name: ENV_VAR1
      value: "value1"
    - name: ENV_VAR2
      value: "value2"
    - name: NODE_NAME
      valueFrom:
        fieldRef:
          fieldPath: spec.nodeName
```

### 4. Pod 带卷挂载 (pod-with-volume.yaml)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-volume
spec:
  containers:
  - name: app
    image: nginx:latest
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
    - name: data-volume
      mountPath: /data
  volumes:
  - name: config-volume
    configMap:
      name: my-config
  - name: data-volume
    emptyDir: {}
```

## 操作脚本

### 基础操作脚本 (basic_operations.sh)
```bash
#!/bin/bash

echo "=== Kubernetes 基础操作示例 ==="

# ============================================
# 1. 创建 Pod
# ============================================

echo -e "\n1. 创建简单 Pod"
kubectl create -f data/pod-simple.yaml

# ============================================
# 2. 查看 Pod
# ============================================

echo -e "\n2. 查看 Pod 列表"
kubectl get pods

echo -e "\n3. 查看 Pod 详情"
kubectl get pod nginx-pod -o wide

# ============================================
# 4. 查看 Pod 详细信息
# ============================================

echo -e "\n4. 查看 Pod 详细信息"
kubectl describe pod nginx-pod

# ============================================
# 5. 查看 Pod 日志
# ============================================

echo -e "\n5. 查看 Pod 日志"
kubectl logs nginx-pod

# ============================================
# 6. 进入 Pod
# ============================================

echo -e "\n6. 进入 Pod（交互式）"
echo "执行: kubectl exec -it nginx-pod -- /bin/bash"

# ============================================
# 7. 在 Pod 中执行命令
# ============================================

echo -e "\n7. 在 Pod 中执行命令"
kubectl exec nginx-pod -- nginx -v

# ============================================
# 8. 复制文件到 Pod
# ============================================

echo -e "\n8. 复制文件到 Pod"
echo "执行: kubectl cp local-file nginx-pod:/path/to/dest"

# ============================================
# 9. 删除 Pod
# ============================================

echo -e "\n9. 删除 Pod"
kubectl delete pod nginx-pod

# ============================================
# 10. 使用 YAML 删除
# ============================================

echo -e "\n10. 使用 YAML 文件删除"
kubectl delete -f data/pod-simple.yaml
```

### Pod 管理脚本 (pod_management.sh)
```bash
#!/bin/bash

echo "=== Pod 管理操作 ==="

# ============================================
# 1. 创建多个 Pod
# ============================================

echo -e "\n1. 创建多个 Pod"
kubectl create -f data/pod-simple.yaml
kubectl create -f data/pod-with-env.yaml

# ============================================
# 2. 按标签查看 Pod
# ============================================

echo -e "\n2. 按标签查看 Pod"
kubectl get pods -l app=nginx

# ============================================
# 3. 查看所有命名空间的 Pod
# ============================================

echo -e "\n3. 查看所有命名空间的 Pod"
kubectl get pods --all-namespaces

# ============================================
# 4. 查看 Pod 资源使用
# ============================================

echo -e "\n4. 查看 Pod 资源使用（需要 metrics-server）"
kubectl top pod

# ============================================
# 5. 编辑 Pod（不推荐，Pod 不可变）
# ============================================

echo -e "\n5. 编辑 Pod"
echo "注意：Pod 是不可变的，编辑会创建新 Pod"
echo "执行: kubectl edit pod nginx-pod"

# ============================================
# 6. 查看 Pod 事件
# ============================================

echo -e "\n6. 查看 Pod 事件"
kubectl get events --field-selector involvedObject.name=nginx-pod

# ============================================
# 7. 清理所有 Pod
# ============================================

echo -e "\n7. 清理所有 Pod"
kubectl delete pods --all
```

## 运行方式

```bash
# 确保 kubectl 已配置并连接到集群
kubectl cluster-info

# 添加执行权限
chmod +x basic_operations.sh pod_management.sh

# 运行脚本
./basic_operations.sh
./pod_management.sh
```

## 预期结果

### Pod 列表
```
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          10s
```

### Pod 详情
```
Name:         nginx-pod
Namespace:    default
Status:       Running
Containers:
  nginx-container:
    Image:          nginx:latest
    Port:           80/TCP
```

## 学习要点

1. **Pod 创建**：使用 YAML 文件创建 Pod
2. **Pod 查看**：get、describe、logs
3. **Pod 交互**：exec、cp
4. **Pod 管理**：标签选择、资源查看
5. **Pod 特性**：不可变性、生命周期
