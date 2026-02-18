"""
机器学习回归示例代码
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def load_data():
    """加载数据"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "regression_data.csv")
    df = pd.read_csv(data_path)
    print("数据概览:")
    print(df.head())
    print(f"\n数据形状: {df.shape}")
    print(f"\n数据统计:\n{df.describe()}")
    return df


def explore_data(df):
    """数据探索"""
    print("\n" + "=" * 50)
    print("数据探索")
    print("=" * 50)
    
    # 相关性分析
    print("\n与目标变量的相关性:")
    correlations = df.corr()['price'].sort_values(ascending=False)
    print(correlations)
    
    return correlations


def preprocess_data(df):
    """数据预处理"""
    # 特征和标签
    X = df.drop('price', axis=1)
    y = df['price']
    
    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, X.columns


def evaluate_regression(y_test, y_pred, model_name):
    """评估回归模型"""
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n{model_name} 评估结果:")
    print(f"  MSE:  {mse:.2f}")
    print(f"  RMSE: {rmse:.2f}")
    print(f"  MAE:  {mae:.2f}")
    print(f"  R²:   {r2:.4f}")
    
    return {'mse': mse, 'rmse': rmse, 'mae': mae, 'r2': r2}


def train_linear_regression(X_train, X_test, y_train, y_test, feature_names):
    """线性回归"""
    print("\n" + "=" * 50)
    print("线性回归")
    print("=" * 50)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    metrics = evaluate_regression(y_test, y_pred, "Linear Regression")
    
    # 系数分析
    coef_df = pd.DataFrame({
        'feature': feature_names,
        'coefficient': model.coef_
    }).sort_values('coefficient', key=abs, ascending=False)
    print(f"\n系数:\n{coef_df}")
    print(f"截距: {model.intercept_:.2f}")
    
    return model, y_pred, metrics


def train_ridge(X_train, X_test, y_train, y_test):
    """岭回归"""
    print("\n" + "=" * 50)
    print("岭回归 (L2 正则化)")
    print("=" * 50)
    
    # 不同 alpha 值比较
    print("\n不同 alpha 值的 R²:")
    for alpha in [0.1, 1, 10, 100]:
        ridge = Ridge(alpha=alpha)
        scores = cross_val_score(ridge, X_train, y_train, cv=5, scoring='r2')
        print(f"  alpha={alpha}: R² = {scores.mean():.4f} (+/- {scores.std():.4f})")
    
    # 训练最佳模型
    model = Ridge(alpha=1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    metrics = evaluate_regression(y_test, y_pred, "Ridge Regression")
    
    return model, y_pred, metrics


def train_lasso(X_train, X_test, y_train, y_test, feature_names):
    """Lasso 回归"""
    print("\n" + "=" * 50)
    print("Lasso 回归 (L1 正则化)")
    print("=" * 50)
    
    model = Lasso(alpha=0.1, max_iter=10000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    metrics = evaluate_regression(y_test, y_pred, "Lasso Regression")
    
    # 特征选择效果
    coef_df = pd.DataFrame({
        'feature': feature_names,
        'coefficient': model.coef_
    }).sort_values('coefficient', key=abs, ascending=False)
    print(f"\nLasso 系数:\n{coef_df}")
    print(f"非零系数数量: {(model.coef_ != 0).sum()}")
    
    return model, y_pred, metrics


def train_random_forest(X_train, X_test, y_train, y_test, feature_names):
    """随机森林回归"""
    print("\n" + "=" * 50)
    print("随机森林回归")
    print("=" * 50)
    
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    metrics = evaluate_regression(y_test, y_pred, "Random Forest")
    
    # 特征重要性
    importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(f"\n特征重要性:\n{importance}")
    
    return model, y_pred, metrics


def plot_predictions(y_test, predictions, labels, save_path=None):
    """绘制预测值 vs 实际值"""
    n_models = len(predictions)
    fig, axes = plt.subplots(1, n_models, figsize=(5*n_models, 4))
    
    if n_models == 1:
        axes = [axes]
    
    for ax, y_pred, label in zip(axes, predictions, labels):
        ax.scatter(y_test, y_pred, alpha=0.5)
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        ax.set_xlabel('Actual')
        ax.set_ylabel('Predicted')
        ax.set_title(label)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"预测对比图已保存到: {save_path}")
    plt.show()


def plot_residuals(y_test, y_pred, save_path=None):
    """残差分析"""
    residuals = y_test - y_pred
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # 残差分布
    axes[0].hist(residuals, bins=20, edgecolor='black')
    axes[0].set_xlabel('Residuals')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Residual Distribution')
    
    # 预测值 vs 残差
    axes[1].scatter(y_pred, residuals, alpha=0.5)
    axes[1].axhline(y=0, color='r', linestyle='--')
    axes[1].set_xlabel('Predicted')
    axes[1].set_ylabel('Residuals')
    axes[1].set_title('Predicted vs Residuals')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"残差分析图已保存到: {save_path}")
    plt.show()


def main():
    """主函数"""
    print("=" * 60)
    print("机器学习回归示例")
    print("=" * 60)
    
    # 1. 加载数据
    df = load_data()
    
    # 2. 数据探索
    correlations = explore_data(df)
    
    # 3. 数据预处理
    X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, feature_names = preprocess_data(df)
    
    # 4. 训练模型
    lr_model, lr_pred, lr_metrics = train_linear_regression(
        X_train_scaled, X_test_scaled, y_train, y_test, feature_names
    )
    
    ridge_model, ridge_pred, ridge_metrics = train_ridge(
        X_train_scaled, X_test_scaled, y_train, y_test
    )
    
    lasso_model, lasso_pred, lasso_metrics = train_lasso(
        X_train_scaled, X_test_scaled, y_train, y_test, feature_names
    )
    
    rf_model, rf_pred, rf_metrics = train_random_forest(
        X_train, X_test, y_train, y_test, feature_names
    )
    
    # 5. 模型对比
    print("\n" + "=" * 50)
    print("模型对比")
    print("=" * 50)
    
    results = pd.DataFrame({
        'Model': ['Linear', 'Ridge', 'Lasso', 'RandomForest'],
        'RMSE': [lr_metrics['rmse'], ridge_metrics['rmse'], 
                 lasso_metrics['rmse'], rf_metrics['rmse']],
        'MAE': [lr_metrics['mae'], ridge_metrics['mae'], 
                lasso_metrics['mae'], rf_metrics['mae']],
        'R²': [lr_metrics['r2'], ridge_metrics['r2'], 
               lasso_metrics['r2'], rf_metrics['r2']]
    })
    print(results.sort_values('R²', ascending=False))
    
    # 6. 可视化（可选）
    # plot_predictions(y_test, [lr_pred, rf_pred], ['Linear', 'RandomForest'])
    # plot_residuals(y_test, rf_pred)
    
    print("\n" + "=" * 60)
    print("回归示例执行完成！")


if __name__ == "__main__":
    main()
