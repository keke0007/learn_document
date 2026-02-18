# n8n 工作流自动化学习指南

## 一、项目简介

n8n 是一个开源、可自托管的工作流自动化平台，支持通过可视化界面连接各种应用和服务，实现数据流转和业务自动化。本模块涵盖 n8n 核心概念、常用节点、集成场景和最佳实践。

---

## 二、目录结构

```
n8n/
├── GUIDE.md                    # 本指南文档
├── README.md                   # 知识点与案例总览
├── cases/
│   ├── basic_workflow.md       # 基础工作流构建
│   ├── webhook_api_integration.md  # Webhook 与 API 集成
│   └── data_sync_etl.md        # 数据同步与 ETL 场景
├── data/
│   ├── sample_webhook_payload.json  # Webhook 请求示例
│   ├── api_response_sample.json     # API 响应示例
│   └── workflow_export.json         # 工作流导出示例
└── scripts/
    ├── setup_notes.md          # 环境搭建说明
    └── api_examples.md         # n8n API 调用示例
```

---

## 三、学习路线

### 第一阶段：基础入门
- n8n 架构与核心概念（Workflow、Node、Connection、Credential）
- 安装与部署（Docker / npm / Desktop）
- 工作流编辑器基本操作
- 触发器类型（Manual、Schedule、Webhook）

### 第二阶段：核心节点与数据处理
- HTTP Request 节点（GET/POST/PUT/DELETE）
- Code 节点（JavaScript/Python 自定义逻辑）
- Set 节点（数据赋值与转换）
- IF / Switch 节点（条件分支）
- Merge / Split 节点（数据合并与拆分）
- Loop Over Items（循环处理）

### 第三阶段：集成与自动化场景
- Webhook 触发与回调
- 数据库节点（MySQL、PostgreSQL、MongoDB）
- 消息通知（Slack、Email、钉钉、企业微信）
- 文件操作（Read/Write File、FTP、S3）
- 第三方 SaaS 集成（Notion、Airtable、Google Sheets）

### 第四阶段：高级特性与生产实践
- 错误处理（Error Trigger、Stop and Error）
- 子工作流（Execute Workflow）
- 变量与表达式（$json, $input, $node, $env）
- 工作流版本管理与导入导出
- 生产部署与监控

---

## 四、快速开始

### 4.1 环境准备

**Docker 方式（推荐）**：
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

**npm 方式**：
```bash
npm install n8n -g
n8n start
```

访问 http://localhost:5678 进入编辑器。

### 4.2 创建第一个工作流

1. 点击 **Add first step** 添加触发器
2. 选择 **Manual Trigger**（手动触发）
3. 添加 **Set** 节点，设置测试数据
4. 添加 **HTTP Request** 节点，请求外部 API
5. 点击 **Execute Workflow** 运行测试

### 4.3 验证结果

每个节点执行后可查看：
- **Input**：输入数据
- **Output**：输出数据
- **Error**：错误信息（如有）

---

## 五、核心知识速查

### 5.1 核心概念

| 概念 | 说明 |
|------|------|
| **Workflow** | 工作流，由多个节点按顺序/分支组成 |
| **Node** | 节点，执行特定操作（触发、处理、输出） |
| **Connection** | 连接线，定义数据流向 |
| **Credential** | 凭证，存储 API Key、密码等敏感信息 |
| **Execution** | 执行记录，包含每次运行的输入输出 |

### 5.2 常用节点

| 节点类型 | 典型节点 | 用途 |
|----------|----------|------|
| **Trigger** | Manual, Schedule, Webhook | 触发工作流 |
| **Action** | HTTP Request, Code, Set | 执行操作 |
| **Flow** | IF, Switch, Merge, Loop | 控制流程 |
| **Data** | MySQL, PostgreSQL, Redis | 数据存取 |
| **Notification** | Slack, Email, Discord | 消息通知 |

### 5.3 表达式语法

```javascript
// 访问当前节点输入
{{ $json.fieldName }}

// 访问指定节点输出
{{ $node["NodeName"].json.fieldName }}

// 访问所有输入项
{{ $input.all() }}

// 环境变量
{{ $env.MY_VAR }}

// 内置函数
{{ $now.format('yyyy-MM-dd') }}
{{ $json.name.toUpperCase() }}
```

### 5.4 触发器对比

| 触发器 | 场景 | 示例 |
|--------|------|------|
| **Manual** | 开发测试 | 手动点击执行 |
| **Schedule** | 定时任务 | 每小时同步数据 |
| **Webhook** | 外部回调 | 接收支付通知 |
| **App Trigger** | SaaS 事件 | Gmail 新邮件触发 |

---

## 六、数据说明

| 文件 | 说明 |
|------|------|
| `data/sample_webhook_payload.json` | Webhook 请求体示例 |
| `data/api_response_sample.json` | API 响应数据示例 |
| `data/workflow_export.json` | 可导入的工作流模板 |

---

## 七、案例总览

| 案例 | 知识点 | 文件 |
|------|--------|------|
| 基础工作流构建 | Manual Trigger, Set, HTTP Request, IF | `cases/basic_workflow.md` |
| Webhook 与 API 集成 | Webhook Trigger, HTTP Request, Code | `cases/webhook_api_integration.md` |
| 数据同步与 ETL | Schedule, MySQL, Loop, Merge | `cases/data_sync_etl.md` |

---

## 八、学习建议

1. **先跑通再深入**：从 Manual Trigger + Set + HTTP Request 开始
2. **善用节点文档**：每个节点右上角有官方文档链接
3. **观察数据流**：执行后点击每个节点查看 Input/Output
4. **表达式调试**：使用 `{{ }}` 内的 Expression Editor
5. **复用工作流**：通过 Execute Workflow 调用子流程

---

## 九、学习检查清单

- [ ] 能用 Docker 或 npm 启动 n8n
- [ ] 理解 Workflow、Node、Connection、Credential 概念
- [ ] 能创建 Manual / Schedule / Webhook 触发的工作流
- [ ] 熟练使用 HTTP Request、Set、Code、IF 节点
- [ ] 掌握 `$json`、`$node`、`$input` 表达式语法
- [ ] 能配置错误处理和子工作流
- [ ] 能导入/导出工作流 JSON

---

## 十、学习成果

完成本模块后，你将能够：

1. 部署和使用 n8n 工作流自动化平台
2. 设计和构建多节点工作流
3. 通过 Webhook 实现外部系统集成
4. 使用 Code 节点编写自定义数据处理逻辑
5. 实现定时数据同步和 ETL 流程
6. 配置错误处理和工作流监控
