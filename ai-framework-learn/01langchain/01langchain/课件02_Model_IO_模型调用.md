# Model I/O - 模型调用

> 尚硅谷大模型技术之LangChain V1.1.0

---

## 1、Model I/O 介绍

### 1.1 什么是 Model I/O

上一节课我们认识了 LangChain 的整体架构（三层：基础层 → 能力层 → 应用层）。从本节开始，我们正式进入代码实战，第一站就是 **Model I/O**——LangChain 中与大语言模型交互的核心流程。

Model I/O 回答的是一个最基本的问题：**"怎么把问题喂给模型，并拿到有用的结果？"**

### 1.2 Model I/O 的三个环节

<img src="images/3、 MOdelIO 的三个环节.png" style="zoom:67%;" />

| 环节 | 做什么 | 本课程对应课件 |
|------|-------|--------------|
| **Prompts（提示词模板）** | 把用户输入和系统指令格式化成模型能理解的消息 | 课件03 |
| **Models（模型调用）** | 统一接口调用不同平台的模型（OpenAI、DeepSeek、本地模型等） | **本节重点** |
| **Output Parsers（输出解析）** | 把模型返回的文本转换为 JSON、Pydantic 对象等结构化数据 | 课件03 |

> 本节聚焦中间的 **Models** 环节——怎么连接模型、怎么调用、怎么接入不同平台。Prompts 和 Output Parsers 将在下一节课件中展开。

### 1.3 LangChain 中的三类模型

LangChain 中有三类"模型"，但它们的用途完全不同，不要混淆：

```
                    LangChain 模型类型
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    Chat Models         LLMs         Embeddings
     "对话型"          "补全型"         "向量型"
                                    
  输入：消息列表      输入：字符串     输入：文本
  输出：AI消息        输出：字符串     输出：数字向量
                                    
  ★ 主流，本课重点    ⚠ 已过时       ★ RAG课件再讲
```

| 类型 | 输入 → 输出 | 代表类 | 说明 |
|------|------------|--------|------|
| **Chat Models** | 消息列表 → AI消息 | `ChatOpenAI`、`ChatAnthropic`、`ChatOllama` | **当前主流**，所有现代模型（GPT-4o、Claude、DeepSeek 等）都是对话模型。本课程全程使用此类型 |
| **LLMs** | 字符串 → 字符串 | `OpenAI`（旧版） | **已基本淘汰**。早期的文本补全模型（如 GPT-3 text-davinci），不支持消息格式。LangChain v1.x 仍保留接口但不推荐使用 |
| **Embeddings** | 文本 → 浮点数向量 | `OpenAIEmbeddings`、`HuggingFaceEmbeddings` | **用途不同**。不生成文本，而是将文本转换为数字向量，用于语义搜索和 RAG。将在 RAG 课件中详细讲解 |

> **结论**：本课程中提到的"模型调用"，除非特别说明，都是指 **Chat Models**。

### 1.4 统一接口的价值

不管你用的是 OpenAI、DeepSeek、Claude 还是本地的 Ollama，LangChain 都提供了完全一致的调用方式：

```python
# 不同平台，同一套代码
llm = ChatOpenAI(model="gpt-4o-mini")          # OpenAI
llm = ChatOpenAI(model="deepseek-chat", ...)    # DeepSeek
llm = ChatAnthropic(model="claude-sonnet-4-20250514")  # Anthropic
llm = ChatOllama(model="qwen2.5:7b")           # 本地模型

# 调用方式完全一致
response = llm.invoke("你好")          # 同步调用
response = await llm.ainvoke("你好")   # 异步调用
for chunk in llm.stream("你好"):       # 流式输出
    print(chunk.content, end="")
responses = llm.batch(["问题1", "问题2"])  # 批量调用
```

这就是 Model I/O 中 Models 层的核心价值：**一次学会，到处能用。**

---

## 2、调用在线模型

> **前置约定**：本章所有代码示例均假设你已在项目根目录创建了 `.env` 文件，配置好 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`（参见课件01 第4.8节）。

### 2.1 为什么不直接用原生 SDK？

刚接触 LangChain 的同学可能会问："我直接用 OpenAI 的 SDK 不就行了，为什么要多学一层框架？"

在回答这个问题之前，先了解一下"原生 SDK"是什么、行业现状如何。

#### 2.1.1 OpenAI SDK：行业事实标准

OpenAI 的 GPT 系列模型不仅推动了大模型技术的发展，还定义了整个行业的**开发范式和接口标准**。目前大部分模型（Qwen、ChatGLM、DeepSeek 等）的 API 都遵循 OpenAI 定义的规范，可以直接使用 OpenAI SDK 来调用。

OpenAI 的 API 经历了两代演进：

| API | 发布时间 | 说明 |
|-----|---------|------|
| **Chat Completions API** | 2023年 | 经典 API，行业标准，几乎所有模型都兼容这套格式 |
| **Responses API** | 2025年中 | 新一代 API，支持服务端内置工具调用、服务端维护对话状态（短期记忆）等 |

> **官方文档**：[Chat Completions API](https://platform.openai.com/docs/api-reference/chat) \| [Responses API](https://platform.openai.com/docs/api-reference/responses)

**Chat Completions API 调用示例**（经典，也是 LangChain 底层使用的格式）：

```python
# uv add openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "将'你好'翻译成意大利语"}],
)
print(completion.choices[0].message.content)
```

**Responses API 调用示例**（新一代，支持内置工具）：

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input="中国国内今天发生了哪些大事儿？",
    tools=[{"type": "web_search"}]   # 服务端内置工具，无需自己实现
)
print(response.output_text)
```

> **本课程说明**：LangChain 目前底层使用的是 Chat Completions API 格式。Responses API 较新，LangChain 的支持还在演进中。了解两者的区别即可，后续代码统一基于 Chat Completions API。

看起来原生 SDK 已经很好用了？那为什么还需要 LangChain？

#### 2.1.2 原生 SDK 的痛点：切换模型

用一个真实场景来感受——**"同一个任务，先用 GPT-4o-mini 跑，再换成 DeepSeek 跑，再换成 Claude 跑，对比结果"**：

