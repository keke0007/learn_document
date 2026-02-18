# 案例3：ConfigMap 和 Secret

## 案例描述
学习使用 ConfigMap 和 Secret 管理应用配置和敏感信息。

## YAML 配置文件

### 1. ConfigMap - 字面量 (configmap-literal.yaml)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
data:
  database_url: "mysql://db:3306/mydb"
  cache_url: "redis://redis:6379"
  log_level: "info"
```

### 2. ConfigMap - 文件 (configmap-file.yaml)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config-file
data:
  app.properties: |
    server.port=8080
    server.host=0.0.0.0
    database.host=db
    database.port=3306
    database.name=mydb
  nginx.conf: |
    server {
        listen 80;
        server_name localhost;
        location / {
            proxy_pass http://backend:5000;
        }
    }
```

### 3. Secret - Opaque (secret-opaque.yaml)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  username: YWRtaW4=          # admin (base64)
  password: cGFzc3dvcmQxMjM=  # password123 (base64)
  api_key: YXBpX2tleV8xMjM0NTY=  # api_key_123456 (base64)
```

### 4. Secret - TLS (secret-tls.yaml)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTi...  # base64编码的证书
  tls.key: LS0tLS1CRUdJTi...  # base64编码的私钥
```

### 5. Pod 使用 ConfigMap (pod-with-configmap.yaml)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-configmap
spec:
  containers:
  - name: app
    image: nginx:latest
    env:
    # 方式1：单个环境变量
    - name: DATABASE_URL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database_url
    # 方式2：所有键值对
    envFrom:
    - configMapRef:
        name: app-config
    # 方式3：挂载为文件
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
      readOnly: true
  volumes:
  - name: config-volume
    configMap:
      name: app-config-file
```

### 6. Pod 使用 Secret (pod-with-secret.yaml)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-secret
spec:
  containers:
  - name: app
    image: nginx:latest
    env:
    # 方式1：单个环境变量
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: username
    # 方式2：所有键值对
    envFrom:
    - secretRef:
        name: app-secret
    # 方式3：挂载为文件
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secret
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: app-secret
```

### 7. Deployment 使用 ConfigMap 和 Secret (deployment-with-config.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: nginx:latest
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secret
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
        - name: secret-volume
          mountPath: /etc/secret
      volumes:
      - name: config-volume
        configMap:
          name: app-config-file
      - name: secret-volume
        secret:
          secretName: app-secret
```

## 操作脚本

### ConfigMap 操作脚本 (configmap_operations.sh)
```bash
#!/bin/bash

echo "=== ConfigMap 操作示例 ==="

# ============================================
# 1. 从 YAML 创建 ConfigMap
# ============================================

echo -e "\n1. 从 YAML 创建 ConfigMap"
kubectl create -f data/configmap-literal.yaml

# ============================================
# 2. 从命令行创建 ConfigMap
# ============================================

echo -e "\n2. 从命令行创建 ConfigMap"
kubectl create configmap app-config-cli \
  --from-literal=key1=value1 \
  --from-literal=key2=value2

# ============================================
# 3. 从文件创建 ConfigMap
# ============================================

echo -e "\n3. 从文件创建 ConfigMap"
kubectl create configmap app-config-from-file \
  --from-file=data/app.properties

# ============================================
# 4. 查看 ConfigMap
# ============================================

echo -e "\n4. 查看 ConfigMap 列表"
kubectl get configmaps

echo -e "\n5. 查看 ConfigMap 详情"
kubectl describe configmap app-config

# ============================================
# 6. 查看 ConfigMap 内容
# ============================================

echo -e "\n6. 查看 ConfigMap 内容"
kubectl get configmap app-config -o yaml

# ============================================
# 7. 编辑 ConfigMap
# ============================================

echo -e "\n7. 编辑 ConfigMap"
echo "执行: kubectl edit configmap app-config"

# ============================================
# 8. 删除 ConfigMap
# ============================================

echo -e "\n8. 删除 ConfigMap"
kubectl delete configmap app-config app-config-cli app-config-from-file
```

### Secret 操作脚本 (secret_operations.sh)
```bash
#!/bin/bash

echo "=== Secret 操作示例 ==="

# ============================================
# 1. 从 YAML 创建 Secret
# ============================================

echo -e "\n1. 从 YAML 创建 Secret"
kubectl create -f data/secret-opaque.yaml

# ============================================
# 2. 从命令行创建 Secret
# ============================================

echo -e "\n2. 从命令行创建 Secret"
kubectl create secret generic app-secret-cli \
  --from-literal=username=admin \
  --from-literal=password=password123

