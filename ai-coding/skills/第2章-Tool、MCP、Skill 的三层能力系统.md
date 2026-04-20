# 第2章-Tool、MCP、Skill 的三层能力系统

## 这一章要解决什么问题

这一章不再只讨论 Skill，而是把 `Tool`、`MCP`、`Skill` 放在同一个运行时里统一理解。

要回答的问题是：

- 三者分别解决什么问题
- 三者分别位于哪一层
- 在 Agent 运行时里，它们是如何从“定义”变成“模型可用能力”的
- `Skill` 为什么不等于 `Tool`
- 当前 Agent 与子 Agent 分别如何接收 Skill
- `allowed-tools` 这样的扩展为什么会出现，以及它在当前实现里处于什么状态

## 结论

- `Tool` 是模型可调用的动作接口，解决“模型如何动手”。
- `MCP` 是运行时接工具的标准协议，解决“工具如何标准化接入和复用”。
- `Skill` 是可复用的能力包 / SOP / 说明书，解决“某类任务如何稳定复现，不必每次都重新教模型”。
- 在当前 `oh-my-opencode` 里，普通 Tool 主要是 upfront 暴露 schema；Skill 主要是按需加载；Skill 自带的 MCP 能力主要通过 `skill_mcp` 桥接调用。
- `allowed-tools` 在当前证据下是 `oh-my-opencode` 这边的工程扩展，而不是我能直接确认的原始 OpenCode 核心 Skill 标准字段；它已经进入 Skill 元数据层，但我目前没有看到它已经完整打通到 `task(load_skills=[...])` 的工具裁剪闭环。

## 先把边界钉死：模型层 vs Agent 层

这一章最容易漏掉、但最该先说清楚的一句话是：

**模型层只原生理解 Tool Calling / Function Calling；Skill 和 MCP 都是 Agent runtime 在模型之上实现出来的能力。**

更具体一点：

- 对模型来说，它最终看到的是：
  - `messages`
  - `tools[]`
  - `tool_calls`
  - `tool results`
- 对模型来说，不存在原生的：
  - `Skill` 协议
  - `MCP` 协议
  - `Subagent` 协议
- `Skill`
  - 是运行时把一份说明书 / 能力包编排进上下文
- `MCP`
  - 是运行时把外部能力接进来，再转成模型可消费的能力
- `Subagent`
  - 在模型视角里，也只是一次新的会话 / 一次新的 prompt / 或一个委托工具调用

所以以后你自己做 Agent 系统时，应该始终记住：

- 模型层只管：`Tool Calling`
- Agent 层才负责：`Skill`、`MCP`、`Task/Subagent`、`Context Assembly`

## 这一章在项目里的证据边界

### 项目已证明

- 普通 Tool 会被注册进统一工具系统，最终暴露给模型。
- `skill` 是一个通用工具，不是把每个 Skill 直接变成独立 Tool。
- `skill` 工具 description 会动态列出可用 Skill 的 `name + description`。
- `skill(name="...")` 会把 Skill 正文作为工具返回值交给当前 Agent。
- `task(load_skills=[...])` 会先解析 Skill 正文，再把它注入子 Agent 的 `system` / hidden context。
- Skill 可以附带 MCP 配置，但模型不是直接“说 MCP”，而是通过 `skill_mcp` 这个桥接工具调用。
- `allowed-tools` 字段在当前插件里可以被解析进 Skill 元数据。

### 教学映射

- 下面的 provider payload 统一用 OpenAI `chat/completions` 风格做教学 mock。
- 当涉及子 Agent 首轮时，本章会同时给两种视角：
  - 项目里更直接可证明的 `session.prompt` body 形状
  - 对应的 OpenAI 风格教学映射
- 某些 `system`、`developer`、`hidden context` 的细粒度 provider 序列化，并不能从当前仓库里 100% 还原，所以本章会明确写成“近似映射”。

## 统一抽象

这一章建议把三层能力系统抽成 6 个对象。

```ts
type ToolSchema = {
  name: string
  description: string
  parameters: Record<string, unknown>
}

type McpServerDescriptor = {
  name: string
  source: "builtin" | "user" | "project" | "skill"
  capabilities: string[]
}

type SkillDescriptor = {
  name: string
  description: string
  body: string
  base_directory?: string
  allowed_tools?: string[]
  mcp_servers?: McpServerDescriptor[]
}

type CapabilityCatalog = {
  tools: ToolSchema[]
  skills: Array<Pick<SkillDescriptor, "name" | "description">>
  mcps: McpServerDescriptor[]
}

type ConversationState = {
  active_agent: string
  stable_instruction: string
  visible_history: ProviderMessage[]
  loaded_skills: SkillDescriptor[]
  available_tools_this_turn: ToolSchema[]
}

type CompiledPrompt = {
  model: string
  messages: ProviderMessage[]
  tools: ToolSchema[]
  tool_choice?: "auto" | "none" | "required"
  stream?: boolean
}
```

