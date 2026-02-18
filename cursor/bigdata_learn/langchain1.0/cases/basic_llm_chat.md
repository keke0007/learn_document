# 案例：基础 LLM 与 Chat 模型

## 目标

掌握 LangChain 1.0 中 Chat Models、Prompt Templates、Output Parsers 的基本使用。

---

## 知识点覆盖

- ChatOpenAI / ChatAnthropic 模型初始化
- ChatPromptTemplate 模板定义
- StrOutputParser / JsonOutputParser 输出解析
- 流式输出（Streaming）
- 基础 LCEL 链组合

---

## 1. Chat Model 初始化

### OpenAI 模型

```python
from langchain_openai import ChatOpenAI

# 基础配置
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,          # 0-2，越低越确定
    max_tokens=1000,        # 最大输出 token
    timeout=30,             # 超时时间（秒）
    max_retries=2           # 重试次数
)

# 直接调用
response = llm.invoke("你好，请介绍一下自己")
print(response.content)
```

### 其他模型

```python
# Anthropic Claude
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-sonnet-20240229")

# 阿里通义千问
from langchain_community.chat_models import ChatTongyi
llm = ChatTongyi(model="qwen-turbo")

# 本地 Ollama
from langchain_community.chat_models import ChatOllama
llm = ChatOllama(model="llama3", base_url="http://localhost:11434")
```

---

## 2. Prompt Templates

### 简单字符串模板

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "请将以下内容翻译成{language}：\n{text}"
)

# 格式化
formatted = prompt.format(language="英文", text="你好世界")
print(formatted)
```

### Chat 消息模板（推荐）

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的{role}，请用{style}的方式回答问题。"),
    ("human", "{question}")
])

# 格式化
messages = prompt.format_messages(
    role="技术顾问",
    style="简洁专业",
    question="什么是 RAG？"
)
print(messages)
```

### 包含示例的模板

```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

examples = [
    {"input": "开心", "output": "happy"},
    {"input": "悲伤", "output": "sad"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译助手，将中文翻译成英文。"),
    few_shot_prompt,
    ("human", "{input}")
])
```

---

## 3. Output Parsers

### 字符串解析器

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

# 组合链
chain = prompt | llm | parser
result = chain.invoke({"question": "什么是 LangChain？"})
print(result)  # 直接返回字符串
```

### JSON 解析器

```python
from langchain_core.output_parsers import JsonOutputParser

# 定义期望的 JSON 结构
parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个数据提取助手，请从文本中提取信息并以 JSON 格式返回。"),
    ("human", """从以下文本中提取人名和年龄：
{text}

请返回 JSON 格式：{{"name": "xxx", "age": xx}}""")
])

chain = prompt | llm | parser
result = chain.invoke({"text": "张三今年25岁，是一名工程师"})
print(result)  # {"name": "张三", "age": 25}
```

### Pydantic 解析器（强类型）

```python
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

class Person(BaseModel):
    name: str = Field(description="人名")
    age: int = Field(description="年龄")
    skills: List[str] = Field(description="技能列表")

parser = PydanticOutputParser(pydantic_object=Person)

prompt = ChatPromptTemplate.from_messages([
    ("system", "提取人物信息。\n{format_instructions}"),
    ("human", "{text}")
])

chain = prompt.partial(
    format_instructions=parser.get_format_instructions()
) | llm | parser

result = chain.invoke({"text": "李四，30岁，擅长 Python 和 Java"})
print(result)  # Person(name='李四', age=30, skills=['Python', 'Java'])
```

---

## 4. 流式输出

### 基础流式

```python
chain = prompt | llm | StrOutputParser()

# 流式输出
for chunk in chain.stream({"question": "详细解释什么是机器学习"}):
    print(chunk, end="", flush=True)
```

### 异步流式

```python
import asyncio

async def stream_response():
    async for chunk in chain.astream({"question": "什么是深度学习"}):
        print(chunk, end="", flush=True)

asyncio.run(stream_response())
```

---

## 5. 完整示例：多功能助手

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 初始化
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 定义多种 Prompt
summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个摘要专家，请用3句话总结以下内容。"),
    ("human", "{text}")
])

translate_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译专家，请将内容翻译成{target_lang}。"),
    ("human", "{text}")
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识问答助手，请准确回答问题。"),
    ("human", "{question}")
])

# 创建链
summarize_chain = summarize_prompt | llm | StrOutputParser()
translate_chain = translate_prompt | llm | StrOutputParser()
qa_chain = qa_prompt | llm | StrOutputParser()

# 使用
text = """
LangChain 是一个用于开发由语言模型驱动的应用程序的框架。
它提供了一系列工具和抽象，使得开发者能够轻松地构建复杂的 LLM 应用。
主要特性包括：模型调用、提示管理、链式组合、RAG、Agent 等。
"""

# 摘要
summary = summarize_chain.invoke({"text": text})
print("摘要:", summary)

# 翻译
translation = translate_chain.invoke({"text": text, "target_lang": "英文"})
print("翻译:", translation)

# 问答
answer = qa_chain.invoke({"question": "LangChain 的主要特性有哪些？"})
print("回答:", answer)
```

---

## 验证步骤

1. **安装依赖**：`pip install langchain langchain-openai`
2. **配置 API Key**：设置 `OPENAI_API_KEY` 环境变量
3. **运行基础示例**：验证模型调用正常
4. **测试 Prompt 模板**：验证变量替换正确
5. **测试解析器**：验证 JSON/Pydantic 解析
6. **测试流式输出**：验证逐字输出效果

---

## 常见问题

### Q1: API Key 配置问题
```python
import os
os.environ["OPENAI_API_KEY"] = "sk-xxx"
# 或使用 python-dotenv 从 .env 文件加载
```

### Q2: 超时错误
```python
llm = ChatOpenAI(timeout=60, max_retries=3)
```

### Q3: 模型不支持某些参数
不同模型支持的参数不同，参考官方文档确认参数兼容性。
