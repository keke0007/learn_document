# n8n API 调用示例

n8n 提供 REST API，可用于外部系统管理和触发工作流。

---

## 一、API 认证

### Basic Auth

```bash
curl -u admin:password https://n8n.example.com/api/v1/workflows
```

### API Key（n8n 1.0+）

在 n8n 设置中生成 API Key，通过 Header 传递：

```bash
curl -H "X-N8N-API-KEY: your-api-key" \
  https://n8n.example.com/api/v1/workflows
```

---

## 二、工作流管理 API

### 获取所有工作流

```bash
curl -X GET \
  -H "X-N8N-API-KEY: your-api-key" \
  "http://localhost:5678/api/v1/workflows"
```

**响应示例**：
```json
{
  "data": [
    {
      "id": "1",
      "name": "订单处理工作流",
      "active": true,
      "createdAt": "2024-01-15T10:00:00.000Z",
      "updatedAt": "2024-01-15T12:00:00.000Z"
    }
  ]
}
```

### 获取单个工作流

```bash
curl -X GET \
  -H "X-N8N-API-KEY: your-api-key" \
  "http://localhost:5678/api/v1/workflows/{workflow_id}"
```

### 创建工作流

```bash
curl -X POST \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "新工作流",
    "nodes": [...],
    "connections": {...},
    "settings": {}
  }' \
  "http://localhost:5678/api/v1/workflows"
```

### 更新工作流

```bash
curl -X PATCH \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "更新后的名称",
    "active": true
  }' \
  "http://localhost:5678/api/v1/workflows/{workflow_id}"
```

### 删除工作流

```bash
curl -X DELETE \
  -H "X-N8N-API-KEY: your-api-key" \
  "http://localhost:5678/api/v1/workflows/{workflow_id}"
```

### 激活/停用工作流

```bash
# 激活
curl -X PATCH \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"active": true}' \
  "http://localhost:5678/api/v1/workflows/{workflow_id}"

# 停用
curl -X PATCH \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"active": false}' \
  "http://localhost:5678/api/v1/workflows/{workflow_id}"
```

---

## 三、执行管理 API

### 获取执行记录列表

```bash
curl -X GET \
  -H "X-N8N-API-KEY: your-api-key" \
  "http://localhost:5678/api/v1/executions?limit=10"
```

### 获取单个执行详情

```bash
curl -X GET \
  -H "X-N8N-API-KEY: your-api-key" \
  "http://localhost:5678/api/v1/executions/{execution_id}"
```

### 删除执行记录

```bash
curl -X DELETE \
  -H "X-N8N-API-KEY: your-api-key" \
  "http://localhost:5678/api/v1/executions/{execution_id}"
```

---

## 四、通过 Webhook 触发工作流

### Production Webhook（工作流激活后）

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORD20240115001",
    "user_id": "U1001",
    "amount": 199.00
  }' \
  "http://localhost:5678/webhook/order-notification"
```

### Test Webhook（编辑器测试）

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORD20240115001",
    "user_id": "U1001",
    "amount": 199.00
  }' \
  "http://localhost:5678/webhook-test/order-notification"
```

### 带认证的 Webhook

```bash
# Basic Auth
curl -X POST \
  -u webhook_user:webhook_password \
  -H "Content-Type: application/json" \
  -d '{"data": "test"}' \
  "http://localhost:5678/webhook/secure-endpoint"

# Header Auth
curl -X POST \
  -H "X-API-Key: your-webhook-secret" \
  -H "Content-Type: application/json" \
  -d '{"data": "test"}' \
  "http://localhost:5678/webhook/secure-endpoint"
```

---

## 五、凭证管理 API

### 获取所有凭证

```bash
curl -X GET \
  -H "X-N8N-API-KEY: your-api-key" \
  "http://localhost:5678/api/v1/credentials"
```

### 创建凭证

```bash
curl -X POST \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MySQL Production",
    "type": "mySql",
    "data": {
      "host": "localhost",
      "port": 3306,
      "database": "mydb",
      "user": "root",
      "password": "password"
    }
  }' \
  "http://localhost:5678/api/v1/credentials"
```

---

## 六、Python SDK 示例

```python
import requests

class N8nClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'X-N8N-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
    
    def get_workflows(self):
        """获取所有工作流"""
        response = requests.get(
            f"{self.base_url}/api/v1/workflows",
            headers=self.headers
        )
        return response.json()
    
    def trigger_webhook(self, webhook_path, data):
        """触发 Webhook"""
        response = requests.post(
            f"{self.base_url}/webhook/{webhook_path}",
            json=data
        )
        return response.json()
    
    def get_executions(self, limit=10):
        """获取执行记录"""
        response = requests.get(
            f"{self.base_url}/api/v1/executions",
            headers=self.headers,
            params={'limit': limit}
        )
        return response.json()
    
    def activate_workflow(self, workflow_id, active=True):
        """激活/停用工作流"""
        response = requests.patch(
            f"{self.base_url}/api/v1/workflows/{workflow_id}",
            headers=self.headers,
            json={'active': active}
        )
        return response.json()


# 使用示例
if __name__ == "__main__":
    client = N8nClient(
        base_url="http://localhost:5678",
        api_key="your-api-key"
    )
    
    # 获取工作流列表
    workflows = client.get_workflows()
    print("工作流列表:", workflows)
    
    # 触发 Webhook
    result = client.trigger_webhook(
        webhook_path="order-notification",
        data={
            "order_id": "ORD20240115001",
            "amount": 199.00
        }
    )
    print("Webhook 响应:", result)
```

---

## 七、JavaScript/Node.js 示例

```javascript
const axios = require('axios');

class N8nClient {
  constructor(baseUrl, apiKey) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
  }

  async getWorkflows() {
    const response = await axios.get(
      `${this.baseUrl}/api/v1/workflows`,
      { headers: { 'X-N8N-API-KEY': this.apiKey } }
    );
    return response.data;
  }

  async triggerWebhook(webhookPath, data) {
    const response = await axios.post(
      `${this.baseUrl}/webhook/${webhookPath}`,
      data
    );
    return response.data;
  }

  async activateWorkflow(workflowId, active = true) {
    const response = await axios.patch(
      `${this.baseUrl}/api/v1/workflows/${workflowId}`,
      { active },
      { headers: { 'X-N8N-API-KEY': this.apiKey } }
    );
    return response.data;
  }
}

// 使用示例
(async () => {
  const client = new N8nClient(
    'http://localhost:5678',
    'your-api-key'
  );

  // 获取工作流
  const workflows = await client.getWorkflows();
  console.log('工作流列表:', workflows);

  // 触发 Webhook
  const result = await client.triggerWebhook('order-notification', {
    order_id: 'ORD20240115001',
    amount: 199.00
  });
  console.log('Webhook 响应:', result);
})();
```
