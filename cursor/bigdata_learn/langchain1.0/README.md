# LangChain 1.0 学习模块

## 概述

LangChain 是构建大语言模型应用的主流框架。1.0 版本（2024年发布）带来了架构重构、LCEL 统一编排语法、标准化接口等重大改进，是学习 LLM 应用开发的核心框架。

---

## 知识点与案例映射

| 知识点 | 说明 | 案例 | 数据/脚本 |
|--------|------|------|-----------|
| **架构概览** | langchain-core/langchain/langchain-community | `cases/basic_llm_chat.md` | - |
| **Chat Models** | ChatOpenAI, ChatAnthropic, 本地模型 | `cases/basic_llm_chat.md` | `scripts/basic_examples.py` |
| **Prompt Templates** | 字符串模板, Chat 模板, 变量注入 | `cases/basic_llm_chat.md` | `scripts/basic_examples.py` |
| **Output Parsers** | StrOutputParser, JsonOutputParser, PydanticOutputParser | `cases/basic_llm_chat.md` | `scripts/basic_examples.py` |
| **LCEL 管道** | `\|` 操作符, Runnable 组合 | `cases/lcel_chains.md` | `scripts/basic_examples.py` |
| **RunnablePassthrough** | 透传输入数据 | `cases/lcel_chains.md` | - |
| **RunnableLambda** | 自定义函数包装 | `cases/lcel_chains.md` | - |
| **RunnableParallel** | 并行执行多个链 | `cases/lcel_chains.md` | - |
| **RunnableBranch** | 条件路由 | `cases/lcel_chains.md` | - |
| **Document Loaders** | 文件/网页/数据库加载 | `cases/rag_knowledge_base.md` | `data/sample_docs.txt` |
| **Text Splitters** | 字符/递归/语义分割 | `cases/rag_knowledge_base.md` | - |
| **Embeddings** | OpenAI/HuggingFace 向量化 | `cases/rag_knowledge_base.md` | - |
| **Vector Stores** | FAISS, Chroma, Milvus | `cases/rag_knowledge_base.md` | `scripts/rag_example.py` |
| **Retrievers** | 相似度/MMR/多查询检索 | `cases/rag_knowledge_base.md` | `scripts/rag_example.py` |
| **Tool 定义** | @tool 装饰器, StructuredTool | `cases/agent_tools.md` | `data/tool_schemas.json` |
| **Agent 类型** | ReAct, OpenAI Functions, Tool Calling | `cases/agent_tools.md` | `scripts/agent_example.py` |
| **AgentExecutor** | Agent 执行引擎 | `cases/agent_tools.md` | `scripts/agent_example.py` |
| **Memory** | 对话历史, ConversationBufferMemory | `cases/agent_tools.md` | - |
| **Streaming** | 流式输出 | `cases/basic_llm_chat.md` | `scripts/basic_examples.py` |
| **Callbacks** | 执行追踪, LangSmith | 所有案例 | - |

---

## 学习路径

```
基础模型 → LCEL 编排 → RAG 构建 → Agent 开发
    ↓          ↓           ↓           ↓
 LLM/Prompt  管道/Runnable 向量检索   工具/执行器
```

---

## 1.0 版本核心变化

| 特性 | 旧版本 | 1.0 版本 |
|------|--------|----------|
| **链组合** | `LLMChain`, `SequentialChain` | LCEL 管道 `\|` |
| **统一接口** | 各组件接口不统一 | 统一 Runnable 接口 |
| **包结构** | 单一 langchain 包 | 模块化拆分 |
| **流式输出** | 需额外配置 | 原生支持 `.stream()` |
| **异步支持** | 部分支持 | 全面异步 `.ainvoke()` |

---

## 快速验证

### 1. 安装

```bash
pip install langchain langchain-openai faiss-cpu
```

### 2. 基础调用

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("用一句话解释: {topic}")
chain = prompt | llm | StrOutputParser()

print(chain.invoke({"topic": "机器学习"}))
```

### 3. 流式输出

```python
for chunk in chain.stream({"topic": "深度学习"}):
    print(chunk, end="", flush=True)
```

---

## 相关资源

- [LangChain 官方文档](https://python.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [LangSmith 平台](https://smith.langchain.com/)
- [LCEL 概念文档](https://python.langchain.com/docs/expression_language/)
