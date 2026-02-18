# 案例：监督学习 - 回归

## 目标

掌握常用回归算法的使用，包括线性回归、岭回归、Lasso、随机森林回归，以及回归模型的评估方法。

---

## 知识点覆盖

- 线性回归（Linear Regression）
- 岭回归（Ridge Regression）
- Lasso 回归
- 随机森林回归（Random Forest Regressor）
- XGBoost 回归
- 回归评估指标（MSE、RMSE、MAE、R²）

---

## 场景描述

**业务场景**：房价预测

根据房屋的面积、房间数、地理位置等特征，预测房屋价格（连续值预测）。

**数据特征**：
- `area`: 房屋面积（平方米）
- `rooms`: 房间数
- `bathrooms`: 卫生间数
- `age`: 房龄（年）
- `distance_to_center`: 到市中心距离（公里）
- `floor`: 楼层
- `price`: 房价（目标变量）

---

## 1. 数据准备

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
df = pd.read_csv('data/regression_data.csv')

# 探索性分析
print(df.describe())
print(df.corr()['price'].sort_values(ascending=False))

# 可视化
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('correlation_matrix.png')

# 特征和标签
X = df.drop('price', axis=1)
y = df['price']

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 特征缩放
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

---

## 2. 线性回归

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

# 训练模型
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

# 预测
y_pred_lr = lr_model.predict(X_test_scaled)

# 评估
print("=== 线性回归 ===")
print(f"MSE: {mean_squared_error(y_test, y_pred_lr):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_lr)):.4f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred_lr):.4f}")
print(f"R²: {r2_score(y_test, y_pred_lr):.4f}")

# 系数分析
coef_df = pd.DataFrame({
    'feature': X.columns,
    'coefficient': lr_model.coef_
}).sort_values('coefficient', key=abs, ascending=False)
print("\n系数:")
print(coef_df)
print(f"\n截距: {lr_model.intercept_:.4f}")
```

**线性回归特点**：
- 最简单的回归方法
- 假设特征与目标线性关系
- 容易受异常值影响
- 可解释性强

---

## 3. 岭回归（L2 正则化）

```python
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score

# 不同 alpha 值的比较
alphas = [0.01, 0.1, 1, 10, 100]
for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    scores = cross_val_score(ridge, X_train_scaled, y_train, cv=5, scoring='r2')
    print(f"Alpha={alpha}: R² = {scores.mean():.4f} (+/- {scores.std():.4f})")

# 选择最佳 alpha
ridge_model = Ridge(alpha=1)
ridge_model.fit(X_train_scaled, y_train)

# 预测
y_pred_ridge = ridge_model.predict(X_test_scaled)

# 评估
print("\n=== 岭回归 ===")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_ridge)):.4f}")
print(f"R²: {r2_score(y_test, y_pred_ridge):.4f}")

# 系数比较
coef_comparison = pd.DataFrame({
    'feature': X.columns,
    'Linear': lr_model.coef_,
    'Ridge': ridge_model.coef_
})
print("\n系数比较:")
print(coef_comparison)
```

**岭回归特点**：
- 添加 L2 正则化（系数平方和惩罚）
- 缓解过拟合
- 系数收缩但不为零
- 适合多重共线性数据

---

## 4. Lasso 回归（L1 正则化）

```python
from sklearn.linear_model import Lasso

# 不同 alpha 值的比较
alphas = [0.001, 0.01, 0.1, 1]
for alpha in alphas:
    lasso = Lasso(alpha=alpha, max_iter=10000)
    scores = cross_val_score(lasso, X_train_scaled, y_train, cv=5, scoring='r2')
    print(f"Alpha={alpha}: R² = {scores.mean():.4f} (+/- {scores.std():.4f})")

# 训练模型
lasso_model = Lasso(alpha=0.1, max_iter=10000)
lasso_model.fit(X_train_scaled, y_train)

# 预测
y_pred_lasso = lasso_model.predict(X_test_scaled)

# 评估
print("\n=== Lasso 回归 ===")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_lasso)):.4f}")
print(f"R²: {r2_score(y_test, y_pred_lasso):.4f}")

# 特征选择效果
lasso_coef = pd.DataFrame({
    'feature': X.columns,
    'coefficient': lasso_model.coef_
}).sort_values('coefficient', key=abs, ascending=False)
print("\nLasso 系数（自动特征选择）:")
print(lasso_coef)
print(f"\n非零系数数量: {(lasso_model.coef_ != 0).sum()}")
```

**Lasso 特点**：
- 添加 L1 正则化（系数绝对值惩罚）
- 自动特征选择（系数可为零）
- 适合高维稀疏数据
- 产生稀疏模型

---

## 5. ElasticNet（L1 + L2）

```python
from sklearn.linear_model import ElasticNet

# 训练模型
en_model = ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=10000)
en_model.fit(X_train_scaled, y_train)