## 用 Python 从 0 到 1 实现这套分层

下面这几段不是在翻译仓库源码，而是把本章真正要学的思想压成框架无关的 Python 伪实现。

### 1. 普通 Tool：直接给模型 schema

```python
tool_catalog = [
    {
        "name": "grep",
        "description": "Search text patterns inside repository files.",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string"},
                "path": {"type": "string"},
            },
            "required": ["pattern", "path"],
        },
    },
    {
        "name": "read_file",
        "description": "Read the content of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
            },
            "required": ["path"],
        },
    },
]

payload = {
    "model": "gpt-5.2",
    "messages": [
        {"role": "system", "content": "You are an engineering agent."},
        {"role": "user", "content": "Find the Agent definition."},
    ],
    "tools": [
        {"type": "function", "function": tool_catalog[0]},
        {"type": "function", "function": tool_catalog[1]},
    ],
    "tool_choice": "auto",
}
```

这段代码体现的是：

- 普通 Tool 需要 upfront schema
- 因为模型要立刻产生合法的 function call

### 2. Skill：先给目录信息，再按需加载正文

```python
skill_catalog = [
    {
        "name": "text-review",
        "description": "Review product or text content for clarity, structure, and risk.",
    },
    {
        "name": "ppt-designer",
        "description": "Create presentation output with consistent visual and narrative style.",
    },
]

skill_tool = {
    "name": "skill",
    "description": (
        "Load a skill and return its full instructions.\n\n"
        "<available_items>\n"
        "  <command><name>/text-review</name>"
        "<description>Review product or text content for clarity, structure, and risk.</description></command>\n"
        "  <command><name>/ppt-designer</name>"
        "<description>Create presentation output with consistent visual and narrative style.</description></command>\n"
        "</available_items>"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
        "required": ["name"],
    },
}
```

这里体现的是：

- Skill 先给 `name + description`
- 完整正文等模型命中后再加载

### 3. 当前 Agent 加载 Skill 的执行环

```python
messages = [
    {"role": "user", "content": "Please review this product requirement."}
]

# 第一步：模型决定加载 skill
messages.append({
    "role": "assistant",
    "tool_calls": [
        {
            "id": "call_skill_001",
            "type": "function",
            "function": {
                "name": "skill",
                "arguments": "{\"name\": \"text-review\"}",
            },
        }
    ],
})

# 第二步：运行时返回 skill 正文
messages.append({
    "role": "tool",
    "tool_call_id": "call_skill_001",
    "content": "## Skill: text-review\n\nReview with rubric...\n1. Check goal\n2. Check scope\n3. Check acceptance criteria",
})

# 第三步：下一轮模型基于 skill 正文继续调普通工具
payload = {
    "model": "gpt-5.2",
    "messages": messages,
    "tools": [
        {"type": "function", "function": skill_tool},
        {"type": "function", "function": tool_catalog[0]},
        {"type": "function", "function": tool_catalog[1]},
    ],
}
```

### 4. 子 Agent 带着 Skill 出生

```python
def build_subagent_system(base_prompt: str, skill_wrappers: list[str]) -> str:
    parts = [base_prompt]
    parts.extend(skill_wrappers)
    return "\n\n".join(parts)

skill_wrapper = """## Skill: pr-review
Base directory: /skills/pr-review
Allowed tools: grep, read_file

Review rubric:
1. Check diff
2. Check tests
3. Grade risk
"""

subagent_payload = {
    "model": "gpt-5.2",
    "messages": [
        {
            "role": "system",
            "content": build_subagent_system(
                "You are a reviewer subagent.",
                [skill_wrapper],
            ),
        },
        {
            "role": "user",
            "content": "Review this change and give a risk level.",
        },
    ],
    "tools": [
        {"type": "function", "function": tool_catalog[0]},
        {"type": "function", "function": tool_catalog[1]},
    ],
}
```

这段代码体现的是：

- 子 Agent 不需要先调 `skill("...")`
- Skill 正文在第一轮出生前就已经被编译进 `system`

### 5. 你未来可以做得比当前插件更好的地方：让 `allowed_tools` 真正生效

