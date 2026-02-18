# 案例：Agent 与工具调用

## 目标

掌握 LangChain 1.0 中 Tool 定义、Agent 类型和 AgentExecutor 的使用。

---

## 知识点覆盖

- Tool 定义（@tool 装饰器、StructuredTool）
- Agent 类型（ReAct、OpenAI Functions、Tool Calling）
- AgentExecutor 执行引擎
- Memory 对话历史
- 自定义工具开发

---

## 1. Tool 定义

### @tool 装饰器（简单）

```python
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """搜索网络获取信息。输入应该是搜索关键词。"""
    # 模拟搜索
    return f"搜索结果: 关于 '{query}' 的信息..."

@tool
def calculator(expression: str) -> str:
    """计算数学表达式。输入应该是有效的数学表达式，如 '2 + 2' 或 '10 * 5'。"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"

# 查看工具信息
print(search.name)        # search
print(search.description) # 搜索网络获取信息...
print(search.args)        # {'query': {'title': 'Query', 'type': 'string'}}
```

### 带类型注解的 Tool

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional

class SearchInput(BaseModel):
    query: str = Field(description="搜索关键词")
    max_results: int = Field(default=5, description="最大结果数")
    language: Optional[str] = Field(default="zh", description="语言")

@tool(args_schema=SearchInput)
def advanced_search(query: str, max_results: int = 5, language: str = "zh") -> str:
    """高级搜索功能，支持指定结果数量和语言。"""
    return f"搜索 '{query}'，返回 {max_results} 条 {language} 结果"
```

### StructuredTool（更灵活）

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    city: str = Field(description="城市名称")
    date: str = Field(default="today", description="日期，格式 YYYY-MM-DD")

def get_weather(city: str, date: str = "today") -> str:
    """获取指定城市的天气信息"""
    # 模拟天气 API
    return f"{city} 在 {date} 的天气: 晴，25°C"

weather_tool = StructuredTool.from_function(
    func=get_weather,
    name="weather",
    description="获取城市天气信息",
    args_schema=WeatherInput
)
```

### 异步工具

```python
import asyncio
from langchain_core.tools import tool

@tool
async def async_search(query: str) -> str:
    """异步搜索"""
    await asyncio.sleep(1)  # 模拟网络请求
    return f"异步搜索结果: {query}"
```

---

## 2. Agent 类型

### Tool Calling Agent（推荐，1.0 新方式）

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 准备工具
tools = [search, calculator, weather_tool]

# 初始化 LLM（需要支持 tool calling）
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 创建 Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的助手，可以使用工具来回答问题。"),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# 创建 Agent
agent = create_tool_calling_agent(llm, tools, prompt)

# 创建执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # 打印执行过程
    max_iterations=5
)

# 运行
result = agent_executor.invoke({
    "input": "北京今天天气怎么样？"
})
print(result["output"])
```

### ReAct Agent

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# 使用官方 ReAct Prompt
prompt = hub.pull("hwchase17/react")

# 创建 ReAct Agent
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

result = agent_executor.invoke({"input": "计算 25 * 4 + 10"})
```

### OpenAI Functions Agent（旧方式，兼容）

```python
from langchain.agents import create_openai_functions_agent

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个助手"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

---

## 3. Memory 对话历史

### 使用 chat_history

```python
from langchain_core.messages import HumanMessage, AIMessage

# 带记忆的 Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的助手。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 维护对话历史
chat_history = []

# 第一轮对话
result1 = agent_executor.invoke({
    "input": "北京天气怎么样？",
    "chat_history": chat_history
})
chat_history.append(HumanMessage(content="北京天气怎么样？"))
chat_history.append(AIMessage(content=result1["output"]))

# 第二轮对话（引用上文）
result2 = agent_executor.invoke({
    "input": "那上海呢？",  # 指代天气
    "chat_history": chat_history
})
print(result2["output"])
```

### 使用 RunnableWithMessageHistory

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# 存储会话历史
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 包装 Agent
agent_with_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

# 使用（自动管理历史）
result = agent_with_history.invoke(
    {"input": "你好"},
    config={"configurable": {"session_id": "user123"}}
)
```

