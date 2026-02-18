# 案例：监督学习 - 分类

## 目标

掌握常用分类算法的使用，包括逻辑回归、决策树、随机森林、XGBoost，以及分类模型的评估方法。

---

## 知识点覆盖

- 逻辑回归（Logistic Regression）
- 决策树（Decision Tree）
- 随机森林（Random Forest）
- XGBoost
- 分类评估指标（准确率、精确率、召回率、F1、AUC）
- 混淆矩阵
- 交叉验证与网格搜索

---

## 场景描述

**业务场景**：客户流失预测

根据客户的消费行为、账户信息等特征，预测客户是否会流失（二分类问题）。

**数据特征**：
- `tenure`: 客户使用时长（月）
- `monthly_charges`: 月消费金额
- `total_charges`: 总消费金额
- `contract_type`: 合同类型
- `payment_method`: 支付方式
- `churn`: 是否流失（目标变量）

---

## 1. 数据准备

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# 加载数据
df = pd.read_csv('data/classification_data.csv')

# 查看数据
print(df.head())
print(df.info())
print(df['churn'].value_counts())

# 特征和标签
X = df.drop('churn', axis=1)
y = df['churn']

# 处理分类特征（示例）
le = LabelEncoder()
for col in X.select_dtypes(include=['object']).columns:
    X[col] = le.fit_transform(X[col])

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 特征缩放
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

---

## 2. 逻辑回归

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

# 训练模型
lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train_scaled, y_train)

# 预测
y_pred_lr = lr_model.predict(X_test_scaled)
y_prob_lr = lr_model.predict_proba(X_test_scaled)[:, 1]

# 评估
print("=== 逻辑回归 ===")
print(f"准确率: {accuracy_score(y_test, y_pred_lr):.4f}")
print(f"AUC: {roc_auc_score(y_test, y_prob_lr):.4f}")
print(classification_report(y_test, y_pred_lr))

# 查看系数
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'coefficient': lr_model.coef_[0]
}).sort_values('coefficient', key=abs, ascending=False)
print(feature_importance)
```

**逻辑回归特点**：
- 简单、可解释性强
- 输出概率值
- 适合线性可分数据
- 计算效率高

---

## 3. 决策树

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# 训练模型
dt_model = DecisionTreeClassifier(
    max_depth=5,
    min_samples_split=10,
    random_state=42
)
dt_model.fit(X_train, y_train)

# 预测
y_pred_dt = dt_model.predict(X_test)

# 评估
print("=== 决策树 ===")
print(f"准确率: {accuracy_score(y_test, y_pred_dt):.4f}")
print(classification_report(y_test, y_pred_dt))

# 特征重要性
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': dt_model.feature_importances_
}).sort_values('importance', ascending=False)
print(feature_importance)

# 可视化决策树
plt.figure(figsize=(20, 10))
plot_tree(dt_model, feature_names=X.columns, class_names=['No', 'Yes'], 
          filled=True, rounded=True, max_depth=3)
plt.tight_layout()
plt.savefig('decision_tree.png')
```

**决策树特点**：
- 可解释性极强（可视化）
- 不需要特征缩放
- 容易过拟合（需剪枝）
- 对数据旋转敏感

---

## 4. 随机森林

```python
from sklearn.ensemble import RandomForestClassifier

# 训练模型
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

# 预测
y_pred_rf = rf_model.predict(X_test)
y_prob_rf = rf_model.predict_proba(X_test)[:, 1]

# 评估
print("=== 随机森林 ===")
print(f"准确率: {accuracy_score(y_test, y_pred_rf):.4f}")
print(f"AUC: {roc_auc_score(y_test, y_prob_rf):.4f}")
print(classification_report(y_test, y_pred_rf))

# 特征重要性
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)
print(feature_importance)

# 可视化特征重要性
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['feature'][:10], feature_importance['importance'][:10])
plt.xlabel('Importance')
plt.title('Top 10 Feature Importance (Random Forest)')
plt.tight_layout()
plt.savefig('rf_feature_importance.png')
```

**随机森林特点**：
- Bagging 集成，抗过拟合
- 不易过拟合，泛化能力强
- 可并行计算，速度快
- 提供特征重要性

---

