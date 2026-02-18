# LangChain 常见问题知识库

## 安装与配置

### Q: 如何安装 LangChain？
A: 使用 pip 安装：
```bash
pip install langchain langchain-openai langchain-community
```

### Q: 如何配置 OpenAI API Key？
A: 有两种方式：
1. 环境变量：`export OPENAI_API_KEY="sk-xxx"`
2. 代码中设置：`os.environ["OPENAI_API_KEY"] = "sk-xxx"`

### Q: 支持哪些 LLM 提供商？
A: 支持 OpenAI、Anthropic、Google、阿里通义、智谱 AI、Ollama 本地模型等众多提供商。

---

## LCEL 相关

### Q: 什么是 LCEL？
A: LCEL（LangChain Expression Language）是 LangChain 1.0 引入的链式编排语法，使用 `|` 操作符组合组件，所有组件实现统一的 Runnable 接口。

### Q: LCEL 有什么优势？
A: 主要优势包括：
- 代码简洁易读
- 原生流式输出支持
- 原生异步支持
- 自动并行执行
- 内置重试和回退

### Q: 如何在 LCEL 中实现条件分支？
A: 使用 RunnableBranch：
```python
from langchain_core.runnables import RunnableBranch
branch = RunnableBranch(
    (condition1, chain1),
    (condition2, chain2),
    default_chain
)
```

---

## RAG 相关

### Q: 什么是 RAG？
A: RAG（Retrieval-Augmented Generation）是检索增强生成的缩写，通过检索外部知识库来增强 LLM 的回答能力，解决 LLM 知识截止和幻觉问题。

### Q: chunk_size 应该设置多大？
A: 一般建议 500-1000 字符，需要根据具体场景调整：
- 较小的 chunk：检索更精确，但可能丢失上下文
- 较大的 chunk：上下文更完整，但可能引入噪音

### Q: 如何提高 RAG 的准确性？
A: 可以尝试：
1. 优化文档分割策略
2. 使用 MMR 检索增加多样性
3. 添加 Reranker 重排序
4. 优化 Prompt 设计
5. 调整检索数量 k

---

## Agent 相关

### Q: Agent 和 Chain 有什么区别？
A: Chain 是预定义的固定流程，而 Agent 可以根据输入动态决定使用哪些工具和执行步骤，更加灵活。

### Q: 如何定义自定义工具？
A: 使用 @tool 装饰器：
```python
from langchain_core.tools import tool

@tool
def my_tool(input: str) -> str:
    """工具描述"""
    return result
```

### Q: Agent 陷入死循环怎么办？
A: 设置 max_iterations 参数限制最大迭代次数：
```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=5
)
```

---

## 性能优化

### Q: 如何减少 API 调用成本？
A: 可以：
1. 使用较便宜的模型（如 gpt-3.5-turbo）
2. 减少 Prompt 长度
3. 使用缓存
4. 批量处理请求

### Q: 如何实现流式输出？
A: 使用 stream 方法：
```python
for chunk in chain.stream({"input": "..."}):
    print(chunk, end="", flush=True)
```

### Q: 如何处理长文档？
A: 使用 Text Splitter 分割文档，配合 Map-Reduce 或 Refine 策略处理。

---

## 调试与监控

### Q: 如何调试 LangChain 应用？
A: 推荐使用 LangSmith 平台，设置环境变量：
```python
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"
```

### Q: 如何查看链的执行过程？
A: 设置 verbose=True 或使用 LangSmith 查看详细 trace。
