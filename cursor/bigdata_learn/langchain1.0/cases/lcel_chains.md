# 案例：LCEL 链式编排

## 目标

掌握 LangChain Expression Language (LCEL) 的管道操作符、Runnable 接口和高级编排模式。

---

## 知识点覆盖

- 管道操作符 `|` 基础
- Runnable 统一接口（invoke, batch, stream, ainvoke）
- RunnablePassthrough（透传输入）
- RunnableLambda（自定义函数）
- RunnableParallel（并行执行）
- RunnableBranch（条件路由）
- 错误处理与回退

---

## 1. LCEL 基础

### 管道操作符

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("用一句话解释: {topic}")
parser = StrOutputParser()

# 使用 | 组合
chain = prompt | llm | parser

# 等价于
# chain = prompt.pipe(llm).pipe(parser)
```

### Runnable 统一接口

所有 LCEL 组件都实现 Runnable 接口：

```python
# 单次调用
result = chain.invoke({"topic": "量子计算"})

# 批量调用
results = chain.batch([
    {"topic": "机器学习"},
    {"topic": "深度学习"},
    {"topic": "强化学习"}
])

# 流式输出
for chunk in chain.stream({"topic": "神经网络"}):
    print(chunk, end="")

# 异步调用
import asyncio
result = asyncio.run(chain.ainvoke({"topic": "自然语言处理"}))

# 异步批量
results = asyncio.run(chain.abatch([{"topic": "CV"}, {"topic": "NLP"}]))
```

---

## 2. RunnablePassthrough

透传输入数据，常用于 RAG 场景：

```python
from langchain_core.runnables import RunnablePassthrough

# 场景：需要同时传递 context 和原始 question
prompt = ChatPromptTemplate.from_template("""
根据以下上下文回答问题：
上下文：{context}
问题：{question}
""")

# retriever 返回 context，question 直接透传
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 调用时只需传入 question
result = chain.invoke("什么是 LCEL？")
```

### 使用 assign 添加字段

```python
from langchain_core.runnables import RunnablePassthrough

chain = (
    RunnablePassthrough.assign(
        word_count=lambda x: len(x["text"].split())
    )
    | prompt
    | llm
)

# 输入 {"text": "hello world"} 
# 变成 {"text": "hello world", "word_count": 2}
```

---

## 3. RunnableLambda

将普通函数包装为 Runnable：

```python
from langchain_core.runnables import RunnableLambda

# 自定义处理函数
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def add_metadata(text):
    return f"[处理时间: {datetime.now()}]\n{text}"

# 包装为 Runnable
format_runnable = RunnableLambda(format_docs)
metadata_runnable = RunnableLambda(add_metadata)

# 在链中使用
chain = retriever | format_runnable | prompt | llm | metadata_runnable
```

### 异步函数

```python
async def async_process(text):
    await asyncio.sleep(0.1)  # 模拟异步操作
    return text.upper()

# 同时支持同步和异步
runnable = RunnableLambda(
    func=lambda x: x.upper(),
    afunc=async_process
)
```

---

## 4. RunnableParallel

并行执行多个链：

```python
from langchain_core.runnables import RunnableParallel

# 定义多个处理链
summary_chain = summary_prompt | llm | StrOutputParser()
keywords_chain = keywords_prompt | llm | StrOutputParser()
sentiment_chain = sentiment_prompt | llm | StrOutputParser()

# 并行执行
parallel = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
    sentiment=sentiment_chain
)

# 调用
result = parallel.invoke({"text": "这是一段需要分析的文本..."})
print(result)
# {
#   "summary": "...",
#   "keywords": "...",
#   "sentiment": "..."
# }
```

### 使用字典简写

```python
# 等价写法
chain = (
    {
        "summary": summary_chain,
        "keywords": keywords_chain,
        "original": RunnablePassthrough()
    }
    | combine_prompt
    | llm
)
```

---

## 5. RunnableBranch

条件路由，根据输入选择不同链：

```python
from langchain_core.runnables import RunnableBranch

# 定义不同领域的链
tech_prompt = ChatPromptTemplate.from_template("作为技术专家回答: {question}")
business_prompt = ChatPromptTemplate.from_template("作为商业顾问回答: {question}")
general_prompt = ChatPromptTemplate.from_template("回答问题: {question}")

tech_chain = tech_prompt | llm | StrOutputParser()
business_chain = business_prompt | llm | StrOutputParser()
general_chain = general_prompt | llm | StrOutputParser()

