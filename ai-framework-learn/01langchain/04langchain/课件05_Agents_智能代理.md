# Agents - 智能代理

> 尚硅谷大模型技术之LangChain V1.1.0

**目录**

| 章节 | 主题 | 核心内容 |
|------|------|---------|
| 一 | Agent 介绍 | 概念、核心组件、工作机制、与Chain对比 |
| 二 | 工具定义与使用 | Function Calling原理、@tool装饰器、create_agent |
| 三 | MCP工具接入 | MCP协议、Server编写、LangChain集成 |
| 四 | 记忆管理 | Checkpointer、Thread ID、多会话隔离 |
| 五 | Agent中间件 | 消息压缩、人工审核 |
| 六 | Agent最佳实践 | 工具设计、提示词优化、调试与性能 |
| 七 | 综合实例 | 智能客服Agent完整项目 |
| 八 | 课程总结 | 知识回顾、常见问题、进阶方向 |

---

## 1、Agent 介绍

### 1.1 从Chain到Agent

在前面的课程中，我们已经学会了用 **Chain（链）** 来组合LLM调用。但为什么还需要Agent？Chain的工作方式是：**预先定义好一条固定的处理流程**，输入数据按顺序流经每一步，最终得到输出。

```
Chain的工作方式：

   用户输入 → 提示词模板 → LLM → 输出解析 → 结果
              └────────────────────────────┘
                     固定流程，预先编排
```

这种方式在很多场景下运行得很好。但现实中有一类问题，Chain处理不了——**你事先不知道该走哪条路**。

**举个例子：** 用户问"帮我查查北京明天会不会下雨，如果下雨，帮我取消明天的户外预约"。

要完成这个任务，程序需要：
1. 先调用天气API查天气
2. 根据查到的结果（下雨/不下雨）做出判断
3. 如果下雨，再调用日程API取消预约；如果不下雨，直接回复用户

问题来了：**步骤2的"判断"和步骤3的"是否执行"，在编写代码时无法预先确定。** 你不能把这个流程硬编码成一条固定的Chain，因为每次用户输入不同，需要走的路径也不同。

这就是 **Agent（智能代理）** 要解决的问题。

### 1.2 什么是Agent

Agent的核心思想是：**把LLM当作"大脑"，让它自己决定下一步做什么。**

**Agent = LLM + 自主决策 + 【工具调用】**

在Chain中，是开发者（你）决定执行流程；在Agent中，是LLM自己决定执行流程。LLM会根据用户的输入和当前的上下文，自主选择要调用哪个工具、要执行什么操作，然后观察执行结果，再决定是否需要继续行动。

用一句话总结二者的区别：

```
Chain：开发者编排流程，LLM负责执行 → "你告诉它怎么做"
Agent：LLM自主编排流程，工具负责执行 → "你告诉它要做什么，它自己想怎么做"
```

### 1.3 核心组件

理解了Agent是什么之后，我们来看它由哪些部件组成。Agent有四个核心组件，它们**不是独立存在的，而是协作运转的**：

<img src="images/1、Agent的核心组件.png" style="zoom:50%;" />

**四个组件之间的协作关系：**

| 组件 | 角色 | 和其他组件的关系 |
|------|------|-----------------|
| **① LLM（大脑）** | 理解用户意图，做出每一步的决策 | 是整个Agent的中枢，驱动其他三个组件 |
| **② Tools（工具）** | 执行LLM的决策，与外部世界交互 | LLM"想"，工具"做"，工具的执行结果会反馈给LLM |
| **③ Memory（记忆）** | 存储上下文，让Agent"记住"对话历史 | 为LLM提供决策所需的历史信息 |
| **④ Planning（规划）** | 把复杂任务分解成可执行的步骤 | 指导LLM按合理顺序调用工具 |

> **注意：** 并不是每个Agent都需要四个组件全部具备。最简单的Agent只需要LLM + Tools即可工作。Memory和Planning是增强能力，让Agent能处理更复杂的任务。

#### 1.3.1 关于Planning（规划）

你可能在一些文章或论文中看到Agent的架构被描述为四个组件：LLM、Tools、Memory、**Planning**（例如Lilian Weng那篇著名的Agent论文）。那么Planning去哪了？

**在LangChain的工程实现中，Planning并不是一个独立的物理组件，而是一种隐含在Agent运行机制和提示词中的"能力"。**你不需要手写`planning = ...`这样的代码——规划能力已经被融合在了LLM的推理过程和Agent的执行引擎中。

具体来说，Planning在不同类型的Agent中以不同的方式体现：

**方式一：边走边看（ReAct模式）**

这是LangChain中最基础、最常用的模式，也是`create_agent`默认使用的模式。

```
用户："帮我查北京天气，如果下雨就取消明天的会议"

  第1步局部规划（Thought）：我需要先查天气 → 调用天气工具
  第2步局部规划（Thought）：天气是下雨，所以下一步取消会议 → 调用日程工具
  第3步局部规划（Thought）：两件事都做完了 → 回复用户
```

在这种模式下，Planning发生在**每一次工具调用的前一刻**——LLM每走一步都思考一下"接下来该干什么"。它没有全局规划，而是步步为营。这个"思考"过程就是LLM内部的推理，体现在提示词引导的Thought步骤中。

**方式二：谋定而后动（Plan-and-Execute模式）**

对于特别复杂的任务（如"调研三个国家的AI市场并写一份对比报告"），步步为营容易迷失方向。这时可以用Plan-and-Execute架构——**先规划再执行**：

```
用户："调研中美欧三地的AI市场，写一份对比报告"

  阶段一（Planner）：先调用LLM纯思考，输出步骤清单：
    步骤1：搜索中国AI市场数据
    步骤2：搜索美国AI市场数据
    步骤3：搜索欧洲AI市场数据
    步骤4：对比分析三地差异
    步骤5：撰写报告

  阶段二（Executor）：按清单逐一执行，调用工具完成每个步骤
```

这种模式需要通过LangGraph来构建更复杂的工作流，不在本课的基础范围内。

**总结：** Planning的灵魂隐藏在你选择的Agent类型和系统提示词中。在LangChain开发中，你实际需要动手构建的核心组件是三个：**LLM、Tools、Memory**——这也是本课程后续章节的学习主线。



### 1.4 工作机制

Agent不是"一次调用就出结果"，而是通过一个**"感知→推理→行动"的循环（Loop）**来逐步完成任务。

<img src="images/2、Agent的工作循环.png" style="zoom:50%;" />

**关键理解：这个循环可能执行多轮。** LLM每次"推理"后，如果判断任务还没完成，就会继续调用工具、观察结果、再推理……直到它认为可以给出最终答案为止。

### 1.5 完整例子

回到1.1节的例子，看看Agent内部是怎么一步步处理的：

> 用户：**"帮我查查北京明天会不会下雨，如果下雨，帮我取消明天的户外预约"**

