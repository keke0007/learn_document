"""
LangChain 1.0 Agent 示例代码
"""
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


# ============================================
# 1. 定义工具
# ============================================
from langchain_core.tools import tool


@tool
def get_current_time() -> str:
    """获取当前时间。当用户询问现在几点或当前时间时使用。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def calculator(expression: str) -> str:
    """
    执行数学计算。
    输入应该是有效的数学表达式，如 '2+2'、'10*5'、'100/4'。
    """
    try:
        # 安全地计算表达式
        allowed_chars = set("0123456789+-*/().% ")
        if not all(c in allowed_chars for c in expression):
            return "错误：表达式包含不允许的字符"
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


@tool
def search_knowledge(query: str) -> str:
    """
    搜索知识库获取信息。
    当需要查找特定主题的信息时使用。
    """
    # 模拟知识库
    knowledge_base = {
        "langchain": "LangChain 是一个用于构建 LLM 应用的开源框架，支持 LCEL 链式编排、RAG 知识库、Agent 等功能。",
        "python": "Python 是一种广泛使用的高级编程语言，以其简洁易读的语法著称。",
        "机器学习": "机器学习是人工智能的一个分支，使计算机能够从数据中学习并做出决策。",
        "深度学习": "深度学习是机器学习的子集，使用多层神经网络来学习数据的复杂模式。",
        "rag": "RAG（检索增强生成）是一种结合检索和生成的技术，通过检索外部知识来增强 LLM 的回答能力。"
    }
    
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value
    
    return f"未找到关于 '{query}' 的信息"


@tool
def weather(city: str) -> str:
    """
    获取指定城市的天气信息。
    输入城市名称，返回天气情况。
    """
    # 模拟天气 API
    weather_data = {
        "北京": "晴，气温 25°C，湿度 40%",
        "上海": "多云，气温 28°C，湿度 65%",
        "广州": "雷阵雨，气温 30°C，湿度 80%",
        "深圳": "晴转多云，气温 29°C，湿度 70%"
    }
    return weather_data.get(city, f"{city}：数据暂不可用")


# ============================================
# 2. 创建 Tool Calling Agent
# ============================================
def create_tool_calling_agent_example():
    """创建 Tool Calling Agent 示例"""
    from langchain_openai import ChatOpenAI
    from langchain.agents import create_tool_calling_agent, AgentExecutor
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    
    print("\n" + "=" * 50)
    print("Tool Calling Agent 示例")
    print("=" * 50)
    
    # 工具列表
    tools = [get_current_time, calculator, search_knowledge, weather]
    
    # LLM（需要支持 tool calling）
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个智能助手，可以使用以下工具帮助用户：
1. get_current_time: 获取当前时间
2. calculator: 进行数学计算
3. search_knowledge: 搜索知识库
4. weather: 查询天气

请根据用户的问题选择合适的工具。如果不需要工具，直接回答即可。"""),
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
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )
    
    return agent_executor


def test_agent(agent_executor):
    """测试 Agent"""
    test_questions = [
        "现在几点了？",
        "计算 25 * 4 + 100",
        "北京今天天气怎么样？",
        "什么是 LangChain？",
        "先告诉我现在的时间，然后计算 2024 减去当前年份"
    ]
    
    for question in test_questions:
        print(f"\n{'='*50}")
        print(f"问题: {question}")
        print("=" * 50)
        
        result = agent_executor.invoke({"input": question})
        print(f"\n最终回答: {result['output']}")


# ============================================
# 3. 带对话历史的 Agent
# ============================================
def create_agent_with_memory():
    """创建带对话历史的 Agent"""
    from langchain_openai import ChatOpenAI
    from langchain.agents import create_tool_calling_agent, AgentExecutor
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import HumanMessage, AIMessage
    
    print("\n" + "=" * 50)
    print("带对话历史的 Agent 示例")
    print("=" * 50)
    
    tools = [get_current_time, calculator, search_knowledge, weather]
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个智能助手，可以使用工具帮助用户。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )
    
    # 对话历史
    chat_history = []
    
    # 多轮对话
    conversations = [
        "北京天气怎么样？",
        "那上海呢？",
        "帮我计算这两个城市温度的平均值"
    ]
    
    for question in conversations:
        print(f"\n用户: {question}")
        
        result = agent_executor.invoke({
            "input": question,
            "chat_history": chat_history
        })
        
        print(f"助手: {result['output']}")
        
        # 更新历史
        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=result['output']))


# ============================================
# 4. ReAct Agent 示例
# ============================================
def create_react_agent_example():
    """创建 ReAct Agent 示例"""
    from langchain_openai import ChatOpenAI
    from langchain.agents import create_react_agent, AgentExecutor
    from langchain import hub
    
    print("\n" + "=" * 50)
    print("ReAct Agent 示例")
    print("=" * 50)
    
    tools = [get_current_time, calculator, search_knowledge]
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    # 使用官方 ReAct prompt
    prompt = hub.pull("hwchase17/react")
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )
    
    # 测试
    question = "什么是 RAG？它和 LangChain 有什么关系？"
    print(f"\n问题: {question}")
    
    result = agent_executor.invoke({"input": question})
    print(f"\n最终回答: {result['output']}")


# ============================================
# 5. 自定义复杂工具
# ============================================
def create_complex_tools_example():
    """复杂工具定义示例"""
    from langchain_core.tools import StructuredTool
    from pydantic import BaseModel, Field
    from typing import Optional
    
    print("\n" + "=" * 50)
    print("复杂工具定义示例")
    print("=" * 50)
    
    # 使用 Pydantic 定义输入 schema
    class OrderInput(BaseModel):
        order_id: str = Field(description="订单 ID")
        action: str = Field(description="操作类型: query/cancel/track")
    
    def process_order(order_id: str, action: str) -> str:
        """处理订单操作"""
        if action == "query":
            return f"订单 {order_id} 状态: 已发货，预计明天送达"
        elif action == "cancel":
            return f"订单 {order_id} 已取消，退款将在3-5个工作日内到账"
        elif action == "track":
            return f"订单 {order_id} 物流: 北京 -> 上海，当前位于南京中转站"
        else:
            return f"不支持的操作: {action}"
    
    order_tool = StructuredTool.from_function(
        func=process_order,
        name="order_management",
        description="订单管理工具，支持查询(query)、取消(cancel)、追踪(track)操作",
        args_schema=OrderInput
    )
    
    # 测试工具
    print(f"工具名称: {order_tool.name}")
    print(f"工具描述: {order_tool.description}")
    print(f"参数 schema: {order_tool.args}")
    
    # 调用工具
    result = order_tool.invoke({"order_id": "ORD12345", "action": "query"})
    print(f"\n调用结果: {result}")


# ============================================
# 主函数
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("LangChain 1.0 Agent 示例")
    print("=" * 50)
    
    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY 环境变量")
        exit(1)
    
    # 1. Tool Calling Agent
    agent_executor = create_tool_calling_agent_example()
    test_agent(agent_executor)
    
    # 2. 带对话历史的 Agent
    create_agent_with_memory()
    
    # 3. ReAct Agent（需要网络访问 hub）
    try:
        create_react_agent_example()
    except Exception as e:
        print(f"ReAct Agent 示例跳过: {e}")
    
    # 4. 复杂工具定义
    create_complex_tools_example()
    
    print("\n" + "=" * 50)
    print("Agent 示例执行完成！")
