# 深度解析：Claude Skill 架构原理与最佳实践

在现代 Agent 架构中，如何赋予大模型极其复杂的垂直领域能力，同时又防止 System Prompt 爆炸和注意力稀释？Anthropic 给出的答案是：**Agent Skills**。

本文系统性总结了 Claude Skill 的核心设计哲学、底层加载机制（以 OpenCode 为例）以及来自 Anthropic 官方的硬核最佳实践。

---

## 1. 什么是 Skill？（认知升级）

很多开发者误以为 Skill 只是一个封装好的 HTTP API 或 Function Calling 工具。但在 Anthropic 的标准架构中，**Skill 是一个“基于文件系统的渐进式暴露模块”**。

如果说普通的 Tool 是给大模型提供“手和脚”（执行算力），那么 Skill 就是给大模型临时下载的“大师级说明书”（认知与策略）。

一个标准的 Skill 本质上是一个目录沙盒：
```text
my-awesome-skill/
├── SKILL.md          # 核心文件：YAML元数据 + Markdown认知指导 (必填)
├── FORMS.md          # 辅助指南：领域知识、参考文档 (选填)
└── scripts/          # 可执行代码：复杂的 API 调用、验证逻辑 (选填)
    └── execute.py    
```
**关键澄清：框架的“弱约束”与“强引导”**
Anthropic 官方规范**仅强制约束了 `SKILL.md` 顶部的 YAML 格式**（必须包含 name 和 description）。它对子目录结构、文件名没有任何硬性限制。你不需要把脚本一定放在 `scripts/` 下。只要你在 `SKILL.md` 的正文里写清楚：“请运行 `python foo/bar/my_script.py`”或者“请读取 `docs/api.md`”，大模型就会通过相对路径渐进式地去探索和加载这些文件。

**核心定律：Text for heuristics, Code for execution（文本管认知，代码管执行）。** 
不要在 Prompt 里教大模型怎么拼装复杂的 JSON，把这些脏活累活写成 Python/Bash 脚本，让 `SKILL.md` 指导大模型在什么时机去调用这些脚本。

---

## 2. 核心机制：渐进式暴露 (Progressive Disclosure)

Skill 解决 Context 过载的核心机制是“按需加载”。它的生命周期分为三个阶段：

1. **发现阶段 (Discovery)**：
   系统启动时，框架只读取 `SKILL.md` 顶部的 YAML Frontmatter（包含 `name` 和 `description`），并将其注入主 Agent 的 System Prompt 中。大模型此时只知道“有这个技能”，不知道具体怎么做。
2. **激活与注入 (Activation & Injection)**：
   当用户意图命中该 Skill 时，大模型发起工具调用（如 `activate_skill(name="ppt-creator")`）。此时，框架才会把 `SKILL.md` 中长篇大论的 Markdown 正文作为 Tool Result 返回，临时“洗脑”大模型的局部上下文。
3. **隔离执行 (Isolated Execution)**：
   如果 Skill 中包含数百行的 `scripts/execute.py`，这些代码**永远不会**进入大模型的上下文窗口。大模型通过 `Code Execution` 或 `Bash` 工具执行脚本，只读取返回的 `stdout/stderr`，极大节省了 Token。

---

## 3. 工程实现剖析（从 0 到 1 的 Python 还原）

在真实的工程落地中，框架是如何解析和加载这些 Skill 的？以 OpenCode 项目为例，它的设计极度轻量且容错率高。以下我们将 OpenCode 的核心 TypeScript 逻辑 1:1 翻译为 Python，展示如何从零写一个符合 Anthropic 标准的 Skill Loader。

### 3.1 扫描与解析（无 AST 的正则暴力美学）
框架并没有使用重型的 Markdown 解析器，而是用正则表达式直接切割文件，这保证了极高的容错率。

```python
import re
import yaml

def parse_frontmatter(content: str) -> dict:
    """
    核心逻辑：使用正则剥离顶部的 --- YAML --- 区域
    等价于 OpenCode src/shared/frontmatter.ts
    """
    # 匹配开头的一对 ---，提取内部的 YAML (group 1) 以及后续的 Body (group 2)
    pattern = re.compile(r"^---\r?\n(.*?)\r?\n?---\r?\n(.*)$", re.DOTALL)
    match = pattern.match(content)
    
    if not match:
        # 如果没有检测到 YAML，直接返回全部作为正文，不做强制拦截
        return {"metadata": {}, "body": content}
        
    yaml_content = match.group(1)
    body_content = match.group(2)
    
    try:
        # 安全地解析 YAML，防止执行恶意代码 (等价于 yaml.JSON_SCHEMA)
        metadata = yaml.safe_load(yaml_content) or {}
        return {"metadata": metadata, "body": body_content}
    except Exception as e:
        print(f"YAML 解析失败: {e}")
        return {"metadata": {}, "body": body_content}
```

