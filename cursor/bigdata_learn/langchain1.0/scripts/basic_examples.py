"""
LangChain 1.0 基础示例代码
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ============================================
# 1. 基础 Chat Model 调用
# ============================================
def example_basic_chat():
    """基础 Chat Model 调用示例"""
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=500
    )
    
    # 直接调用
    response = llm.invoke("用一句话介绍 LangChain")
    print(f"基础调用结果: {response.content}")
    return response


# ============================================
# 2. Prompt Template 示例
# ============================================
def example_prompt_template():
    """Prompt Template 示例"""
    from langchain_core.prompts import ChatPromptTemplate
    
    # 简单模板
    simple_prompt = ChatPromptTemplate.from_template(
        "将以下内容翻译成{language}: {text}"
    )
    
    # 多消息模板
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的{role}"),
        ("human", "{question}")
    ])
    
    # 格式化
    messages = chat_prompt.format_messages(
        role="技术顾问",
        question="什么是 LCEL？"
    )
    print(f"格式化后的消息: {messages}")
    return messages


# ============================================
# 3. LCEL 链式调用
# ============================================
def example_lcel_chain():
    """LCEL 链式调用示例"""
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = ChatPromptTemplate.from_template("用简洁的中文解释: {topic}")
    parser = StrOutputParser()
    
    # LCEL 链
    chain = prompt | llm | parser
    
    # 调用
    result = chain.invoke({"topic": "机器学习"})
    print(f"LCEL 链结果: {result}")
    return result


# ============================================
# 4. 批量调用
# ============================================
def example_batch():
    """批量调用示例"""
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = ChatPromptTemplate.from_template("一句话解释: {topic}")
    chain = prompt | llm | StrOutputParser()
    
    # 批量调用
    topics = [
        {"topic": "Python"},
        {"topic": "JavaScript"},
        {"topic": "Rust"}
    ]
    results = chain.batch(topics)
    
    for topic, result in zip(topics, results):
        print(f"{topic['topic']}: {result}")
    return results


# ============================================
# 5. 流式输出
# ============================================
def example_streaming():
    """流式输出示例"""
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    prompt = ChatPromptTemplate.from_template("详细解释: {topic}")
    chain = prompt | llm | StrOutputParser()
    
    print("流式输出: ", end="")
    for chunk in chain.stream({"topic": "神经网络"}):
        print(chunk, end="", flush=True)
    print()  # 换行


# ============================================
# 6. JSON 输出解析
# ============================================
def example_json_parser():
    """JSON 输出解析示例"""
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个数据提取助手，返回 JSON 格式。"),
        ("human", """从以下文本中提取人名和年龄:
{text}

返回格式: {{"name": "xxx", "age": xx}}""")
    ])
    
    chain = prompt | llm | JsonOutputParser()
    
    result = chain.invoke({"text": "张三今年25岁，是一名工程师"})
    print(f"JSON 解析结果: {result}")
    return result


# ============================================
# 7. RunnableParallel 并行执行
# ============================================
def example_parallel():
    """并行执行示例"""
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnableParallel
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # 定义多个处理链
    summary_prompt = ChatPromptTemplate.from_template("用一句话总结: {text}")
    translate_prompt = ChatPromptTemplate.from_template("翻译成英文: {text}")
    
    summary_chain = summary_prompt | llm | StrOutputParser()
    translate_chain = translate_prompt | llm | StrOutputParser()
    
    # 并行执行
    parallel = RunnableParallel(
        summary=summary_chain,
        translation=translate_chain
    )
    
    text = "LangChain 是一个强大的 LLM 应用开发框架。"
    result = parallel.invoke({"text": text})
    
    print(f"并行执行结果:")
    print(f"  摘要: {result['summary']}")
    print(f"  翻译: {result['translation']}")
    return result


# ============================================
# 8. 异步调用
# ============================================
async def example_async():
    """异步调用示例"""
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = ChatPromptTemplate.from_template("解释: {topic}")
    chain = prompt | llm | StrOutputParser()
    
    # 异步调用
    result = await chain.ainvoke({"topic": "异步编程"})
    print(f"异步调用结果: {result}")
    
    # 异步流式
    print("异步流式输出: ", end="")
    async for chunk in chain.astream({"topic": "协程"}):
        print(chunk, end="", flush=True)
    print()
    
    return result


# ============================================
# 主函数
# ============================================
if __name__ == "__main__":
    import asyncio
    
    print("=" * 50)
    print("LangChain 1.0 基础示例")
    print("=" * 50)
    
    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY 环境变量")
        exit(1)
    
    print("\n1. 基础 Chat Model 调用")
    example_basic_chat()
    
    print("\n2. Prompt Template 示例")
    example_prompt_template()
    
    print("\n3. LCEL 链式调用")
    example_lcel_chain()
    
    print("\n4. 批量调用")
    example_batch()
    
    print("\n5. 流式输出")
    example_streaming()
    
    print("\n6. JSON 输出解析")
    example_json_parser()
    
    print("\n7. 并行执行")
    example_parallel()
    
    print("\n8. 异步调用")
    asyncio.run(example_async())
    
    print("\n" + "=" * 50)
    print("所有示例执行完成！")