```python
def filter_tools_by_skill(
    all_tools: list[dict],
    allowed_tools: list[str] | None,
) -> list[dict]:
    if not allowed_tools:
        return all_tools
    allowed = set(allowed_tools)
    return [tool for tool in all_tools if tool["name"] in allowed]

skill_wrapper = {
    "name": "pr-review",
    "allowed_tools": ["grep", "read_file"],
    "body": "Review rubric ...",
}

subagent_payload = {
    "model": "gpt-5.2",
    "messages": [
        {"role": "system", "content": skill_wrapper["body"]},
        {"role": "user", "content": "Review this change."},
    ],
    "tools": [
        {"type": "function", "function": t}
        for t in filter_tools_by_skill(tool_catalog, skill_wrapper["allowed_tools"])
    ],
}
```

这段 Python 伪实现，就是我们讨论出来、但当前插件还没有完全打通的那个升级方向。

## 这几个对象为什么需要分开

因为三者职责完全不同：

- `ToolSchema`
  - 是给模型发合法 function call 的合同
- `McpServerDescriptor`
  - 是给运行时接外部能力的协议来源
- `SkillDescriptor`
  - 是给 Agent 提供做事方法、流程、约束和渐进式暴露入口

如果把三者混成一个“能力”概念，会立刻出现四个误区：

1. 以为 Skill 和 Tool 是同一层
2. 以为 MCP 是模型原生协议，而不是运行时接入协议
3. 以为加载 Skill 就等于自动执行完整流程
4. 以为一个 Skill 就应该直接变成一个独立 Tool schema

## 三者分别解决什么问题

### 1. Tool 解决什么问题

Tool 解决的是：

- 模型如何从“会说话”变成“会动手”
- 某个动作的名称是什么
- 这个动作需要什么参数
- 调完以后能返回什么结果

Tool 的最关键特征是：

- 模型若想直接调用它，必须事先拿到 schema

否则模型就没法稳定地产生合法的 `tool_calls`。

### 2. MCP 解决什么问题

MCP 解决的是：

- 工具如何被标准化提供
- Agent runtime 如何标准化发现和连接这些工具
- 外部能力如何跨项目、跨工具复用

MCP 不是模型原生协议。更准确地说：

- 模型不需要“认识 MCP”
- 运行时接入 MCP server
- 再把可调用能力变成模型能消费的 Tool 形态

所以链路应理解为：

`MCP Server -> Agent Runtime 发现/连接 -> 转成模型可用能力`

### 3. Skill 解决什么问题

Skill 解决的是：

- 某类任务如何稳定复现
- 某类事应该按照什么 SOP 执行
- 做这类事时要遵守什么约束
- 需要哪些额外上下文、脚本、文档、MCP 能力

Skill 不直接等于动作，它更像：

- 能力说明书
- 任务模板
- 方法论包
- 渐进式暴露入口

一句话记忆：

- Tool 给 Agent 手
- Skill 给 Agent 手艺
- MCP 给 Agent 接更多手的标准方式

## 为什么 Skill 不等于 Tool

这个点非常关键。

Tool 和 Skill 的本质差别，不只是“一个是动作，一个是流程”，更重要的是：

### Tool 在调用前必须给模型什么

模型如果要直接调用某个 Tool，它必须事先知道：

- 工具名
- 参数名
- 必填字段
- 参数类型
- 合法 JSON 长什么样

也就是：

- `name`
- `description`
- `parameters schema`

所以普通 Tool 通常要先进入 `tools[]`。

### Skill 在加载前必须给模型什么

Skill 在第一阶段只需要让模型知道：

- 这个 Skill 叫什么
- 这个 Skill 大概解决什么问题

也就是：

- `name`
- `description`

模型先做的是“要不要加载这个 Skill”的决策，而不是“立刻执行其中某个动作”的决策。

所以 Skill 可以按需加载。

这就是为什么：

- Tool 更像 protocol object
- Skill 更像 discovery item

## 项目里的对应实现

这一章不做文件导览，但保留最小证据入口。

### Tool 注册

- 统一工具注册表：
[tool-registry.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/plugin/tool-registry.ts)

这里能看到：

- `skill`
- `skill_mcp`
- `task`
- 以及各种普通 Tool

都会被注册进同一个工具系统。

### Skill 列表如何暴露给模型

- 通用 `skill` 工具的 description 动态列出可用 Skill：
[tools.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/skill/tools.ts)
[constants.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/skill/constants.ts)

### MCP 如何接入运行时