# 条件路由
def is_tech_question(x):
    keywords = ["代码", "编程", "API", "数据库", "算法"]
    return any(k in x["question"] for k in keywords)

def is_business_question(x):
    keywords = ["市场", "营销", "销售", "财务", "投资"]
    return any(k in x["question"] for k in keywords)

branch = RunnableBranch(
    (is_tech_question, tech_chain),
    (is_business_question, business_chain),
    general_chain  # 默认链
)

# 使用
result = branch.invoke({"question": "如何优化数据库查询？"})
```

### 使用 Router 实现更复杂路由

```python
from langchain_core.runnables import RouterRunnable

# 定义路由映射
routes = {
    "tech": tech_chain,
    "business": business_chain,
    "general": general_chain
}

# 分类链决定路由
classify_prompt = ChatPromptTemplate.from_template("""
将以下问题分类为: tech, business, general
问题: {question}
只返回分类名称。
""")

classify_chain = classify_prompt | llm | StrOutputParser()

# 完整路由链
full_chain = (
    {"question": RunnablePassthrough(), "route": classify_chain}
    | RunnableLambda(lambda x: routes[x["route"].strip()].invoke(x))
)
```

---

## 6. 错误处理与回退

### with_fallbacks

```python
# 主模型
main_llm = ChatOpenAI(model="gpt-4")
# 回退模型
fallback_llm = ChatOpenAI(model="gpt-3.5-turbo")

# 带回退的链
robust_llm = main_llm.with_fallbacks([fallback_llm])

chain = prompt | robust_llm | parser
```

### with_retry

```python
# 自动重试
chain_with_retry = chain.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)
```

### 异常处理

```python
from langchain_core.runnables import RunnableLambda

def safe_parse(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "解析失败", "raw": text}

safe_parser = RunnableLambda(safe_parse)
chain = prompt | llm | safe_parser
```

---

## 7. 完整示例：智能文档处理

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel,
    RunnableBranch
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 文档分类
classify_prompt = ChatPromptTemplate.from_template("""
判断以下文档类型: 合同, 报告, 邮件, 其他
文档: {text}
只返回类型名称。
""")

# 不同类型的处理 Prompt
contract_prompt = ChatPromptTemplate.from_template("""
从合同中提取关键信息（JSON格式）:
- parties: 合同双方
- date: 签订日期
- amount: 金额
- terms: 主要条款

合同内容: {text}
""")

report_prompt = ChatPromptTemplate.from_template("""
总结报告的要点:
{text}
""")

email_prompt = ChatPromptTemplate.from_template("""
提取邮件信息:
- 发件人意图
- 需要回复的问题
- 优先级

邮件: {text}
""")

# 分类链
classify_chain = classify_prompt | llm | StrOutputParser()

# 处理链
contract_chain = contract_prompt | llm | JsonOutputParser()
report_chain = report_prompt | llm | StrOutputParser()
email_chain = email_prompt | llm | StrOutputParser()
default_chain = RunnableLambda(lambda x: {"summary": x["text"][:200]})

# 路由分支
process_branch = RunnableBranch(
    (lambda x: "合同" in x["doc_type"], contract_chain),
    (lambda x: "报告" in x["doc_type"], report_chain),
    (lambda x: "邮件" in x["doc_type"], email_chain),
    default_chain
)

# 完整处理链
full_chain = (
    RunnablePassthrough.assign(doc_type=classify_chain)
    | RunnableParallel(
        doc_type=lambda x: x["doc_type"],
        result=process_branch,
        original_length=lambda x: len(x["text"])
    )
)

# 使用
doc = """
本合同由甲方（北京科技有限公司）与乙方（上海数据服务有限公司）
于2024年1月15日签订。甲方向乙方支付服务费用人民币50万元整...
"""

result = full_chain.invoke({"text": doc})
print(result)
```

---

## 验证步骤

1. **基础链测试**：验证 `|` 操作符组合正常
2. **Runnable 接口**：分别测试 invoke/batch/stream
3. **Passthrough**：验证数据透传和 assign 功能
4. **Lambda**：验证自定义函数包装
5. **Parallel**：验证并行执行结果合并
6. **Branch**：验证条件路由正确选择

---

## 调试技巧

### 查看链结构

```python
print(chain.get_graph().print_ascii())
```

### 启用 LangSmith 追踪

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-key"
```

### 中间结果打印

```python
def debug_print(x):
    print(f"DEBUG: {x}")
    return x

chain = (
    prompt
    | RunnableLambda(debug_print)
    | llm
    | RunnableLambda(debug_print)
    | parser
)
```
