# Memory 管理案例

## 案例概述

本案例通过实际代码演示 LangChain 中的 Memory 管理，包括不同类型的 Memory 和使用场景。

## 知识点

1. **Memory 类型**
   - ConversationBufferMemory
   - ConversationSummaryMemory
   - ConversationBufferWindowMemory
   - ConversationSummaryBufferMemory

2. **Memory 应用**
   - 对话历史管理
   - 上下文保持
   - 记忆优化

## 案例代码

### 案例1：ConversationBufferMemory

```python
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType

# 基础 Memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 手动保存上下文
memory.save_context(
    {"input": "你好，我是 Alice"},
    {"output": "你好 Alice！很高兴认识你"}
)

memory.save_context(
    {"input": "我的名字是什么？"},
    {"output": "你的名字是 Alice"}
)

# 获取历史记录
history = memory.buffer
print(history)

# 在 Agent 中使用
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)
```

### 案例2：ConversationSummaryMemory

```python
from langchain.memory import ConversationSummaryMemory
from langchain.llms import OpenAI

# 摘要 Memory
summary_memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)

# 保存多轮对话
summary_memory.save_context(
    {"input": "什么是机器学习？"},
    {"output": "机器学习是人工智能的一个分支..."}
)

summary_memory.save_context(
    {"input": "它有哪些应用？"},
    {"output": "机器学习在图像识别、自然语言处理等领域有广泛应用"}
)

# 获取摘要
summary = summary_memory.buffer
print(summary)
```

### 案例3：ConversationBufferWindowMemory

```python
from langchain.memory import ConversationBufferWindowMemory

# 窗口 Memory（只保留最近 N 轮对话）
window_memory = ConversationBufferWindowMemory(
    k=3,  # 保留最近3轮对话
    memory_key="chat_history",
    return_messages=True
)

# 保存多轮对话
for i in range(5):
    window_memory.save_context(
        {"input": f"问题 {i+1}"},
        {"output": f"回答 {i+1}"}
    )

# 只保留最近3轮
history = window_memory.buffer
print(f"保留的对话轮数：{len(history)}")
```

### 案例4：ConversationSummaryBufferMemory

```python
from langchain.memory import ConversationSummaryBufferMemory

# 摘要缓冲 Memory
summary_buffer_memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=1000,  # 最大 token 数
    memory_key="chat_history",
    return_messages=True
)

# 自动管理：超过限制时自动摘要
for i in range(10):
    summary_buffer_memory.save_context(
        {"input": f"问题 {i+1}"},
        {"output": f"回答 {i+1}"}
    )
```

### 案例5：Entity Memory

```python
from langchain.memory import ConversationEntityMemory

# 实体 Memory（记住实体信息）
entity_memory = ConversationEntityMemory(
    llm=llm,
    memory_key="chat_history"
)

# 保存包含实体的对话
entity_memory.save_context(
    {"input": "我的名字是 Alice，我25岁"},
    {"output": "好的，我记住了你的信息"}
)

entity_memory.save_context(
    {"input": "我多大了？"},
    {"output": "你25岁"}
)
```

### 案例6：Memory 链式使用

```python
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

# 创建对话链
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template="""以下是对话历史：
{history}

当前输入：{input}
助手回答："""
)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True
)

# 多轮对话
response1 = conversation.predict(input="你好")
response2 = conversation.predict(input="我的名字是 Bob")
response3 = conversation.predict(input="我的名字是什么？")
```

## 验证数据

### Memory 性能对比

| Memory 类型 | 内存占用 | 响应时间 | 适用场景 |
|------------|---------|---------|---------|
| Buffer | 高 | 快 | 短对话 |
| Summary | 中 | 中等 | 长对话 |
| Window | 中 | 快 | 限制历史 |
| SummaryBuffer | 中 | 中等 | 长对话优化 |

### Token 使用统计

```
Buffer Memory：随对话增长线性增长
Summary Memory：固定大小，摘要压缩
Window Memory：固定大小，截断历史
```

## 总结

1. **Memory 选择**
   - 短对话：Buffer Memory
   - 长对话：Summary Memory
   - 限制历史：Window Memory
   - 平衡：SummaryBuffer Memory

2. **优化建议**
   - 合理设置窗口大小
   - 使用摘要减少 token
   - 定期清理历史记录

3. **最佳实践**
   - 根据场景选择 Memory
   - 监控 token 使用
   - 优化 Memory 配置
