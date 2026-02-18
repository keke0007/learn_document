# n8n 环境搭建说明

## 一、安装方式

### 方式 1：Docker（推荐）

**基础启动**：
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  n8nio/n8n
```

**持久化数据**：
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

**带环境变量**：
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=your_password \
  -e GENERIC_TIMEZONE=Asia/Shanghai \
  -e TZ=Asia/Shanghai \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

### 方式 2：Docker Compose

创建 `docker-compose.yml`：
```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your_password
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678/
      - GENERIC_TIMEZONE=Asia/Shanghai
      - TZ=Asia/Shanghai
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

启动：
```bash
docker-compose up -d
```

### 方式 3：npm 全局安装

```bash
npm install n8n -g
n8n start
```

### 方式 4：npx 临时运行

```bash
npx n8n
```

---

## 二、关键配置

### 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `N8N_BASIC_AUTH_ACTIVE` | 启用 Basic Auth | `true` |
| `N8N_BASIC_AUTH_USER` | 用户名 | `admin` |
| `N8N_BASIC_AUTH_PASSWORD` | 密码 | `password123` |
| `N8N_HOST` | 主机地址 | `0.0.0.0` |
| `N8N_PORT` | 端口 | `5678` |
| `WEBHOOK_URL` | Webhook 基础 URL | `https://n8n.example.com/` |
| `N8N_ENCRYPTION_KEY` | 凭证加密密钥 | `your-encryption-key` |
| `GENERIC_TIMEZONE` | 时区 | `Asia/Shanghai` |
| `EXECUTIONS_DATA_PRUNE` | 自动清理执行记录 | `true` |
| `EXECUTIONS_DATA_MAX_AGE` | 执行记录保留时长(小时) | `168` |

### 数据库配置（生产环境）

默认使用 SQLite，生产环境建议使用 PostgreSQL 或 MySQL：

**PostgreSQL**：
```bash
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=localhost
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_USER=n8n
DB_POSTGRESDB_PASSWORD=password
```

**MySQL**：
```bash
DB_TYPE=mysqldb
DB_MYSQLDB_HOST=localhost
DB_MYSQLDB_PORT=3306
DB_MYSQLDB_DATABASE=n8n
DB_MYSQLDB_USER=n8n
DB_MYSQLDB_PASSWORD=password
```

---

## 三、生产部署检查清单

- [ ] 配置 HTTPS（通过 Nginx/Traefik 反向代理）
- [ ] 设置 `N8N_BASIC_AUTH_ACTIVE=true` 或配置 SSO
- [ ] 配置 `N8N_ENCRYPTION_KEY`（用于加密凭证）
- [ ] 使用 PostgreSQL/MySQL 替代 SQLite
- [ ] 设置 `WEBHOOK_URL` 为公网可访问地址
- [ ] 配置执行记录自动清理
- [ ] 设置时区 `GENERIC_TIMEZONE`
- [ ] 配置日志级别和输出

---

## 四、常用命令

```bash
# 查看 n8n 版本
n8n --version

# 导出所有工作流
n8n export:workflow --all --output=workflows.json

# 导入工作流
n8n import:workflow --input=workflows.json

# 导出凭证
n8n export:credentials --all --output=credentials.json

# 导入凭证
n8n import:credentials --input=credentials.json

# 执行指定工作流
n8n execute --id=<workflow_id>
```

---

## 五、故障排查

### 问题 1：Webhook 无法接收请求

- 检查 `WEBHOOK_URL` 配置是否正确
- 确认防火墙/安全组开放端口
- 使用 `webhook-test` 路径在编辑器中测试

### 问题 2：凭证无法保存

- 检查 `N8N_ENCRYPTION_KEY` 是否配置
- 确认数据卷权限正确

### 问题 3：定时任务不触发

- 确认工作流已激活（Active 状态）
- 检查时区配置 `GENERIC_TIMEZONE`
- 查看执行记录中的错误信息

### 问题 4：内存不足

- 增加容器内存限制
- 配置 `EXECUTIONS_DATA_PRUNE=true` 清理历史执行
- 使用 `Split In Batches` 处理大数据量