**用原生 SDK：每换一个平台，改一堆代码**

```python
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# ---- 调用 OpenAI ----
client_openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)
resp1 = client_openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "用一句话解释量子计算"}],
)
print(resp1.choices[0].message.content)

# ---- 换成 DeepSeek ----
# 要重新创建 client、改 api_key、改 base_url、改 model……
client_deepseek = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)
resp2 = client_deepseek.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "用一句话解释量子计算"}],
)
print(resp2.choices[0].message.content)

# ---- 换成 Anthropic？不兼容 OpenAI 格式，整套代码重写…… ----
import anthropic
client_claude = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
)
message = client_claude.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "用一句话解释量子计算"}],
)
print(message.content[0].text)   # 注意：取值方式都不一样！
```

三个平台，三套 client，三种取值方式。如果还要加流式输出、错误重试、对话记忆……代码量会爆炸式增长。

#### 2.1.3 用 LangChain：只改一行初始化，其余代码不动

```python
# uv add langchain-openai langchain-anthropic
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()

# ---- 调用 OpenAI ----
llm = ChatOpenAI(model="gpt-4o-mini")
print(llm.invoke("用一句话解释量子计算").content)

# ---- 换成 DeepSeek？改一行 ----
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)
print(llm.invoke("用一句话解释量子计算").content)  # 调用代码完全一样

# ---- 换成 Anthropic？也是改一行初始化 ----
llm = ChatAnthropic(model="claude-sonnet-4-20250514")
print(llm.invoke("用一句话解释量子计算").content)  # 调用代码还是一样
```

**差距在哪？**

| 维度 | 原生 SDK | LangChain |
|------|---------|-----------|
| 切换模型 | 改 client、改参数、可能改整套代码 | 只改一行初始化 |
| 调用方式 | 每个平台不一样（OpenAI 用 `client.chat.completions.create()`，Anthropic 用 `client.messages.create()`） | 统一 `llm.invoke()` |
| 取值方式 | OpenAI 用 `.choices[0].message.content`，Anthropic 用 `.content[0].text` | 统一 `.content` |
| 流式输出 | 每个平台的 stream 写法不同 | 统一 `llm.stream()` |
| 批量调用 | 自己写循环或并发 | 内置 `llm.batch()` |
| 加功能（记忆、工具、RAG） | 全部从零写 | 框架内置，直接组合 |

> 模型只有一两个时感觉差不多，但当你要对比 3-5 个模型、加上流式输出、再接上 RAG 管道时，原生 SDK 的代码量会呈指数增长，而 LangChain 始终保持简洁。


### 2.2 基础使用：ChatOpenAI

`ChatOpenAI` 是你在 LangChain 中最常用的类，日常开发 90% 的场景都用它。

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# 最简写法：环境变量里已配好 OPENAI_API_KEY 和 OPENAI_BASE_URL
llm = ChatOpenAI(model="gpt-4o-mini")

response = llm.invoke("你好，介绍一下LangChain")

# response 是一个 AIMessage 对象，不是普通字符串
print(type(response))            # <class 'langchain_core.messages.ai.AIMessage'>
print(response.content)          # 模型返回的文本内容
print(response.response_metadata)  # 模型名称、token消耗等元信息
```

> **注意**：`llm.invoke()` 返回的是 `AIMessage` 对象，不是字符串。要拿文本内容需要 `.content`。这个设计是为了保留消息的元信息（角色、token 用量等），在构建对话链时会用到。

### 2.3 核心参数详解

初始化 `ChatOpenAI` 时可以传入多个参数来控制模型行为：

```python
llm = ChatOpenAI(
    model="gpt-4o-mini",       # 模型名称（必填）
    temperature=0.7,            # 随机性，0=确定性，1=有创意（默认因模型而异）
    max_tokens=1000,            # 最大输出长度
    timeout=60,                 # 超时时间（秒）
    max_retries=2,              # 失败重试次数
)
```

#### 2.3.1 temperature 到底怎么选？

`temperature` 是最常调的参数，它控制模型输出的"创造力"：

```python
from langchain_openai import ChatOpenAI

question = "给我的咖啡店起个名字"

# temperature=0 —— 确定性输出，每次结果几乎一样
llm_precise = ChatOpenAI(model="gpt-4o-mini", temperature=0)
print(llm_precise.invoke(question).content)
# → "醇香时光咖啡馆"（每次运行结果固定）

