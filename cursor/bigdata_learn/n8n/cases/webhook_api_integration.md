# 案例：Webhook 与 API 集成

## 目标

掌握 n8n Webhook 触发器和 HTTP Request 节点，实现外部系统与 n8n 的双向集成。

---

## 知识点覆盖

- Webhook Trigger（HTTP 回调触发）
- HTTP Request（调用外部 API）
- Code 节点（自定义数据处理）
- 错误处理（Error Trigger）
- Respond to Webhook（返回响应）

---

## 场景描述

构建订单通知工作流：
1. 接收外部系统的订单 Webhook 回调
2. 解析订单数据并校验
3. 调用库存 API 检查库存
4. 发送通知（成功/失败）
5. 返回处理结果给调用方

---

## 工作流设计

```
Webhook Trigger
      ↓
Code（数据校验）
      ↓
HTTP Request（检查库存）
      ↓
    IF（库存充足？）
    ↙        ↘
发送成功通知  发送失败通知
    ↘        ↙
Respond to Webhook
```

---

## 节点配置详解

### 1. Webhook Trigger

**HTTP Method**: POST  
**Path**: `order-notification`  
**Authentication**: None（生产环境建议配置）

**生成的 Webhook URL**:
```
http://localhost:5678/webhook/order-notification       # 测试
http://localhost:5678/webhook-test/order-notification  # 编辑器测试
```

**期望接收的请求体**：
```json
{
  "order_id": "ORD20240115001",
  "user_id": "U1001",
  "product_id": "P2001",
  "quantity": 2,
  "amount": 199.00,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### 2. Code 节点 - 数据校验

**Language**: JavaScript

```javascript
// 获取 Webhook 输入数据
const order = $input.first().json;

// 校验必填字段
const requiredFields = ['order_id', 'user_id', 'product_id', 'quantity', 'amount'];
const missingFields = requiredFields.filter(field => !order[field]);

if (missingFields.length > 0) {
  throw new Error(`缺少必填字段: ${missingFields.join(', ')}`);
}

// 校验数量和金额
if (order.quantity <= 0) {
  throw new Error('数量必须大于 0');
}
if (order.amount <= 0) {
  throw new Error('金额必须大于 0');
}

// 返回校验通过的数据
return [{
  json: {
    ...order,
    validated: true,
    validated_at: new Date().toISOString()
  }
}];
```

---

### 3. HTTP Request - 检查库存

**Method**: GET  
**URL**: `https://httpbin.org/get`  
（实际场景替换为库存 API）

**Query Parameters**:
```
product_id: {{ $json.product_id }}
quantity: {{ $json.quantity }}
```

**响应处理**：
在后续节点中模拟库存判断：
```javascript
// 模拟：product_id 以 P2 开头的有库存
const hasStock = $json.product_id.startsWith('P2');
```

---

### 4. Code 节点 - 处理库存响应

```javascript
const order = $input.first().json;

// 模拟库存检查结果（实际从 API 响应获取）
const stockAvailable = order.quantity <= 10; // 假设库存上限 10

return [{
  json: {
    ...order,
    stock_available: stockAvailable,
    stock_message: stockAvailable ? '库存充足' : '库存不足'
  }
}];
```

---

### 5. IF 节点 - 判断库存

**Conditions**:
```
Value 1: {{ $json.stock_available }}
Operation: Equal
Value 2: true
```

---

### 6. Set 节点 - 成功响应

**添加字段**：
```json
{
  "success": true,
  "message": "订单处理成功",
  "order_id": "{{ $json.order_id }}",
  "status": "confirmed"
}
```

---

### 7. Set 节点 - 失败响应

**添加字段**：
```json
{
  "success": false,
  "message": "库存不足，订单处理失败",
  "order_id": "{{ $json.order_id }}",
  "status": "rejected"
}
```

---

### 8. Respond to Webhook

**Response Code**: 200  
**Response Body**: 
```
{{ JSON.stringify($json) }}
```

---

## 错误处理

### 添加 Error Trigger

在工作流中添加 Error Trigger 节点，捕获任意节点的错误：

```
Error Trigger
      ↓
Set（构造错误响应）
      ↓
HTTP Request（发送告警）
```

**Error Trigger 输出**：
```javascript
{
  "execution": { "id": "xxx", "url": "xxx" },
  "workflow": { "id": "xxx", "name": "xxx" },
  "node": { "name": "xxx", "type": "xxx" },
  "error": { "message": "xxx", "stack": "xxx" }
}
```

---

## 测试方法

### 使用 curl 测试

```bash
# 成功场景
curl -X POST http://localhost:5678/webhook/order-notification \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORD20240115001",
    "user_id": "U1001",
    "product_id": "P2001",
    "quantity": 2,
    "amount": 199.00
  }'

# 库存不足场景
curl -X POST http://localhost:5678/webhook/order-notification \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORD20240115002",
    "user_id": "U1002",
    "product_id": "P2002",
    "quantity": 100,
    "amount": 9900.00
  }'

# 缺少字段场景
curl -X POST http://localhost:5678/webhook/order-notification \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORD20240115003"
  }'
```

### 在 n8n 编辑器测试

1. 点击 Webhook 节点的 **Listen for Test Event**
2. 使用 curl 发送请求到 webhook-test URL
3. 数据捕获后点击 **Execute Workflow**

---

## Webhook 安全配置

### Basic Auth

```
Authentication: Basic Auth
Credential: 创建 HTTP Basic Auth 凭证
```

### Header Auth

```
Authentication: Header Auth
Header Name: X-API-Key
Header Value: your-secret-key
```

### 验证签名（Code 节点）

```javascript
const crypto = require('crypto');
const secret = 'your-webhook-secret';
const signature = $input.first().headers['x-signature'];
const payload = JSON.stringify($input.first().json);

const expectedSignature = crypto
  .createHmac('sha256', secret)
  .update(payload)
  .digest('hex');

if (signature !== expectedSignature) {
  throw new Error('签名验证失败');
}

return $input.all();
```

---

## 扩展练习

1. 添加 Slack/Email 节点，在订单处理成功后发送通知
2. 添加 MySQL 节点，将订单记录写入数据库
3. 使用 Execute Workflow 调用独立的通知子工作流