- MCP 合并与配置：
[mcp-config-handler.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/plugin-handlers/mcp-config-handler.ts)

### Skill 自带 MCP 能力如何桥接

- `skill_mcp`：
[tools.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/skill-mcp/tools.ts)

### 子 Agent 如何接收 `load_skills`

- 解析 Skill 正文：
[skill-resolver.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/delegate-task/skill-resolver.ts)
- 把 Skill 正文注入 `systemContent`：
[tools.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/delegate-task/tools.ts)
[prompt-builder.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/delegate-task/prompt-builder.ts)
[sync-prompt-sender.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/delegate-task/sync-prompt-sender.ts)

### `allowed-tools`

- 扩展字段定义与解析：
[types.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/features/opencode-skill-loader/types.ts)
[loaded-skill-from-path.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/features/opencode-skill-loader/loaded-skill-from-path.ts)
[allowed-tools-parser.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/features/opencode-skill-loader/allowed-tools-parser.ts)
[configuration.md](/Users/IdeaProjects/learn_ai/oh-my-opencode/docs/reference/configuration.md)

## Skill 在这个项目里有两条路径

这是本章最重要的结论之一。

### 路径 A：当前 Agent 通过 `skill("...")` 动态加载

链路是：

1. 模型先看到 `skill` 这个通用工具
2. `skill` 的 description 里列出所有可用 Skill 的 `name + description`
3. 模型根据用户意图和 description 匹配，决定要不要调用某个 Skill
4. 调用 `skill(name="...")`
5. 工具返回 Skill 正文
6. Skill 正文以 `role: "tool"` 的内容进入当前会话
7. 当前 Agent 再依据这份说明去调用普通 Tool

### 路径 B：主 Agent 通过 `task(load_skills=[...])` 注入子 Agent

链路是：

1. 主 Agent 决定委托子 Agent
2. 在 `load_skills=[...]` 里点名要带的 Skill
3. 运行时先把这些 Skill 的正文解析出来
4. 把它们拼进子 Agent 的 `system` / hidden context
5. 子 Agent 第一轮出生时就带着这套能力包工作

一句话区分：

- `skill("...")`
  - 当前 Agent 读取说明书
- `task(load_skills=[...])`
  - 子 Agent 带着说明书出生

## 场景一：普通 Tool 的首轮请求体

先看没有 Skill 的最普通情况。

```json
{
  "model": "gpt-5.2",
  "messages": [
    {
      "role": "system",
      "content": "你是一个工程向 Agent。必要时可以调用工具获取事实和执行动作。"
    },
    {
      "role": "user",
      "content": "帮我在仓库里查一下 Agent 的定义位置。"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "grep",
        "description": "Search text patterns inside repository files.",
        "parameters": {
          "type": "object",
          "properties": {
            "pattern": { "type": "string" },
            "path": { "type": "string" }
          },
          "required": ["pattern", "path"],
          "additionalProperties": false
        }
      }
    }
  ],
  "tool_choice": "auto",
  "stream": true
}
```

这一版没有 Skill，也没有 MCP，只体现：

- Tool 要直接进 `tools[]`
- 因为模型要立刻知道合法参数结构

## 场景二：有 2 个普通 Tool + 3 个 Skill 的首轮请求体

这是本章最值得反复看的第一份结构。

假设当前有：

- 普通 Tool：`grep`、`write_file`
- 通用能力 Tool：`skill`、`skill_mcp`、`task`
- Skills：`text-review`、`ppt-designer`、`git-master`

那么首轮更接近这样：

```json
{
  "model": "gpt-5.2",
  "messages": [
    {
      "role": "system",
      "content": "你是一个具备编排能力的工程 Agent。普通 Tool 负责具体动作，Skill 负责可复用的方法和约束。当任务与某个 Skill 的描述匹配时，先通过 skill 工具加载完整说明；若需要委托子 Agent，使用 task(load_skills=[...])。"
    },
    {
      "role": "user",
      "content": "帮我检查产品需求文档是否合理。"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "grep",
        "description": "Search text patterns inside repository files."
      }
    },
    {
      "type": "function",
      "function": {
        "name": "write_file",
        "description": "Write content to a file."
      }
    },
    {
      "type": "function",
      "function": {
        "name": "skill",
        "description": "Load a skill or execute a slash command to get detailed instructions for a specific task.\n\n<available_items>\n  <command>\n    <name>/text-review</name>\n    <description>Review product or text content for clarity, structure, and risk.</description>\n  </command>\n  <command>\n    <name>/ppt-designer</name>\n    <description>Create presentation output with consistent visual and narrative style.</description>\n  </command>\n  <command>\n    <name>/git-master</name>\n    <description>Git workflow guidance for commit, rebase, blame, bisect, and history search.</description>\n  </command>\n</available_items>"
      }
    },
    {
      "type": "function",
      "function": {
        "name": "skill_mcp",
        "description": "Call MCP capabilities exposed by a loaded skill."
      }
    },
    {
      "type": "function",
      "function": {
        "name": "task",
        "description": "Delegate work to a subagent and optionally inject skills."
      }
    }
  ],
  "tool_choice": "auto",
  "stream": true
}
```

