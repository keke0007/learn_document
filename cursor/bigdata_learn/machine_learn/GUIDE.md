# 机器学习（Machine Learning）学习指南

## 一、项目简介

机器学习是人工智能的核心分支，使计算机能够从数据中学习规律并做出预测或决策。本模块涵盖机器学习核心概念、经典算法、特征工程、模型评估和实战案例，基于 scikit-learn 框架进行实践。

---

## 二、目录结构

```
machine_learn/
├── GUIDE.md                        # 本指南文档
├── README.md                       # 知识点与案例总览
├── cases/
│   ├── supervised_classification.md    # 监督学习-分类案例
│   ├── supervised_regression.md        # 监督学习-回归案例
│   ├── unsupervised_clustering.md      # 无监督学习-聚类案例
│   └── feature_engineering.md          # 特征工程案例
├── data/
│   ├── classification_data.csv         # 分类数据集
│   ├── regression_data.csv             # 回归数据集
│   └── clustering_data.csv             # 聚类数据集
└── scripts/
    ├── setup_env.md                    # 环境搭建说明
    ├── classification_example.py       # 分类示例代码
    ├── regression_example.py           # 回归示例代码
    └── clustering_example.py           # 聚类示例代码
```

---

## 三、学习路线

### 第一阶段：基础概念
- 机器学习定义与分类（监督/无监督/强化学习）
- 训练集、验证集、测试集划分
- 欠拟合与过拟合
- 偏差-方差权衡（Bias-Variance Tradeoff）

### 第二阶段：监督学习算法
- **回归算法**：线性回归、多项式回归、岭回归、Lasso
- **分类算法**：逻辑回归、KNN、朴素贝叶斯、SVM、决策树
- **集成学习**：随机森林、Bagging、Boosting、XGBoost、LightGBM

### 第三阶段：无监督学习算法
- **聚类**：K-Means、层次聚类、DBSCAN
- **降维**：PCA、t-SNE、LDA
- **关联规则**：Apriori

### 第四阶段：特征工程与模型优化
- 特征选择（过滤法、包装法、嵌入法）
- 特征缩放（标准化、归一化）
- 特征编码（One-Hot、Label Encoding）
- 超参数调优（GridSearchCV、RandomizedSearchCV）
- 交叉验证（K-Fold、分层K-Fold）

### 第五阶段：模型评估
- 分类指标：准确率、精确率、召回率、F1、AUC-ROC
- 回归指标：MSE、RMSE、MAE、R²
- 聚类指标：轮廓系数、Calinski-Harabasz

---

## 四、快速开始

### 4.1 环境准备

```bash
# 创建虚拟环境
python -m venv ml_env
source ml_env/bin/activate  # Linux/Mac
# ml_env\Scripts\activate   # Windows

# 安装核心包
pip install numpy pandas scikit-learn matplotlib seaborn

# 安装扩展包
pip install xgboost lightgbm catboost
pip install jupyter notebook
```

### 4.2 第一个分类模型

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. 加载数据
iris = load_iris()
X, y = iris.data, iris.target

# 2. 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. 训练模型
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. 预测与评估
y_pred = model.predict(X_test)
print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred, target_names=iris.target_names))
```

### 4.3 第一个回归模型

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# 1. 加载数据
housing = fetch_california_housing()
X, y = housing.data, housing.target

# 2. 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. 训练模型
model = LinearRegression()
model.fit(X_train, y_train)

# 4. 预测与评估
y_pred = model.predict(X_test)
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
print(f"R²: {r2_score(y_test, y_pred):.4f}")
```

---

## 五、核心知识速查

### 5.1 学习类型

| 类型 | 说明 | 典型任务 |
|------|------|----------|
| **监督学习** | 有标签数据，学习输入到输出的映射 | 分类、回归 |
| **无监督学习** | 无标签数据，发现数据内在结构 | 聚类、降维 |
| **半监督学习** | 少量标签+大量无标签 | 标签传播 |
| **强化学习** | 智能体与环境交互获取奖励 | 游戏、机器人 |

### 5.2 常用算法速查