### 3.2 目录探测与预加载 (Discovery)
在服务启动时，框架会遍历特定的 Skill 目录。OpenCode 的探测策略非常聪明：不仅认 `SKILL.md`，也认同名文件。

```python
import os
from pathlib import Path

def scan_skills(skills_dir: str) -> list:
    """
    等价于 OpenCode src/features/opencode-skill-loader/skill-directory-loader.ts
    """
    loaded_skills = []
    
    for entry in os.scandir(skills_dir):
        if entry.name.startswith("."):
            continue
            
        if entry.is_dir():
            dir_path = Path(entry.path)
            
            # 策略1: 优先寻找 SKILL.md (Anthropic 官方标准)
            skill_file = dir_path / "SKILL.md"
            
            # 策略2: 如果不存在 SKILL.md，降级寻找与文件夹同名的 .md
            if not skill_file.exists():
                skill_file = dir_path / f"{entry.name}.md"
                
            if skill_file.exists():
                with open(skill_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                parsed = parse_frontmatter(content)
                metadata = parsed["metadata"]
                
                # 提取名片信息：如果没有填 name，就拿文件夹名字顶替
                skill_name = metadata.get("name", entry.name)
                description = metadata.get("description", "")
                
                # 核心：将正文用特定标签包裹，但此时不发给模型！
                wrapped_body = f"<skill-instruction>\n{parsed['body'].strip()}\n</skill-instruction>"
                
                loaded_skills.append({
                    "name": skill_name,
                    "description": description,
                    "template": wrapped_body, # 潜伏在内存中
                    "path": str(skill_file)
                })
                
    return loaded_skills
```

### 3.3 激活与内存 Map (Injection)
经过上述扫描后，所有的 Skill 都会变成内存中的一个 Map：
```python
# 框架启动时的内存状态
loaded_skills_map = {
    "ppt-creator": {
        "description": "用于创建专业的咨询风格 PPT...", # 仅仅把这句喂给 System Prompt
        "template": "<skill-instruction>\n...\n</skill-instruction>" # 长篇大论藏在内存里
    }
}
```
当大模型在对话中输出工具调用 `execute(args={name: "ppt-creator"})` 时，框架的执行器会去 `loaded_skills_map` 中根据名字 `getValue`。拿到那个巨大的 `template` 字符串后，将其作为 `tool_result` 塞入当前的对话上下文中。至此，渐进式暴露闭环完成。

---

## 4. 官方硬核最佳实践 (Advanced Tricks)

除了基础的结构要求，Anthropic 官方文档中隐藏了几个极具杀伤力的 Prompt Engineering 技巧：

### Trick 1: 目录索引欺骗 (The 100-Line TOC Trick)
当大模型使用 Bash 读取辅助文档时，如果文件过长，它经常偷懒只读取前 100 行（`head -100`）。
**解法**：在所有长参考文档的最顶部，强制手写一份**目录（Table of Contents）**。这能让模型在仅读取头部时，就掌控全局结构，知道后续去哪一行精准检索。

### Trick 2: “复制粘贴”式状态机 (The Checklist State Pattern)
在多步长任务中，模型极易迷失或死循环。
**解法**：在 `SKILL.md` 中写下带有 `[ ]` 的 Markdown 检查清单。并严厉命令模型：**“在你的每一次回复开头，必须复制并输出这个清单的最新打勾状态！”**。这相当于强行在外层维持了一个状态机。

### Trick 3: 剥夺自由度 (Degrees of Freedom Management)
**解法**：明确划分“高自由度”和“低自由度”区域。
- 对于代码审查、文案排版：给出原则（Heuristics），让其自由发挥。
- 对于数据库迁移、环境编译：**绝不给原则，只给死命令**。必须在文档中给出精确到字符的 Bash 模板，并警告“绝不允许修改参数或添加任何 Flags”。

### Trick 4: “解决它，别抛给我” (Solve, Don't Punt)
不要把辅助脚本写得太“娇气”。如果脚本因为缺少临时目录而报错退出，大模型会浪费一轮对话来问你“是否需要创建目录”。
**解法**：脚本必须具备高度自愈能力。自动 `mkdir -p`，自动填充缺省配置。只把真正需要大模型进行逻辑推演的错误（比如循环依赖）通过 `stderr` 暴露给它。

