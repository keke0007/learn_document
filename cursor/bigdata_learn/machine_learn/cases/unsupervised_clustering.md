# 案例：无监督学习 - 聚类

## 目标

掌握常用聚类算法的使用，包括 K-Means、层次聚类、DBSCAN，以及聚类效果的评估方法。

---

## 知识点覆盖

- K-Means 聚类
- 层次聚类（Hierarchical Clustering）
- DBSCAN 密度聚类
- PCA 降维可视化
- 聚类评估指标（轮廓系数、Calinski-Harabasz）
- 确定最优簇数（肘部法则）

---

## 场景描述

**业务场景**：客户分群

根据客户的消费行为特征，将客户划分为不同群体，以便进行精准营销。

**数据特征**：
- `annual_income`: 年收入
- `spending_score`: 消费评分
- `age`: 年龄
- `purchase_frequency`: 购买频率
- `avg_order_value`: 平均订单金额

---

## 1. 数据准备

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
df = pd.read_csv('data/clustering_data.csv')

# 探索性分析
print(df.describe())

# 可视化
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].scatter(df['annual_income'], df['spending_score'])
axes[0].set_xlabel('Annual Income')
axes[0].set_ylabel('Spending Score')
axes[0].set_title('Income vs Spending')

axes[1].scatter(df['age'], df['spending_score'])
axes[1].set_xlabel('Age')
axes[1].set_ylabel('Spending Score')
axes[1].set_title('Age vs Spending')
plt.tight_layout()
plt.savefig('data_exploration.png')

# 准备特征
X = df.values

# 标准化（聚类前必须标准化）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

---

## 2. K-Means 聚类

### 确定最优 K 值（肘部法则）

```python
from sklearn.cluster import KMeans

# 肘部法则
inertias = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

# 绘制肘部曲线
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.title('Elbow Method')

# 轮廓系数选择 K
from sklearn.metrics import silhouette_score

silhouette_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    silhouette_scores.append(score)
    print(f"K={k}: Silhouette Score = {score:.4f}")

plt.subplot(1, 2, 2)
plt.plot(range(2, 11), silhouette_scores, 'go-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score vs K')
plt.tight_layout()
plt.savefig('k_selection.png')
```

### 训练 K-Means

```python
# 选择 K=4
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
clusters_kmeans = kmeans.fit_predict(X_scaled)

# 添加聚类标签
df['cluster_kmeans'] = clusters_kmeans

# 聚类中心
centers = scaler.inverse_transform(kmeans.cluster_centers_)
print("聚类中心:")
print(pd.DataFrame(centers, columns=df.columns[:-1]))

# 各簇统计
print("\n各簇样本数:")
print(df['cluster_kmeans'].value_counts().sort_index())

# 各簇特征均值
print("\n各簇特征均值:")
print(df.groupby('cluster_kmeans').mean())
```

### 可视化（2D）

```python
# 使用前两个特征可视化
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    df['annual_income'], 
    df['spending_score'],
    c=clusters_kmeans, 
    cmap='viridis',
    alpha=0.6
)
plt.scatter(
    centers[:, 0], 
    centers[:, 1],
    c='red', 
    marker='X', 
    s=200, 
    label='Centroids'
)
plt.colorbar(scatter, label='Cluster')
plt.xlabel('Annual Income')
plt.ylabel('Spending Score')
plt.title('K-Means Clustering (K=4)')
plt.legend()
plt.savefig('kmeans_result.png')
```

---

## 3. 层次聚类

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# 绘制树状图
plt.figure(figsize=(12, 5))
linkage_matrix = linkage(X_scaled, method='ward')
dendrogram(linkage_matrix, truncate_mode='level', p=5)
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('Sample Index')
plt.ylabel('Distance')
plt.savefig('dendrogram.png')

# 层次聚类
hierarchical = AgglomerativeClustering(n_clusters=4, linkage='ward')
clusters_hier = hierarchical.fit_predict(X_scaled)

df['cluster_hier'] = clusters_hier

# 评估
print("层次聚类轮廓系数:", silhouette_score(X_scaled, clusters_hier))

# 可视化
plt.figure(figsize=(10, 6))
plt.scatter(
    df['annual_income'], 
    df['spending_score'],
    c=clusters_hier, 
    cmap='viridis',
    alpha=0.6
)
plt.xlabel('Annual Income')
plt.ylabel('Spending Score')
plt.title('Hierarchical Clustering')
plt.colorbar(label='Cluster')
plt.savefig('hierarchical_result.png')
```

**层次聚类特点**：
- 不需要预先指定簇数（可从树状图选择）
- 可视化层次结构
- 计算复杂度高 O(n³)
- 适合小数据集

---

## 4. DBSCAN 密度聚类

```python
from sklearn.cluster import DBSCAN

# DBSCAN 聚类
dbscan = DBSCAN(eps=0.5, min_samples=5)
clusters_dbscan = dbscan.fit_predict(X_scaled)

df['cluster_dbscan'] = clusters_dbscan

# 统计
n_clusters = len(set(clusters_dbscan)) - (1 if -1 in clusters_dbscan else 0)
n_noise = list(clusters_dbscan).count(-1)

print(f"聚类数量: {n_clusters}")
print(f"噪声点数量: {n_noise}")
print(f"各簇样本数: {pd.Series(clusters_dbscan).value_counts().sort_index()}")

# 评估（排除噪声点）
mask = clusters_dbscan != -1
if mask.sum() > 0 and len(set(clusters_dbscan[mask])) > 1:
    score = silhouette_score(X_scaled[mask], clusters_dbscan[mask])
    print(f"轮廓系数（排除噪声）: {score:.4f}")

