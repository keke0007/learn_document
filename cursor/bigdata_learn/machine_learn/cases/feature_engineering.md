# 案例：特征工程

## 目标

掌握机器学习中常用的特征工程技术，包括缺失值处理、特征编码、特征缩放、特征选择和特征构造。

---

## 知识点覆盖

- 缺失值处理（SimpleImputer）
- 特征编码（Label Encoding、One-Hot Encoding）
- 特征缩放（StandardScaler、MinMaxScaler）
- 特征选择（过滤法、包装法、嵌入法）
- 特征构造
- Pipeline 流水线

---

## 1. 缺失值处理

### 查看缺失值

```python
import pandas as pd
import numpy as np

# 示例数据
df = pd.DataFrame({
    'age': [25, 30, np.nan, 35, 40],
    'income': [50000, np.nan, 70000, np.nan, 90000],
    'city': ['Beijing', 'Shanghai', np.nan, 'Guangzhou', 'Beijing'],
    'target': [0, 1, 0, 1, 1]
})

# 查看缺失值
print("缺失值统计:")
print(df.isnull().sum())
print(f"\n缺失值比例:\n{df.isnull().mean() * 100}")
```

### 删除法

```python
# 删除包含缺失值的行
df_dropna = df.dropna()

# 删除缺失值超过阈值的列
threshold = 0.5
df_drop_cols = df.dropna(thresh=int(len(df) * (1 - threshold)), axis=1)
```

### 填充法

```python
from sklearn.impute import SimpleImputer

# 数值型：均值/中位数/众数填充
num_imputer = SimpleImputer(strategy='mean')  # 'median', 'most_frequent'
df['age_filled'] = num_imputer.fit_transform(df[['age']])

# 类别型：众数/常量填充
cat_imputer = SimpleImputer(strategy='most_frequent')
df['city_filled'] = cat_imputer.fit_transform(df[['city']]).ravel()

# 常量填充
const_imputer = SimpleImputer(strategy='constant', fill_value='Unknown')
df['city_const'] = const_imputer.fit_transform(df[['city']]).ravel()
```

### KNN 填充

```python
from sklearn.impute import KNNImputer

# KNN 填充（仅数值型）
knn_imputer = KNNImputer(n_neighbors=3)
df_numeric = df[['age', 'income']].copy()
df_knn_filled = pd.DataFrame(
    knn_imputer.fit_transform(df_numeric),
    columns=df_numeric.columns
)
print(df_knn_filled)
```

---

## 2. 特征编码

### Label Encoding（有序类别）

```python
from sklearn.preprocessing import LabelEncoder

# 有序类别
education = ['高中', '本科', '硕士', '博士', '本科', '高中']

le = LabelEncoder()
education_encoded = le.fit_transform(education)
print(f"编码结果: {education_encoded}")
print(f"类别映射: {dict(zip(le.classes_, range(len(le.classes_))))}")

# 反向转换
print(f"反向转换: {le.inverse_transform(education_encoded)}")
```

### One-Hot Encoding（无序类别）

```python
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

# 无序类别
cities = [['Beijing'], ['Shanghai'], ['Guangzhou'], ['Beijing'], ['Shanghai']]

# sklearn OneHotEncoder
ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
cities_encoded = ohe.fit_transform(cities)
print(f"One-Hot 编码:\n{cities_encoded}")
print(f"特征名: {ohe.get_feature_names_out()}")

# pandas get_dummies（更方便）
df_cities = pd.DataFrame({'city': ['Beijing', 'Shanghai', 'Guangzhou', 'Beijing']})
df_dummies = pd.get_dummies(df_cities, prefix='city', drop_first=False)
print(f"\npandas get_dummies:\n{df_dummies}")
```

### Target Encoding（高基数类别）

```python
# 手动实现 Target Encoding
def target_encoding(df, col, target, smoothing=1):
    """目标编码"""
    global_mean = df[target].mean()
    agg = df.groupby(col)[target].agg(['mean', 'count'])
    
    # 平滑处理
    smooth = (agg['mean'] * agg['count'] + global_mean * smoothing) / (agg['count'] + smoothing)
    return df[col].map(smooth)

# 示例
df['city_target_encoded'] = target_encoding(df, 'city', 'target')
```

---

## 3. 特征缩放

### StandardScaler（标准化）

```python
from sklearn.preprocessing import StandardScaler

# 标准化：均值0，标准差1
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"均值: {X_scaled.mean(axis=0)}")
print(f"标准差: {X_scaled.std(axis=0)}")

# 反向转换
X_original = scaler.inverse_transform(X_scaled)
```

**适用场景**：
- 特征近似正态分布
- 对异常值不太敏感
- SVM、逻辑回归、神经网络

### MinMaxScaler（归一化）

```python
from sklearn.preprocessing import MinMaxScaler

# 归一化：缩放到 [0, 1]
minmax_scaler = MinMaxScaler()
X_minmax = minmax_scaler.fit_transform(X)

print(f"最小值: {X_minmax.min(axis=0)}")
print(f"最大值: {X_minmax.max(axis=0)}")
```

**适用场景**：
- 需要有界范围
- 图像像素处理
- KNN、神经网络

### RobustScaler（鲁棒缩放）

