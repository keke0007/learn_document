# LangChain 1.0 学习指南

## 一、项目简介

LangChain 是构建大语言模型（LLM）应用的开源框架，1.0 版本引入了 LCEL（LangChain Expression Language）统一编排语法、模块化架构重构、标准化 Runnable 接口等重大改进。本模块涵盖 LangChain 1.0 核心概念、组件使用、RAG 构建和 Agent 开发。

---

## 二、目录结构

```
langchain1.0/
├── GUIDE.md                        # 本指南文档
├── README.md                       # 知识点与案例总览
├── cases/
│   ├── basic_llm_chat.md           # 基础 LLM 与 Chat 模型
│   ├── lcel_chains.md              # LCEL 链式编排
│   ├── rag_knowledge_base.md       # RAG 知识库问答
│   └── agent_tools.md              # Agent 与工具调用
├── data/
│   ├── sample_docs.txt             # 示例文档（RAG 用）
│   ├── faq_knowledge.md            # FAQ 知识库内容
│   └── tool_schemas.json           # 工具定义示例
└── scripts/
    ├── setup_env.md                # 环境搭建说明
    ├── basic_examples.py           # 基础示例代码
    ├── rag_example.py              # RAG 示例代码
    └── agent_example.py            # Agent 示例代码
```

---

## 三、学习路线

### 第一阶段：基础入门
- LangChain 架构概览（langchain-core, langchain, langchain-community）
- LLM vs Chat Models
- Prompt Templates（字符串模板、Chat 模板）
- Output Parsers（字符串、JSON、Pydantic）

### 第二阶段：LCEL 与链式编排
- Runnable 接口（invoke, batch, stream, ainvoke）
- 管道操作符 `|` 组合
- RunnablePassthrough、RunnableLambda、RunnableParallel
- 条件分支与路由

### 第三阶段：RAG 知识库
- Document Loaders（文件、网页、数据库）
- Text Splitters（字符、递归、语义分割）
- Embeddings（OpenAI、HuggingFace、本地模型）
- Vector Stores（FAISS、Chroma、Milvus）
- Retrievers 与检索策略

### 第四阶段：Agent 与工具
- Tool 定义（@tool 装饰器、StructuredTool）
- Agent 类型（ReAct、OpenAI Functions、Tool Calling）
- AgentExecutor 执行流程
- Memory 与对话历史
- Callbacks 与可观测性

---

## 四、快速开始

### 4.1 环境准备

```bash
# 创建虚拟环境
python -m venv langchain_env
source langchain_env/bin/activate  # Linux/Mac
# langchain_env\Scripts\activate   # Windows

# 安装核心包
pip install langchain langchain-openai langchain-community

# 安装向量数据库（RAG 用）
pip install faiss-cpu chromadb

# 安装其他常用包
pip install python-dotenv tiktoken
```

### 4.2 配置 API Key

```python
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI
os.environ["OPENAI_API_KEY"] = "sk-xxx"

# 或使用其他模型
os.environ["ANTHROPIC_API_KEY"] = "xxx"
os.environ["DASHSCOPE_API_KEY"] = "xxx"  # 阿里通义
```

### 4.3 第一个示例

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 初始化模型
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 定义 Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的助手，用简洁的中文回答问题。"),
    ("human", "{question}")
])

# LCEL 链式组合
chain = prompt | llm | StrOutputParser()

# 调用
response = chain.invoke({"question": "什么是 LangChain？"})
print(response)
```

---

## 五、核心知识速查

### 5.1 架构模块

| 包名 | 说明 |
|------|------|
| `langchain-core` | 核心抽象（Runnable, Prompt, Parser） |
| `langchain` | 高层组件（Chains, Agents） |
| `langchain-openai` | OpenAI 集成 |
| `langchain-anthropic` | Anthropic Claude 集成 |
| `langchain-community` | 社区集成（向量库、文档加载器等） |

### 5.2 核心类

```python
# Chat Model
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Prompt Template
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template("翻译成英文: {text}")

