"""
机器学习分类示例代码
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def load_data():
    """加载数据"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "classification_data.csv")
    df = pd.read_csv(data_path)
    print("数据概览:")
    print(df.head())
    print(f"\n数据形状: {df.shape}")
    print(f"\n目标变量分布:\n{df['churn'].value_counts()}")
    return df


def preprocess_data(df):
    """数据预处理"""
    # 特征和标签
    X = df.drop('churn', axis=1)
    y = df['churn']
    
    # 编码类别特征
    le = LabelEncoder()
    for col in X.select_dtypes(include=['object']).columns:
        X[col] = le.fit_transform(X[col])
    
    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, X.columns


def train_logistic_regression(X_train, X_test, y_train, y_test):
    """逻辑回归"""
    print("\n" + "=" * 50)
    print("逻辑回归")
    print("=" * 50)
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
    print(f"精确率: {precision_score(y_test, y_pred):.4f}")
    print(f"召回率: {recall_score(y_test, y_pred):.4f}")
    print(f"F1 分数: {f1_score(y_test, y_pred):.4f}")
    print(f"AUC: {roc_auc_score(y_test, y_prob):.4f}")
    
    return model, y_pred, y_prob


def train_decision_tree(X_train, X_test, y_train, y_test):
    """决策树"""
    print("\n" + "=" * 50)
    print("决策树")
    print("=" * 50)
    
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
    print(f"AUC: {roc_auc_score(y_test, y_prob):.4f}")
    
    return model, y_pred, y_prob


def train_random_forest(X_train, X_test, y_train, y_test, feature_names):
    """随机森林"""
    print("\n" + "=" * 50)
    print("随机森林")
    print("=" * 50)
    
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
    print(f"AUC: {roc_auc_score(y_test, y_prob):.4f}")
    print("\n分类报告:")
    print(classification_report(y_test, y_pred))
    
    # 特征重要性
    importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\n特征重要性:")
    print(importance)
    
    return model, y_pred, y_prob


def grid_search_rf(X_train, y_train):
    """随机森林网格搜索"""
    print("\n" + "=" * 50)
    print("网格搜索调参")
    print("=" * 50)
    
    param_grid = {
        'n_estimators': [50, 100],
        'max_depth': [5, 10],
        'min_samples_split': [2, 5]
    }
    
    grid_search = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid,
        cv=3,
        scoring='roc_auc',
        n_jobs=-1
    )
    grid_search.fit(X_train, y_train)
    
    print(f"最佳参数: {grid_search.best_params_}")
    print(f"最佳 AUC: {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_


def plot_confusion_matrix(y_test, y_pred, save_path=None):
    """绘制混淆矩阵"""
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['No Churn', 'Churn'],
                yticklabels=['No Churn', 'Churn'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    
    if save_path:
        plt.savefig(save_path)
        print(f"混淆矩阵已保存到: {save_path}")
    plt.show()


def plot_feature_importance(model, feature_names, save_path=None):
    """绘制特征重要性"""
    importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=True)
    
    plt.figure(figsize=(10, 6))
    plt.barh(importance['feature'], importance['importance'])
    plt.xlabel('Importance')
    plt.title('Feature Importance (Random Forest)')
    
    if save_path:
        plt.savefig(save_path)
        print(f"特征重要性图已保存到: {save_path}")
    plt.show()


def main():
    """主函数"""
    print("=" * 60)
    print("机器学习分类示例")
    print("=" * 60)
    
    # 1. 加载数据
    df = load_data()
    
    # 2. 数据预处理
    X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, feature_names = preprocess_data(df)
    
    # 3. 训练模型
    lr_model, lr_pred, lr_prob = train_logistic_regression(X_train_scaled, X_test_scaled, y_train, y_test)
    dt_model, dt_pred, dt_prob = train_decision_tree(X_train, X_test, y_train, y_test)
    rf_model, rf_pred, rf_prob = train_random_forest(X_train, X_test, y_train, y_test, feature_names)
    
    # 4. 网格搜索
    best_model = grid_search_rf(X_train, y_train)
    
    # 5. 模型对比
    print("\n" + "=" * 50)
    print("模型对比")
    print("=" * 50)
    results = pd.DataFrame({
        'Model': ['Logistic Regression', 'Decision Tree', 'Random Forest'],
        'Accuracy': [
            accuracy_score(y_test, lr_pred),
            accuracy_score(y_test, dt_pred),
            accuracy_score(y_test, rf_pred)
        ],
        'AUC': [
            roc_auc_score(y_test, lr_prob),
            roc_auc_score(y_test, dt_prob),
            roc_auc_score(y_test, rf_prob)
        ]
    })
    print(results.sort_values('AUC', ascending=False))
    
    # 6. 可视化（可选）
    # plot_confusion_matrix(y_test, rf_pred)
    # plot_feature_importance(rf_model, feature_names)
    
    print("\n" + "=" * 60)
    print("分类示例执行完成！")


if __name__ == "__main__":
    main()
