# 机器学习环境搭建说明

## 一、Python 环境

### 版本要求
- Python 3.8+（推荐 3.10 或 3.11）

### 创建虚拟环境

```bash
# 使用 venv
python -m venv ml_env
source ml_env/bin/activate  # Linux/Mac
ml_env\Scripts\activate     # Windows

# 或使用 conda
conda create -n ml python=3.11
conda activate ml
```

---

## 二、安装依赖

### 核心包

```bash
# 数据处理
pip install numpy pandas

# 机器学习
pip install scikit-learn

# 可视化
pip install matplotlib seaborn

# Jupyter
pip install jupyter notebook
```

### 进阶包

```bash
# 梯度提升
pip install xgboost lightgbm catboost

# 超参数优化
pip install optuna hyperopt

# 特征工程
pip install featuretools

# 模型解释
pip install shap lime
```

### 一键安装

```bash
pip install numpy pandas scikit-learn matplotlib seaborn \
    xgboost lightgbm jupyter
```

### requirements.txt

```
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
xgboost>=1.5.0
lightgbm>=3.3.0
jupyter>=1.0.0
```

安装：
```bash
pip install -r requirements.txt
```

---

## 三、验证安装

```python
# test_installation.py
import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns

print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"Scikit-learn: {sklearn.__version__}")
print(f"Matplotlib: {plt.matplotlib.__version__}")
print(f"Seaborn: {sns.__version__}")

# 测试机器学习
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier().fit(X_train, y_train)
print(f"测试准确率: {accuracy_score(y_test, model.predict(X_test)):.4f}")

print("\n环境配置成功！")
```

---

## 四、Jupyter Notebook 配置

### 启动

```bash
jupyter notebook
```

### 常用插件

```bash
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
```

### 推荐扩展
- Table of Contents (toc2)
- Variable Inspector
- Collapsible Headings
- ExecuteTime

---

## 五、GPU 支持（可选）

### XGBoost GPU

```bash
pip install xgboost
# 使用时指定 tree_method='gpu_hist'
```

### LightGBM GPU

```bash
pip install lightgbm --install-option=--gpu
```

---

## 六、常见问题

### Q1: ImportError: cannot import name
更新到最新版本：
```bash
pip install --upgrade scikit-learn
```

### Q2: matplotlib 中文乱码
```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
plt.rcParams['axes.unicode_minus'] = False
```

### Q3: 内存不足
- 使用 `dtype` 优化 pandas 数据类型
- 使用 `n_jobs=-1` 利用多核
- 分批处理大数据集
