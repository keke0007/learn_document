"""
基础 Agent 示例
演示如何创建和使用 LangChain Agent
"""

from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool

# 初始化 LLM
llm = OpenAI(temperature=0)
# 或使用 Chat Model
# chat_llm = ChatOpenAI(temperature=0)

# 定义工具
def search_tool(query: str) -> str:
    """搜索工具"""
    # 模拟搜索功能
    results = {
        "LangChain": "LangChain 是一个用于构建 LLM 应用的框架",
        "Python": "Python 是一种高级编程语言",
        "AI": "人工智能是模拟人类智能的技术"
    }
    return results.get(query, f"未找到关于'{query}'的信息")

def calculator(expression: str) -> str:
    """计算器工具"""
    try:
        # 安全计算（实际应用中应使用更安全的方法）
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误：{str(e)}"

# 创建工具列表
tools = [
    Tool(
        name="Search",
        func=search_tool,
        description="用于搜索信息的工具，输入搜索关键词"
    ),
    Tool(
        name="Calculator",
        func=calculator,
        description="执行数学计算，输入数学表达式，例如：2+2, 10*5"
    )
]

# 创建 ReAct Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,  # 显示详细执行过程
    max_iterations=5  # 最大迭代次数
)

# 使用 Agent
if __name__ == "__main__":
    # 简单任务
    result1 = agent.run("什么是 LangChain?")
    print(f"\n结果1: {result1}\n")
    
    # 使用工具的任务
    result2 = agent.run("计算 25 * 4 的结果")
    print(f"\n结果2: {result2}\n")
    
    # 复杂任务
    result3 = agent.run("搜索 LangChain 的信息，然后计算 100 除以 4")
    print(f"\n结果3: {result3}\n")