### 这份 JSON 最重要的两个结论

1. 3 个 Skill 不会直接变成 3 个独立 Tool
2. 它们主要出现在：
  - `skill` 通用工具的 description 里

也就是说，Skill 在首轮更像“可发现能力目录”，不是独立动作接口。

## 场景三：当前 Agent 动态加载 Skill 的第二轮

继续上面的例子。模型可能先命中 `text-review`：

```json
{
  "model": "gpt-5.2",
  "messages": [
    {
      "role": "system",
      "content": "你是一个具备编排能力的工程 Agent。"
    },
    {
      "role": "user",
      "content": "帮我检查产品需求文档是否合理。"
    },
    {
      "role": "assistant",
      "tool_calls": [
        {
          "id": "call_skill_001",
          "type": "function",
          "function": {
            "name": "skill",
            "arguments": "{\"name\":\"text-review\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_skill_001",
      "content": "## Skill: text-review\n\n**Base directory**: /path/to/skills/text-review\n\n请按以下步骤审查：\n1. 检查目标是否明确\n2. 检查边界是否完整\n3. 检查是否缺少验收标准\n4. 输出风险等级与建议"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "grep",
        "description": "Search text patterns inside repository files."
      }
    },
    {
      "type": "function",
      "function": {
        "name": "write_file",
        "description": "Write content to a file."
      }
    },
    {
      "type": "function",
      "function": {
        "name": "skill",
        "description": "Load a skill or execute a slash command to get detailed instructions for a specific task."
      }
    },
    {
      "type": "function",
      "function": {
        "name": "skill_mcp",
        "description": "Call MCP capabilities exposed by a loaded skill."
      }
    }
  ],
  "tool_choice": "auto",
  "stream": true
}
```

这一轮最关键的事情是：

- Skill 正文不进 `tools[]`
- Skill 正文进入：
  - `messages[]`
  - `role: "tool"`
  - `content`

而且当前 Agent 路径下，Skill 返回值会自动带：

- `Skill name`
- `Base directory`
- Skill 正文
- 如果 Skill 带 MCP，还可能带能力说明

## 场景四：Skill 自带 MCP 能力时的第二阶段

假设某个 Skill 自带 MCP 配置。链路不是：

- Skill 直接摊平成一堆 Tool

而是：

1. 先加载 Skill
2. Skill 返回内容里告诉模型：
  - 有哪些 `mcp_name`
  - 这些 MCP 下有哪些 tool/resource/prompt
3. 模型再调用通用桥接工具 `skill_mcp(...)`

教学 mock 如下：

```json
{
  "messages": [
    {
      "role": "user",
      "content": "请按这个 Skill 去生成 PPT。"
    },
    {
      "role": "assistant",
      "tool_calls": [
        {
          "id": "call_skill_001",
          "type": "function",
          "function": {
            "name": "skill",
            "arguments": "{\"name\":\"ppt-designer\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_skill_001",
      "content": "## Skill: ppt-designer\n\n该 Skill 附带 MCP server: slides\n可用能力:\n- tool: create_deck\n- tool: update_slide\n- resource: theme://apple-style"
    },
    {
      "role": "assistant",
      "tool_calls": [
        {
          "id": "call_skill_mcp_002",
          "type": "function",
          "function": {
            "name": "skill_mcp",
            "arguments": "{\"mcp_name\":\"slides\",\"tool_name\":\"create_deck\",\"arguments\":{\"title\":\"Agent 上下文设计\"}}"
          }
        }
      ]
    }
  ]
}
```

一句话记忆：

- Skill 暴露能力说明
- `skill_mcp` 负责真正桥接执行

## 场景五：子 Agent 首轮，`task(load_skills=[...])` 的项目真实边界

这个场景不能只用 OpenAI payload 去理解，必须同时看项目里更直接可证明的 `session.prompt` body。

### 项目里更直接可证明的子 Agent 首轮 body

