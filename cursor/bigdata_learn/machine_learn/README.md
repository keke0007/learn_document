# 机器学习学习模块

## 概述

机器学习（Machine Learning）是人工智能的核心技术，使计算机能够从数据中自动学习规律。本模块基于 scikit-learn 框架，涵盖监督学习、无监督学习、特征工程和模型评估。

---

## 知识点与案例映射

| 知识点 | 说明 | 案例 | 数据/脚本 |
|--------|------|------|-----------|
| **监督学习概念** | 有标签数据的学习 | `cases/supervised_classification.md` | - |
| **逻辑回归** | 线性分类器，输出概率 | `cases/supervised_classification.md` | `scripts/classification_example.py` |
| **决策树** | 树结构分类/回归 | `cases/supervised_classification.md` | `scripts/classification_example.py` |
| **随机森林** | 决策树集成，抗过拟合 | `cases/supervised_classification.md` | `scripts/classification_example.py` |
| **XGBoost** | 梯度提升，竞赛常用 | `cases/supervised_classification.md` | `scripts/classification_example.py` |
| **线性回归** | 连续值预测基础 | `cases/supervised_regression.md` | `scripts/regression_example.py` |
| **岭回归/Lasso** | 正则化回归 | `cases/supervised_regression.md` | `scripts/regression_example.py` |
| **K-Means** | 划分式聚类 | `cases/unsupervised_clustering.md` | `scripts/clustering_example.py` |
| **层次聚类** | 树状聚类结构 | `cases/unsupervised_clustering.md` | `scripts/clustering_example.py` |
| **DBSCAN** | 密度聚类，发现任意形状 | `cases/unsupervised_clustering.md` | `scripts/clustering_example.py` |
| **PCA** | 主成分分析降维 | `cases/unsupervised_clustering.md` | `scripts/clustering_example.py` |
| **特征缩放** | StandardScaler, MinMaxScaler | `cases/feature_engineering.md` | - |
| **特征编码** | OneHot, LabelEncoder | `cases/feature_engineering.md` | - |
| **缺失值处理** | SimpleImputer | `cases/feature_engineering.md` | - |
| **特征选择** | 过滤/包装/嵌入法 | `cases/feature_engineering.md` | - |
| **交叉验证** | K-Fold, StratifiedKFold | 所有案例 | - |
| **网格搜索** | GridSearchCV 超参调优 | 所有案例 | - |
| **分类评估** | 准确率/精确率/召回率/F1/AUC | `cases/supervised_classification.md` | - |
| **回归评估** | MSE/RMSE/MAE/R² | `cases/supervised_regression.md` | - |
| **聚类评估** | 轮廓系数/CH指数 | `cases/unsupervised_clustering.md` | - |

---

## 学习路径

```
基础概念 → 监督学习 → 无监督学习 → 特征工程 → 模型优化
    ↓          ↓           ↓           ↓          ↓
  定义/分类  分类/回归    聚类/降维   预处理    调参/评估
```

---

## 算法选择指南

```
                    ┌─ 分类 ─┬─ 二分类 ─→ 逻辑回归/SVM/XGBoost
                    │        └─ 多分类 ─→ 随机森林/XGBoost
        ┌─ 监督 ───┤
        │          └─ 回归 ───────────→ 线性回归/随机森林/XGBoost
问题 ───┤
        │          ┌─ 聚类 ─────────→ K-Means/DBSCAN
        └─ 无监督 ─┤
                   └─ 降维 ─────────→ PCA/t-SNE
```

---

## 快速验证

### 1. 安装

```bash
pip install numpy pandas scikit-learn matplotlib xgboost
```

### 2. 分类示例

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier().fit(X_train, y_train)
print(f"准确率: {accuracy_score(y_test, model.predict(X_test)):.4f}")
```

### 3. 回归示例

```python
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

X, y = fetch_california_housing(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression().fit(X_train, y_train)
print(f"R²: {r2_score(y_test, model.predict(X_test)):.4f}")
```

---

## 相关资源

- [scikit-learn 官方文档](https://scikit-learn.org/)
- [Kaggle 竞赛平台](https://www.kaggle.com/)
- [机器学习实战（书籍）](https://github.com/ageron/handson-ml3)
- [StatQuest 视频教程](https://www.youtube.com/c/joshstarmer)