# temperature=1 —— 有创意，每次结果不同
llm_creative = ChatOpenAI(model="gpt-4o-mini", temperature=1)
print(llm_creative.invoke(question).content)
# → "晨雾与豆语"（下次运行可能是另一个名字）
```

**选择建议**：

| 场景 | 推荐 temperature | 原因 |
|------|-----------------|------|
| 代码生成、数据提取、翻译 | **0 ~ 0.3** | 需要准确、稳定的输出 |
| 问答、摘要、分析 | **0.3 ~ 0.7** | 兼顾准确性和流畅性 |
| 创意写作、头脑风暴、起名 | **0.7 ~ 1.0** | 需要多样性和创造力 |

#### 2.3.2 Token 是什么？

讲 token，最容易误解的一点就是：**它不是“字数”，也不是“单词数”**。

大模型真正处理的最小单位，是 token。你可以把它理解成：模型内部用来读写文本的“最小片段”。这个片段有时候是一个字，有时候是半个词，有时候是一个完整单词，甚至可能只是一个标点。

所以，同样一句话，**人眼看起来长度差不多，token 数却可能差很多**。

| 语言 | 1 个 Token ≈ | 示例 |
|------|-------------|------|
| 中文 | 1 ~ 1.8 个汉字 | "你好世界" 可能被切成 2 ~ 4 个 token |
| 英文 | 3 ~ 4 个字母 | "Hello World" 通常是 2 ~ 3 个 token |

这里一定要注意：**同一段文本，在不同模型、不同分词器下，token 数并不一定相同。**

为什么？因为每家模型厂商背后的**分词器（tokenizer）**不一样。

分词器本质上就是：**把一段文本切成 token 的规则和词表**。不同分词器的词表不同、切分策略不同，所以最后统计出来的 token 数也会不同。

比如下面三种情况就很常见：

- 同样是 `Hello world`，有的分词器可能切成 **2 个 token**，有的会更多
- 同样是 `LangChain 很好用`，中英混合文本常常比纯英文更容易出现 token 差异
- 同样一段 Python 代码，空格、换行、括号、变量名都会参与切分，所以代码的 token 数往往比肉眼估算更高

#### 2.3.3 常见分词器例子

1. **OpenAI 的 `cl100k_base`**  
   GPT-4、GPT-4o 这一代模型常见的分词器，很多英文文本和代码场景都会用它来计数。

2. **OpenAI 的 `o200k_base`**  
   更新一代的分词器，词表更大，在部分多语言文本里会比 `cl100k_base` 更省 token。

3. **Anthropic / Claude 自家的分词器**  
   Claude 使用自己的 token 切分规则，所以同一句中文、同一段提示词，放到 Claude 里统计，结果通常不会和 OpenAI 完全一样。

> **一句话记忆**：token 不是固定按“几个字”来算，而是按“当前模型使用的分词器怎么切”来算。

#### 2.3.4 可以直接在线测试的工具

- **OpenAI Tokenizer**：<https://platform.openai.com/tokenizer>  

模型提供商通常按 token 数量计费，`max_tokens` 参数限制的是**输出**的最大 token 数。如果你发现模型的回答被截断了，通常是 `max_tokens` 设太小了。

补充理解：

- **输入 token**：你发给模型的提示词、上下文、历史对话
- **输出 token**：模型生成的回答
- **总消耗 token** = 输入 token + 输出 token

所以，一次调用是否贵，不只取决于回答长不长，也取决于你喂给模型的上下文有多长。

### 2.4 进阶：init_chat_model（动态切换模型）

当你需要在**运行时动态切换**不同提供商的模型时，`init_chat_model` 比 `ChatOpenAI` 更方便——不需要 import 不同的类：

```python
# uv add langchain-openai
# uv add langchain-anthropic
# uv add google-genai

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()

# 一个函数搞定所有提供商，通过 model_provider 参数区分
llm_openai = init_chat_model("gpt-5.4-nano-2026-03-17", model_provider="openai",api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("OPENAI_BASE_URL")) 
llm_claude = init_chat_model("claude-opus-4-7", model_provider="anthropic",api_key=os.getenv("ANTHROPIC_API_KEY"),base_url=os.getenv("ANTHROPIC_BASE_URL"))
llm_gemini = init_chat_model("gemini-3.1-flash-lite-preview", model_provider="google_genai",api_key=os.getenv("GEMINI_API_KEY"),base_url=os.getenv("GEMINI_BASE_URL"))

# 调用方式完全一致
for name, llm in [("OpenAI", llm_openai), ("Claude", llm_claude), ("Gemini", llm_gemini)]:
    response = llm.invoke("用一句话介绍你自己")
    print(f"{name}: {response.content}")
```

**什么时候用哪个？**

| 场景 | 用什么 | 原因 |
|------|-------|------|
| 日常开发，模型固定 | `ChatOpenAI` / `ChatAnthropic` 等具体类 | 代码提示好，参数明确 |
| 需要动态切换模型（A/B测试、用户选择模型） | `init_chat_model` | 一个函数搞定所有提供商 |
| 不兼容 OpenAI 格式的平台（Anthropic、Google） | `init_chat_model` 或对应的专用类 | `ChatOpenAI` 只能调 OpenAI 兼容的接口 |

---

## 3、模型调用方式详解

调用大模型就像打电话：你得先知道"说什么"（消息类型），再知道"怎么说"（传入方式），最后知道"怎么拨号"（调用方式）。这一节按这个逻辑展开。

### 3.1 消息类型：传什么

LangChain 用标准化的消息格式来传递不同角色的内容。理解这四种消息类型，是构建对话应用的基础。

| 消息类型 | 类名 | 用途 | 示例 |
|----------|------|------|------|
| **系统消息** | `SystemMessage` | 设定AI的行为、角色和规则 | "你是一个有帮助的助手" |
| **用户消息** | `HumanMessage` | 用户的输入 | "帮我解释一下量子计算" |
| **AI消息** | `AIMessage` | AI的回复，可用于对话历史 | "量子计算是..." |
| **工具消息** | `ToolMessage` | 工具执行返回的结果 | 工具调用的输出 |

> **记忆口诀**：系统定规则，用户提问题，AI给回复，工具报结果。

**基础示例**：

```python
from langchain_core.messages import (
    HumanMessage
)
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# 单个消息
response = llm.invoke([HumanMessage(content="你好")])
print(response.content)
```

**实战示例：构建完整对话历史**

```python
from langchain_core.messages import (
    HumanMessage,SystemMessage,AIMessage
)
# 对话历史——模拟多轮对话
conversation = [
    SystemMessage(content="你是一个有帮助的AI助手"),
    HumanMessage(content="你好，我叫hzk"),
    AIMessage(content="你好！hzk,有什么我可以帮助你的吗？"),
    HumanMessage(content="我叫什么名字？"),
]

response = llm.invoke(conversation)
print(response.content)
```

> **为什么需要区分消息类型？**
>
> - 系统消息：设定AI的"人设"和行为规则
> - 用户消息：真正的问题或指令
> - AI消息：保留历史上下文，让AI"记得"之前说过什么
> - 工具消息：当AI调用外部工具时，工具返回的结果

---

### 3.2 传入方式：怎么传

知道"传什么"之后，下一个问题是："怎么传给模型？"常用三种传入方式，各有适用场景。

#### 快速决策表

| 你的需求 | 推荐方式 | 代码示例 |
|---------|---------|---------|
| **简单问答**，不需要上下文 | 直接传字符串 | `llm.invoke("你好")` |
| **需要角色设定**或**对话历史** | 传消息列表 | `llm.invoke([SystemMessage(...), HumanMessage(...)])` |
| **动态构建**消息，或从其他格式转换 | 用元组/字典 | `llm.invoke([("system", "..."), ("user", "...")])` |

**一句话记忆**：

- 能用字符串就用字符串（最简单）
- 需要对话/角色时用消息列表（最常见）
- 动态构建时用元组/字典（最灵活）

#### 方式一：直接传入字符串（最简单）

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke("你好，介绍一下LangChain")
print(response.content)
```