```
第1轮循环：
  ① 感知：收到用户消息
  ② 推理：用户想知道天气，我需要先查天气 → 决定调用"天气查询"工具
  ③ 行动：调用 get_weather("北京", "明天") → 返回"明天北京：小雨"

第2轮循环：
  ① 感知：收到工具返回结果"小雨"
  ② 推理：明天下雨，用户要求下雨时取消户外预约 → 决定调用"取消预约"工具
  ③ 行动：调用 cancel_appointment("户外预约", "明天") → 返回"已取消"

第3轮循环：
  ① 感知：收到工具返回结果"已取消"
  ② 推理：天气查了，预约也取消了，任务完成 → 决定直接回复用户
  ③ 输出："北京明天预报有小雨，我已经帮您取消了明天的户外预约。"
```

**注意观察：** 整个过程中，没有任何一行代码预先规定了"先查天气再取消预约"这个流程。是LLM根据用户意图和中间结果，**自主决定**了每一步该做什么。如果明天不下雨，LLM在第2轮就会直接回复用户，根本不会调用取消预约的工具。

**这就是Agent和Chain的根本区别：执行路径不是写死的，而是由LLM动态决定的。**

### 1.6 Agent与Chain对比

现在我们可以更深入地对比二者：

| 对比维度 | Chain（链） | Agent（智能代理） |
|---------|------------|-----------------|
| **谁决定流程** | 开发者在代码中预定义 | LLM在运行时自主决定 |
| **执行路径** | 线性的，固定的 | 循环的，动态的 |
| **工具调用** | 在固定位置调用固定工具 | LLM按需选择工具，调用次数不确定 |
| **处理意外情况** | 无法应对预期之外的情况 | LLM可以根据工具返回结果调整策略 |
| **适合的任务** | 结构明确、步骤固定的任务 | 开放式、需要判断和决策的任务 |
| **可预测性** | 高——每次执行路径相同 | 低——不同输入可能走不同路径 |
| **开发复杂度** | 低——流程清晰可控 | 较高——需要设计好工具和提示词 |

> **实际开发建议：** 不要所有场景都用Agent。如果你的任务流程是确定的（比如"翻译一段文字"），用Chain更简单可靠。只有当任务需要**动态判断和多步决策**时，才需要Agent。

### 1.7 技术栈定位

回顾我们整个课程的学习路径，Agent处于技术栈的最上层：

<img src="images/3、技术栈定位.png" style="zoom:50%;" />

每一层都是在上一层的基础上增加新的能力：Model I/O让你能调用模型，Chain让你能编排流程，RAG让模型拥有知识，而**Agent让模型拥有"判断力"和"行动力**。

### 1.8 本章小结

本章的核心内容可以归结为三句话：

1. **为什么需要Agent：** Chain只能处理固定流程，面对需要动态判断的任务无能为力，Agent通过让LLM自主决策来解决这个问题。
2. **Agent是什么：** LLM作为大脑，配合工具（执行）和记忆（上下文）三大核心组件，通过"感知→推理→行动"的循环来完成任务。规划能力则隐含在LLM的推理过程和提示词策略中。
3. **什么时候用Agent：** 任务流程固定用Chain，任务需要动态判断和多步决策用Agent。

接下来的章节，我们将学习如何用LangChain实际构建一个Agent——从定义工具开始。

---

## 2、工具定义与使用

上一章我们知道了Agent的四大组件中，**工具（Tools）是Agent与外部世界交互的唯一通道**——LLM负责"想"，工具负责"做"。没有工具的Agent，就像一个只会说话但没有手脚的人，什么实际操作也完成不了。

因此，构建Agent的第一步，就是**定义工具**。

### 2.1 工具的本质

在深入LangChain的工具定义之前，我们需要先理解一个底层机制：**工具调用的本质是大模型的Function Calling能力。**

当我们给Agent配置工具时，实际上发生的事情是：

```
① 你定义工具（函数名 + 参数说明 + 功能描述）
                    ↓
② LangChain把工具信息转换成JSON Schema，随提示词一起发给LLM
                    ↓
③ LLM阅读工具描述，根据用户问题决定：
   - 需要调用哪个工具
   - 传入什么参数
                    ↓
④ LLM返回一个"工具调用指令"（不是直接执行，而是告诉框架"我要调用XX工具"）
                    ↓
⑤ LangChain框架接收指令，在本地执行对应的函数
                    ↓
⑥ 执行结果返回给LLM，LLM继续推理
```

**关键理解：LLM自身并不能执行任何工具。** 它只是根据工具描述"选择"要调用什么、传什么参数。真正执行工具的是你的代码。LLM的角色更像是一个"调度员"。

> 这意味着：**工具的描述写得好不好，直接决定了LLM能不能正确地选择和调用它。** 这是工具定义中最重要的事。

### 2.2 原生Function Calling

为了理解LangChain在背后做了什么，我们先看一下不用LangChain时，直接用OpenAI SDK实现Function Calling是什么样的。**这一节是帮你理解原理，实际开发中不需要这样写。**

```python
from openai import OpenAI
import json

client = OpenAI()

# ===== 第1步：用JSON Schema手动描述工具 =====
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市在指定日期的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称",
                    },
                    "date": {
                        "type": "string",
                        "description": "日期，格式为YYYY-MM-DD",
                    }
                },
                "required": ["city", "date"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

# ===== 第2步：定义工具的实际执行逻辑 =====
def get_weather(city, date):
    # 实际项目中这里会调用真实的天气API
    return f"{city} 在 {date} 天气多云，有下雨的可能性。"

# ===== 第3步：把用户消息和工具描述一起发给LLM =====
messages = [
    {"role": "user", "content": "北京2025-12-25的天气怎么样？"}
]

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    tools=tools,      # ← 工具描述随请求一起发送
)

# ===== 第4步：LLM返回的不是文字，而是"工具调用指令" =====
# response.choices[0].message.tool_calls 包含了LLM想调用的工具和参数

# ===== 第5步：我们在本地执行工具，把结果喂回给LLM =====
messages.append(response.choices[0].message)
for tool_call in response.choices[0].message.tool_calls or []:
    if tool_call.function.name == "get_weather":
        args = json.loads(tool_call.function.arguments)
        result = get_weather(args["city"], args["date"])
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps({"weather": result}),
        })

# ===== 第6步：LLM拿到工具结果后，生成最终的自然语言回复 =====
final_response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    tools=tools,
)
print(final_response.choices[0].message.content)
```

观察这段代码，你会发现**手动实现Function Calling非常繁琐**：要手写JSON Schema、要手动解析工具调用指令、要手动把结果喂回去、要手动管理消息列表……而且如果有多个工具、多轮调用，代码量会爆炸式增长。

这就是为什么我们需要LangChain——**它把上面所有的脏活都封装好了**。

### 2.3 LangChain定义工具

LangChain提供了`@tool`装饰器，只需要**写一个普通的Python函数**，加上装饰器和类型注解，LangChain就会自动帮你：
- 根据函数签名生成JSON Schema
- 根据docstring生成工具描述
- 处理参数的序列化和反序列化