## 5. XGBoost

```python
from xgboost import XGBClassifier

# 训练模型
xgb_model = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)
xgb_model.fit(X_train, y_train)

# 预测
y_pred_xgb = xgb_model.predict(X_test)
y_prob_xgb = xgb_model.predict_proba(X_test)[:, 1]

# 评估
print("=== XGBoost ===")
print(f"准确率: {accuracy_score(y_test, y_pred_xgb):.4f}")
print(f"AUC: {roc_auc_score(y_test, y_prob_xgb):.4f}")
print(classification_report(y_test, y_pred_xgb))

# 特征重要性
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': xgb_model.feature_importances_
}).sort_values('importance', ascending=False)
print(feature_importance)
```

**XGBoost 特点**：
- Boosting 集成，迭代优化
- 支持正则化，防过拟合
- 缺失值自动处理
- 竞赛和工业界广泛使用

---

## 6. 模型评估详解

### 混淆矩阵

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# 绘制混淆矩阵
cm = confusion_matrix(y_test, y_pred_rf)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['No Churn', 'Churn'])
disp.plot(cmap='Blues')
plt.title('Confusion Matrix - Random Forest')
plt.savefig('confusion_matrix.png')
```

### ROC 曲线

```python
from sklearn.metrics import roc_curve, auc

# 计算 ROC
fpr, tpr, thresholds = roc_curve(y_test, y_prob_rf)
roc_auc = auc(fpr, tpr)

# 绘制 ROC 曲线
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.savefig('roc_curve.png')
```

### 指标解释

| 指标 | 公式 | 说明 |
|------|------|------|
| 准确率 | (TP+TN)/(TP+TN+FP+FN) | 整体预测正确比例 |
| 精确率 | TP/(TP+FP) | 预测为正的准确率 |
| 召回率 | TP/(TP+FN) | 实际正类被正确预测的比例 |
| F1 | 2×(P×R)/(P+R) | 精确率和召回率的调和平均 |
| AUC | ROC曲线下面积 | 模型区分能力，0.5-1.0 |

---

## 7. 超参数调优

```python
from sklearn.model_selection import GridSearchCV, cross_val_score

# 随机森林网格搜索
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)
grid_search.fit(X_train, y_train)

print(f"最佳参数: {grid_search.best_params_}")
print(f"最佳 AUC: {grid_search.best_score_:.4f}")

# 使用最佳模型
best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test)
print(f"测试集准确率: {accuracy_score(y_test, y_pred_best):.4f}")
```

---

## 8. 模型对比

```python
# 汇总各模型结果
results = pd.DataFrame({
    'Model': ['Logistic Regression', 'Decision Tree', 'Random Forest', 'XGBoost'],
    'Accuracy': [
        accuracy_score(y_test, y_pred_lr),
        accuracy_score(y_test, y_pred_dt),
        accuracy_score(y_test, y_pred_rf),
        accuracy_score(y_test, y_pred_xgb)
    ],
    'AUC': [
        roc_auc_score(y_test, y_prob_lr),
        roc_auc_score(y_test, dt_model.predict_proba(X_test)[:, 1]),
        roc_auc_score(y_test, y_prob_rf),
        roc_auc_score(y_test, y_prob_xgb)
    ]
})
print(results.sort_values('AUC', ascending=False))
```

---

## 验证步骤

1. **数据加载**：验证数据读取正常
2. **数据预处理**：验证编码和缩放正确
3. **模型训练**：验证各模型训练无报错
4. **模型评估**：对比各模型的准确率和 AUC
5. **特征重要性**：分析关键特征
6. **调参优化**：使用网格搜索提升性能

---

## 常见问题

### Q1: 类别不平衡怎么办？
- 使用 `class_weight='balanced'` 参数
- 过采样（SMOTE）或欠采样
- 使用 AUC 而非准确率评估

### Q2: 过拟合怎么办？
- 增加正则化（C 参数）
- 减小模型复杂度（max_depth）
- 增加训练数据
- 使用交叉验证

### Q3: 选择哪个模型？
- 可解释性要求高：逻辑回归/决策树
- 追求性能：XGBoost/随机森林
- 数据量小：逻辑回归
- 数据量大：XGBoost/LightGBM
