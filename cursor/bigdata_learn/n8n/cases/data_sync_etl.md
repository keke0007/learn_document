# 案例：数据同步与 ETL 场景

## 目标

掌握 n8n 定时任务、数据库操作、循环处理和数据合并，实现数据同步和 ETL 流程。

---

## 知识点覆盖

- Schedule Trigger（定时触发）
- MySQL / PostgreSQL 节点
- Loop Over Items（循环处理）
- Merge 节点（数据合并）
- Split In Batches（分批处理）
- Execute Workflow（子工作流）

---

## 场景描述

构建数据同步工作流：
1. 每小时定时触发
2. 从源数据库读取增量数据
3. 数据转换和清洗
4. 分批写入目标数据库
5. 记录同步日志

---

## 工作流设计

```
Schedule Trigger (每小时)
         ↓
MySQL (读取增量数据)
         ↓
Split In Batches (每批 100 条)
         ↓
    ┌────┴────┐
    ↓         ↓
Code (转换)  Loop
    ↓         
PostgreSQL (写入)
         ↓
Set (统计结果)
         ↓
HTTP Request (发送日志)
```

---

## 节点配置详解

### 1. Schedule Trigger - 定时触发

**Trigger Interval**: Hours  
**Hours Between Triggers**: 1

或使用 Cron 表达式：
```
Cron Expression: 0 * * * *  # 每小时整点
```

常用 Cron 示例：
```
*/5 * * * *     # 每 5 分钟
0 */2 * * *     # 每 2 小时
0 9 * * *       # 每天 9 点
0 9 * * 1-5     # 工作日 9 点
0 0 1 * *       # 每月 1 号
```

---

### 2. MySQL 节点 - 读取增量数据

**Credential**: 配置 MySQL 连接信息  
**Operation**: Execute Query

**查询语句**：
```sql
SELECT 
    id,
    user_name,
    email,
    status,
    created_at,
    updated_at
FROM users
WHERE updated_at > DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY id
LIMIT 1000;
```

**使用表达式动态时间**：
```sql
SELECT * FROM users 
WHERE updated_at > '{{ $now.minus({hours: 1}).toFormat("yyyy-MM-dd HH:mm:ss") }}'
```

---

### 3. IF 节点 - 检查是否有数据

**Conditions**:
```
Value 1: {{ $json.length }}
Operation: Larger
Value 2: 0
```

如果没有数据，可以提前结束或发送空同步通知。

---

### 4. Split In Batches - 分批处理

**Batch Size**: 100

将大量数据拆分为小批次处理，避免内存溢出和写入超时。

**输出**：每批次 100 条记录，循环执行后续节点。

---

### 5. Code 节点 - 数据转换

```javascript
// 获取当前批次的所有数据
const items = $input.all();

// 数据转换和清洗
const transformedItems = items.map(item => {
  const data = item.json;
  
  return {
    json: {
      // 字段映射
      user_id: data.id,
      username: data.user_name?.toLowerCase().trim(),
      email: data.email?.toLowerCase().trim(),
      
      // 状态转换
      is_active: data.status === 'active' ? 1 : 0,
      
      // 添加同步时间
      synced_at: new Date().toISOString(),
      
      // 保留原始时间
      source_created_at: data.created_at,
      source_updated_at: data.updated_at
    }
  };
});

return transformedItems;
```

---

### 6. PostgreSQL 节点 - 批量写入

**Credential**: 配置 PostgreSQL 连接信息  
**Operation**: Insert  
**Table**: user_sync

或使用 Upsert（有则更新，无则插入）：
**Operation**: Upsert  
**Table**: user_sync  
**Unique Column**: user_id

**手动 SQL 方式**：
```sql
INSERT INTO user_sync (user_id, username, email, is_active, synced_at)
VALUES 
{{ $json.map(item => 
  `(${item.user_id}, '${item.username}', '${item.email}', ${item.is_active}, '${item.synced_at}')`
).join(',') }}
ON CONFLICT (user_id) 
DO UPDATE SET 
  username = EXCLUDED.username,
  email = EXCLUDED.email,
  is_active = EXCLUDED.is_active,
  synced_at = EXCLUDED.synced_at;
```

---

### 7. Merge 节点 - 汇总所有批次

**Mode**: Append  
将所有批次的处理结果合并为一个数组。

---

### 8. Code 节点 - 统计同步结果

```javascript
const allItems = $input.all();

const stats = {
  total_synced: allItems.length,
  sync_time: new Date().toISOString(),
  batches_processed: Math.ceil(allItems.length / 100),
  status: 'completed'
};

// 可以添加更详细的统计
const activeCount = allItems.filter(item => item.json.is_active === 1).length;
stats.active_users = activeCount;
stats.inactive_users = allItems.length - activeCount;

return [{ json: stats }];
```

---

### 9. HTTP Request - 发送同步日志

**Method**: POST  
**URL**: `https://your-log-service.com/api/sync-log`  
**Body Content Type**: JSON

```json
{
  "workflow": "user_data_sync",
  "stats": {{ JSON.stringify($json) }},
  "timestamp": "{{ $now.toISO() }}"
}
```

---

## 子工作流模式

### 主工作流
```
Schedule Trigger
      ↓
Execute Workflow (user_sync_sub)
      ↓
Execute Workflow (order_sync_sub)
      ↓
Merge (合并结果)
      ↓
Send Summary
```

### Execute Workflow 节点配置

**Source**: Database  
**Workflow**: 选择子工作流  
**Mode**: 
- Run Once for All Items: 传递所有数据执行一次
- Run Once for Each Item: 每条数据执行一次

**传递数据**：
```javascript
{
  "sync_type": "incremental",
  "start_time": "{{ $now.minus({hours: 1}).toISO() }}",
  "end_time": "{{ $now.toISO() }}"
}
```

---

## 错误处理与重试

### 节点级别重试

在 HTTP Request 或数据库节点设置中：
- **Continue On Fail**: true（失败继续执行）
- **Retry On Fail**: true（失败自动重试）
- **Max Tries**: 3（最大重试次数）
- **Wait Between Tries**: 1000ms（重试间隔）

### 全局错误处理

添加 Error Trigger 工作流：
```
Error Trigger
      ↓
Set (构造错误信息)
      ↓
Slack/Email (发送告警)
      ↓
MySQL (记录错误日志)
```

---

## 验证步骤

### 1. 准备测试数据

在源 MySQL 创建测试表：
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(100),
    email VARCHAR(200),
    status VARCHAR(20),
    created_at DATETIME,
    updated_at DATETIME
);

INSERT INTO users (user_name, email, status, created_at, updated_at)
VALUES 
('张三', 'zhangsan@example.com', 'active', NOW(), NOW()),
('李四', 'lisi@example.com', 'inactive', NOW(), NOW()),
('王五', 'wangwu@example.com', 'active', NOW(), NOW());
```

### 2. 准备目标表

在目标 PostgreSQL 创建表：
```sql
CREATE TABLE user_sync (
    user_id INT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(200),
    is_active INT,
    synced_at TIMESTAMP,
    source_created_at TIMESTAMP,
    source_updated_at TIMESTAMP
);
```

### 3. 手动执行测试

先用 Manual Trigger 替换 Schedule Trigger，手动执行验证。

### 4. 启用定时调度

验证通过后，切换为 Schedule Trigger 并激活工作流。

---

## 扩展练习

1. 添加数据校验，跳过无效记录并记录日志
2. 实现全量同步 + 增量同步两种模式
3. 添加数据对比，检测源和目标差异
4. 使用 Redis 缓存上次同步位点