**适用场景**：
- 单轮问答，不需要上下文
- 不需要设定 AI 的角色或行为规则
- 快速测试或调试

**优势**：代码最简洁，一行搞定

**局限**：无法保留对话历史，无法设定系统提示词

#### 方式二：传入消息列表（最常用）

```python
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

llm = ChatOpenAI(model="gpt-4o-mini")

response = llm.invoke([
    SystemMessage(content="你是一个专业的Python编程助手"),
    HumanMessage(content="什么是装饰器？")
])
print(response.content)
```

**适用场景**：
- 需要**设定 AI 角色**（比如"你是一个翻译助手"）
- 需要**保留对话历史**
- 需要**区分**系统指令/用户输入/AI回复

**实战示例：多轮对话**

```python
from langchain_core.messages import HumanMessage, AIMessage

# 对话历史
conversation = [
    HumanMessage(content="什么是LangChain？"),
    AIMessage(content="LangChain是一个用于开发大模型应用的框架。"),
    HumanMessage(content="它有哪些核心组件？")  # 这依赖于上一轮的上下文
]

response = llm.invoke(conversation)
print(response.content)
```

#### 方式三：使用元组或字典（最灵活）

```python
# 元组方式：(角色, 内容)
tuple_messages = [
    ("system", "你是一个专业的Python编程助手"),
    ("user", "什么是装饰器？")
]

# 字典方式：{"role": 角色, "content": 内容}
dict_messages = [
    {"role": "system", "content": "你是一个专业的Python编程助手"},
    {"role": "user", "content": "什么是装饰器？"}
]

print(llm.invoke(tuple_messages))
print(llm.invoke(dict_messages))

```

**适用场景**：
- 从 API 返回的 JSON 数据直接转成消息列表
- 从配置文件或数据库读取对话模板
- 动态构建消息列表

**实战示例：从配置读取对话模板**

```python
# 假设这是从配置文件读取的
prompt_template = [
    {"role": "system", "content": "你是一个{role}"},
    {"role": "user",   "content": "请解释{topic}"}
]

# 动态填充
messages = [
    {
        "role": t["role"],
        "content": t["content"].format(
            role="翻译助手",
            topic="机器翻译",
        ),
    }
    for t in prompt_template
]
print(llm.invoke(messages).content)
```

---

### 3.3 调用方式：怎么调

知道"传什么"和"怎么传"之后，最后一个问题是："怎么调用模型？"LangChain 提供了多种调用方式，适应不同场景。

#### 3.3.1 同步调用 - `invoke()`（最常用）

最基础的调用方式，适合大多数场景：

```python
response = llm.invoke("什么是LangChain？")
print(response.content)
```

**适用场景**：

- 单次调用，不需要高并发
- 简单问答、文本生成
- 快速原型开发

#### 3.3.2 异步调用 - `ainvoke()`（高并发）

适用于需要同时处理多个请求的高并发场景。要理解 `ainvoke()` 的价值，需要先搞清楚一个前置知识：**Python 的异步编程（async/await）**。

##### 前置知识：同步 vs 异步

```
同步（invoke）：排队买奶茶
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
你 → 点单 → 等10分钟 → 拿到 → 再点下一杯 → 等10分钟 → 拿到
     5杯奶茶总耗时：50分钟（串行等待）

异步（ainvoke）：扫码下单
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
你 → 5杯同时下单 → 哪杯好了取哪杯
     5杯奶茶总耗时：≈10分钟（并行等待）
```

**为什么模型调用特别适合异步？** 因为 `llm.invoke()` 的耗时几乎全花在"等网络响应"上，CPU 其实是闲着的。异步让你在等第1个响应的同时，把第2、3、4、5个请求也发出去，所有等待时间重叠，总耗时 ≈ 单次最慢的那个请求。

##### 基础用法

```python
import asyncio
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

async def call_llm_async():
    response = await llm.ainvoke("什么是LangChain？")
    print(response.content)

# Jupyter Notebook 中直接 await（见下方说明）
await call_llm_async() # 方式一
asyncio.run(call_llm_async()) # 方式二
```

##### invoke() vs ainvoke() 性能对比

```python
import time
import asyncio
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# 准备 5 个测试问题
prompts = [
    "用一句话介绍一下北京",
    "用一句话介绍一下上海",
    "用一句话介绍一下广州",
    "用一句话介绍一下深圳",
    "用一句话介绍一下杭州"
]


# ========== 测试一：同步 invoke（串行） ==========
def test_sync_invoke():
    print("=== 同步 invoke ===")
    start_time = time.time()

    for i, prompt in enumerate(prompts):
        print(f"  [同步] 正在发送第 {i + 1} 个请求...")
        llm.invoke(prompt)  # 死等，拿到结果才进入下一次循环

    print(f"总耗时: {time.time() - start_time:.2f} 秒\n")


# ========== 测试二：异步 ainvoke（并行） ==========
async def test_async_ainvoke():
    print("=== 异步 ainvoke ===")
    start_time = time.time()

    # 关键：用 asyncio.gather 同时派发所有请求
    print("  [异步] 瞬间派发 5 个请求...")
    tasks = [llm.ainvoke(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks)

    for r in results:
        print(f"  回答: {r.content[:20]}...")

    print(f"总耗时: {time.time() - start_time:.2f} 秒\n")


# ========== 运行对比 ==========
async def main():
    test_sync_invoke()         # 先跑同步
    await test_async_ainvoke() # 再跑异步

await main()
```

**典型输出**：

```
=== 同步 invoke ===
  [同步] 正在发送第 1 个请求...
  [同步] 正在发送第 2 个请求...
  ...
总耗时: 8.73 秒

=== 异步 ainvoke ===
  [异步] 瞬间派发 5 个请求...
总耗时: 1.92 秒
```

> 5个请求，同步耗时 ~9秒，异步耗时 ~2秒——快了 4-5 倍。请求越多，差距越大。

