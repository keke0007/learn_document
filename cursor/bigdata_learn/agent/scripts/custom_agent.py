"""
自定义 Agent 示例
演示如何创建自定义 Agent
"""

from langchain.agents import AgentExecutor, AgentType
from langchain.agents.react.base import ReActDocstoreAgent
from langchain.llms import OpenAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.callbacks import BaseCallbackHandler
from typing import Any, Dict, List

llm = OpenAI(temperature=0)

# 定义工具
tools = [
    Tool(
        name="Search",
        func=lambda x: f"搜索结果：{x}",
        description="搜索工具"
    )
]

# 自定义提示模板
custom_prompt = PromptTemplate(
    template="""
你是一个专业的AI助手，擅长{expertise}领域。

可用工具：
{tools}

使用以下格式：
Question: 需要回答的问题
Thought: 你应该思考要做什么
Action: 要采取的行动，应该是[{tool_names}]中的一个
Action Input: 行动的输入
Observation: 行动的结果
... (这个 Thought/Action/Action Input/Observation 可以重复N次)
Thought: 我现在知道最终答案了
Final Answer: 原始问题的最终答案

开始！

Question: {input}
Thought: {agent_scratchpad}
""",
    input_variables=["expertise", "tools", "tool_names", "input", "agent_scratchpad"]
)

# 自定义回调处理器
class CustomCallbackHandler(BaseCallbackHandler):
    """自定义回调处理器，用于监控 Agent 执行"""
    
    def on_agent_action(self, action, **kwargs):
        print(f"\n[回调] Agent 执行动作：{action.tool}")
        print(f"[回调] 输入：{action.tool_input}")
    
    def on_agent_finish(self, finish, **kwargs):
        print(f"\n[回调] Agent 完成")
        print(f"[回调] 输出：{finish.return_values}")
    
    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"\n[回调] 工具开始：{serialized.get('name')}")
    
    def on_tool_end(self, output, **kwargs):
        print(f"[回调] 工具输出：{output}")

# 创建自定义 Agent
def create_custom_agent(expertise: str = "通用"):
    """创建自定义 Agent"""
    
    # 创建 Agent
    agent = ReActDocstoreAgent.from_llm_and_tools(
        llm=llm,
        tools=tools,
        prompt=custom_prompt.partial(expertise=expertise)
    )
    
    # 创建执行器
    executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        callbacks=[CustomCallbackHandler()],
        max_iterations=5,
        handle_parsing_errors=True
    )
    
    return executor

# 使用示例
if __name__ == "__main__":
    # 创建专业领域的 Agent
    python_agent = create_custom_agent(expertise="Python 开发")
    
    result = python_agent.run("如何优化 Python 代码性能？")
    print(f"\n最终结果: {result}\n")
    
    # 创建数据科学领域的 Agent
    ds_agent = create_custom_agent(expertise="数据科学")
    
    result = ds_agent.run("什么是机器学习？")
    print(f"\n最终结果: {result}\n")