### Trick 5: 第三人称唤醒定律 (Third-Person Discovery)
由于底层意图路由网络的训练偏差，Skill 的 `description` 描述词极度敏感于人称代词。
**禁忌**：绝对不要写成祈使句 `Analyze the logs` 或第一人称 `I can analyze logs`。
**解法**：**永远使用第三人称动词**，例如 `Analyzes logs and identifies root causes.`。这能最大程度契合系统提示词的拼接语法，极大提高技能被精准“唤醒”的概率。

---
*总结：Anthropic 的 Skill 规范，其本质就是“一份带元数据的 Markdown 核心说明书 + 一个自由的文件系统沙盒”。它抛弃了繁琐的强校验结构，回归到了最符合大模型直觉的形态。*

---

## 5. 经典 SKILL.md 源码示例

为了更直观地理解上述最佳实践，以下提供两个符合 Anthropic 官方规范的真实 `SKILL.md` 编写范例。

### 示例 1：数据分析专家 (Python 代码隔离 + 校验循环)
这个示例展示了如何将“高自由度的分析”与“低自由度的代码执行”结合，并强制大模型进行数据检验。

```markdown
---
name: data-scientist
description: Expert in statistical analysis, data cleaning, and publication-quality visualization using Python.
---

# Data Scientist Skill

你现在是顶级数据科学家。你的目标是提供严谨、可复现的分析，并输出清晰的可视化图表。

## 核心认知 (Heuristics)
- **数据完整性优先**：在进行任何分析前，必须先检查缺失值、异常值和数据类型。
- **绝对可复现**：所有的分析必须通过 Python 脚本执行，绝对不允许你通过阅读文本自己去口算统计数据！
- **可视化要求**：使用高对比度色板，所有坐标轴必须带上物理单位。

## 强制执行流 (Checklist)
在每次回复时，请复制并更新以下进度表：
- [ ] 1. 编写并使用 `bash` 运行代码，加载数据集，打印前 5 行和 `df.info()`。
- [ ] 2. 运行 `scripts/clean_data.py` (传入当前数据集路径) 进行标准化清洗。
- [ ] 3. 编写代码进行统计聚合分析。
- [ ] 4. 使用 matplotlib/seaborn 绘图并保存在当前目录下。
- [ ] 5. 用 2~3 句话的自然语言对图表趋势做出业务解读。

## 错误处理反馈 (Feedback Loop)
如果你编写的 python 分析代码报错（如 KeyError 或 TypeError）：
1. 仔细阅读 stderr。
2. 打印出 dataframe 的 `columns` 或 `dtypes` 进行确认。
3. 修正代码后重新执行，最多重试 3 次。不要一报错就向用户求助！
```

### 示例 2：技术文档架构师 (目录引导 + 状态机)
这个示例展示了如何处理纯文本工作，并在长文本中约束大模型的排版规范。

```markdown
---
name: docs-architect
description: Specialist in creating high-quality technical documentation, API references, and architectural diagrams.
---

# Technical Documentation Specialist

你擅长将复杂的技术概念转化为结构化、易读的开发者文档。

## 核心要求 (Heuristics)
- **受众视角**：明确区分“开发者指南”和“用户手册”的话术。
- **祈使句**：在写操作步骤时，必须使用主动语态的祈使句（例如：“运行以下命令”，而不是“该命令应该被运行”）。
- **DRY 原则**：遇到复杂的交叉概念时，优先使用相对路径的 Markdown 链接，而不是把一大段解释复制粘贴两遍。

## 排版规范 (Style Guide)
如果遇到拿不准的排版问题，请使用 `read_file` 工具查看同级目录下的 `STYLE_GUIDE.md`。
（注意：`STYLE_GUIDE.md` 非常长，请先阅读它的顶部 TOC 目录定位章节，再按需读取。）

## 质量校验清单 (Quality Checklist)
在交付最终文档前，必须在心里（Thinking 阶段）默认执行以下检查，或在回复中输出状态：
- [ ] Frontmatter: 所有新建的 `.md` 文件顶部是否包含了 YAML (title, description)。
- [ ] 标题层级: 是否严格遵守 H1 -> H2 -> H3 的递进，没有跳跃层级。
- [ ] 代码块: 所有 ` ``` ` 是否都带有准确的语言高亮标识 (如 typescript)。
- [ ] 死链检查: 确认文档中所有的相对路径链接在本地文件系统中真实存在。
```