##### 关键知识点：ainvoke() 和 asyncio.gather() 各自干了什么？

看完对比你可能会问：既然 `ainvoke()` 是异步函数，为什么逐个 `await ainvoke()` 跟同步一样慢？

因为 **`ainvoke()` 和 `gather()` 解决的是两个不同的问题**：

```
ainvoke() 解决的是 → "等待时不阻塞"（让出 CPU，别的任务有机会插进来）
gather()  解决的是 → "同时派发多个任务"（把多个协程塞进事件循环并行跑）
```

回到奶茶店的比喻：

- `invoke()` = 你**站在柜台前死等**，奶茶没做好之前你哪儿也去不了，后面的人也点不了单
- `ainvoke()` = 你**扫码下单后去旁边坐着**，不占柜台了，后面的人可以继续点单
- `asyncio.gather()` = **同时帮5个人下单**，让奶茶店并行制作

所以：如果只有你一个人买奶茶，`ainvoke()`（坐着等）和 `invoke()`（站着等）时间一样长——因为没有"后面的人"需要你让位。**`ainvoke()` 的价值在于"让出控制权"，而 `gather()` 的价值在于"利用让出的控制权塞入更多任务"。两者缺一不可。**

```python
# ❌ 错误理解：用了 ainvoke 就会快
# 实际效果：还是串行，因为每次 await 都在等当前这个完成
async def wrong_way():
    r1 = await llm.ainvoke("问题1")    # 等第1个完成（2秒）
    r2 = await llm.ainvoke("问题2")    # 再等第2个完成（2秒）
    r3 = await llm.ainvoke("问题3")    # 再等第3个完成（2秒）
    # 总耗时：~6秒（串行）

# ✅ 正确写法：ainvoke 负责"能让出"，gather 负责"同时跑"
async def right_way():
    tasks = [
        llm.ainvoke("问题1"),       # 创建协程，但不等待
        llm.ainvoke("问题2"),       # 创建协程，但不等待
        llm.ainvoke("问题3"),       # 创建协程，但不等待
    ]
    r1, r2, r3 = await asyncio.gather(*tasks)  # 三个请求同时发出，同时等待
    # 总耗时：~2秒（并行）
```

| 写法 | 效果 | 类比 |
|------|------|------|
| `invoke()` 逐个调用 | 串行，阻塞 | 站在柜台前死等，一杯一杯买 |
| `await ainvoke()` 逐个调用 | 串行，不阻塞但没利用起来 | 扫码后坐着等，但只点了1杯，没人需要你让位 |
| `asyncio.gather(*tasks)` | 并行，耗时 ≈ 最慢的那个 | 同时下单5杯，谁好了取谁 |

> `*tasks` 是 Python 的解包语法：`gather(*[a, b, c])` 等价于 `gather(a, b, c)`。

##### 运行环境差异：Jupyter vs 普通 .py 文件

你可能注意到了，上面的代码直接写了 `await main()`，而不是 `asyncio.run(main())`。这是因为运行环境不同：

| 环境 | 启动异步的方式 | 原因 |
|------|--------------|------|
| **Jupyter Notebook / IPython** | `await main()` | Jupyter 内部已经有一个事件循环在运行，不能再创建新的 |
| **普通 .py 文件** | `asyncio.run(main())` | 需要自己创建并启动事件循环 |

```python
# ===== Jupyter Notebook 中 =====
async def main():
    response = await llm.ainvoke("你好")
    print(response.content)

await main()           # ✅ 直接 await
# asyncio.run(main())  # ❌ 会报错：Cannot run nested event loops


# ===== 普通 .py 文件中 =====
import asyncio

async def main():
    response = await llm.ainvoke("你好")
    print(response.content)

# await main()          # ❌ 会报错：await 只能在 async 函数内使用
asyncio.run(main())     # ✅ 创建事件循环并运行
```

> **本课程代码默认在 Jupyter 环境中运行**，所以统一使用 `await` 写法。如果你在 PyCharm 的 .py 文件中运行，把 `await main()` 改成 `asyncio.run(main())` 即可。

**适用场景**：

- 需要同时处理多个请求（批量调用、并行对比）
- Web 服务、API 接口（FastAPI 等异步框架）
- 对响应时间有要求的应用


#### 3.3.3 流式调用 - `stream()`（打字机效果）

实现打字机效果，提升用户体验：

```python
def streaming_example():
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini")

    print("AI回答: ")
    full_message = None
    for chunk in llm.stream("请写一首关于春天的诗"):
        # 累积消息块
        full_message = chunk if full_message is None else full_message + chunk
        print(chunk.content, end="", flush=True)

    # 完整消息
    print(f"\n\n完整消息:\n{full_message.content}")

streaming_example()
```

> `flush=True` 的作用是**强制将内存缓冲区中的内容立刻推送到屏幕上显示**，而不是等攒够了一定数量或者遇到换行符才显示。

**流式事件监听**（高级用法）：

```python
async def stream_events():
    async for event in llm.astream_events("你好"):
        if event["event"] == "on_chat_model_start":
            print(f"输入: {event['data']['input']}")
        elif event["event"] == "on_chat_model_stream":
            print(f"Token: {event['data']['chunk'].content}", end="",flush=True)
        elif event["event"] == "on_chat_model_end":
            print(f"\n完成!")
await stream_events()
```

**适用场景**：
- 聊天机器人、对话系统
- 长文本生成（让用户看到进度）
- 实时交互应用

#### 3.3.4 批次调用 - `batch()`（并行处理）

并行处理多个独立请求：

```python
def batch_example():
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini")

    questions = [
        "什么是Python？",
        "什么是JavaScript？",
        "什么是Go语言？"
    ]

    responses = llm.batch(questions)
    for q, r in zip(questions, responses):
        print(f"Q: {q}")
        print(f"A: {r.content}\n")

batch_example()
```



**适用场景**：
- 批量处理多个独立请求
- 数据分析、批量内容生成
- 不需要按顺序返回结果



批量异步调用：

```python
async def batch_async():
    questions = [
        "什么是LangChain？",
        "LangChain的核心组件有哪些？",
        "如何使用LangChain构建Agent？"
    ]
    responses = await llm.abatch(questions)
    for q, r in zip(questions, responses):
        print(f"Q: {q}\nA: {r.content}\n")

await batch_async()
```



