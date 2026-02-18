# Dify API 调用示例（学习用）

> 说明：不同部署/版本的 API 形态可能不同，本文件给“示例模板”，便于你在实际环境中替换参数使用。

## 1. 调用 Chat 应用（示例模板）

```bash
curl -X POST "http://<dify-host>/v1/chat-messages" \
  -H "Authorization: Bearer <APP_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {},
    "query": "多久发货？",
    "response_mode": "blocking",
    "user": "demo_user_1"
  }'
```

## 2. 调用 Workflow 应用（示例模板）

```bash
curl -X POST "http://<dify-host>/v1/workflows/run" \
  -H "Authorization: Bearer <APP_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
      "order_id": 1001
    },
    "user": "demo_user_1"
  }'
```