近似形状如下：

```json
{
  "path": { "id": "ses_sub_001" },
  "body": {
    "agent": "sisyphus-junior",
    "system": "这里是子 Agent 通用 prompt + Skill 正文 + category/agent 附加上下文",
    "tools": {
      "task": false,
      "call_omo_agent": true,
      "question": false,
      "grep": true,
      "read_file": true
    },
    "parts": [
      {
        "type": "text",
        "text": "Review this change and give risk level.\n<!-- OMO_INTERNAL_INITIATOR -->"
      }
    ],
    "model": {
      "providerID": "openai",
      "modelID": "gpt-5.2"
    }
  }
}
```

### OpenAI 风格教学映射

如果把它近似投影成 provider 请求体，更像：

```json
{
  "model": "gpt-5.2",
  "messages": [
    {
      "role": "system",
      "content": "你是 reviewer 子 Agent。\n\n## Injected Skill Context\n请按公司 review rubric 工作：先看 diff，再看测试，再给风险等级；高风险必须指出证据和回滚点。"
    },
    {
      "role": "user",
      "content": "Review this change and give risk level."
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "grep",
        "description": "Search repository content."
      }
    },
    {
      "type": "function",
      "function": {
        "name": "read_file",
        "description": "Read a file."
      }
    }
  ],
  "tool_choice": "auto",
  "stream": true
}
```

### 这个场景最关键的结论

- 子 Agent 不会先自己调用一次 `skill("pr-review")`
- Skill 正文会直接注入：
  - 子 Agent 的 `system` / hidden context
- `parts` / `user` 里放的是：
  - 主 Agent 编译后的委托任务说明
  - 不一定等于用户原话

## 场景六：子 Agent 第二轮，带 Skill 继续调普通 Tool

Skill 不是自动执行器。子 Agent 带着 Skill 出生后，仍然要继续走普通工具循环。

```json
{
  "messages": [
    {
      "role": "system",
      "content": "这里已经包含 pr-review 的 Skill 正文。"
    },
    {
      "role": "user",
      "content": "Review this change and give risk level."
    },
    {
      "role": "assistant",
      "tool_calls": [
        {
          "id": "call_grep_001",
          "type": "function",
          "function": {
            "name": "grep",
            "arguments": "{\"pattern\":\"TODO|FIXME|risk\",\"path\":\"src\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_grep_001",
      "content": "匹配到 5 处高风险线索。"
    }
  ]
}
```

也就是说：

- Skill 负责指导
- Tool 负责执行

## 子 Agent 注入 Skill 时，一个值得记录的工程缺口

这个点非常重要，是本章最大的工程观察之一。

### 当前 Agent 路径

`skill("...")` 返回的是带 wrapper 的内容：

- `Skill name`
- `Base directory`
- 正文

### 子 Agent 路径

`task(load_skills=[...])` 当前注入进去的是：

- 去掉 frontmatter 后的 Skill 正文
- 多个 Skill 正文直接 join

我目前没看到这条路径自动补：

- `Skill name`
- `Base directory`
- `allowed_tools`
- `mcp capabilities`

这意味着：

- 当前 Agent 路径更“自解释”
- 子 Agent 路径更“轻量”
- 但轻量的代价是目录/包装信息可能丢失

这也是为什么后面我们得出一个更稳的设计建议：

**如果以后自己做 Agent，最好给 `task(load_skills=[...])` 的子 Agent 注入也补一个 Skill wrapper。**

## `allowed-tools` 到底是什么

这是本章一个必须单独澄清的点。

### 当前我能直接确认的事实

在 `oh-my-opencode` 里：

- `allowed-tools` 可以配置
- 可以写在 Skill frontmatter
- 也可以来自配置定义或内建 Skill
- loader 会把它解析进 `LoadedSkill.allowedTools`

### 当前我不能过度声称的部分

我目前没有看到它已经在 `task(load_skills=[...])` 路径里完整打通为：

- “根据 Skill 的 `allowed-tools` 自动裁剪子 Agent 的 `tools[]`”

所以更稳的判断是：

- 它已经是一个正式元数据字段
- 但更像“已设计好的约束能力”
- 还不是我当前能确认已完全闭环的运行时强约束

### 这一点意味着什么

如果以后你自己做 Agent，最合理的升级是：

1. `skill_body` 进入 `system`
2. `allowed_tools` 真正参与子 Agent 工具裁剪

也就是让 Skill 不只影响“怎么想”，也影响“能动哪些手”。