---

### 3.4 调用配置与高级特性

#### 3.4.1 运行时配置

通过 `config` 参数传递运行时配置：

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

response = llm.invoke(
    "讲一个笑话",
    config={
        "tags": ["humor", "demo"],          # 标签
        "metadata": {"user_id": "123"},     # 元数据
    }
)
print(response)
```

> `config` 字典是在 LangChain 框架层流转的“元数据”，专门用于系统的观测、调试和日志记录，它与业务层面的问答结果 `response` 是严格分离的。

**用途**：

- 调试和追踪
- 日志记录（通过 metadata 传递额外信息）
- 监控和分析

**. 这些 `config` 数据到底去哪了？**

这些数据被 LangChain 的 **回调系统（Callback System）** 拦截并收集起来了。它们主要用于以下两个场景：

场景 A：云端监控与可视化（LangSmith）通过在环境变量中配置了 LangSmith（LangChain 官方的监控平台）

场景 B：本地回调拦截,通过**回调处理器（Callback Handler）**来拦截它们

```python
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler

# 1. 自定义一个回调处理器，拦截并打印运行信息
class MyDebugCallback(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, prompts, **kwargs):
        print("\n" + "="*40)
        print(" [拦截到 LLM 启动请求]")
        print(f" Tags: {kwargs.get('tags')}")
        print(f" Metadata: {kwargs.get('metadata')}")

        print("="*40 + "\n")

llm = ChatOpenAI(model="gpt-4o-mini")

# 2. 在调用时，将你的回调处理器传进去
response = llm.invoke(
    "讲一个短笑话",
    config={
        "tags": ["humor", "demo"],
        "metadata": {"user_id": "123"},
        "callbacks": [MyDebugCallback()]  # 关键：挂载你的回调
    }
)

print("最终返回的 response 依然只有大模型的内容：")
print(response.content)
```

> **`messages` / `prompts`**：包裹里的货品（比如“讲个笑话”）。
>
> **`config / kwargs`**：运单上的加急标签、客户编号（比如 `tags`, `metadata`）。
>
> **`serialized`**：这辆快递车的**车辆行驶证**。上面写着车牌号（模型名称）、排量（Temperature）、车辆品牌（OpenAI 类路径），它不影响包裹的内容，但对车队管理员（框架和开发者）来说是必不可少的档案。



#### 3.4.2 运行时动态切换模型

2.4 节介绍了用 `init_chat_model` 在初始化时选择不同模型。这里展示一个更高级的用法——**不重新初始化，在调用时通过 config 参数动态切换**：

```python
from langchain.chat_models import init_chat_model

configurable_model = init_chat_model(temperature=0)

# 使用GPT-4
result1 = configurable_model.invoke(
    "你好",
    config={"configurable": {"model": "gpt-4o-mini"}}
)

# 使用Claude
result2 = configurable_model.invoke(
    "你好",
    config={"configurable": {"model": "claude-sonnet-4-6"}}
)
```

**适用场景**：

- 需要在运行时根据用户选择切换模型
- A/B 测试不同模型效果
- 多租户系统（不同客户使用不同模型）

---

## 4、不同平台的模型调用实战

课件01 介绍了多种大模型服务平台，本节逐一演示如何用 LangChain 接入它们。每个平台都给出完整的 `.env` 配置和代码示例，复制即用。

### 4.1 通过 CloseAI 代理调用 OpenAI（本课程推荐）

CloseAI 提供与 OpenAI 完全兼容的 API 接口，只需替换 `base_url`。

**.env 配置**：

```env
OPENAI_API_KEY=sk-你的CloseAI密钥
OPENAI_BASE_URL=https://api.closeai-asia.com/v1
```

**代码示例**：

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# 无需手动传参，自动读取环境变量 OPENAI_API_KEY 和 OPENAI_BASE_URL
llm = ChatOpenAI(model="gpt-4o-mini")

response = llm.invoke("你好，介绍一下LangChain")
print(response.content)
```

> **要点**：CloseAI 的接口和 OpenAI 完全一致，代码无需任何适配。`langchain-openai` 包会自动识别 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL` 这两个环境变量。

### 4.2 直连 DeepSeek

DeepSeek 的 API 兼容 OpenAI 接口格式，可以直接使用 `ChatOpenAI`。

**.env 配置**：

```env
DEEPSEEK_API_KEY=sk-你的DeepSeek密钥
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

**代码示例**：

```python
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# DeepSeek 兼容 OpenAI 接口，直接用 ChatOpenAI 即可
llm = ChatOpenAI(
    model="deepseek-chat",               # DeepSeek-V3.2
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)

response = llm.invoke("用一句话解释什么是大语言模型")
print(response.content)
```

> **提示**：DeepSeek 也提供了专用的 `langchain-deepseek` 包（`uv add langchain-deepseek`），用法类似。但由于 DeepSeek 兼容 OpenAI 格式，直接用 `ChatOpenAI` 更简单，不需要多装一个包。

### 4.3 硅基流动调用开源模型

硅基流动聚合了 50+ 开源模型（DeepSeek、Qwen、GLM 等），同样兼容 OpenAI 接口格式。

**.env 配置**：

```env
SILICONFLOW_API_KEY=sk-你的硅基流动密钥
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
```

**代码示例**：

```python
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# 硅基流动的模型名称格式：厂商/模型名
llm = ChatOpenAI(
    model="Qwen/Qwen3-8B",                       
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL"),
)

response = llm.invoke("什么是量子计算？")
print(response.content)
```

> **省钱技巧**：硅基流动新用户送 2000 万 Token，部分模型（如 Qwen3-8B）完全免费，非常适合学习阶段使用。

### 4.4 接入不兼容 OpenAI 格式的平台

4.1 ~ 4.3 的平台都兼容 OpenAI 格式，所以直接用 `ChatOpenAI` 就能搞定。但 Anthropic（Claude）和 Google（Gemini）有自己的 API 格式，需要用对应的专用类，或者用 2.4 节介绍的 `init_chat_model` 统一管理：

