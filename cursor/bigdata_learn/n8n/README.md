# n8n 学习模块

## 概述

n8n 是一个开源的工作流自动化工具，可自托管，支持 400+ 集成节点，适用于数据同步、API 编排、消息通知等场景。

---

## 知识点与案例映射

| 知识点 | 说明 | 案例 | 数据/脚本 |
|--------|------|------|-----------|
| 核心概念 | Workflow, Node, Credential | `cases/basic_workflow.md` | - |
| Manual Trigger | 手动触发，用于开发测试 | `cases/basic_workflow.md` | - |
| Schedule Trigger | 定时触发（Cron 表达式） | `cases/data_sync_etl.md` | - |
| Webhook Trigger | HTTP 回调触发 | `cases/webhook_api_integration.md` | `data/sample_webhook_payload.json` |
| HTTP Request | 调用外部 API | `cases/basic_workflow.md` | `data/api_response_sample.json` |
| Set 节点 | 数据赋值与字段映射 | `cases/basic_workflow.md` | - |
| Code 节点 | JavaScript/Python 自定义逻辑 | `cases/webhook_api_integration.md` | - |
| IF / Switch | 条件分支 | `cases/basic_workflow.md` | - |
| Loop Over Items | 循环处理数组 | `cases/data_sync_etl.md` | - |
| Merge 节点 | 多数据源合并 | `cases/data_sync_etl.md` | - |
| 数据库节点 | MySQL, PostgreSQL 操作 | `cases/data_sync_etl.md` | - |
| 错误处理 | Error Trigger, Stop and Error | `cases/webhook_api_integration.md` | - |
| 子工作流 | Execute Workflow 节点 | `cases/data_sync_etl.md` | - |
| 表达式语法 | $json, $node, $input, $env | 所有案例 | - |
| 工作流导入导出 | JSON 格式 | - | `data/workflow_export.json` |

---

## 学习路径

```
基础概念 → 核心节点 → 触发器类型 → 集成场景 → 高级特性
   ↓           ↓           ↓            ↓           ↓
 概念理解   HTTP/Set/IF  Webhook/Cron  API/DB/通知  错误处理/子流程
```

---

## 快速验证

### 1. 启动 n8n
```bash
# Docker
docker run -it --rm -p 5678:5678 n8nio/n8n

# 或 npm
npx n8n
```

### 2. 创建测试工作流
- Manual Trigger → Set（设置测试数据） → HTTP Request（请求 httpbin.org）

### 3. 导入示例工作流
- 复制 `data/workflow_export.json` 内容
- 在 n8n 编辑器中点击 Import from URL/File

---

## 相关资源

- [n8n 官方文档](https://docs.n8n.io/)
- [n8n 社区节点](https://n8n.io/integrations/)
- [n8n GitHub](https://github.com/n8n-io/n8n)