## Slash Command、Rule、Workflow 和 Skill 的关系

这一节要专门解决一个很容易越聊越乱的问题：

- `Skill`
- `Slash Command`
- `Rule`
- `Workflow`

它们是不是一回事？

答案是：

- 从更高抽象层看，它们都可以被理解成“帮助 Agent 稳定完成某类事的能力单元”
- 但从运行时载体和触发方式看，它们不是同一个东西

### 1. Skill

更像：

- 潜伏的、可按需加载的能力包
- Agent 自己可以根据意图命中
- 典型载体是：
  - `SKILL.md`
  - 可选的附带 MCP / 辅助资源

### 2. Slash Command

更像：

- 用户显式触发的工作流入口
- 一个预制 prompt/template
- 有时还会指定：
  - 某个 agent
  - 某个 model
  - 是否强制 subtask

OpenCode 原始文档里也明确是这么定义的：

- 命令本质是一个 prompt/template
- 用户通过 `/xxx` 显式触发  
参考：[commands.mdx](/Users/IdeaProjects/learn_ai/opencode/packages/web/src/content/docs/commands.mdx)

### 3. Rule

更像：

- 长期生效的上下文约束
- 一种“默认一直在”的 instruction layer
- 它不是按需触发的 Tool
- 也不是一个 latent capability catalog item

在 OpenCode 里，Rule 更接近：

- `AGENTS.md`
- `instructions`
- 以及类似 Cursor rules 的全局/项目级上下文  
参考：[rules.mdx](/Users/IdeaProjects/learn_ai/opencode/packages/web/src/content/docs/rules.mdx)

所以一定不要把 Rule 也粗暴说成：

- “一个 Tool”
- “一个可加载 Skill”

它更像 pinned context。

### 4. Workflow

`Workflow` 不是当前这套系统里一个强约束的底层协议，而是更高层的抽象名字。

它可以指：

- 一个 Slash Command 驱动的流程
- 一个 Skill 驱动的流程
- 一个 Rule 约束下再配合 Tool / MCP / Subagent 跑出来的流程

所以更稳的理解是：

- `Workflow` 是抽象概念
- `Skill` / `Slash Command` / `Rule` 是不同载体

### 5. 在这个插件里的一个重要收敛点

在 `oh-my-opencode` 里，确实有一个很有意思的设计：

- 通用 `skill` 工具不仅能加载 Skill
- 还会把 Slash Command 一起列进自己的 description
- 并且在执行时，既能返回 Skill，也能返回 Command 的格式化内容

这意味着在 Agent 视角里，当前插件已经在做一件事：

**把 Skill 和 Slash Command 统一成“可按需调入的说明书型能力”。**

最小事实入口：

- [tools.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/skill/tools.ts)
- [command-output-formatter.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/slashcommand/command-output-formatter.ts)

### 6. 这一节最值得记住的一张心智图

- `Rule`
  - 永久在线
  - 属于 pinned context
- `Skill`
  - 按需命中
  - 属于 latent capability package
- `Slash Command`
  - 用户显式触发
  - 属于 explicit workflow entrypoint
- `Workflow`
  - 上层抽象词
  - 可以由 Rule / Skill / Slash Command / Tool / MCP / Subagent 共同组成

所以如果你以后自己做 Agent，可以用一句话统一它们：

**Rule 管长期约束，Skill 管按需方法，Slash Command 管显式入口，Workflow 是它们在运行时组合后的总称。**

## 运行时流转

本章把完整流转压成 6 步：

1. 运行时建立能力目录
  - Tool 注册
  - MCP 加载
  - Skill 发现
2. 编译首轮请求
  - 普通 Tool 进入 `tools[]`
  - Skill 名称和描述进入通用 `skill` 工具 description
3. 模型做能力选择
  - 直接调普通 Tool
  - 或先调 `skill`
  - 或直接 `task(load_skills=[...])`
4. 若调 `skill("...")`
  - Skill 正文进入当前会话的 `tool result`
5. 若调 `task(load_skills=[...])`
  - Skill 正文进入子 Agent 的 `system`
6. 后续继续普通工具循环
  - `assistant.tool_calls`
  - `tool`
  - `assistant`

## 页面渲染怎么受影响

用户在页面上通常只能看到：

- 模型调用了某个工具
- 工具返回了某个结果
- 子 Agent 给出了一个最终结论

但看不到：

- 某个 Skill 是出现在 `tool description` 里
- 某个 Skill 是以 `tool result` 进入当前会话
- 某个 Skill 是直接进入子 Agent `system`