```python
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()

# 一个函数搞定所有提供商，通过 model_provider 参数区分
llm_openai = init_chat_model("gpt-5.4-nano-2026-03-17", model_provider="openai",api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("OPENAI_BASE_URL"))
llm_claude = init_chat_model("claude-opus-4-7", model_provider="anthropic",api_key=os.getenv("ANTHROPIC_API_KEY"),base_url=os.getenv("ANTHROPIC_BASE_URL"))
llm_gemini = init_chat_model("gemini-3.1-flash-lite-preview", model_provider="google_genai",api_key=os.getenv("GEMINI_API_KEY"),base_url=os.getenv("GEMINI_BASE_URL"))

# 调用方式完全一致
for name, llm in [("OpenAI", llm_openai), ("Claude", llm_claude), ("Gemini", llm_gemini)]:
    response = llm.invoke("用一句话介绍你自己")
    print(f"{name}: {response.content}")
```

### 4.5 各平台接入速查表

| 平台 | 用哪个类 | 模型名称示例 | 环境变量 |
|------|---------|-------------|---------|
| **OpenAI（CloseAI代理）** | `ChatOpenAI` | `gpt-4o-mini` | `OPENAI_API_KEY` + `OPENAI_BASE_URL` |
| **DeepSeek** | `ChatOpenAI` | `deepseek-chat` | `DEEPSEEK_API_KEY` + `DEEPSEEK_BASE_URL` |
| **硅基流动** | `ChatOpenAI` | `Qwen/Qwen3-8B` | `SILICONFLOW_API_KEY` + `SILICONFLOW_BASE_URL` |
| **Anthropic** | `ChatAnthropic` | `claude-sonnet-4-20250514` | `ANTHROPIC_API_KEY` |
| **Google** | `ChatGoogleGenerativeAI` | `gemini-2.5-flash` | `GOOGLE_API_KEY` |
| **Ollama（本地）** | `ChatOllama` | `qwen3.5:4b` | 无需API Key |

> **发现规律了吗？** 凡是兼容 OpenAI 接口格式的平台（DeepSeek、硅基流动 等），都可以直接用 `ChatOpenAI`，只需改 `base_url` 和 `api_key`。这就是标准化接口的威力。

---

## 5、调用本地模型

### 5.1 Ollama介绍

Ollama是一个开源项目，用于在本地运行大语言模型。

**特点**：
- 支持多种开源模型（Llama、Qwen、DeepSeek等）
- 一键下载和运行
- 适合原型开发和本地测试
- 提供OpenAI兼容的API

### 5.2 Ollama安装

**Windows系统**：
- 访问 https://ollama.com/download
- 下载并安装.exe文件

**Linux系统**：

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 5.3 模型下载和运行

```bash
# 下载并运行模型（首次使用会自动下载）
ollama run qwen3.5:4b

# 列出已下载的模型
ollama list

# 查看模型信息
ollama show qwen3.5:4b
```

### 5.4 使用LangChain调用Ollama

```python
# uv add langchain-ollama
from langchain_ollama import ChatOllama

# 基本用法
ollama_llm = ChatOllama(model="qwen3.5:4b",  base_url="http://localhost:11434")
response = ollama_llm.invoke("你好，介绍一下你自己")
print(response.content)
```

---

## 6、高级主题

### 6.1 多模态输入

支持图像、音频等多模态输入：

```python
import base64
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o")  # 需要使用支持视觉语言的模型（VLM模型:视觉语言模型 LLM模型）
# 视觉模型：只能看懂图片的内容(OCR---yolox yolo-v8)
# 视觉语言模型：即能看懂图片内容 也能把看到的内容输出出来（VLM:各个平台都有各种各样的视觉模型）

# 读取图片
with open("image.jpg", "rb") as f:
    image_data = f.read()

message = HumanMessage(content=[
    {"type": "text", "text": "描述这张图片"},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode()}"}}
])
# type:image_url :既支持远程可以访问的图片地址 也支持本地图片(不能把本地图片路径丢给它 本地图片内容)
response = llm.invoke([message])
print(response.content)
```

**扩展：Base64 编码**

**概念：** 将二进制数据编码为可打印文本，常用于在文本协议（如 JSON）中传输二进制数据。

**编码原理：** 原始二进制每个字节可以是 0-255 中的任意值，其中很多是不可打印的控制字符，无法直接放进 JSON。Base64 将每 3 个字节（24 比特）切分为 4 组（每组 6 比特），每组对应 64 个可打印字符之一（A-Z、a-z、0-9、+、/）。如果末尾不足 3 个字节，用 `=` 填充。

```python
import base64

# 编码
with open("image.png", "rb") as f:
    binary_data = f.read()                                # bytes: 原始二进制
    base64_bytes = base64.b64encode(binary_data)          # bytes: Base64 编码后仍是 bytes 类型
    base64_string = base64_bytes.decode("utf-8")          # str:   转成字符串（Python 类型要求）

# .decode("utf-8") 的作用：
# Python 的 b64encode 返回 bytes 类型，但 JSON/f-string 需要 str 类型
# 因为 Base64 输出全是 ASCII 字符，所以这里只是做类型转换，不涉及字符编码解读

# 解码
binary_data = base64.b64decode(base64_string)
```

**在 VLM 中的应用：**

```
  原始图片 (二进制)
        │
        ▼ base64.b64encode()
  Base64 字符串: "iVBORw0KGgoAAAANSUhEUgAA..."
        │
        ▼ 拼接为 Data URL
  "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAA..."
        │      │              │    │
        │      │              │    └── 实际的图片数据
        │      │              └── 编码方式
        │      └── 媒体类型（告诉 API 这是 JPEG 图片）
        └── Data URL 协议前缀
```

### 6.2 速率限制