```python
from langchain.tools import tool

@tool
def get_weather(city: str, date: str) -> str:
    """获取指定城市在指定日期的天气。

    Args:
        city: 城市名称，如"北京"、"上海"
        date: 日期，格式为YYYY-MM-DD
    """
    # 实际项目中调用天气API，这里用模拟数据
    return f"{city} 在 {date} 天气多云，有下雨的可能性。"
```

**对比一下：** 原生方式需要手写十几行JSON Schema来描述一个工具，LangChain只需要一个`@tool`装饰器加上规范的docstring。效果是一样的——LangChain会在背后自动生成JSON Schema发给LLM。

**三个影响LLM调用准确性的关键点：**

| 要素 | 作用 | 写法建议 |
|------|------|---------|
| **函数名** | LLM根据函数名初步判断工具用途 | 用清晰的动词+名词，如`get_weather`、`search_documents` |
| **docstring** | LLM根据描述理解工具的具体功能 | 写清楚"这个工具做什么"，越具体越好 |
| **参数类型注解** | LLM根据类型和描述决定传入什么值 | 每个参数都要有类型注解和说明 |

> **常见错误：** docstring写得太简略（如"查天气"），导致LLM不确定什么时候该用这个工具、该传什么参数。**docstring是你和LLM之间的"说明书"，写得越清楚，LLM用得越准。**

#### Pydantic定义复杂参数

当工具的参数比较复杂时，可以用Pydantic模型来定义参数结构，提供更精确的约束：

```python
from langchain.tools import tool
from pydantic import BaseModel, Field

class GetWeatherArgs(BaseModel):
    """天气查询参数"""
    city: str = Field(description="城市名称，如'北京'、'上海'")
    date: str = Field(description="查询日期，格式为YYYY-MM-DD")

@tool(args_schema=GetWeatherArgs)
def get_weather(city: str, date: str) -> str:
    """获取指定城市在指定日期的天气预报"""
    return f"{city} 在 {date} 天气多云，有下雨的可能性。"
```

### 2.4 构建Agent

工具定义好之后，就可以用LangChain的`create_agent`函数来构建一个完整的Agent了。`create_agent`会帮你处理第2.1节中描述的所有底层细节——消息管理、工具调用解析、结果回传、循环控制。



https://app.tavily.com/api/auth/callback?code=Cz6f2gEuJ60vEAw6rnoNAkwA9Lu5ZF1rJsk-0ynYH0dHC&state=eyJyZXR1cm5UbyI6Imh0dHBzOi8vYXBwLnRhdmlseS5jb20ifQ

```python
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

# ===== 第1步：初始化LLM =====
llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai",
)

# ===== 第2步：准备工具列表 =====
# 这里同时使用自定义工具和第三方工具
from langchain_tavily import TavilySearch

search = TavilySearch(max_results=5)     # 第三方搜索工具
tools = [get_weather, search]             # 把所有工具放进列表

# ===== 第3步：创建Agent =====
agent = create_agent(
    model=llm,                            # 指定LLM作为大脑
    tools=tools,                          # 传入工具列表
    system_prompt="你是一个智能助手，请根据用户的需求调用合适的工具来帮助他们。",
)
```

`create_agent`函数的核心参数：

| 参数 | 作用 | 是否必填 |
|------|------|---------|
| `model` | 指定LLM（Agent的大脑） | ✅ 必填 |
| `tools` | 工具列表（Agent的手脚） | ✅ 必填 |
| `system_prompt` | 系统提示词，指导Agent的行为风格 | 可选 |
| `checkpointer` | 记忆存储（下一章详细讲） | 可选 |
| `middleware` | 中间件列表（后续章节详细讲） | 可选 |

### 2.5 调用方式

Agent创建好之后，有两种调用方式：**一次性调用**和**流式调用**。

#### 2.5.1 invoke（一次性调用）

等待Agent完成所有推理和工具调用后，一次性返回最终结果：

```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "今天北京的天气怎么样？"}]}
)

# 取出最终回复
print(result["messages"][-1].content)
```

> 注意：目前 LangChain 最新的推荐模式， 采用**LangGraph** 架构的 Agent，在这种模式下，Agent 内部是通过一个名为 **`messages`** 的变量来管理整个对话状态。

#### 2.5.2 stream（流式调用）

实时输出Agent每一步的中间过程，适合需要展示"Agent正在思考/执行"的场景：

```python
for step in agent.stream(
    {"messages": [{"role": "user", "content": "今天北京的天气怎么样？"}]}
):
    print(step, end="\n\n")
```

流式调用的输出会依次展示：
2. LLM推理过程，进行工具调用（调用`get_weather`工具）
3. 工具返回结果
4. LLM的最终回复

> **注意：**`agent.stream` 默认吐出的是**“当前这一步做完后的完整状态”**。
>
> **实际开发建议：** 开发调试阶段用`stream`可以观察Agent每一步在干什么，方便排查问题；生产环境中根据产品形态选择——聊天界面适合流式，后台任务适合一次性调用。

### 2.6 完整实例

下面是一个完整的、可直接运行的例子，把本章所有知识点串起来：

```python
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_tavily import TavilySearch

# ===== 1. 定义自定义工具 =====
@tool
def calculate(expression: str) -> str:
    """计算数学表达式的结果。

    Args:
        expression: 数学表达式，如 "2 + 3 * 4"、"100 / 7"
    """
    try:
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算出错：{e}"

@tool
def get_current_date() -> str:
    """获取当前日期和时间，不需要任何参数。"""
    from datetime import datetime
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

# ===== 2. 使用第三方工具 =====
search = TavilySearch(max_results=3)

# ===== 3. 初始化LLM =====
llm = init_chat_model(model="gpt-4o-mini", model_provider="openai")

# ===== 4. 创建Agent =====
agent = create_agent(
    model=llm,
    tools=[calculate, get_current_date, search],
    system_prompt="""你是一个智能助手，拥有以下能力：
- 计算数学表达式
- 查询当前日期时间
- 搜索网络信息

请根据用户的问题，选择合适的工具来回答。如果不需要工具就能回答，直接回答即可。""",
)

# ===== 5. 运行Agent =====
for i, step in enumerate(agent.stream(
    {"messages": [{"role": "user", "content": "今天是几号？帮我算一下距离2026年五一还有多少天"}]}
), start=1):
    print(f"=== 第 {i} 步 ===")
    print(step, end="\n\n")
```

在这个例子中，Agent会自主完成以下步骤（无需我们编码控制流程）：
1. 调用`get_current_date`获取今天日期
2. 自己计算天数差，或调用`calculate`来辅助计算
3. 组织语言回复用户

### 2.7 LangSmith调试

Agent的执行过程是动态的，有时候出了问题很难排查——比如LLM选错了工具、传错了参数、或者陷入了无限循环。LangSmith是LangChain官方提供的追踪调试工具，可以可视化Agent每一步的执行细节。

