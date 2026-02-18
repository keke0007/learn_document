# 案例：RAG 知识库问答

## 目标

掌握使用 LangChain 1.0 构建完整的 RAG（Retrieval-Augmented Generation）知识库问答系统。

---

## 知识点覆盖

- Document Loaders（文档加载）
- Text Splitters（文本分割）
- Embeddings（向量嵌入）
- Vector Stores（向量存储）
- Retrievers（检索器）
- RAG Chain 组装

---

## RAG 架构流程

```
┌─────────────────────────────────────────────────────────────┐
│                      索引阶段（Indexing）                     │
├─────────────────────────────────────────────────────────────┤
│  Documents → Loader → Splitter → Embeddings → VectorStore   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      查询阶段（Query）                        │
├─────────────────────────────────────────────────────────────┤
│  Query → Embedding → Retriever → Context + Prompt → LLM     │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Document Loaders

### 文本文件

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("data/sample_docs.txt", encoding="utf-8")
documents = loader.load()
print(f"加载了 {len(documents)} 个文档")
```

### PDF 文件

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("document.pdf")
pages = loader.load_and_split()
```

### 网页

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://example.com/article")
docs = loader.load()
```

### 目录批量加载

```python
from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader(
    "data/",
    glob="**/*.md",
    loader_cls=TextLoader
)
docs = loader.load()
```

### CSV/Excel

```python
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("data.csv", encoding="utf-8")
docs = loader.load()
```

---

## 2. Text Splitters

### 递归字符分割（推荐）

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # 每块最大字符数
    chunk_overlap=50,      # 块之间重叠字符数
    separators=["\n\n", "\n", "。", ".", " ", ""]
)

chunks = splitter.split_documents(documents)
print(f"分割成 {len(chunks)} 个块")
```

### 按 Token 分割

```python
from langchain_text_splitters import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)
```

### Markdown 分割

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
chunks = splitter.split_text(markdown_text)
```

---

## 3. Embeddings

### OpenAI Embeddings

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# 单个文本向量化
vector = embeddings.embed_query("这是一段测试文本")
print(f"向量维度: {len(vector)}")

# 批量向量化
vectors = embeddings.embed_documents([
    "文本1",
    "文本2",
    "文本3"
])
```

### HuggingFace Embeddings（本地）

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

---

## 4. Vector Stores

### FAISS（推荐入门）

```python
from langchain_community.vectorstores import FAISS

# 创建向量库
vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

# 保存到本地
vectorstore.save_local("faiss_index")

# 加载
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)
```

### Chroma（带元数据过滤）

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

# 带元数据过滤的检索
results = vectorstore.similarity_search(
    "查询内容",
    k=3,
    filter={"source": "doc1.txt"}
)
```

---

## 5. Retrievers

### 基础检索器

```python
# 从向量库创建检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",  # similarity / mmr / similarity_score_threshold
    search_kwargs={"k": 3}
)

# 检索
docs = retriever.invoke("什么是 LangChain？")
for doc in docs:
    print(doc.page_content[:100])
```

### MMR 检索（多样性）

```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20,  # 先检索 20 个，再 MMR 筛选 5 个
        "lambda_mult": 0.5  # 多样性参数 0-1
    }
)
```

### 相似度阈值

```python
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.7,
        "k": 5
    }
)
```

### 多查询检索器

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

multi_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm
)
# 会自动生成多个相关查询，合并结果
```

---

## 6. RAG Chain 组装

### 基础 RAG Chain

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# RAG Prompt
prompt = ChatPromptTemplate.from_template("""
根据以下上下文回答问题。如果上下文中没有相关信息，请说"我不知道"。

上下文：
{context}

问题：{question}

回答：
""")

# 格式化检索结果
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 使用
answer = rag_chain.invoke("LangChain 的主要特性是什么？")
print(answer)
```

### 带来源引用的 RAG