```python
import time
from langchain_openai import ChatOpenAI
from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,     # 10 秒才产生 1 个令牌  也即10 秒只能发1 个请求
    check_every_n_seconds=0.1,   # 每 0.1 秒检查一下“桶里有没有令牌可以用” 
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    rate_limiter=rate_limiter,
)

def test_rate_limit(n=3):
    print("开始时间：", time.strftime("%X"))
    last = time.time()
    for i in range(n):
        t0 = time.time()
        resp = llm.invoke(f"第 {i} 次调用，简单回一句话就行")
        t1 = time.time()
        print(
            f"调用 {i} 完成，耗时 {t1 - t0:.2f}s，"
            f"距上次调用结束间隔 {t1 - last:.2f}s"
        )
        last = t1

test_rate_limit(3)

```

### 6.3 Token使用追踪

```python
from langchain_core.callbacks import get_usage_metadata_callback

llm = ChatOpenAI(model="gpt-4o-mini")

with get_usage_metadata_callback() as cb:
    llm.invoke("你好")
    llm.invoke("再见")

    print(cb.usage_metadata)
    # {
    #     'input_tokens': 总输入token数,
    #     'output_tokens': 总输出token数,
    #     'total_tokens': 总token数
    # }
```

### 6.4 模型配置文件

查看模型的能力和限制：

```python
llm = ChatOpenAI(model="gpt-4o")
print(llm.profile)
# {
#     'max_input_tokens': 128000,
#     'image_inputs': True,
#     'tool_calling': True,
#     'structured_output': True,
#     ...
# }
```

### 6.5 提示词缓存（Prompt Caching）

#### 6.5.1 什么是提示词缓存？

当你反复用同一段很长的系统提示词（System Prompt）调用模型时，模型每次都要重新"读"这段提示词，消耗时间和 token 费用。**提示词缓存**让模型服务商在服务器端缓存这段已处理的提示词，后续调用直接复用，跳过重复计算。

```
第1次调用：
  [系统提示词 3000字] + [用户问题] → 模型处理全部内容 → 💰 全价计费

第2次调用（缓存命中）：
  [系统提示词 3000字 ← 已缓存，跳过] + [用户问题] → 模型只处理新内容 → 💰 大幅省钱
```

> **关键认知**：这里的"缓存"发生在**模型服务商的服务器上**，不是你本地硬盘上的某个文件。你的项目目录里不会多出 cache.sqlite 之类的东西。

#### 6.5.2 不同平台的缓存机制

| 平台 | 缓存方式 | 你需要做什么 | 省多少 |
|------|---------|-------------|--------|
| **OpenAI** | 全自动 | 什么都不用做，OpenAI 自动识别相同前缀并缓存 | 缓存命中的 token 费用减半 |
| **Anthropic** | 显式标记 | 用中间件告诉 API "这段可以缓存" | 缓存命中的 token 费用降低 90% |

**OpenAI — 自动缓存（零配置）**

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# 不需要任何额外配置
# OpenAI 会自动识别：如果连续多次请求的前缀（如系统提示词）相同，
# 服务器会复用已计算的 KV cache，减少延迟和费用
response = llm.invoke("你好")
```

你在代码层面看不到"缓存存在哪"或"命中率多少"，只能通过费用账单感知到缓存生效了。

**Anthropic — 显式缓存（需要中间件）**

```python
from langchain_anthropic import ChatAnthropic, AnthropicPromptCachingMiddleware

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    # 中间件会自动把长的系统提示词标记为"可缓存"
    middleware=[AnthropicPromptCachingMiddleware()]
)

# 第1次调用：全价（缓存写入）
# 第2次及之后：缓存命中，token 费用降低 90%
response = llm.invoke("你好")
```

`AnthropicPromptCachingMiddleware` 的作用是：按照 Anthropic 的 API 规范，将系统提示词等长文本片段包装成带 `cache_control` 标记的请求，告诉 Anthropic 服务器"这段内容可以缓存"。缓存的存储和命中完全由 Anthropic 服务端负责，LangChain 只负责标记。



#### 6.5.4 提示词缓存 vs 本地缓存

这是两个完全不同的东西，不要混淆：

| 维度 | 提示词缓存（Prompt Caching） | 本地缓存（LLM Cache） |
|------|---------------------------|---------------------|
| **缓存位置** | 模型服务商的服务器 | 你本地的内存/磁盘/Redis |
| **缓存什么** | 已计算的提示词中间状态（KV cache） | 完整的"问题→回答"键值对 |
| **效果** | 减少 token 费用和延迟 | 相同问题完全不调 API，零费用 |
| **你能控制吗** | 不能 | 完全由你控制 |
| **本节讲的** | ✅ 是这个 | ❌ 不是这个 |

如果你需要"相同问题直接从本地返回、完全不打 API"的缓存，那是 LangChain 的 `LLMCache` 机制（如 `InMemoryCache`、`SQLiteCache`），属于另一个话题，不在本节范围内。

## 7、小结

本节介绍了Model I/O中的模型调用部分：

### 已学内容

| 主题 | 核心要点 |
|------|----------|
| **Model I/O概述** | Prompts → Models → Output Parsers 三部分 |
| **初始化模型** | `init_chat_model` 或特定包的类 |
| **消息类型** | SystemMessage, HumanMessage, AIMessage, ToolMessage |
| **调用方式** | invoke, ainvoke, stream, batch |
| **平台接入** | CloseAI代理、DeepSeek、硅基流动、init_chat_model统一切换 |
| **本地模型** | Ollama等框架 |
| **高级特性** | 多模态、速率限制、Token追踪 |

### 统一接口优势

```python
# 同样的代码，只需更换初始化方式即可切换模型
llm = init_chat_model("gpt-4o-mini", model_provider="openai")
llm = init_chat_model("claude-sonnet-4-6", model_provider="anthropic")
llm = init_chat_model("gemini-2.5-flash", model_provider="google")
llm = ChatOllama(model="qwen2.5:7b")  # 本地模型

# 调用方式完全一致
response = llm.invoke("你好")
```

### 下一节预告

下一节我们将学习：
- **提示词模板（Prompts）**：如何管理和优化模型输入
- **输出解析器（Output Parsers）**：如何处理和转换模型输出

---

## 参考资料

- [LangChain Models 官方文档](https://docs.langchain.com/oss/python/langchain/models)
- [LangChain Messages 文档](https://docs.langchain.com/oss/python/langchain/messages)
- [Ollama 官网](https://ollama.com)