---

## 4. 实用工具示例

### 网络搜索工具

```python
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
result = search.invoke("LangChain 最新版本")
```

### 数据库查询工具

```python
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

db = SQLDatabase.from_uri("sqlite:///data.db")
query_tool = QuerySQLDataBaseTool(db=db)
```

### 自定义 API 工具

```python
import requests
from langchain_core.tools import tool

@tool
def get_stock_price(symbol: str) -> str:
    """获取股票实时价格。输入股票代码如 AAPL、GOOGL。"""
    # 模拟 API 调用
    # response = requests.get(f"https://api.example.com/stock/{symbol}")
    return f"{symbol} 当前价格: $150.00"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """发送邮件。需要收件人、主题和正文。"""
    # 模拟发送
    return f"邮件已发送到 {to}"
```

---

## 5. 完整示例：智能助手

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from datetime import datetime
import json

# 定义工具
@tool
def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculator(expression: str) -> str:
    """计算数学表达式。输入如 '2+2' 或 '10*5'"""
    try:
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {e}"

@tool
def search_knowledge(query: str) -> str:
    """搜索知识库获取信息"""
    # 模拟知识库搜索
    knowledge = {
        "langchain": "LangChain 是一个用于构建 LLM 应用的框架",
        "python": "Python 是一种广泛使用的编程语言",
        "ai": "人工智能是计算机科学的一个分支"
    }
    for key, value in knowledge.items():
        if key in query.lower():
            return value
    return "未找到相关信息"

@tool
def create_reminder(content: str, time: str) -> str:
    """创建提醒。content 是提醒内容，time 是提醒时间"""
    return f"已创建提醒: '{content}' 于 {time}"

# 准备工具列表
tools = [get_current_time, calculator, search_knowledge, create_reminder]

# 初始化 LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 创建 Prompt
system_prompt = """你是一个智能助手，可以使用以下工具帮助用户：
1. get_current_time: 获取当前时间
2. calculator: 进行数学计算
3. search_knowledge: 搜索知识库
4. create_reminder: 创建提醒

请根据用户需求选择合适的工具。如果不需要工具，直接回答即可。
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# 创建 Agent
agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
    handle_parsing_errors=True
)

# 交互式对话
def chat():
    chat_history = []
    print("智能助手已启动，输入 'quit' 退出\n")
    
    while True:
        user_input = input("你: ")
        if user_input.lower() == 'quit':
            break
        
        result = agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history
        })
        
        print(f"\n助手: {result['output']}\n")
        
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=result['output']))

if __name__ == "__main__":
    chat()
```

---

## 6. 流式输出 Agent

```python
# 流式输出 Agent 执行过程
async def stream_agent():
    async for event in agent_executor.astream_events(
        {"input": "计算 100 除以 5，然后告诉我现在的时间"},
        version="v1"
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                print(content, end="", flush=True)
        elif kind == "on_tool_start":
            print(f"\n[调用工具: {event['name']}]")
        elif kind == "on_tool_end":
            print(f"[工具结果: {event['data']['output']}]\n")

import asyncio
asyncio.run(stream_agent())
```

---

## 验证步骤

1. **定义简单工具**：验证 @tool 装饰器
2. **测试工具调用**：验证 Agent 能正确选择和调用工具
3. **测试多步推理**：验证 Agent 能完成需要多个工具的任务
4. **测试对话记忆**：验证上下文引用正常
5. **测试错误处理**：验证工具异常时的处理

---

## 常见问题

### Q1: Agent 不调用工具
- 检查工具描述是否清晰
- 确保 LLM 支持 tool calling
- 调整 system prompt

### Q2: 工具调用失败
- 检查工具参数类型
- 添加 handle_parsing_errors=True
- 查看 verbose 输出定位问题

### Q3: 死循环
- 设置 max_iterations 限制
- 优化工具描述避免歧义
