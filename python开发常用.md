1.venv创建虚拟环境

```
python -m venv venv
```

2.miniconda创建虚拟环境

```
conda create -n venv python=3.10
```

3.uv创建虚拟环境

3.1 基于本地python环境创建虚拟环境

```
uv venv --python "D:\Program Files\Miniconda3\envs\pyspark3.8\python.exe"
修改 uv项目中的python版本
uv sync
D:\Program Files\Miniconda3\envs\python3.12
uv venv --python "D:\Program Files\Miniconda3\envs\python3.12\python.exe"
```

3.2 uv初始化项目

```
uv init ai-agent-test

cd ai-agent-test 

创建uv虚拟环境

uv add pyyaml

uv sync  同步uv的依赖
```

4.基于requirement.txt管理python的依赖

```
pip freeze > requirements.txt
pip install -r requirements.txt

conda env export > environment.yml
conda env create -f environment.yml
```

5.python安装依赖指定镜像源

````
pip install numpy -i https://mirrors.aliyun.com/pypi/simple/
pip install jupyter -i https://mirrors.aliyun.com/pypi/simple/
pip install matplotlib -i https://mirrors.aliyun.com/pypi/simple/

pip install langgraph https://mirrors.aliyun.com/pypi/simple/

pip install langgraph -i https://pypi.tuna.tsinghua.edu.cn/simple/
````

5.jupyter notebook的安装使用

```
1.在默认的虚拟环境中安装jupyter 与 ipykernel
pip install ipykernel
2.在指定的虚拟环境中安装 jupyter 的 ikernel注册
python -m ipykernel install --user --name 虚拟环境名称 --display-name "ikernel显示名称"
3.启动本地的jupyter notebook 通过切换虚拟环境的 ikernel切换到对应的虚拟环境中,不需要每个环境都安装 jupyter
```

