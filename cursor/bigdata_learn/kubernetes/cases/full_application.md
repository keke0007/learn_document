# 案例5：完整应用部署

## 案例描述
使用 Kubernetes 部署完整的应用，包括 Web 应用、数据库、缓存、配置管理等。

## 项目结构

```
application/
├── deployment-web.yaml
├── deployment-api.yaml
├── service-web.yaml
├── service-api.yaml
├── service-db.yaml
├── configmap-app.yaml
├── secret-db.yaml
├── pvc-db.yaml
├── ingress.yaml
└── namespace.yaml
```

## YAML 配置文件

### 1. Namespace (namespace.yaml)
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: myapp
  labels:
    name: myapp
    environment: production
```

### 2. ConfigMap (configmap-app.yaml)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: myapp
data:
  app.properties: |
    app.name=MyApp
    app.version=1.0.0
    api.url=http://api-service:5000
    cache.url=redis://redis-service:6379
  nginx.conf: |
    server {
        listen 80;
        server_name localhost;
        location / {
            proxy_pass http://api-service:5000;
        }
    }
```

### 3. Secret (secret-db.yaml)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
  namespace: myapp
type: Opaque
data:
  username: cm9vdA==        # root (base64)
  password: cGFzc3dvcmQ=    # password (base64)
  database: bXlkYg==        # mydb (base64)
```

### 4. PersistentVolumeClaim (pvc-db.yaml)
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-pvc
  namespace: myapp
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: local-storage
```

### 5. Deployment - Web (deployment-web.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
  namespace: myapp
  labels:
    app: web
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
        version: v1
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        volumeMounts:
        - name: config
          mountPath: /etc/nginx/conf.d
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: config
        configMap:
          name: app-config
```

### 6. Deployment - API (deployment-api.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
  namespace: myapp
  labels:
    app: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
        version: v1
    spec:
      containers:
      - name: api
        image: nginx:latest  # 实际应该是应用镜像
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: database
        - name: DB_USERNAME
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: username
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        envFrom:
        - configMapRef:
            name: app-config
        resources:
          requests:
            memory: "128Mi"
            cpu: "500m"
          limits:
            memory: "256Mi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### 7. Deployment - Database (deployment-db.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: db-deployment
  namespace: myapp
  labels:
    app: db
spec:
  replicas: 1
  selector:
    matchLabels:
      app: db
  template:
    metadata:
      labels:
        app: db
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        - name: MYSQL_DATABASE
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: database
        - name: MYSQL_USER
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: username
        volumeMounts:
        - name: db-data
          mountPath: /var/lib/mysql
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
      volumes:
      - name: db-data
        persistentVolumeClaim:
          claimName: db-pvc
```

### 8. Service - Web (service-web.yaml)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
  namespace: myapp
  labels:
    app: web
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
```

### 9. Service - API (service-api.yaml)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: myapp
  labels:
    app: api
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
  - port: 5000
    targetPort: 5000
    protocol: TCP
    name: http
```

### 10. Service - Database (service-db.yaml)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: db-service
  namespace: myapp
  labels:
    app: db
spec:
  type: ClusterIP
  selector:
    app: db
  ports:
  - port: 3306
    targetPort: 3306
    protocol: TCP
    name: mysql
```

### 11. Ingress (ingress.yaml)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: myapp
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 5000
```

## 部署脚本

### 完整部署脚本 (deploy.sh)
```bash
#!/bin/bash

echo "=== Kubernetes 完整应用部署 ==="

# ============================================
# 1. 创建 Namespace
# ============================================

echo -e "\n1. 创建 Namespace"
kubectl create -f data/namespace.yaml

# ============================================
# 2. 创建 ConfigMap 和 Secret
# ============================================

echo -e "\n2. 创建 ConfigMap 和 Secret"
kubectl create -f data/configmap-app.yaml
kubectl create -f data/secret-db.yaml

# ============================================
# 3. 创建 PersistentVolumeClaim
# ============================================

echo -e "\n3. 创建 PersistentVolumeClaim"
kubectl create -f data/pvc-db.yaml

# ============================================
# 4. 创建 Deployments
# ============================================

echo -e "\n4. 创建 Deployments"
kubectl create -f data/deployment-db.yaml
sleep 10  # 等待数据库启动
kubectl create -f data/deployment-api.yaml
kubectl create -f data/deployment-web.yaml

# ============================================
# 5. 创建 Services
# ============================================

echo -e "\n5. 创建 Services"
kubectl create -f data/service-db.yaml
kubectl create -f data/service-api.yaml
kubectl create -f data/service-web.yaml

# ============================================
# 6. 创建 Ingress
# ============================================

echo -e "\n6. 创建 Ingress"
kubectl create -f data/ingress.yaml

# ============================================
# 7. 查看部署状态
# ============================================

echo -e "\n7. 查看部署状态"
kubectl get all -n myapp

# ============================================
# 8. 查看资源详情
# ============================================

echo -e "\n8. 查看资源详情"
kubectl get configmap,secret,pvc -n myapp
kubectl get ingress -n myapp

# ============================================
# 9. 等待 Pod 就绪
# ============================================

echo -e "\n9. 等待 Pod 就绪"
kubectl wait --for=condition=ready pod -l app=web -n myapp --timeout=60s
kubectl wait --for=condition=ready pod -l app=api -n myapp --timeout=60s
kubectl wait --for=condition=ready pod -l app=db -n myapp --timeout=60s

# ============================================
# 10. 测试应用
# ============================================

echo -e "\n10. 测试应用"
kubectl get pods -n myapp
kubectl get services -n myapp
kubectl get ingress -n myapp
```

### 清理脚本 (cleanup.sh)
```bash
#!/bin/bash

echo "=== 清理 Kubernetes 资源 ==="

# ============================================
# 1. 删除所有资源
# ============================================

echo -e "\n1. 删除所有资源"
kubectl delete -f data/ --ignore-not-found=true

# ============================================
# 2. 删除 Namespace（会删除所有资源）
# ============================================

echo -e "\n2. 删除 Namespace"
kubectl delete namespace myapp --ignore-not-found=true

# ============================================
# 3. 确认删除
# ============================================

echo -e "\n3. 确认删除"
kubectl get all -n myapp 2>/dev/null || echo "Namespace myapp 已删除"
```

## 运行方式

```bash
# 确保 kubectl 已配置
kubectl cluster-info

# 添加执行权限
chmod +x deploy.sh cleanup.sh

# 部署应用
./deploy.sh

# 清理应用
./cleanup.sh
```

## 预期结果

### 所有资源状态
```
NAME                                    READY   STATUS    RESTARTS   AGE
pod/api-deployment-xxx                  1/1     Running   0          10s
pod/db-deployment-xxx                  1/1     Running   0          20s
pod/web-deployment-xxx                 1/1     Running   0          10s

NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
service/api-service     ClusterIP   10.96.0.1       <none>        5000/TCP
service/db-service      ClusterIP   10.96.0.2       <none>        3306/TCP
service/web-service     ClusterIP   10.96.0.3       <none>        80/TCP

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment/api-deployment   3/3     3            3           10s
deployment/db-deployment     1/1     1            1           20s
deployment/web-deployment    2/2     2            2           10s
```

## 学习要点

1. **Namespace**：资源隔离和组织
2. **多服务编排**：Web、API、数据库协调
3. **配置管理**：ConfigMap 和 Secret 使用
4. **存储管理**：数据库数据持久化
5. **服务发现**：Service 和 Ingress 配置
6. **健康检查**：liveness 和 readiness 探针
7. **资源限制**：requests 和 limits
8. **完整部署流程**：从创建到验证