只需要设置环境变量即可启用：

```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "你的API Key"
os.environ["LANGSMITH_PROJECT"] = "my-agent-project"
```

启用后，每次Agent运行的完整轨迹（每轮推理、每次工具调用、每个参数和返回值）都会记录到LangSmith平台上，方便回溯和分析。

### 2.8 本章小结

本章的学习路径是：

1. **理解原理：** 工具调用的本质是Function Calling——LLM只负责"选择调用什么"，框架负责"实际执行"。
2. **定义工具：** 用`@tool`装饰器把普通Python函数变成Agent可用的工具，重点是写好docstring和类型注解。
3. **构建Agent：** 用`create_agent`把LLM和工具组装起来，一行代码搞定所有底层细节。
4. **调用Agent：** `invoke`一次性获取结果，`stream`实时观察执行过程。

到目前为止，我们定义的工具都是**本地工具**——函数代码写在我们自己的项目里。但实际开发中，你经常需要使用别人已经封装好的工具服务（比如查火车票、操作数据库、读取GitHub仓库）。每个服务的接入方式都不一样，难道要为每个服务单独写适配代码吗？

下一章我们将学习**MCP（模型上下文协议）**——一个标准化的工具接入协议，让Agent能像"插USB"一样轻松接入各种外部工具服务。

---

## 3、MCP工具接入

### 3.1 为什么需要MCP

上一章我们学会了用`@tool`装饰器定义本地工具。本地工具虽然灵活，但有一个现实问题：

```
场景：你想让Agent具备"查火车票"的能力

方式一：自己写本地工具
  → 需要研究12306的API文档
  → 需要处理认证、签名、加密
  → 需要处理各种异常和边界情况
  → 需要持续维护（API一更新就得改）

方式二：如果有人已经把"查火车票"封装成了一个标准化的服务，你只需要"接上去"就能用呢？
```

问题在于，不同的人封装工具服务的方式各不相同——有的用REST API，有的用WebSocket，有的用gRPC……如果每接入一个外部工具都要写一套不同的适配代码，那就太麻烦了。

**MCP（Model Context Protocol，模型上下文协议）就是来解决这个问题的。** 它定义了一套统一的标准，让所有工具服务都以相同的方式暴露能力，AI应用以相同的方式接入——无论底层工具是什么、在哪里运行。

### 3.2 MCP是什么

理解MCP最简单的方式是类比USB-C：

<img src="images/4、 MCP是什么.png" style="zoom:50%;" />

**一句话总结：MCP是AI领域的"USB-C标准"，它统一了LLM与外部工具之间的通信方式。**

### 3.3 MCP架构

MCP采用客户端-服务器架构，涉及三个角色：

<img src="images/5、MCP架构.png" style="zoom:50%;" />

| 角色 | 职责 | 在我们场景中的对应 |
|------|------|-----------------|
| **MCP Host** | 运行AI应用的宿主程序，内含MCP Client | 你的LangChain Agent程序 |
| **MCP Client** | 与MCP Server通信的客户端 | LangChain的MCP适配器 |
| **MCP Server** | 提供工具能力的服务端 | 别人封装好的工具服务 |

### 3.4 MCP工作流程

当Agent通过MCP调用一个外部工具时，完整的流程是这样的：

```
第①步 - 握手：Agent启动时连接MCP Server，获取工具列表和描述
  Host："你有哪些工具？"
  Server："我有 query_train（查火车票）、book_ticket（订票）……"

         ↓

第②步 - 注入：Host将工具描述和用户问题一起发给LLM
  （和本地工具完全一样——LLM不知道也不关心工具是本地的还是远程的）

         ↓

第③步 - 决策：LLM决定要调用哪个工具、传什么参数
  LLM："我要调用 query_train，参数是 {from: '北京', to: '上海', date: '2026-05-01'}"

         ↓

第④步 - 路由执行：Host通过MCP协议将调用请求发给Server，Server执行并返回结果
  Host → Server："执行 query_train({from: '北京', to: '上海', date: '2026-05-01'})"
  Server → Host："找到3趟列车：G1 07:00, G3 08:00, G5 09:00"

         ↓

第⑤步 - 继续推理：Host将结果返回给LLM，LLM继续推理或输出最终回复
```

**关键理解：** 对LLM来说，MCP工具和本地工具没有任何区别——它看到的都是"工具名 + 描述 + 参数"。MCP只是改变了工具在**你的代码端**的接入方式，对LLM完全透明。

### 3.5 传输协议

MCP Server和Client之间的通信支持多种传输方式，适用于不同的部署场景：

| 传输协议 | 原理 | 适用场景 | 示例 |
|---------|------|---------|------|
| **Stdio** | 通过标准输入/输出通信 | MCP Server和你的程序在**同一台机器**上 | 本地开发、调试 |
| **Streamable HTTP** | 通过HTTP流式传输通信 | MCP Server部署在**远程服务器**上 | 生产环境、云服务 |
| **SSE** | 服务器发送事件（Server-Sent Events） | 需要服务端主动推送的场景 | 实时通知（较少使用） |

> **实际开发中用得最多的是前两种：** 本地开发调试用Stdio（简单、无需网络），生产部署用Streamable HTTP（支持远程调用）。

### 3.6 编写MCP Server（Stdio）

在接入别人的MCP Server之前，我们先自己写一个，理解Server端是怎么工作的。

```python
# 文件名：mcp_server_stdio.py
# uv add mcp

from mcp.server.fastmcp import FastMCP

# ===== 创建MCP Server实例 =====
mcp = FastMCP("MyTools")

# ===== 用 @mcp.tool() 定义工具 =====
# 注意：写法和LangChain的 @tool 非常相似
@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个整数的和"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积"""
    return a * b

# ===== 启动Server =====
if __name__ == "__main__":
    mcp.run(transport="stdio")   # 以Stdio方式运行
```

MCP Server还支持暴露**资源（Resource）**和**提示词模板（Prompt）**，不仅仅是工具：

```python
# 资源：提供可读取的数据（类似GET接口）
@mcp.resource("greeting://default")
def get_greeting() -> str:
    """返回一条默认问候语"""
    return "Hello from MCP Server!"

# 提示词模板：提供预定义的提示词
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """生成问候语的提示词"""
    styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
        "casual": "写一句轻松的问候",
    }
    return f"为{name}{styles.get(style, styles['friendly'])}"
```

**资源：`@mcp.resource` —— “静态的文件柜”**

**工作机制：** 定义了一个唯一的 URI（统一资源标识符）`greeting://default`。当 Agent 连接到这个 Server 时，它会知道：“哦，这里有一份叫做 `greeting://default` 的文档可以看”。

**场景**：比如读取一份系统日志、读取公司的员工手册、读取当前的配置参数

> **核心理解：** 它就像是一个只读的 API 接口，或者一个虚拟的文件柜。大模型（LLM）不需要去“执行”什么动作，只是去**“读取”**里面的背景资料。



 **提示词：`@mcp.prompt` —— “标准化的模版库”**

