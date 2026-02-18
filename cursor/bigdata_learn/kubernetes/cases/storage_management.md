# 案例4：存储管理

## 案例描述
学习 Kubernetes 的存储管理，包括 PersistentVolume、PersistentVolumeClaim、StorageClass。

## YAML 配置文件

### 1. PersistentVolume - HostPath (pv-hostpath.yaml)
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-hostpath
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  hostPath:
    path: /data/pv-hostpath
```

### 2. PersistentVolume - NFS (pv-nfs.yaml)
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs
spec:
  capacity:
    storage: 20Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs-storage
  nfs:
    server: nfs-server.example.com
    path: /exports/data
```

### 3. PersistentVolumeClaim (pvc.yaml)
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

### 4. StorageClass (storageclass.yaml)
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
parameters:
  type: ssd
```

### 5. Pod 使用 PVC (pod-with-pvc.yaml)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-pvc
spec:
  containers:
  - name: app
    image: nginx:latest
    volumeMounts:
    - name: data-volume
      mountPath: /data
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: my-pvc
```

### 6. Deployment 使用 PVC (deployment-with-pvc.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-storage
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
        volumeMounts:
        - name: data-volume
          mountPath: /data
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: my-pvc
```

## 操作脚本

### 存储操作脚本 (storage_operations.sh)
```bash
#!/bin/bash

echo "=== Kubernetes 存储操作示例 ==="

# ============================================
# 1. 创建 PersistentVolume
# ============================================

echo -e "\n1. 创建 PersistentVolume"
kubectl create -f data/pv-hostpath.yaml

# ============================================
# 2. 查看 PersistentVolume
# ============================================

echo -e "\n2. 查看 PersistentVolume"
kubectl get pv

echo -e "\n3. 查看 PersistentVolume 详情"
kubectl describe pv pv-hostpath

# ============================================
# 4. 创建 PersistentVolumeClaim
# ============================================

echo -e "\n4. 创建 PersistentVolumeClaim"
kubectl create -f data/pvc.yaml

# ============================================
# 5. 查看 PersistentVolumeClaim
# ============================================

echo -e "\n5. 查看 PersistentVolumeClaim"
kubectl get pvc

echo -e "\n6. 查看 PersistentVolumeClaim 详情"
kubectl describe pvc my-pvc

# ============================================
# 7. 查看 PV 和 PVC 绑定状态
# ============================================

echo -e "\n7. 查看 PV 和 PVC 绑定状态"
kubectl get pv,pvc

# ============================================
# 8. 创建使用 PVC 的 Pod
# ============================================

echo -e "\n8. 创建使用 PVC 的 Pod"
kubectl create -f data/pod-with-pvc.yaml

# ============================================
# 9. 验证存储挂载
# ============================================

echo -e "\n9. 验证存储挂载"
sleep 5
kubectl exec pod-with-pvc -- df -h /data
kubectl exec pod-with-pvc -- touch /data/test.txt
kubectl exec pod-with-pvc -- ls -la /data

# ============================================
# 10. 创建 StorageClass
# ============================================

echo -e "\n10. 创建 StorageClass"
kubectl create -f data/storageclass.yaml

echo -e "\n11. 查看 StorageClass"
kubectl get storageclass

# ============================================
# 12. 清理
# ============================================

echo -e "\n12. 清理"
kubectl delete pod pod-with-pvc
kubectl delete pvc my-pvc
kubectl delete pv pv-hostpath
kubectl delete storageclass fast-ssd
```

### 动态存储脚本 (dynamic_storage.sh)
```bash
#!/bin/bash

echo "=== 动态存储示例 ==="

# ============================================
# 1. 创建 StorageClass（支持动态供应）
# ============================================

echo -e "\n1. 创建 StorageClass"
cat <<EOF | kubectl create -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
EOF

# ============================================
# 2. 创建使用动态存储的 PVC
# ============================================

echo -e "\n2. 创建使用动态存储的 PVC"
cat <<EOF | kubectl create -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
EOF

# ============================================
# 3. 查看动态创建的 PV
# ============================================

echo -e "\n3. 查看动态创建的 PV"
sleep 5
kubectl get pv,pvc

# ============================================
# 4. 使用动态 PVC 创建 Pod
# ============================================

echo -e "\n4. 使用动态 PVC 创建 Pod"
cat <<EOF | kubectl create -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-dynamic-storage
spec:
  containers:
  - name: app
    image: nginx:latest
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: dynamic-pvc
EOF

# ============================================
# 5. 清理
# ============================================

echo -e "\n5. 清理"
kubectl delete pod pod-dynamic-storage
kubectl delete pvc dynamic-pvc
kubectl delete storageclass standard
```

## 运行方式

```bash
# 确保 kubectl 已配置
kubectl cluster-info

# 添加执行权限
chmod +x storage_operations.sh dynamic_storage.sh

# 运行脚本
./storage_operations.sh
./dynamic_storage.sh
```

## 预期结果

### PV 和 PVC 状态
```
NAME          CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM
pv-hostpath   10Gi       RWO            Retain           Bound    default/my-pvc

NAME        STATUS   VOLUME        CAPACITY   ACCESS MODES   STORAGECLASS
my-pvc      Bound    pv-hostpath   10Gi       RWO            local-storage
```

### Pod 存储挂载
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        10G  1.0G  9.0G  10% /data
```

## 学习要点

1. **PersistentVolume**：集群级别的存储资源
2. **PersistentVolumeClaim**：Pod 的存储请求
3. **StorageClass**：动态存储供应
4. **访问模式**：ReadWriteOnce、ReadWriteMany、ReadOnlyMany
5. **回收策略**：Retain、Recycle、Delete
6. **动态供应**：自动创建 PV
