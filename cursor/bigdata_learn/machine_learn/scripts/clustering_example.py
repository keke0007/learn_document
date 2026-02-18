"""
机器学习聚类示例代码
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def load_data():
    """加载数据"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "clustering_data.csv")
    df = pd.read_csv(data_path)
    print("数据概览:")
    print(df.head())
    print(f"\n数据形状: {df.shape}")
    print(f"\n数据统计:\n{df.describe()}")
    return df


def preprocess_data(df):
    """数据预处理"""
    X = df.values
    
    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X, X_scaled, df.columns


def find_optimal_k(X_scaled, k_range=range(2, 11)):
    """使用肘部法则和轮廓系数找最优 K"""
    print("\n" + "=" * 50)
    print("寻找最优 K 值")
    print("=" * 50)
    
    inertias = []
    silhouette_scores = []
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        
        labels = kmeans.labels_
        score = silhouette_score(X_scaled, labels)
        silhouette_scores.append(score)
        print(f"K={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={score:.4f}")
    
    # 找轮廓系数最大的 K
    best_k = list(k_range)[np.argmax(silhouette_scores)]
    print(f"\n推荐 K 值（轮廓系数最大）: {best_k}")
    
    return inertias, silhouette_scores, best_k


def train_kmeans(X_scaled, n_clusters, feature_names):
    """K-Means 聚类"""
    print("\n" + "=" * 50)
    print(f"K-Means 聚类 (K={n_clusters})")
    print("=" * 50)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    
    # 评估
    silhouette = silhouette_score(X_scaled, labels)
    ch_score = calinski_harabasz_score(X_scaled, labels)
    db_score = davies_bouldin_score(X_scaled, labels)
    
    print(f"轮廓系数: {silhouette:.4f}")
    print(f"CH 指数: {ch_score:.2f}")
    print(f"DB 指数: {db_score:.4f}")
    
    # 各簇样本数
    unique, counts = np.unique(labels, return_counts=True)
    print(f"\n各簇样本数: {dict(zip(unique, counts))}")
    
    return labels, kmeans


def train_hierarchical(X_scaled, n_clusters):
    """层次聚类"""
    print("\n" + "=" * 50)
    print(f"层次聚类 (n_clusters={n_clusters})")
    print("=" * 50)
    
    hierarchical = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    labels = hierarchical.fit_predict(X_scaled)
    
    # 评估
    silhouette = silhouette_score(X_scaled, labels)
    print(f"轮廓系数: {silhouette:.4f}")
    
    # 各簇样本数
    unique, counts = np.unique(labels, return_counts=True)
    print(f"各簇样本数: {dict(zip(unique, counts))}")
    
    return labels


def train_dbscan(X_scaled, eps=0.5, min_samples=5):
    """DBSCAN 密度聚类"""
    print("\n" + "=" * 50)
    print(f"DBSCAN 聚类 (eps={eps}, min_samples={min_samples})")
    print("=" * 50)
    
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X_scaled)
    
    # 统计
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    
    print(f"聚类数量: {n_clusters}")
    print(f"噪声点数量: {n_noise}")
    
    # 各簇样本数
    unique, counts = np.unique(labels, return_counts=True)
    print(f"各簇样本数: {dict(zip(unique, counts))}")
    
    # 评估（排除噪声点）
    mask = labels != -1
    if mask.sum() > 0 and len(set(labels[mask])) > 1:
        silhouette = silhouette_score(X_scaled[mask], labels[mask])
        print(f"轮廓系数（排除噪声）: {silhouette:.4f}")
    
    return labels


def analyze_clusters(df, labels, algorithm_name):
    """分析聚类结果"""
    print(f"\n=== {algorithm_name} 聚类分析 ===")
    
    df_with_cluster = df.copy()
    df_with_cluster['cluster'] = labels
    
    # 各簇特征均值
    cluster_profile = df_with_cluster.groupby('cluster').mean()
    print("\n各簇特征均值:")
    print(cluster_profile.round(2))
    
    return df_with_cluster