> **核心理解：** 它是存在 Server 端的一套“话术模板”。它让 U盘（Server）自带说明书，告诉 Host（主机/大模型）：“如果你想用我，你应该这样问问题”。

**工作机制：** 当 Agent 连接上 Server 时，Server 会告诉它：“我这有个模板叫 `greet_user`，你只要给我填入 `name` 和 `style`，我就会吐出一句完美的提示词给你。”

**为什么要把提示词放在 Server 里？**

- 如果你用 LangChain 写代码，你通常会在 Host（客户端）里硬编码系统提示词。但如果这个 Server 是别人写的第三方服务（比如 GitHub 官方提供的一个 MCP Server），GitHub 最知道怎么引导大模型写出高质量的 PR Review。所以 GitHub 直接在 Server 里把提示词写好，你只管调用，生成出来的提示词直接喂给 LLM。

#### 测试Server

写好Server后，可以用MCP SDK自带的Client来测试：

```python
import asyncio
import sys
import os
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

async def test():
    # 动态获取当前脚本所在的绝对路径所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 拼接出 server 脚本的绝对路径
    server_script_path = os.path.join(current_dir, "mcp_server.py")

    # 配置Server的启动命令
    server_params = StdioServerParameters(
        command=sys.executable,        #  1：使用当前跑Client的同一个Python解释器(虚拟环境)
        args=[server_script_path],     #  2：使用绝对路径
    )

    # 连接Server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()       # 第①步：握手

            # 查看Server提供了哪些工具 它 只去拉取工具
            tools = await session.list_tools()
            print("可用工具:", tools)

            # 调用工具
            result = await session.call_tool("add", {"a": 10, "b": 20})
            print("调用结果:", result)        # 输出: 30

asyncio.run(test())
```

#### 核心代码解读

上面代码中最核心的一行是：

```python
async with stdio_client(server_params) as (read, write):
```

用之前的USB类比来说，**这行代码就是"把准备好的U盘插到主机的USB接口上，并接通数据线"**。拆成三个部分来理解：

**① `stdio_client(server_params)` —— 启动Server进程**

`stdio`是Standard Input/Output（标准输入/输出）的缩写。这个函数会根据`server_params`的配置（即`python ./mcp_server_stdio.py`），在后台启动Server脚本。启动后，Client和Server之间**不走网络端口**，而是直接通过进程的标准输入/输出来通信——Client往Server的stdin写数据，从Server的stdout读结果。这种方式极其轻量，非常适合本地运行的工具。

**② `as (read, write)` —— 获取两根"数据线"**

连接建立后，返回两个通信对象：

```
write（写通道）：Host → Server 发送指令的管道
                 比如"调用add工具，参数是10和20"

read （读通道）：Server → Host 返回结果的管道
                 比如Server算出结果30，Host通过read接收
```

可以把它想象成一部对讲机：一根线负责说（write），一根线负责听（read）。后续代码中的`session.initialize()`（握手）、`session.call_tool()`（调用工具）等操作，底层都是通过这两根线收发数据的。

**③ `async with ...` —— 自动管理生命周期**

这是Python的异步上下文管理器。它的作用是：进入缩进块时建立连接，**退出时自动关闭Server进程并断开通信管道**——无论是正常执行结束还是中途报错。你不需要手写`session.close()`或`server.kill()`，不会出现后台残留僵尸进程的问题。



### 3.7 编写MCP Server（HTTP）

当Server需要部署在远程服务器上供多个Client调用时，使用Streamable HTTP方式：

```python
# 文件名：mcp_server_http.py

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyTools")

@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个整数的和"""
    return a + b

if __name__ == "__main__":
    mcp.run(transport="streamable-http")   # 默认启动在 127.0.0.1:8000
```

对应的Client代码：

```python
# 文件名：test_mcp_http_client.py

import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def test():
    url = "http://127.0.0.1:8000/mcp"     # Server的HTTP地址
    # 第三个对象 _（被忽略的对象）： 这是跟底层网络传输（Transport）相关的元数据或回调函数。在流式 HTTP 的实现中，它通常是一个用来获取当前底层 HTTP 连接的 Session ID（会话标识） 的函数。除非你在写极其复杂的底层重连机制、或者需要追踪排查极端的网络断线日志，否则在日常调用工具开发 Agent 时根本用不到它
    async with streamable_http_client(url=url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("可用工具:", tools)

            result = await session.call_tool("add", {"a": 10, "b": 20})
            print("调用结果:", result)

asyncio.run(test())
```

**对比两种方式：** Server端的工具定义代码完全一样，只是启动时的`transport`参数不同。Client端的连接方式不同（一个启动本地进程，一个连HTTP地址），但调用工具的API完全一致。这就是MCP协议标准化带来的好处。

### 3.8 LangChain接入MCP

前面两节我们手写了Client来测试MCP Server。但在实际开发中，我们不需要手写Client——LangChain提供了`langchain-mcp-adapters`包，可以**直接把MCP Server的工具转换成Agent可用的工具**。

```python
# uv add langchain-mcp-adapters

import os
import sys
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# ===== 精准定位 Server 文件的绝对路径 =====
# 1. 获取当前脚本 (langchain_integration_mcp.py) 所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 向上退一级到 mcp 目录，然后进入 stdio 目录，找到 mcp_server.py
server_script_path = os.path.normpath(os.path.join(current_dir, "..", "stdio", "mcp_server.py"))

print(f"准备调用的 Server 路径: {server_script_path}")

# ===== 第1步：配置MCP Server连接 =====
client = MultiServerMCPClient({
    # 连接一个本地Stdio Server
    "my-local-tools": {
        "transport": "stdio",
        "command": sys.executable,  # 使用当前虚拟环境的 Python
        "args": [server_script_path],  # 使用计算好的绝对路径
    },

    "12306-mcp": {
        "transport": "streamable_http",
        "url": "https://mcp.api-inference.modelscope.net/8e63d4dbeef046/mcp"
    }
})


# ===== 第2步：获取所有Server的工具，创建Agent =====
async def main():
    # 自动连接所有Server，获取全部工具列表
    tools = await client.get_tools()
    print(f"✅ 成功获取到 {len(tools)} 个工具")

    # 此时tools里包含了Server的所有工具，和本地@tool定义的工具格式完全相同
    llm = ChatOpenAI(model="gpt-4o-mini")
    agent = create_agent(llm, tools)

    # ===== 第3步：像平常一样使用Agent =====
    print("\n 开始执行Agent...")
    result = await agent.ainvoke({
        "messages": [("user", "信阳有多少个火车站")]
    })

    # 打印最终结果
    print("\n🤖 Agent回复:", result["messages"][-1].content)


asyncio.run(main())

```

**核心价值：** 通过`MultiServerMCPClient`，你可以同时接入任意数量的MCP Server，它们的工具会被统一转换成LangChain工具格式。对Agent来说，MCP工具和本地`@tool`工具用起来没有任何区别。

