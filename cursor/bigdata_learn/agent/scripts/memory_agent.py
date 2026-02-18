"""
Memory Agent 示例
演示如何使用 Memory 管理对话历史
"""

from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)
from langchain.tools import Tool

llm = OpenAI(temperature=0)

# 定义简单工具
def search_tool(query: str) -> str:
    """搜索工具"""
    return f"关于'{query}'的搜索结果..."

tools = [
    Tool(
        name="Search",
        func=search_tool,
        description="搜索工具"
    )
]

# 示例1：ConversationBufferMemory（保存所有对话）
print("=== ConversationBufferMemory ===")
buffer_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

buffer_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=buffer_memory,
    verbose=True
)

# 多轮对话
result1 = buffer_agent.run("我的名字是 Alice")
print(f"结果1: {result1}\n")

result2 = buffer_agent.run("我的名字是什么？")
print(f"结果2: {result2}\n")

# 示例2：ConversationSummaryMemory（摘要对话）
print("\n=== ConversationSummaryMemory ===")
summary_memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)

summary_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=summary_memory,
    verbose=True
)

result3 = summary_agent.run("什么是机器学习？")
print(f"结果3: {result3}\n")

result4 = summary_agent.run("它有哪些应用？")
print(f"结果4: {result4}\n")

# 示例3：ConversationBufferWindowMemory（窗口记忆）
print("\n=== ConversationBufferWindowMemory ===")
window_memory = ConversationBufferWindowMemory(
    k=2,  # 只保留最近2轮对话
    memory_key="chat_history",
    return_messages=True
)

window_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=window_memory,
    verbose=True
)

# 多轮对话（只保留最近2轮）
for i in range(4):
    result = window_agent.run(f"这是第 {i+1} 轮对话")
    print(f"结果 {i+1}: {result}\n")
