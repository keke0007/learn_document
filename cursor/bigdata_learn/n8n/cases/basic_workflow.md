# 案例：基础工作流构建

## 目标

掌握 n8n 工作流的基本构建方法，包括触发器、数据处理、条件分支和 HTTP 请求。

---

## 知识点覆盖

- Manual Trigger（手动触发）
- Set 节点（数据设置）
- HTTP Request 节点（API 调用）
- IF 节点（条件分支）
- 表达式语法

---

## 场景描述

构建一个工作流：
1. 手动触发并设置用户数据
2. 根据用户等级判断是否 VIP
3. 调用外部 API 获取额外信息
4. 输出最终结果

---

## 工作流设计

```
Manual Trigger
      ↓
    Set（设置用户数据）
      ↓
    IF（判断 level >= 3）
    ↙     ↘
 VIP路径   普通路径
    ↓         ↓
HTTP Request  Set
    ↓         ↓
   输出      输出
```

---

## 节点配置详解

### 1. Manual Trigger

无需配置，用于开发测试时手动点击执行。

---

### 2. Set 节点 - 设置用户数据

**Operation**: Set  
**Mode**: Manual Mapping

添加字段：
```
user_id: 1001
user_name: "张三"
level: 3
email: "zhangsan@example.com"
```

**输出示例**：
```json
{
  "user_id": 1001,
  "user_name": "张三",
  "level": 3,
  "email": "zhangsan@example.com"
}
```

---

### 3. IF 节点 - 条件分支

**Conditions**:
```
Value 1: {{ $json.level }}
Operation: Larger or Equal
Value 2: 3
```

- **true 分支**：VIP 用户，走 HTTP Request
- **false 分支**：普通用户，走 Set 设置默认值

---

### 4. HTTP Request 节点 - 获取 VIP 信息

**Method**: GET  
**URL**: `https://httpbin.org/get`  
**Query Parameters**:
```
user_id: {{ $json.user_id }}
type: vip_info
```

**响应处理**：
```javascript
// 在后续 Code 节点中可以这样访问
const response = $json;
const args = response.args; // httpbin 返回的 query 参数
```

---

### 5. Set 节点 - 普通用户默认值

**添加字段**：
```
vip_status: false
discount: 1.0
message: "普通用户，暂无优惠"
```

---

## 表达式示例

### 访问当前输入数据
```javascript
{{ $json.user_name }}           // "张三"
{{ $json.level }}               // 3
```

### 访问指定节点输出
```javascript
{{ $node["Set"].json.user_id }}
```

### 条件表达式
```javascript
{{ $json.level >= 3 ? "VIP" : "普通" }}
```

### 字符串拼接
```javascript
{{ "用户：" + $json.user_name + "，等级：" + $json.level }}
```

### 日期处理
```javascript
{{ $now.format('yyyy-MM-dd HH:mm:ss') }}
{{ $now.minus({days: 7}).toISO() }}
```

---

## 验证步骤

1. **创建工作流**：按上述步骤添加节点并连接
2. **执行测试**：点击 Execute Workflow
3. **检查每个节点**：
   - Set 节点输出用户数据
   - IF 节点根据 level 分流
   - HTTP Request 返回 httpbin 响应
4. **修改测试数据**：将 level 改为 2，验证走普通用户分支

---

## 常见问题

### Q1: 表达式不生效？
确保使用双花括号 `{{ }}`，并检查字段名拼写。

### Q2: HTTP Request 超时？
检查网络连接，或在节点设置中增加 Timeout 时间。

### Q3: 如何查看完整数据？
点击节点，在右侧面板切换 Table / JSON 视图。

---

## 扩展练习

1. 添加 Switch 节点，根据 level 值（1/2/3/4/5）分别处理
2. 添加 Merge 节点，合并 VIP 和普通用户的处理结果
3. 添加 Code 节点，用 JavaScript 计算折扣金额