```python
from langchain_core.runnables import RunnableParallel

# 同时返回答案和来源
rag_chain_with_source = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
).assign(
    answer=lambda x: (
        prompt.format(
            context=format_docs(x["context"]),
            question=x["question"]
        )
        | llm
        | StrOutputParser()
    ).invoke({})
)

# 或更简洁的方式
def create_rag_with_source(retriever, llm):
    def get_answer_with_source(question):
        docs = retriever.invoke(question)
        context = format_docs(docs)
        answer = (prompt | llm | StrOutputParser()).invoke({
            "context": context,
            "question": question
        })
        return {
            "answer": answer,
            "sources": [doc.metadata.get("source", "unknown") for doc in docs]
        }
    return get_answer_with_source

rag_func = create_rag_with_source(retriever, llm)
result = rag_func("什么是 LCEL？")
print(f"答案: {result['answer']}")
print(f"来源: {result['sources']}")
```

### 对话式 RAG（带历史）

```python
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# 带历史的 Prompt
prompt_with_history = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识库助手。根据上下文回答问题。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", """
上下文：
{context}

问题：{question}
""")
])

# 历史感知的检索（重写查询）
contextualize_prompt = ChatPromptTemplate.from_messages([
    ("system", "根据对话历史重写用户问题，使其独立可理解。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

contextualize_chain = contextualize_prompt | llm | StrOutputParser()

def contextualize_question(input_dict):
    if input_dict.get("chat_history"):
        return contextualize_chain.invoke(input_dict)
    return input_dict["question"]

# 完整对话 RAG
conversational_rag = (
    RunnablePassthrough.assign(
        standalone_question=contextualize_question
    )
    | {
        "context": lambda x: retriever.invoke(x["standalone_question"]) | format_docs,
        "question": lambda x: x["standalone_question"],
        "chat_history": lambda x: x["chat_history"]
    }
    | prompt_with_history
    | llm
    | StrOutputParser()
)

# 使用
chat_history = []
question1 = "LangChain 是什么？"
answer1 = conversational_rag.invoke({
    "question": question1,
    "chat_history": chat_history
})
chat_history.extend([HumanMessage(content=question1), AIMessage(content=answer1)])

question2 = "它有哪些主要特性？"  # 代词指代上文的 LangChain
answer2 = conversational_rag.invoke({
    "question": question2,
    "chat_history": chat_history
})
print(answer2)
```

---

## 7. 完整示例

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. 加载文档
loader = TextLoader("data/sample_docs.txt", encoding="utf-8")
documents = loader.load()

# 2. 分割文档
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)
print(f"文档分割成 {len(chunks)} 个块")

# 3. 创建向量库
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("knowledge_base")

# 4. 创建检索器
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 5. 创建 RAG Chain
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt = ChatPromptTemplate.from_template("""
你是一个知识库问答助手。根据提供的上下文回答问题。
如果上下文中没有相关信息，请诚实地说"根据现有知识库，我无法回答这个问题"。

上下文：
{context}

问题：{question}

回答：
""")

def format_docs(docs):
    return "\n\n---\n\n".join(
        f"[来源: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 6. 测试
questions = [
    "什么是 LangChain？",
    "LCEL 的作用是什么？",
    "如何构建 RAG 系统？"
]

for q in questions:
    print(f"\n问题: {q}")
    answer = rag_chain.invoke(q)
    print(f"回答: {answer}")
```

---

## 验证步骤

1. **准备测试文档**：使用 `data/sample_docs.txt`
2. **运行索引流程**：验证文档加载、分割、向量化
3. **检查向量库**：验证保存和加载正常
4. **测试检索**：验证相关文档能被检索到
5. **测试 RAG Chain**：验证端到端问答

---

## 常见问题

### Q1: 检索结果不相关
- 调整 chunk_size 和 chunk_overlap
- 尝试 MMR 检索增加多样性
- 检查 embedding 模型是否适合中文

### Q2: 回答不准确
- 优化 Prompt，添加更多约束
- 增加检索的 k 值
- 考虑使用 reranker 重排序

### Q3: 向量库太大
- 使用更小维度的 embedding 模型
- 考虑使用 Milvus 等分布式向量库