| 算法 | 类型 | 适用场景 | sklearn 类 |
|------|------|----------|------------|
| 线性回归 | 回归 | 连续值预测 | `LinearRegression` |
| 逻辑回归 | 分类 | 二分类/多分类 | `LogisticRegression` |
| KNN | 分类/回归 | 小数据集 | `KNeighborsClassifier` |
| 决策树 | 分类/回归 | 可解释性要求高 | `DecisionTreeClassifier` |
| 随机森林 | 分类/回归 | 通用、抗过拟合 | `RandomForestClassifier` |
| SVM | 分类 | 高维数据 | `SVC` |
| 朴素贝叶斯 | 分类 | 文本分类 | `GaussianNB` |
| K-Means | 聚类 | 球形簇 | `KMeans` |
| DBSCAN | 聚类 | 任意形状簇 | `DBSCAN` |
| PCA | 降维 | 特征压缩 | `PCA` |
| XGBoost | 分类/回归 | 竞赛/生产 | `XGBClassifier` |

### 5.3 评估指标

**分类指标**：
```python
from sklearn.metrics import (
    accuracy_score,     # 准确率
    precision_score,    # 精确率
    recall_score,       # 召回率
    f1_score,           # F1 分数
    roc_auc_score,      # AUC
    confusion_matrix,   # 混淆矩阵
    classification_report
)
```

**回归指标**：
```python
from sklearn.metrics import (
    mean_squared_error,     # MSE
    mean_absolute_error,    # MAE
    r2_score,               # R² 决定系数
    mean_absolute_percentage_error  # MAPE
)
```

### 5.4 数据预处理

```python
from sklearn.preprocessing import (
    StandardScaler,      # 标准化 (mean=0, std=1)
    MinMaxScaler,        # 归一化 [0, 1]
    LabelEncoder,        # 标签编码
    OneHotEncoder,       # 独热编码
)
from sklearn.impute import SimpleImputer  # 缺失值填充

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### 5.5 模型选择与调优

```python
from sklearn.model_selection import (
    train_test_split,       # 数据划分
    cross_val_score,        # 交叉验证
    GridSearchCV,           # 网格搜索
    RandomizedSearchCV,     # 随机搜索
    StratifiedKFold         # 分层 K-Fold
)

# 网格搜索
param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [3, 5, 7]}
grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
grid_search.fit(X_train, y_train)
print(f"最佳参数: {grid_search.best_params_}")
```

---

## 六、数据说明

| 文件 | 说明 | 任务类型 |
|------|------|----------|
| `data/classification_data.csv` | 客户分类数据集 | 二分类 |
| `data/regression_data.csv` | 房价预测数据集 | 回归 |
| `data/clustering_data.csv` | 客户分群数据集 | 聚类 |

---

## 七、案例总览

| 案例 | 知识点 | 文件 |
|------|--------|------|
| 监督学习-分类 | 逻辑回归、决策树、随机森林、XGBoost | `cases/supervised_classification.md` |
| 监督学习-回归 | 线性回归、岭回归、随机森林回归 | `cases/supervised_regression.md` |
| 无监督学习-聚类 | K-Means、层次聚类、DBSCAN | `cases/unsupervised_clustering.md` |
| 特征工程 | 缺失值、编码、缩放、特征选择 | `cases/feature_engineering.md` |

---

## 八、学习建议

1. **数学基础**：线性代数、概率统计、微积分基础
2. **先实践后理论**：先跑通代码，再深入理解原理
3. **从简单到复杂**：线性模型 → 树模型 → 集成模型
4. **重视特征工程**：特征工程往往比模型选择更重要
5. **多做项目**：Kaggle 竞赛是最好的实战练习

---

## 九、学习检查清单

- [ ] 理解监督学习、无监督学习、强化学习的区别
- [ ] 掌握 train_test_split 和交叉验证
- [ ] 能使用逻辑回归、决策树、随机森林进行分类
- [ ] 能使用线性回归、随机森林进行回归预测
- [ ] 理解过拟合/欠拟合，能使用正则化缓解
- [ ] 掌握 K-Means 聚类和 PCA 降维
- [ ] 能进行特征缩放、编码、缺失值处理
- [ ] 能使用 GridSearchCV 进行超参数调优
- [ ] 理解并能计算准确率、精确率、召回率、F1、AUC
- [ ] 能使用 XGBoost/LightGBM 训练模型

---

## 十、学习成果

完成本模块后，你将能够：

1. 根据业务问题选择合适的机器学习算法
2. 完成数据预处理和特征工程流程
3. 使用 scikit-learn 训练和评估模型
4. 使用交叉验证和网格搜索优化模型
5. 解读模型评估指标，分析模型性能
6. 使用 XGBoost/LightGBM 处理结构化数据
7. 具备参加 Kaggle 竞赛的基础能力
