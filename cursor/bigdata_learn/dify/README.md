# Dify 学习总览

本文是 `dify/` 模块的总览文档，按“知识点 → 案例 → 验证数据”的方式组织，便于系统学习与复现。

---

## 一、核心知识点清单

### 1. 应用与能力边界

- **应用类型**：Chat / Completion / Workflow（工作流）
- **系统提示词（System Prompt）**：角色、目标、边界、输出格式
- **变量与上下文**：用户输入、会话历史、检索结果、工具返回

### 2. RAG（知识库问答）

- 数据集导入：文档格式、清洗、切分
- 检索：TopK、相似度阈值、召回噪声
- 引用：要求可追溯来源，降低幻觉
- 评测：问题集回归（`data/sample_queries.json`）

### 3. 工作流（Workflow）

- 节点与数据流：输入 → 判断 → 检索 → 工具调用 → 汇总输出
- 可控性：每一步可解释、可观测、可调参
- 失败处理：空检索、工具失败、超时、异常字段

### 4. 工具与集成

- OpenAPI/HTTP 工具：请求参数、鉴权、响应解析（见 `data/tool_openapi.yaml`）
- 函数调用：结构化输入输出、参数校验

### 5. 工程化要点（学习阶段重点掌握）

- 环境与密钥：模型供应商 Key、权限隔离、最小权限
- 成本与可观测：调用次数、token 消耗、失败率
- 版本迭代：Prompt/知识库/工作流变更后的回归验证

---

## 二、案例与验证数据对照表

| 模块 | 关键点 | 案例文档 | 验证数据 |
|------|--------|----------|----------|
| Chatbot 客服 | Prompt、边界、输出格式、简单记忆 | `cases/chatbot_customer_support.md` | `faq_kb.md`, `order_policy.md`, `sample_queries.json` |
| RAG 知识库 | 文档导入、切分、检索、引用、回归 | `cases/rag_knowledge_base.md` | 同上 |
| 工作流 + 工具 | 流程编排、OpenAPI 工具、异常处理 | `cases/workflow_tool_calling.md` | `tool_openapi.yaml`, `workflow_example.json` |

---

## 三、推荐学习顺序

1. 先跑通 `cases/chatbot_customer_support.md`（不接知识库）。
2. 再跑通 `cases/rag_knowledge_base.md`（把答案约束到可引用）。
3. 最后跑通 `cases/workflow_tool_calling.md`（把“外部查询”接入工具）。

