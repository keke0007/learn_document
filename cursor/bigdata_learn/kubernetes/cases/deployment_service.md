# 案例2：Deployment 和 Service

## 案例描述
学习使用 Deployment 管理 Pod 副本，使用 Service 暴露应用。

## YAML 配置文件

### 1. Deployment (deployment.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
        version: v1
    spec:
      containers:
      - name: nginx
        image: nginx:1.20
        ports:
        - containerPort: 80
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
```

### 2. Service - ClusterIP (service-clusterip.yaml)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  labels:
    app: nginx
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
```

### 3. Service - NodePort (service-nodeport.yaml)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
  labels:
    app: nginx
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
    protocol: TCP
    name: http
```

### 4. Service - LoadBalancer (service-loadbalancer.yaml)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-loadbalancer
  labels:
    app: nginx
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
```

### 5. Ingress (ingress.yaml)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: nginx.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx-service
            port:
              number: 80
```

## 操作脚本

### Deployment 操作脚本 (deployment_operations.sh)
```bash
#!/bin/bash

echo "=== Deployment 操作示例 ==="

# ============================================
# 1. 创建 Deployment
# ============================================

echo -e "\n1. 创建 Deployment"
kubectl create -f data/deployment.yaml

# ============================================
# 2. 查看 Deployment
# ============================================

echo -e "\n2. 查看 Deployment"
kubectl get deployments

echo -e "\n3. 查看 Deployment 详情"
kubectl describe deployment nginx-deployment

# ============================================
# 4. 查看 Pod（由 Deployment 创建）
# ============================================

echo -e "\n4. 查看 Pod"
kubectl get pods -l app=nginx

# ============================================
# 5. 扩展 Deployment
# ============================================

echo -e "\n5. 扩展 Deployment 到 5 个副本"
kubectl scale deployment nginx-deployment --replicas=5

echo -e "\n6. 查看扩展后的 Pod"
kubectl get pods -l app=nginx

# ============================================
# 7. 更新 Deployment
# ============================================

echo -e "\n7. 更新镜像版本"
kubectl set image deployment/nginx-deployment nginx=nginx:1.21

# ============================================
# 8. 查看滚动更新状态
# ============================================

echo -e "\n8. 查看滚动更新状态"
kubectl rollout status deployment/nginx-deployment

# ============================================
# 9. 查看更新历史
# ============================================

echo -e "\n9. 查看更新历史"
kubectl rollout history deployment/nginx-deployment

# ============================================
# 10. 回滚 Deployment
# ============================================

echo -e "\n10. 回滚到上一个版本"
kubectl rollout undo deployment/nginx-deployment

# ============================================
# 11. 删除 Deployment
# ============================================

echo -e "\n11. 删除 Deployment"
kubectl delete deployment nginx-deployment
```

### Service 操作脚本 (service_operations.sh)
```bash
#!/bin/bash

echo "=== Service 操作示例 ==="

# ============================================
# 1. 创建 Deployment（前提）
# ============================================

echo -e "\n1. 创建 Deployment"
kubectl create -f data/deployment.yaml
sleep 5

# ============================================
# 2. 创建 ClusterIP Service
# ============================================

echo -e "\n2. 创建 ClusterIP Service"
kubectl create -f data/service-clusterip.yaml

# ============================================
# 3. 查看 Service
# ============================================

echo -e "\n3. 查看 Service"
kubectl get services

echo -e "\n4. 查看 Service 详情"
kubectl describe service nginx-service

# ============================================
# 5. 测试 Service（在集群内）
# ============================================

echo -e "\n5. 测试 Service"
kubectl run test-pod --image=busybox --rm -it --restart=Never -- wget -qO- http://nginx-service

# ============================================
# 6. 创建 NodePort Service
# ============================================

echo -e "\n6. 创建 NodePort Service"
kubectl create -f data/service-nodeport.yaml

echo -e "\n7. 查看 NodePort Service"
kubectl get service nginx-nodeport

# ============================================
# 8. 查看 Service Endpoints
# ============================================

echo -e "\n8. 查看 Service Endpoints"
kubectl get endpoints nginx-service

# ============================================
# 9. 删除 Service
# ============================================

echo -e "\n9. 删除 Service"
kubectl delete service nginx-service nginx-nodeport
```

### Ingress 操作脚本 (ingress_operations.sh)
```bash
#!/bin/bash

echo "=== Ingress 操作示例 ==="

# ============================================
# 1. 确保 Deployment 和 Service 存在
# ============================================

echo -e "\n1. 创建 Deployment 和 Service"
kubectl create -f data/deployment.yaml
kubectl create -f data/service-clusterip.yaml
sleep 5

# ============================================
# 2. 创建 Ingress
# ============================================

echo -e "\n2. 创建 Ingress"
kubectl create -f data/ingress.yaml

# ============================================
# 3. 查看 Ingress
# ============================================

echo -e "\n3. 查看 Ingress"
kubectl get ingress

echo -e "\n4. 查看 Ingress 详情"
kubectl describe ingress nginx-ingress

# ============================================
# 5. 测试 Ingress
# ============================================

echo -e "\n5. 测试 Ingress"
echo "执行: curl -H 'Host: nginx.example.com' http://<ingress-ip>"

# ============================================
# 6. 删除 Ingress
# ============================================

echo -e "\n6. 删除 Ingress"
kubectl delete ingress nginx-ingress
```

## 运行方式

```bash
# 确保 kubectl 已配置
kubectl cluster-info

# 添加执行权限
chmod +x deployment_operations.sh service_operations.sh ingress_operations.sh

# 运行脚本
./deployment_operations.sh
./service_operations.sh
./ingress_operations.sh
```

## 预期结果

### Deployment 状态
```
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           10s
```

### Service 状态
```
NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
nginx-service   ClusterIP   10.96.0.1      <none>        80/TCP    5s
```

### Pod 状态
```
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-xxx-xxx           1/1     Running   0          10s
nginx-deployment-xxx-xxx           1/1     Running   0          10s
nginx-deployment-xxx-xxx           1/1     Running   0          10s
```

## 学习要点

1. **Deployment**：管理 Pod 副本、滚动更新
2. **Service**：服务发现、负载均衡
3. **Service 类型**：ClusterIP、NodePort、LoadBalancer
4. **Ingress**：HTTP/HTTPS 路由
5. **健康检查**：livenessProbe、readinessProbe
6. **滚动更新**：零停机更新
7. **回滚**：版本回退
