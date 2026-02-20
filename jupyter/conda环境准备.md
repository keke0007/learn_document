# 学习环境准备



[TOC]



# 1. Conda 基本介绍

## 1.1  什么是Conda、MiniConda、Anaconda

<img src="./assets/conda-1.jpg" width="600px" align="left">

> Conda是一个包和环境管理的工具。支持Windows、macOS和Linux。Conda可以快速的安装、运行和更新包和相关的依赖。Conda也可以轻易地创建、保存、加载和转换环境。

> Anaconda 是一个用于科学计算的 Python 发行版，支持 Linux, Mac, Windows, 包含了conda、conda-build、Python和众多科学计算的包及其依赖。

> Miniconda 是一个 Anaconda 的轻量级替代，默认只包含了 conda，Python 和一些它们所以依赖的包。





## 1.2 Anaconda 和 Miniconda 区别？

Miniconda 是 Anaconda 的精简版本，同样也是一個开源环境，两者都是conda系统的一部分。不同之处在于Anaconda会预先安装许多常用的 Python套件，因此占用较多的硬盘空间。相比之下，Miniconda 因为名为 ”Mini”，因此仅安装运行所需的基本套件，对于有多个不同 Python 版本共存的情況，可以节省大量空间。

> Miniconda可以依据自己需求建立自己的Python环境，想要的套件自行安装。



## 1.3 为什么要使用 Conda？

一个典型的Python 项目会使用多个包来完成其功能。其中一些包也可能被其他项目所使用（共享）。 **项目之间共享的包可能会引起冲突。** 比如，我们有两个项目P1和P2，P1使用NumPy 1.2版本，而P2需要NumPy 1.3版本，一个环境中存在两个版本就可能导致冲突。 解决这个问题的办法就是使用虚拟环境。我们可以为每个项目分别创建一个独立的虚拟环境，来隔离包冲突。

<img src="./assets/conda-3.png" width="600px" align="left">

常用的Python虚拟环境管理工具有：

1. Virtualenv
2. Conda
3. pipenv
4. venv

通过使用这些工具，我们可以很容易的创建虚拟环境。



# 2 Conda 安装

## 2.1 Miniconda 下载安装

官网下载地址：https://www.anaconda.com/download/success

**Anaconda Installers vs Miniconda Installers**

<img src="./assets/conda-2.png" width="800px" align="left">

下载后依据指引进行 Miniconda 安装。



## 2.2 使用 Anaconda Powershell Prompt 终端

<img src="./assets/conda-4.png"  align="left">

安装完成后，打开终端 `Anaconda Powershell Prompt`，如果有看到命令列提示中的（base），那表示安装成功。

我们可以輸入 `python --version`  确认 Python版本。

<img src="./assets/conda-5.png" width="600px" align="left">



# 3. Conda 常用命令

## 3.1 基本命令

```powershell
conda –help # 查看帮助
conda info # 查看 conda 信息
conda --version  # 查看 conda 版本
conda update conda  # 更新Conda（慎用）
conda clean –all # 清理不再需要的包
conda <指令> --help # 查看某一个指令的详细帮助
conda config --show #查看 conda 的环境配置
conda clean -p  # 清理没有用，没有安装的包
conda clean -t  # 清理 tarball
conda clean --all  # 清理所有包和 conda 的缓存文件
```



## 3.2 环境管理

### 3.2.1 创建 Conda 环境

使用conda可以在电脑上创建很多套相互隔离的Python环境，命令如下：

```powershell
# 语法
conda create --name <env_name> python=<version> [package_name1] [package_name2] [...]
# 样例 创建一个名为 learn 的环境，python 版本为3.10
conda create --name learn python=3.10 # --name 可以简写为 -n
```

**（可选）** 如果要指定conda环境的路径，需要设置 envs_dirs，命令如下：

只需要执行一次！

```powershell
conda config --add envs_dirs D:/envs/
```



### 3.2.2 切换 Conda 环境

前面说到Conda可以创建多套相互隔离的Python环境，使用 `conda activate env_name` 可以切换不同的环境。

```powershell
# 语法
conda activate env_name
# 样例 切换到 learn 环境
conda activate learn
```

如果要退出此环境，回到基础环境，可以使用如下命令