# 可视化
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    df['annual_income'], 
    df['spending_score'],
    c=clusters_dbscan, 
    cmap='viridis',
    alpha=0.6
)
plt.xlabel('Annual Income')
plt.ylabel('Spending Score')
plt.title(f'DBSCAN Clustering (eps=0.5, min_samples=5)')
plt.colorbar(scatter, label='Cluster (-1 = Noise)')
plt.savefig('dbscan_result.png')
```

### DBSCAN 参数选择

```python
from sklearn.neighbors import NearestNeighbors

# 使用 k-距离图选择 eps
k = 5
neigh = NearestNeighbors(n_neighbors=k)
neigh.fit(X_scaled)
distances, indices = neigh.kneighbors(X_scaled)

# 排序距离
distances = np.sort(distances[:, k-1])

plt.figure(figsize=(10, 5))
plt.plot(distances)
plt.xlabel('Points sorted by distance')
plt.ylabel(f'{k}-th Nearest Neighbor Distance')
plt.title('K-Distance Graph (for eps selection)')
plt.savefig('k_distance.png')
```

**DBSCAN 特点**：
- 不需要预先指定簇数
- 能发现任意形状的簇
- 能识别噪声点
- 对参数敏感（eps, min_samples）

---

## 5. PCA 降维可视化

```python
from sklearn.decomposition import PCA

# PCA 降维到 2D
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"解释方差比例: {pca.explained_variance_ratio_}")
print(f"累计解释方差: {pca.explained_variance_ratio_.sum():.4f}")

# 可视化
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, (clusters, title) in zip(axes, [
    (clusters_kmeans, 'K-Means'),
    (clusters_hier, 'Hierarchical'),
    (clusters_dbscan, 'DBSCAN')
]):
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis', alpha=0.6)
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_title(f'{title} (PCA Visualization)')
    plt.colorbar(scatter, ax=ax)

plt.tight_layout()
plt.savefig('pca_comparison.png')
```

---

## 6. 聚类评估指标

```python
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

def evaluate_clustering(X, labels, name):
    """评估聚类效果"""
    # 过滤噪声点
    mask = labels != -1
    if mask.sum() == 0 or len(set(labels[mask])) < 2:
        print(f"{name}: 无法评估（簇数不足或全为噪声）")
        return
    
    X_clean = X[mask]
    labels_clean = labels[mask]
    
    silhouette = silhouette_score(X_clean, labels_clean)
    ch_score = calinski_harabasz_score(X_clean, labels_clean)
    db_score = davies_bouldin_score(X_clean, labels_clean)
    
    print(f"{name}:")
    print(f"  轮廓系数 (越大越好): {silhouette:.4f}")
    print(f"  CH 指数 (越大越好): {ch_score:.4f}")
    print(f"  DB 指数 (越小越好): {db_score:.4f}")

print("=== 聚类评估 ===")
evaluate_clustering(X_scaled, clusters_kmeans, "K-Means")
evaluate_clustering(X_scaled, clusters_hier, "Hierarchical")
evaluate_clustering(X_scaled, clusters_dbscan, "DBSCAN")
```

### 指标说明

| 指标 | 说明 | 范围 | 最优 |
|------|------|------|------|
| 轮廓系数 | 衡量簇内紧密度和簇间分离度 | [-1, 1] | 越大越好 |
| CH 指数 | 簇间离散度 / 簇内离散度 | [0, +∞) | 越大越好 |
| DB 指数 | 簇内距离 / 簇间距离 的最大值 | [0, +∞) | 越小越好 |

---

## 7. 客户分群解读

```python
# 给每个簇命名（基于 K-Means 结果）
df['cluster_kmeans'] = clusters_kmeans

# 分析各簇特征
cluster_profile = df.groupby('cluster_kmeans').agg({
    'annual_income': ['mean', 'std'],
    'spending_score': ['mean', 'std'],
    'age': ['mean', 'std'],
    'purchase_frequency': ['mean', 'std'],
    'avg_order_value': ['mean', 'std']
}).round(2)

print("各客户群画像:")
print(cluster_profile)

# 客户分群命名（示例）
cluster_names = {
    0: '高收入高消费',
    1: '低收入高消费',
    2: '高收入低消费',
    3: '低收入低消费'
}

df['customer_segment'] = df['cluster_kmeans'].map(cluster_names)
print("\n客户分群分布:")
print(df['customer_segment'].value_counts())
```

---

## 8. 模型对比总结

```python
# 对比表
comparison = pd.DataFrame({
    '算法': ['K-Means', '层次聚类', 'DBSCAN'],
    '需要指定簇数': ['是', '是/否', '否'],
    '簇形状': ['球形', '任意', '任意'],
    '处理噪声': ['否', '否', '是'],
    '时间复杂度': ['O(n·k·i)', 'O(n²)~O(n³)', 'O(n·log n)'],
    '适用场景': ['大数据、球形簇', '小数据、层次结构', '任意形状、有噪声']
})
print(comparison)
```

---

## 验证步骤

1. **数据预处理**：标准化特征
2. **K 值选择**：使用肘部法则和轮廓系数
3. **运行聚类**：K-Means、层次聚类、DBSCAN
4. **评估对比**：轮廓系数、CH 指数
5. **可视化**：PCA 降维展示
6. **业务解读**：分析各簇特征，命名客户群

---

## 常见问题

### Q1: 如何选择聚类算法？
- 数据量大、簇形状球形：K-Means
- 需要层次结构、小数据：层次聚类
- 有噪声、任意形状：DBSCAN

### Q2: K-Means 结果不稳定？
- 设置 `n_init` 多次初始化
- 使用 `random_state` 固定随机种子
- 尝试 K-Means++ 初始化（默认）

### Q3: DBSCAN 全是噪声？
- eps 太小，增大 eps
- 使用 k-距离图选择合适的 eps
- 减小 min_samples