def pca_visualization(X_scaled, labels_dict):
    """PCA 降维可视化"""
    print("\n" + "=" * 50)
    print("PCA 降维可视化")
    print("=" * 50)
    
    # PCA 降维
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    print(f"解释方差比例: {pca.explained_variance_ratio_}")
    print(f"累计解释方差: {pca.explained_variance_ratio_.sum():.4f}")
    
    # 可视化
    n_plots = len(labels_dict)
    fig, axes = plt.subplots(1, n_plots, figsize=(6*n_plots, 5))
    
    if n_plots == 1:
        axes = [axes]
    
    for ax, (name, labels) in zip(axes, labels_dict.items()):
        scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='viridis', alpha=0.6)
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_title(f'{name} (PCA)')
        plt.colorbar(scatter, ax=ax)
    
    plt.tight_layout()
    plt.savefig('clustering_comparison.png')
    print("可视化图已保存到: clustering_comparison.png")
    plt.show()


def plot_elbow_silhouette(k_range, inertias, silhouette_scores, save_path=None):
    """绘制肘部曲线和轮廓系数曲线"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # 肘部曲线
    axes[0].plot(list(k_range), inertias, 'bo-')
    axes[0].set_xlabel('K')
    axes[0].set_ylabel('Inertia')
    axes[0].set_title('Elbow Method')
    
    # 轮廓系数
    axes[1].plot(list(k_range), silhouette_scores, 'go-')
    axes[1].set_xlabel('K')
    axes[1].set_ylabel('Silhouette Score')
    axes[1].set_title('Silhouette Score vs K')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"图已保存到: {save_path}")
    plt.show()


def main():
    """主函数"""
    print("=" * 60)
    print("机器学习聚类示例")
    print("=" * 60)
    
    # 1. 加载数据
    df = load_data()
    
    # 2. 数据预处理
    X, X_scaled, feature_names = preprocess_data(df)
    
    # 3. 找最优 K
    inertias, silhouette_scores, best_k = find_optimal_k(X_scaled)
    
    # 4. K-Means 聚类
    kmeans_labels, kmeans_model = train_kmeans(X_scaled, best_k, feature_names)
    
    # 5. 层次聚类
    hier_labels = train_hierarchical(X_scaled, best_k)
    
    # 6. DBSCAN 聚类
    dbscan_labels = train_dbscan(X_scaled, eps=0.8, min_samples=3)
    
    # 7. 聚类分析
    df_kmeans = analyze_clusters(df, kmeans_labels, "K-Means")
    
    # 8. 算法对比
    print("\n" + "=" * 50)
    print("算法对比")
    print("=" * 50)
    
    results = []
    for name, labels in [('K-Means', kmeans_labels), ('Hierarchical', hier_labels)]:
        silhouette = silhouette_score(X_scaled, labels)
        ch = calinski_harabasz_score(X_scaled, labels)
        db = davies_bouldin_score(X_scaled, labels)
        results.append({
            'Algorithm': name,
            'Silhouette': silhouette,
            'CH Index': ch,
            'DB Index': db
        })
    
    # DBSCAN（排除噪声）
    mask = dbscan_labels != -1
    if mask.sum() > 0 and len(set(dbscan_labels[mask])) > 1:
        silhouette = silhouette_score(X_scaled[mask], dbscan_labels[mask])
        ch = calinski_harabasz_score(X_scaled[mask], dbscan_labels[mask])
        db = davies_bouldin_score(X_scaled[mask], dbscan_labels[mask])
        results.append({
            'Algorithm': 'DBSCAN',
            'Silhouette': silhouette,
            'CH Index': ch,
            'DB Index': db
        })
    
    results_df = pd.DataFrame(results)
    print(results_df)
    
    # 9. PCA 可视化
    labels_dict = {
        'K-Means': kmeans_labels,
        'Hierarchical': hier_labels,
        'DBSCAN': dbscan_labels
    }
    pca_visualization(X_scaled, labels_dict)
    
    print("\n" + "=" * 60)
    print("聚类示例执行完成！")


if __name__ == "__main__":
    main()