所以这章一定要分清：

- UI 看到的是执行过程
- 运行时真正维护的是能力目录和上下文编译

## 最终 LLM endpoint 请求体

这章最重要的不是记住一个固定 JSON，而是记住这 4 种形态：

1. **普通 Tool 轮**
  - Tool schema 直接进 `tools[]`
2. **Skill 发现轮**
  - Skill 名称和描述藏在通用 `skill` 工具 description 里
3. **当前 Agent Skill 加载轮**
  - Skill 正文进入 `messages[].role="tool".content`
4. **子 Agent Skill 注入轮**
  - Skill 正文进入子 Agent `system / hidden context`

## 用当前项目做证据

本章最少需要记住这些事实入口：

- 统一工具注册  
[tool-registry.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/plugin/tool-registry.ts)
- Skill 列表出现在通用 `skill` 工具 description 中  
[tools.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/skill/tools.ts)
- OpenCode 官方文档也明确写了：
可用 Skill 会列在 `skill` 工具描述中  
[skills.mdx](/Users/IdeaProjects/learn_ai/opencode/packages/web/src/content/docs/skills.mdx)
- Skill 自带 MCP 能力通过 `skill_mcp` 桥接  
[tools.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/skill-mcp/tools.ts)
- 子 Agent 首轮直接带着 Skill 正文出生  
[tools.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/delegate-task/tools.ts)  
[prompt-builder.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/delegate-task/prompt-builder.ts)  
[sync-prompt-sender.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/tools/delegate-task/sync-prompt-sender.ts)
- `allowed-tools` 已进入 Skill 元数据层  
[types.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/features/opencode-skill-loader/types.ts)  
[loaded-skill-from-path.ts](/Users/IdeaProjects/learn_ai/oh-my-opencode/src/features/opencode-skill-loader/loaded-skill-from-path.ts)

## 引用文件

这一章建议同时参考下面这份总结文档：

- [Claude-Skill架构与最佳实践.md](/Users/IdeaProjects/learn_ai/oh-my-opencode/learn/设计思想/Claude-Skill架构与最佳实践.md)

它更偏：

- Claude/Anthropic Skill 的设计哲学
- 渐进式暴露
- SKILL.md 最佳实践

而本章更偏：

- 在实际 Agent runtime 里，Tool、MCP、Skill 如何一起工作
- 以及它们如何进入最终 endpoint

## 与 studio-agent 的对应关系

如果和你以前那种“工具说明写在 prompt 里”的系统相比，这一章最重要的升级点有 4 个：

1. Tool 不再只是 prompt 约定，而是 protocol object
2. Skill 不再只是随手附带的 Markdown，而是按需加载能力包
3. MCP 不再只是外部脚本集合，而是运行时接入协议
4. 子 Agent 不再只是复制父 prompt，而是携带有选择的 Skill 上下文出生

## 对 LangGraph / Java 手写意味着什么

如果以后你自己实现，建议显式建模：

1. `tool_catalog`
  - 当前可直接给模型的 Tool schema
2. `skill_catalog`
  - Skill name + description + body + base_directory + allowed_tools + mcp_capabilities
3. `mcp_registry`
  - 外部能力来源
4. `subagent_skill_wrapper`
  - 给子 Agent 注入 Skill 时，最好补：
    - `skill_name`
    - `base_directory`
    - `allowed_tools`
    - `mcp_capabilities`
    - `skill_body`

这是比当前插件更稳的一种设计。

## 动手练习

请你手工写出下面 3 份 JSON：

1. 有 2 个普通 Tool、3 个 Skill 的首轮请求体
2. 当前 Agent 调 `skill("text-review")` 后的第二轮请求体
3. 子 Agent 调 `task(load_skills=["pr-review"])` 的首轮请求体

写完以后检查这 5 点：

- Skill 有没有被错误地直接变成顶层 Tool
- `skill` 工具 description 里有没有 Skill 的名字和描述
- Skill 正文有没有进入正确位置
- 当前 Agent 路径和子 Agent 路径有没有分开
- `allowed-tools` 有没有被你误当成当前实现已完整闭环的强约束

## 还没闭合的问题

下一步如果继续深挖这一章，还可以讨论：

- 原始 OpenCode 是否应该也引入真正的 `allowed-tools` 运行时裁剪
- 普通 Tool 是否值得设计成 `tool_search -> 二次注入 schema` 的通用懒加载体系
- Slash Command、Rule、Workflow 和 Skill 是否值得统一抽象成一个“按需加载能力包协议”