# Output Parser
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# Embedding
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

# Vector Store
from langchain_community.vectorstores import FAISS, Chroma
```

### 5.3 LCEL 语法

```python
# 基础链
chain = prompt | llm | parser

# 并行执行
from langchain_core.runnables import RunnableParallel
parallel = RunnableParallel(
    summary=summary_chain,
    translation=translate_chain
)

# 传递输入
from langchain_core.runnables import RunnablePassthrough
chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

# 自定义函数
from langchain_core.runnables import RunnableLambda
def format_docs(docs):
    return "\n".join(d.page_content for d in docs)
chain = retriever | RunnableLambda(format_docs) | prompt | llm

# 条件路由
from langchain_core.runnables import RunnableBranch
branch = RunnableBranch(
    (lambda x: "技术" in x["question"], tech_chain),
    (lambda x: "商务" in x["question"], biz_chain),
    default_chain
)
```

### 5.4 Runnable 接口

| 方法 | 说明 | 示例 |
|------|------|------|
| `invoke(input)` | 单次调用 | `chain.invoke({"question": "xxx"})` |
| `batch(inputs)` | 批量调用 | `chain.batch([{"q": "a"}, {"q": "b"}])` |
| `stream(input)` | 流式输出 | `for chunk in chain.stream({...}): print(chunk)` |
| `ainvoke(input)` | 异步调用 | `await chain.ainvoke({...})` |

### 5.5 RAG 流程

```
Documents → Loader → Splitter → Embeddings → VectorStore
                                                  ↓
User Query → Embedding → Retriever → Context + Prompt → LLM → Answer
```

---

## 六、数据说明

| 文件 | 说明 |
|------|------|
| `data/sample_docs.txt` | RAG 演示用的示例文档 |
| `data/faq_knowledge.md` | FAQ 知识库内容 |
| `data/tool_schemas.json` | Agent 工具定义示例 |

---

## 七、案例总览

| 案例 | 知识点 | 文件 |
|------|--------|------|
| 基础 LLM 与 Chat 模型 | ChatOpenAI, Prompt, Parser | `cases/basic_llm_chat.md` |
| LCEL 链式编排 | 管道操作符, Runnable, 路由 | `cases/lcel_chains.md` |
| RAG 知识库问答 | Loader, Splitter, Embedding, VectorStore | `cases/rag_knowledge_base.md` |
| Agent 与工具调用 | Tool, Agent, AgentExecutor | `cases/agent_tools.md` |

---

## 八、学习建议

1. **从 LCEL 开始**：1.0 的核心是 LCEL，先掌握 `|` 管道操作
2. **理解 Runnable**：所有组件都实现 Runnable 接口，统一调用方式
3. **善用 LangSmith**：开启 tracing 观察链路执行过程
4. **本地模型优先**：开发阶段可用 Ollama + llama3 降低成本
5. **参考官方文档**：[python.langchain.com](https://python.langchain.com/)

---

## 九、学习检查清单

- [ ] 能区分 langchain-core / langchain / langchain-community 包
- [ ] 掌握 ChatOpenAI、ChatPromptTemplate、StrOutputParser 基本用法
- [ ] 理解 LCEL 管道操作符 `|` 和 Runnable 接口
- [ ] 能使用 RunnablePassthrough、RunnableLambda、RunnableParallel
- [ ] 能构建完整的 RAG 流程（加载→分割→向量化→检索→生成）
- [ ] 能定义 Tool 并创建 Agent
- [ ] 了解 Memory 和对话历史管理
- [ ] 能使用 stream 实现流式输出

---

## 十、学习成果

完成本模块后，你将能够：

1. 使用 LangChain 1.0 构建 LLM 应用
2. 熟练使用 LCEL 编排复杂处理链
3. 构建 RAG 知识库问答系统
4. 开发具备工具调用能力的 Agent
5. 实现流式输出和异步处理
6. 集成 LangSmith 进行调试和监控