```powershell
# 退出当前环境
conda deactivate
```

### 3.2.3 查看 Conda 环境

当电脑上安装了很多台Conda环境的时候，可以使用 `conda env list` 命令查看所有已创建的Conda环境。

```powershell
# 查看当前电脑上所有的conda环境
conda env list
```

### 3.2.4 删除某个 Conda 环境

```powershell
# 语法
conda remove --name <env_name> --all
# 样例
conda remove --name learn --all
```

### 3.2.5 克隆环境

```powershell
# 语法
conda create --name <new_evn_name> --clone <old_env_name>
# 样例
conda create --name myclone --clone myenv
```



## 3.3 包管理

一旦激活了环境，你就可以使用`conda`和`pip`在当前环境下安装你所需要的包。

### 3.3.1 安装包

在激活的环境中安装包，例如安装NumPy：

```powershell
pip install numpy
```

可以使用以下命令安装特定版本的包：

```powershell
pip install numpy==2.2.1
```

 从 requirements.txt 文件安装

```powershell
pip install -r requirements.txt
```

### 3.3.2 更新包

更新某个包到最新版本：

```powershell
pip install --upgrade numpy
```

升级所有包

```powershell
# 将当前环境中的所有包信息保存到 requirements.txt 文件中
pip freeze > requirements.txt
# 卸载所有包
pip uninstall -r requirements.txt
# 重新安装所有包
pip install -r requirements.txt
```

### 3.3.3 卸载包

如果不再需要某个包，可以将其卸载：

```postgresql
pip uninstall numpy
```

### 3.3.4 列出环境中的所有包

查看当前环境中已安装的所有包：

```powershell
pip list
```

查看当前虚拟环境中已安装的某个包的信息

```powershell
pip show numpy
```

### 3.3.5 搜索包

搜索可用的包及其版本信息：

```powershell
conda search numpy
```



## 3.4 环境导入与导出

**导出环境**

将当前环境导出为一个YAML文件，方便共享：

```powershell
conda env export > environment.yml
```

**从文件创建环境**

使用YAML文件创建一个新环境：

```powershell
conda env create -f environment.yml
```



# 4. Jupyter Lab 使用

## 4.1 Jupyter 介绍

JupyterLab 是最新的基于 Web 的交互式开发环境，适用于notebooks、代码和数据。其灵活的界面允许用户配置和安排数据科学、科学计算、计算新闻和机器学习中的工作流程。模块化设计允许扩展来扩展和丰富功能。

<img src="./assets/conda-6.webp" width="800px" align="left">

## 4.2 Jupyter 安装使用

使用 安装 JupyterLab ：`pip`

```powershell
pip install jupyterlab
```

**注意**：如果您使用 conda 或 mamba 安装 JupyterLab。

安装后，使用以下命令启动 JupyterLab：

```powershell
jupyter lab
```

## 4.3 Jupyter 添加 Conda 环境

**1. 在conda环境中安装ipykernel**

1）创建环境时直接加入ipykernel

```powershell
conda create -n 环境名称 python=3.10 ipykernel
```

2）创建环境没有安装ipykernel，那么在虚拟环境下创建kernel文件

```powershell
conda install -n 环境名称 ipykernel
```

**2. 激活conda环境**

```powershell
conda activate 环境名称
```

**3. 将环境写入notebook的kernel中**

```powershell
python -m ipykernel install --user --name 环境名称 --display-name "环境名称"
```

**4. 打开notebook服务器**

```powershell
jupyter notebook
```

浏览器打开对应地址，新建python，就会有对应的环境提示了

**5. 删除kernel环境**

```powershell
jupyter kernelspec remove 环境名称
```



# 5. PyCharm 中使用 Conda 环境

1）创建项目所需要的虚拟环境

```powershell
conda create -n llamaindex-rag python=3.10
```

2）创建项目，选择 `自定义环境`，类型选择 `Conda`，环境选择 `llamaindex-rag`，点击 **创建** 即可

<img src="./assets/conda-7.png" width="800px" align="left">



3）查看项目环境配置

<img src="./assets/conda-8.png" width="800px" align="left">



**注意：项目中需要另外的依赖库，直接到 Conda Powershell  Prompt 终端下，激活 llamaindex-rag 环境，使用 pip 安装依赖库即可！**