```python
from sklearn.preprocessing import RobustScaler

# 使用中位数和四分位数，对异常值鲁棒
robust_scaler = RobustScaler()
X_robust = robust_scaler.fit_transform(X)
```

**适用场景**：
- 数据有异常值
- 分布偏斜

### 对比

| 方法 | 公式 | 特点 |
|------|------|------|
| StandardScaler | (x-μ)/σ | 均值0，标准差1 |
| MinMaxScaler | (x-min)/(max-min) | 缩放到[0,1] |
| RobustScaler | (x-Q2)/(Q3-Q1) | 使用中位数，鲁棒 |

---

## 4. 特征选择

### 过滤法（Filter）

```python
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.feature_selection import VarianceThreshold

# 方差阈值（去除低方差特征）
var_selector = VarianceThreshold(threshold=0.1)
X_var = var_selector.fit_transform(X)
print(f"保留特征数: {X_var.shape[1]}")

# 单变量统计检验（分类）
selector = SelectKBest(score_func=f_classif, k=5)
X_selected = selector.fit_transform(X, y)

# 查看分数
scores = pd.DataFrame({
    'feature': feature_names,
    'score': selector.scores_
}).sort_values('score', ascending=False)
print(scores)

# 互信息
mi_selector = SelectKBest(score_func=mutual_info_classif, k=5)
X_mi = mi_selector.fit_transform(X, y)
```

### 包装法（Wrapper）

```python
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier

# 递归特征消除 (RFE)
estimator = RandomForestClassifier(n_estimators=50, random_state=42)
rfe = RFE(estimator, n_features_to_select=5, step=1)
rfe.fit(X, y)

# 查看选择的特征
selected_features = [f for f, s in zip(feature_names, rfe.support_) if s]
print(f"RFE 选择的特征: {selected_features}")
print(f"特征排名: {dict(zip(feature_names, rfe.ranking_))}")
```

### 嵌入法（Embedded）

```python
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestClassifier

# Lasso L1 正则化
lasso = Lasso(alpha=0.1)
lasso.fit(X, y)
print(f"Lasso 系数: {dict(zip(feature_names, lasso.coef_))}")

# 基于模型的特征选择
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

# 选择重要性高于均值的特征
selector = SelectFromModel(rf, threshold='mean', prefit=True)
X_selected = selector.transform(X)
print(f"选择的特征数: {X_selected.shape[1]}")

# 特征重要性
importance = pd.DataFrame({
    'feature': feature_names,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
print(importance)
```

---

## 5. 特征构造

### 数值特征

```python
# 多项式特征
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
print(f"特征名: {poly.get_feature_names_out()}")

# 手动构造
df['income_per_age'] = df['income'] / df['age']
df['income_squared'] = df['income'] ** 2
df['income_log'] = np.log1p(df['income'])
```

### 时间特征

```python
# 从日期提取特征
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['dayofweek'] = df['date'].dt.dayofweek
df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
df['quarter'] = df['date'].dt.quarter
df['hour'] = df['date'].dt.hour
```

### 分箱（Binning）

```python
from sklearn.preprocessing import KBinsDiscretizer

# 等宽分箱
binner = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='uniform')
df['age_binned'] = binner.fit_transform(df[['age']])

# 等频分箱
binner_quantile = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='quantile')
df['income_binned'] = binner_quantile.fit_transform(df[['income']])

# 手动分箱
df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 100], labels=['青年', '中青年', '中年', '老年'])
```

---

## 6. Pipeline 流水线

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# 定义数值和类别特征
numeric_features = ['age', 'income', 'tenure']
categorical_features = ['city', 'gender']

# 数值特征处理
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# 类别特征处理
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# 组合预处理器
preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# 完整流水线
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# 训练
pipeline.fit(X_train, y_train)

# 预测
y_pred = pipeline.predict(X_test)
print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")

# 保存模型
import joblib
joblib.dump(pipeline, 'model_pipeline.pkl')

# 加载模型
loaded_pipeline = joblib.load('model_pipeline.pkl')
```

---

## 7. 完整特征工程流程

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. 加载数据
df = pd.read_csv('data.csv')

# 2. 划分特征和标签
X = df.drop('target', axis=1)
y = df['target']

# 3. 识别特征类型
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = X.select_dtypes(include=['object']).columns.tolist()

# 4. 构建预处理器
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# 5. 构建完整流水线
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('feature_selection', SelectFromModel(RandomForestClassifier(n_estimators=50))),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# 6. 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. 训练
pipeline.fit(X_train, y_train)

# 8. 评估
y_pred = pipeline.predict(X_test)
print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
```

---

## 验证步骤

1. **缺失值检查**：统计各列缺失值比例
2. **编码验证**：检查编码后的特征是否正确
3. **缩放验证**：检查缩放后的均值和方差
4. **特征选择**：对比选择前后模型性能
5. **Pipeline 测试**：验证流水线端到端工作

---

## 常见问题

### Q1: 先划分数据还是先预处理？
先划分数据，防止数据泄露。预处理器应在训练集上 fit，在测试集上 transform。

### Q2: 高基数类别特征怎么处理？
- Target Encoding
- Frequency Encoding
- 特征哈希
- 降维或分组

### Q3: 特征太多怎么办？
- 特征选择（过滤/包装/嵌入）
- PCA 降维
- L1 正则化（Lasso）
