# LangChain 1.0 环境搭建说明

## 一、Python 环境

### 版本要求
- Python 3.9+（推荐 3.10 或 3.11）

### 创建虚拟环境

```bash
# 使用 venv
python -m venv langchain_env
source langchain_env/bin/activate  # Linux/Mac
langchain_env\Scripts\activate     # Windows

# 或使用 conda
conda create -n langchain python=3.11
conda activate langchain
```

---

## 二、安装依赖

### 核心包

```bash
# LangChain 核心
pip install langchain langchain-core

# OpenAI 集成
pip install langchain-openai

# 社区集成（文档加载器、向量库等）
pip install langchain-community
```

### 可选包

```bash
# 向量数据库
pip install faiss-cpu          # FAISS（CPU版）
pip install chromadb           # Chroma
pip install pymilvus           # Milvus

# 文档加载
pip install pypdf              # PDF 加载
pip install unstructured       # 多格式文档
pip install beautifulsoup4     # 网页解析

# Embedding
pip install sentence-transformers  # HuggingFace Embeddings

# 其他
pip install python-dotenv      # 环境变量管理
pip install tiktoken           # Token 计数
```

### 一键安装

```bash
pip install langchain langchain-openai langchain-community \
    faiss-cpu chromadb python-dotenv tiktoken
```

---

## 三、API Key 配置

### 方式 1：环境变量

**Linux/Mac**:
```bash
export OPENAI_API_KEY="sk-xxx"
export ANTHROPIC_API_KEY="xxx"
```

**Windows CMD**:
```cmd
set OPENAI_API_KEY=sk-xxx
```

**Windows PowerShell**:
```powershell
$env:OPENAI_API_KEY="sk-xxx"
```

### 方式 2：.env 文件

创建 `.env` 文件：
```
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=xxx
LANGCHAIN_API_KEY=xxx
LANGCHAIN_TRACING_V2=true
```

代码中加载：
```python
from dotenv import load_dotenv
load_dotenv()
```

### 方式 3：代码中设置

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-xxx"
```

---

## 四、模型提供商配置

### OpenAI

```bash
pip install langchain-openai
```

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

llm = ChatOpenAI(model="gpt-4")
embeddings = OpenAIEmbeddings()
```

### Anthropic Claude

```bash
pip install langchain-anthropic
```

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-sonnet-20240229")
```

### 阿里通义千问

```bash
pip install dashscope
```

```python
from langchain_community.chat_models import ChatTongyi

llm = ChatTongyi(model="qwen-turbo")
```

### 本地 Ollama

```bash
# 安装 Ollama：https://ollama.ai
ollama pull llama3
```

```python
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="llama3", base_url="http://localhost:11434")
```

---

## 五、LangSmith 配置（可选）

LangSmith 是 LangChain 官方的调试和监控平台。

### 注册账号
访问 https://smith.langchain.com/ 注册账号并获取 API Key。

### 配置环境变量

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your-langsmith-api-key
export LANGCHAIN_PROJECT=your-project-name  # 可选
```

### 验证

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
result = llm.invoke("Hello")  # 执行后可在 LangSmith 中查看 trace
```

---

## 六、验证安装

```python
# test_installation.py
import langchain
print(f"LangChain version: {langchain.__version__}")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 测试基础调用
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
prompt = ChatPromptTemplate.from_template("用一句话介绍: {topic}")
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"topic": "Python"})
print(f"测试结果: {result}")

print("环境配置成功！")
```

运行测试：
```bash
python test_installation.py
```

---

## 七、常见问题

### Q1: ImportError: cannot import name 'xxx'
检查 langchain 版本，1.0 版本有很多 breaking changes。确保使用最新版本。

### Q2: OpenAI API 超时
设置代理或使用国内镜像：
```python
llm = ChatOpenAI(
    openai_api_base="https://your-proxy.com/v1",
    timeout=60
)
```

### Q3: FAISS 安装失败
尝试使用 conda 安装：
```bash
conda install -c conda-forge faiss-cpu
```

### Q4: Token 超限
使用 tiktoken 计算 token 数，控制输入长度：
```python
import tiktoken
encoding = tiktoken.encoding_for_model("gpt-4")
tokens = encoding.encode(text)
print(f"Token 数: {len(tokens)}")
```