# ============================================
# 3. 从文件创建 Secret
# ============================================

echo -e "\n3. 从文件创建 Secret"
echo -n 'admin' > username.txt
echo -n 'password123' > password.txt
kubectl create secret generic app-secret-from-file \
  --from-file=username=username.txt \
  --from-file=password=password.txt
rm username.txt password.txt

# ============================================
# 4. 查看 Secret
# ============================================

echo -e "\n4. 查看 Secret 列表"
kubectl get secrets

echo -e "\n5. 查看 Secret 详情"
kubectl describe secret app-secret

# ============================================
# 6. 查看 Secret 内容（解码）
# ============================================

echo -e "\n6. 查看 Secret 内容（解码）"
kubectl get secret app-secret -o jsonpath='{.data.username}' | base64 -d
echo
kubectl get secret app-secret -o jsonpath='{.data.password}' | base64 -d
echo

# ============================================
# 7. 使用 Secret 创建 Pod
# ============================================

echo -e "\n7. 创建使用 Secret 的 Pod"
kubectl create -f data/pod-with-secret.yaml

# ============================================
# 8. 验证 Secret 在 Pod 中的使用
# ============================================

echo -e "\n8. 验证 Secret 在 Pod 中的使用"
sleep 5
kubectl exec pod-with-secret -- env | grep -E "USERNAME|PASSWORD"

# ============================================
# 9. 清理
# ============================================

echo -e "\n9. 清理"
kubectl delete pod pod-with-secret
kubectl delete secret app-secret app-secret-cli app-secret-from-file
```

### 综合使用脚本 (configmap_secret_usage.sh)
```bash
#!/bin/bash

echo "=== ConfigMap 和 Secret 综合使用 ==="

# ============================================
# 1. 创建 ConfigMap 和 Secret
# ============================================

echo -e "\n1. 创建 ConfigMap 和 Secret"
kubectl create -f data/configmap-literal.yaml
kubectl create -f data/secret-opaque.yaml

# ============================================
# 2. 创建使用 ConfigMap 和 Secret 的 Deployment
# ============================================

echo -e "\n2. 创建 Deployment"
kubectl create -f data/deployment-with-config.yaml

# ============================================
# 3. 查看 Pod 状态
# ============================================

echo -e "\n3. 查看 Pod 状态"
kubectl get pods -l app=myapp

# ============================================
# 4. 验证配置
# ============================================

echo -e "\n4. 验证环境变量"
sleep 5
POD_NAME=$(kubectl get pods -l app=myapp -o jsonpath='{.items[0].metadata.name}')
kubectl exec $POD_NAME -- env | grep -E "DATABASE|CACHE|LOG|USERNAME|PASSWORD"

# ============================================
# 5. 验证挂载的文件
# ============================================

echo -e "\n5. 验证挂载的文件"
kubectl exec $POD_NAME -- ls -la /etc/config
kubectl exec $POD_NAME -- ls -la /etc/secret

# ============================================
# 6. 更新 ConfigMap
# ============================================

echo -e "\n6. 更新 ConfigMap"
kubectl patch configmap app-config --type merge -p '{"data":{"log_level":"debug"}}'

# ============================================
# 7. 重启 Pod 使配置生效
# ============================================

echo -e "\n7. 重启 Pod 使配置生效"
kubectl rollout restart deployment/app-deployment

# ============================================
# 8. 清理
# ============================================

echo -e "\n8. 清理"
kubectl delete deployment app-deployment
kubectl delete configmap app-config
kubectl delete secret app-secret
```

## 运行方式

```bash
# 确保 kubectl 已配置
kubectl cluster-info

# 添加执行权限
chmod +x configmap_operations.sh secret_operations.sh configmap_secret_usage.sh

# 运行脚本
./configmap_operations.sh
./secret_operations.sh
./configmap_secret_usage.sh
```

## 预期结果

### ConfigMap 列表
```
NAME                DATA   AGE
app-config          3      10s
app-config-file     2      5s
```

### Secret 列表
```
NAME          TYPE     DATA   AGE
app-secret    Opaque   3      10s
```

### Pod 环境变量
```
DATABASE_URL=mysql://db:3306/mydb
CACHE_URL=redis://redis:6379
LOG_LEVEL=info
USERNAME=admin
PASSWORD=password123
```

## 学习要点

1. **ConfigMap**：配置管理、多种创建方式
2. **Secret**：敏感信息管理、base64编码
3. **使用方式**：环境变量、文件挂载
4. **更新配置**：更新 ConfigMap/Secret、重启 Pod
5. **最佳实践**：配置与代码分离、敏感信息加密