# 预测
y_pred_en = en_model.predict(X_test_scaled)

# 评估
print("=== ElasticNet ===")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_en)):.4f}")
print(f"R²: {r2_score(y_test, y_pred_en):.4f}")
```

---

## 6. 随机森林回归

```python
from sklearn.ensemble import RandomForestRegressor

# 训练模型
rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)  # 随机森林不需要特征缩放

# 预测
y_pred_rf = rf_model.predict(X_test)

# 评估
print("=== 随机森林回归 ===")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_rf)):.4f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred_rf):.4f}")
print(f"R²: {r2_score(y_test, y_pred_rf):.4f}")

# 特征重要性
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)
print("\n特征重要性:")
print(feature_importance)
```

---

## 7. XGBoost 回归

```python
from xgboost import XGBRegressor

# 训练模型
xgb_model = XGBRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
xgb_model.fit(X_train, y_train)

# 预测
y_pred_xgb = xgb_model.predict(X_test)

# 评估
print("=== XGBoost 回归 ===")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_xgb)):.4f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred_xgb):.4f}")
print(f"R²: {r2_score(y_test, y_pred_xgb):.4f}")
```

---

## 8. 评估指标详解

| 指标 | 公式 | 说明 | 最优值 |
|------|------|------|--------|
| MSE | Σ(y-ŷ)²/n | 均方误差，对大误差敏感 | 0 |
| RMSE | √MSE | 均方根误差，与y同单位 | 0 |
| MAE | Σ\|y-ŷ\|/n | 平均绝对误差，鲁棒 | 0 |
| R² | 1 - SS_res/SS_tot | 决定系数，解释方差比例 | 1 |
| MAPE | Σ\|y-ŷ\|/y/n | 平均绝对百分比误差 | 0 |

```python
# 自定义 MAPE
def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

print(f"MAPE: {mape(y_test, y_pred_rf):.2f}%")
```

---

## 9. 残差分析

```python
# 残差分析
residuals = y_test - y_pred_rf

# 残差分布
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 残差直方图
axes[0].hist(residuals, bins=30, edgecolor='black')
axes[0].set_xlabel('Residuals')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Residual Distribution')

# 预测值 vs 残差
axes[1].scatter(y_pred_rf, residuals, alpha=0.5)
axes[1].axhline(y=0, color='r', linestyle='--')
axes[1].set_xlabel('Predicted Values')
axes[1].set_ylabel('Residuals')
axes[1].set_title('Predicted vs Residuals')

# 实际值 vs 预测值
axes[2].scatter(y_test, y_pred_rf, alpha=0.5)
axes[2].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
axes[2].set_xlabel('Actual Values')
axes[2].set_ylabel('Predicted Values')
axes[2].set_title('Actual vs Predicted')

plt.tight_layout()
plt.savefig('residual_analysis.png')
```

---

## 10. 模型对比与调优

```python
from sklearn.model_selection import GridSearchCV

# 模型对比
results = pd.DataFrame({
    'Model': ['Linear', 'Ridge', 'Lasso', 'ElasticNet', 'RandomForest', 'XGBoost'],
    'RMSE': [
        np.sqrt(mean_squared_error(y_test, y_pred_lr)),
        np.sqrt(mean_squared_error(y_test, y_pred_ridge)),
        np.sqrt(mean_squared_error(y_test, y_pred_lasso)),
        np.sqrt(mean_squared_error(y_test, y_pred_en)),
        np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        np.sqrt(mean_squared_error(y_test, y_pred_xgb))
    ],
    'R²': [
        r2_score(y_test, y_pred_lr),
        r2_score(y_test, y_pred_ridge),
        r2_score(y_test, y_pred_lasso),
        r2_score(y_test, y_pred_en),
        r2_score(y_test, y_pred_rf),
        r2_score(y_test, y_pred_xgb)
    ]
})
print(results.sort_values('R²', ascending=False))

# 随机森林调参
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid,
    cv=5,
    scoring='r2',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

print(f"\n最佳参数: {grid_search.best_params_}")
print(f"最佳 R²: {grid_search.best_score_:.4f}")
```

---

## 验证步骤

1. **数据探索**：检查相关性和分布
2. **模型训练**：训练各回归模型
3. **模型评估**：对比 RMSE 和 R²
4. **残差分析**：检查残差是否随机
5. **特征重要性**：分析关键特征
6. **调参优化**：网格搜索提升性能

---

## 常见问题

### Q1: R² 为负数？
- 模型比均值预测还差
- 检查数据是否有问题
- 尝试更复杂的模型

### Q2: 如何选择正则化参数？
- 使用交叉验证选择最佳 alpha
- Ridge: 多重共线性时使用
- Lasso: 需要特征选择时使用

### Q3: 线性模型效果差？
- 数据可能是非线性关系
- 尝试多项式特征
- 使用树模型（随机森林/XGBoost）
