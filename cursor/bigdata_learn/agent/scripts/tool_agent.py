"""
Tool Agent 示例
演示如何创建和使用自定义 Tools
"""

from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.tools import Tool, tool
from typing import Dict
import json

llm = OpenAI(temperature=0)

# 方法1：使用 Tool 类
def get_weather(city: str) -> str:
    """获取天气信息"""
    weather_data = {
        "北京": "晴天，25°C，湿度60%",
        "上海": "多云，22°C，湿度70%",
        "广州": "雨天，28°C，湿度80%",
        "深圳": "晴天，30°C，湿度65%"
    }
    return weather_data.get(city, f"未找到{city}的天气信息")

weather_tool = Tool(
    name="Weather",
    func=get_weather,
    description="获取指定城市的天气信息，输入城市名称，例如：北京、上海"
)

# 方法2：使用 @tool 装饰器
@tool
def get_user_info(user_id: str) -> str:
    """获取用户信息"""
    users = {
        "1": {"name": "Alice", "age": 25, "role": "developer"},
        "2": {"name": "Bob", "age": 30, "role": "data_scientist"}
    }
    user = users.get(user_id)
    if user:
        return json.dumps(user, ensure_ascii=False)
    return f"未找到用户 ID: {user_id}"

@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        # 实际应用中应使用更安全的计算方法
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误：{str(e)}"

# 方法3：复杂 Tool（带多个参数）
def database_query(query: str) -> str:
    """数据库查询工具"""
    # 模拟数据库查询结果
    results = {
        "SELECT * FROM users LIMIT 2": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ],
        "SELECT COUNT(*) FROM users": 100
    }
    return json.dumps(results.get(query, []), ensure_ascii=False)

db_tool = Tool(
    name="DatabaseQuery",
    func=database_query,
    description="执行数据库查询，输入 SQL 查询语句"
)

# 组合所有工具
tools = [weather_tool, get_user_info, calculate, db_tool]

# 创建 Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 使用示例
if __name__ == "__main__":
    # 查询天气
    result1 = agent.run("查询北京的天气")
    print(f"\n结果1: {result1}\n")
    
    # 查询用户信息
    result2 = agent.run("获取用户 ID 为 1 的信息")
    print(f"\n结果2: {result2}\n")
    
    # 计算
    result3 = agent.run("计算 123 + 456 的结果")
    print(f"\n结果3: {result3}\n")
    
    # 数据库查询
    result4 = agent.run("查询用户表中的前2条记录")
    print(f"\n结果4: {result4}\n")