### 3.9 本地工具 vs MCP工具

| 对比维度 | 本地工具（@tool） | MCP工具 |
|---------|-----------------|---------|
| **定义位置** | 写在你的项目代码中 | 运行在独立的MCP Server上 |
| **适合场景** | 业务逻辑简单、不需要复用 | 通用能力、需要跨项目/跨团队复用 |
| **维护方式** | 和主项目一起维护 | 独立部署、独立维护 |
| **使用门槛** | 低——写个函数加个装饰器 | 中——需要启动Server |
| **生态复用** | 无——只有你自己能用 | 强——任何支持MCP的应用都能接入 |

> **实际建议：** 项目早期或工具逻辑简单时，直接用`@tool`定义本地工具最快。当工具需要被多个项目复用、或者你想接入社区已有的工具服务时，用MCP。两种方式可以混合使用——在同一个Agent中同时挂载本地工具和MCP工具。

### 3.10 本章小结

本章围绕"如何接入外部工具"展开：

1. **为什么需要MCP：** 不同的工具服务有不同的接入方式，MCP通过统一的协议标准解决了这个问题。
2. **MCP的工作方式：** Host（你的应用）通过MCP Client连接MCP Server，获取工具列表，然后像使用本地工具一样使用远程工具。
3. **两种传输协议：** Stdio适合本地开发，Streamable HTTP适合远程部署。
4. **LangChain集成：** `langchain-mcp-adapters`的`MultiServerMCPClient`可以同时接入多个MCP Server，对Agent完全透明。

到目前为止，我们的Agent已经拥有了强大的工具调用能力（本地工具 + MCP远程工具）。但它还有一个明显的不足：**每次调用都是"失忆"的**——它不记得上一轮对话说了什么。下一章我们将学习如何给Agent添加记忆。

---

## 4、记忆管理

### 4.1 失忆问题

试想这样一个场景：

```
第1次调用：
  用户："我叫张三"
  Agent："你好张三！有什么可以帮你？"

第2次调用：
  用户："我叫什么名字？"
  Agent："抱歉，我不知道你叫什么名字。"   ← 失忆了
```

这不是Bug，而是Agent的默认行为。回忆第一章的工作循环——Agent每次`invoke`都是一次独立的"感知→推理→行动"过程。**上一次调用的对话内容，不会自动带入下一次调用中。**

这就好比你每天找同一个客服咨询问题，但对方每天换一个新人，昨天说过的话今天得从头说一遍。

要解决这个问题，我们需要给Agent加上**记忆（Memory）**。

### 4.2 Checkpointer

LangChain通过`checkpointer`机制实现Agent的记忆。它的工作原理非常简单：

```
每次调用结束后：
  Checkpointer 自动保存本次对话的所有消息
                    ↓
下次调用开始时：
  Checkpointer 自动加载之前保存的消息，拼接到新的输入前面
                    ↓
效果：
  LLM看到的消息列表 = 历史消息 + 本次新消息
  → Agent就"记住"了之前的对话
```

使用方式只需两步：创建一个`checkpointer`实例，传入`create_agent`。

```python
from langgraph.checkpoint.memory import InMemorySaver

# 创建checkpointer（内存存储，程序重启后数据会丢失）
checkpointer = InMemorySaver()

# 创建Agent时传入checkpointer
agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=checkpointer,     # ← 就这一行
)
```

### 4.3 Thread ID

一个Agent通常会同时服务多个用户。不同用户的对话历史不应该互相干扰——用户A的聊天记录不应该出现在用户B的对话中。

LangChain通过`thread_id`来隔离不同的会话。**每个不同的`thread_id`维护一份独立的消息列表：**

```
thread_id: "user_张三"  →  [消息1, 消息2, 消息3, ...]
thread_id: "user_李四"  →  [消息A, 消息B, ...]
thread_id: "user_王五"  →  [消息X, 消息Y, ...]
```

调用Agent时，通过`config`参数指定`thread_id`：

```python
# 张三的对话
agent.invoke(
    {"messages": [{"role": "user", "content": "我叫张三"}]},
    config={"configurable": {"thread_id": "user_张三"}},
)

# 李四的对话（完全独立，互不干扰）
agent.invoke(
    {"messages": [{"role": "user", "content": "我叫李四"}]},
    config={"configurable": {"thread_id": "user_李四"}},
)
```

### 4.4 完整示例

下面的例子展示了添加记忆前后的对比效果：

```python
import datetime
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

# 准备工具和模型
search = TavilySearch(max_results=5)
llm = init_chat_model(model="gpt-4o-mini", model_provider="openai")

# 创建有记忆的Agent
checkpointer = InMemorySaver()
agent = create_agent(
    model=llm,
    tools=[search],
    checkpointer=checkpointer,
)

# ===== 第1次调用 =====
print("=== 第1次调用 ===")
for chunk in agent.stream(
    input={
        "messages": [
            {
                "role": "system",
                "content": f"当前时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            },
            {"role": "user", "content": "今天北京天气怎么样？"},
        ]
    },
    config={"configurable": {"thread_id": "abc123"}},
):
    print(chunk, end="\n\n")

# ===== 第2次调用（相同thread_id → 有记忆） =====
print("=== 第2次调用 ===")
for chunk in agent.stream(
    input={
        "messages": [{"role": "user", "content": "我刚才问你什么了？"}]
    },
    config={"configurable": {"thread_id": "abc123"}},   # ← 相同thread_id
):
    print(chunk, end="\n\n")
# Agent会回答："你刚才问了北京今天的天气"

# ===== 第3次调用（不同thread_id → 无记忆） =====
print("=== 第3次调用（新会话） ===")
for chunk in agent.stream(
    input={
        "messages": [{"role": "user", "content": "我刚才问你什么了？"}]
    },
    config={"configurable": {"thread_id": "xyz789"}},   # ← 不同thread_id
):
    print(chunk, end="\n\n")
# Agent会回答："这是我们第一次对话，你还没有问过任何问题"
```

### 4.5 记忆的局限性

Checkpointer解决了"失忆"问题，但引入了一个新问题：**随着对话轮次增加，保存的消息列表会越来越长。**

```
第1轮：  [用户消息1, AI回复1]                          → 2条消息
第10轮： [用户消息1, AI回复1, ..., 用户消息10, AI回复10]  → 20条消息
第100轮：[用户消息1, AI回复1, ..., 用户消息100, AI回复100] → 200+条消息
```

每次调用时，所有历史消息都会发送给LLM。消息太多会导致两个问题：Token消耗剧增（费钱），甚至超出模型的上下文窗口限制（报错）。

这个问题的解决方案就是下一章要讲的**中间件**——可以在消息发给LLM之前自动进行压缩和总结。

### 4.6 本章小结

1. **Agent默认无记忆：** 每次`invoke`是独立的，上一轮对话不会自动带入下一轮。
2. **添加记忆只需一步：** 创建`InMemorySaver`实例传给`checkpointer`参数即可。
3. **Thread ID实现多会话隔离：** 不同的`thread_id`维护各自独立的对话历史。
4. **记忆有代价：** 消息列表会无限增长，需要通过中间件来压缩——这是下一章的主题。

---

## 5、Agent中间件

### 5.1 中间件概念

上一章结尾提到了记忆带来的消息膨胀问题。在解决它之前，我们先理解一个更通用的概念：**中间件（Middleware）**。

中间件是一种**插入Agent执行流程中的"拦截器"**。它可以在Agent执行的各个关键节点上介入，对数据进行加工处理。

<img src="images/6、 中间件概念.png" style="zoom:50%;" />

中间件可以在以下位置介入：

| 介入位置 | 时机 | 典型用途 |
|---------|------|---------|
| **before_model** | 消息发给LLM之前 | 压缩历史消息、注入额外上下文 |
| **after_model** | LLM返回结果之后 | 记录日志、过滤敏感内容 |
| **wrap_tool** | 工具执行前后 | 人工审核、权限控制 |

使用中间件的方式也很简单——创建中间件实例，通过`middleware`参数传入`create_agent`：

```python
agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=checkpointer,
    middleware=[middleware_a, middleware_b],   # ← 中间件列表
)
```

### 5.2 消息压缩中间件

这就是上一章留下的问题的解决方案。`SummarizationMiddleware`会在消息发给LLM之前，自动检查消息列表的长度。当消息量超过设定的阈值时，它会用一个独立的LLM调用，把旧消息**压缩成一段摘要**，从而大幅减少Token消耗。

```python
from langchain.agents.middleware import SummarizationMiddleware
from langchain_openai import ChatOpenAI

summary_middleware = SummarizationMiddleware(
    model=ChatOpenAI(model="gpt-4o-mini"),   # 用于生成摘要的LLM
    trigger=("messages", 100),                # 触发条件：消息数量达到100条时压缩
)
```

压缩的效果示意：

```
压缩前（100条消息）：
  [用户:你好, AI:你好, 用户:天气?, AI:晴天, ..., 用户:最新问题]
                                ↓ SummarizationMiddleware 介入
压缩后（2条消息）：
  [系统:以下是之前对话的摘要：用户询问了天气、订单状态等问题..., 用户:最新问题]
```

`trigger`参数支持三种触发策略：

| 触发策略 | 写法 | 含义 |
|---------|------|------|
| 按消息数量 | `("messages", 100)` | 消息数量达到100条时触发压缩 |
| 按Token比例 | `("fraction", 0.5)` | Token数达到模型上下文窗口的50%时触发 |
| 按Token绝对值 | `("tokens", 3000)` | Token数达到3000时触发 |

### 5.3 人工审核中间件

有些操作是高风险的——比如转账、删除数据、发送邮件。即使LLM决定要执行这些操作，我们也希望**先让人类确认一下再真正执行**。

`HumanInTheLoopMiddleware`就是做这件事的。它会在指定的工具执行前暂停Agent，等待人类审核。

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware

# 配置哪些工具需要人工审核
hitl_middleware = HumanInTheLoopMiddleware(
    interrupt_on={
        "transfer_money": True,    # 转账 → 需要审核
        "delete_record": True,     # 删除 → 需要审核
        "get_weather": False,      # 查天气 → 不需要审核
    }
)
```

#### 完整示例

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

# ===== 1. 定义工具 =====
@tool
def get_weather(city: str) -> str:
    """查询天气"""
    return f"{city}的天气晴朗，气温25度。"

@tool
def transfer_money(amount: int, to_account: str) -> str:
    """转账操作（敏感操作，需要审核）

    Args:
        amount: 转账金额（元）
        to_account: 收款账户名称
    """
    print(f">>> 正在执行转账: {amount}元 → {to_account}")
    return f"成功转账 {amount} 元给 {to_account}。"

# ===== 2. 配置中间件 =====
hitl_middleware = HumanInTheLoopMiddleware(
    interrupt_on={
        "transfer_money": True,    # 转账需要审核
        "get_weather": False,      # 查天气不需要
    }
)

# ===== 3. 创建Agent =====
llm = init_chat_model("gpt-4o-mini", model_provider="openai")
checkpointer = InMemorySaver()

agent = create_agent(
    model=llm,
    tools=[get_weather, transfer_money],
    middleware=[hitl_middleware],
    checkpointer=checkpointer,        # 人工审核必须配合checkpointer使用
)

def run_demo():
    config = {"configurable": {"thread_id": "thread-1"}}

    # 改为同步的 invoke
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "请帮我转账 100 元给 Alice"}]},
        config=config,
    )
    print("------",result)

    if "__interrupt__" in result:
        interrupt_value = result["__interrupt__"][0].value
        print(f"⚠️ 操作被拦截，等待审核")

        decision = "approve"

        action_requests = interrupt_value.get("action_requests", [])
        decisions = [{"type": decision} for _ in action_requests]
        result = agent.invoke(
            Command(resume={"decisions": decisions}),
            config=config,
        )

    for msg in result.get("messages", []):
        if hasattr(msg, "type") and msg.type == "ai" and not getattr(msg, "tool_calls", None):
            print(f"[Agent]: {msg.content}")

run_demo()
```

执行流程图示：

<img src="images/7、执行流程图示.png" style="zoom:50%;" />

### 5.4 本章小结

1. **中间件是Agent的"拦截器"：** 可以在LLM调用前后、工具执行前后介入处理。
2. **SummarizationMiddleware：** 解决长对话中消息无限增长的问题，自动压缩历史消息为摘要。
3. **HumanInTheLoopMiddleware：** 对高风险操作增加人工审核环节，避免Agent自动执行敏感操作。
4. **中间件可以叠加使用：** 在`middleware`列表中传入多个中间件，它们会按顺序依次执行。



## 6、Agent最佳实践

前面五章我们学习了Agent的概念和各项能力。在实际项目中，光会用API还不够——**工具怎么设计、提示词怎么写、出了问题怎么排查**，这些"怎么用好"的经验往往决定了Agent的实际表现。

### 6.1 工具设计原则

工具是Agent与外部世界的接口。工具设计得好，LLM就能准确调用；设计得不好，LLM就会选错工具、传错参数，甚至根本不知道什么时候该用它。

**五条核心原则：**

| 原则 | 为什么重要 | 正面示例 | 反面示例 |
|------|-----------|---------|---------|
| **单一职责** | LLM更容易理解功能明确的工具 | `get_weather`、`get_forecast` 各做一件事 | `handle_weather_and_forecast_and_alert` 一个工具做太多事 |
| **描述清晰** | LLM完全依赖描述来决定何时用、怎么用 | "获取指定城市今天的实时天气，返回温度和天气状况" | "查天气" |
| **参数具体** | 减少LLM猜测参数格式的可能 | `date: str = Field(description="日期，格式YYYY-MM-DD")` | `date: str`（没有格式说明） |
| **错误友好** | LLM可以根据错误信息调整策略 | 返回 `"城市名'北精'无法识别，你是否指'北京'？"` | 抛出 `KeyError: '北精'` |
| **幂等安全** | 避免Agent重试时产生副作用 | `get_user(id=123)` 调用多次结果相同 | `create_order()` 调用多次会创建多个订单 |

> **经验法则：** 如果一个工具的docstring超过3句话才能描述清楚它做什么，说明这个工具承担了太多职责，应该拆分。

### 6.2 提示词优化

系统提示词是你给Agent的"工作手册"。一个好的系统提示词应该告诉Agent**它的角色、可用的工具、工作流程和注意事项**。

```python
# ✅ 好的系统提示词：结构清晰，指导明确
GOOD_PROMPT = """你是一个专业的数据分析助手。

你的工作流程：
1. 理解用户的分析需求
2. 使用 search 工具获取相关数据
3. 使用 calculate 工具进行计算
4. 用简洁的语言呈现分析结果

注意事项：
- 计算结果保留2位小数
- 如果数据不足以得出结论，主动告知用户
- 不要编造数据，所有数据必须来自工具查询
"""

# ❌ 差的系统提示词：太模糊，没有指导价值
BAD_PROMPT = """你是一个AI助手，帮助用户解决问题。"""
```

**提示词优化的关键点：**

| 要素 | 作用 | 示例 |
|------|------|------|
| **角色定位** | 约束Agent的回答风格和专业度 | "你是一个专业的数据分析助手" |
| **工作流程** | 引导Agent按合理顺序操作 | "先搜索数据，再计算，最后呈现" |
| **约束条件** | 避免Agent犯常见错误 | "不要编造数据" |
| **输出格式** | 统一回复的格式和质量 | "计算结果保留2位小数" |

### 6.3 调试技巧

Agent的执行过程是动态的、不确定的，出了问题比固定流程的Chain更难排查。以下是三个层次的调试手段：

**第一层：开启日志（快速定位）**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

开启后可以在控制台看到每次LLM调用的输入输出、每次工具调用的参数和结果。

**第二层：使用LangSmith（可视化追踪）**

```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "your-key"
os.environ["LANGSMITH_PROJECT"] = "my-agent-debug"
```

LangSmith会把Agent的每一步执行记录下来，在Web界面上以时间线的形式展示，可以清晰地看到：LLM每次推理的输入输出、选择了哪个工具、传了什么参数、工具返回了什么、共执行了多少轮循环。

**第三层：流式输出排查（观察中间过程）**

```python
# 用stream替代invoke，实时观察每一步
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "你的测试问题"}]}
):
    print(chunk, end="\n\n")
```

> **调试经验：** 大多数Agent问题的根源可以归为三类——工具描述不够清晰（LLM选错工具）、系统提示词引导不足（LLM执行顺序混乱）、工具返回值格式不规范（LLM无法解读结果）。遇到问题时优先从这三个方向排查。

### 6.4 性能优化

| 问题 | 优化方法 | 效果 |
|------|---------|------|
| **响应慢** | 只加载当前任务必需的工具，避免给LLM太多选择 | 减少LLM决策时间 |
| **Token消耗高** | 使用SummarizationMiddleware压缩历史消息 | 降低每次调用的Token用量 |
| **工具调用次数多** | 优化工具设计，一次返回尽量完整的信息 | 减少循环轮次 |
| **吞吐量不足** | 使用`ainvoke`异步调用，支持并发处理多个请求 | 提高吞吐量 |

### 6.5 本章小结

好的Agent不仅仅是能跑起来，更重要的是跑得准、跑得快、出了问题能排查。核心经验是：工具描述要像"说明书"一样清晰，系统提示词要像"工作手册"一样具体，调试时善用LangSmith可视化追踪。



---

## 7、课程总结

### 7.1 本课知识回顾

本课程围绕Agent展开，按照**"是什么 → 怎么造 → 怎么用好"**的逻辑，逐步构建了一个具备完整能力的Agent：

| 章节 | 核心问题 | 学到了什么 |
|------|---------|-----------|
| **一、Agent介绍** | Agent是什么？和Chain有什么区别？ | Agent = LLM + 自主决策 + 工具调用，通过循环完成动态任务 |
| **二、工具定义与使用** | 怎么让Agent能"做事"？ | `@tool`定义工具，`create_agent`组装Agent |
| **三、MCP工具** | 怎么接入别人已有的工具？ | MCP统一工具接入标准，`MultiServerMCPClient`接入远程工具 |
| **四、记忆** | 怎么让Agent"记住"对话？ | `checkpointer` + `thread_id` 实现多会话记忆 |
| **五、中间件** | 怎么控制Agent的执行过程？ | 消息压缩（SummarizationMiddleware）、人工审核（HumanInTheLoopMiddleware） |
| **六、最佳实践** | 怎么把Agent做好？ | 工具设计原则、提示词优化、调试技巧 |
| **七、完整实例** | 所有知识怎么组合？ | 智能客服Agent：综合运用工具+记忆+中间件 |

### 7.2 技术栈定位

<img src="images/8、LangChain完整知识体系.png" style="zoom:50%;" />

### 7.3 常见问题解答

**Q1: Chain和Agent如何选择？**

任务流程确定时用Chain（简单可靠），任务需要动态判断时用Agent（灵活但复杂度更高）。两者可以结合——Agent内部的某些子任务可以用Chain实现。

**Q2: RAG和Agent可以结合吗？**

可以，而且非常常见。典型做法是把RAG检索封装成一个工具，Agent在需要时自主调用它。本课第七章的`query_knowledge_base`工具就是一个简化版的RAG。

**Q3: 如何优化Agent的响应速度？**

四个方向：只加载必需的工具（减少LLM决策开销）、用SummarizationMiddleware压缩长对话（减少Token）、使用异步调用`ainvoke`（支持并发）、优化工具的返回值格式（减少循环轮次）。

**Q4: 什么时候需要LangGraph？**

当你需要多个Agent协作、需要复杂的条件分支和循环逻辑、或需要比`create_agent`更精细的流程控制时，就需要LangGraph。LangGraph是Agent的进阶编排工具，将在后续课程中详细讲解。

### 7.4 下一步建议

- **动手实践：** 选择一个实际场景（如个人知识库问答、自动化数据分析），用本课学到的知识构建一个Agent
- **深入LangGraph：** 学习状态图、条件边、多Agent协作，构建更复杂的工作流
- **关注AI生态：** 关注社区动态可以快速扩展Agent的能力

**推荐资源：**

- LangChain官方文档：https://docs.langchain.com/
- LangSmith调试追踪：https://www.langchain.com/langsmith
- LangGraph文档：https://docs.langchain.com/oss/python/langgraph
- GitHub示例库：https://github.com/langchain-ai/langgraph/tree/main/examples

---
