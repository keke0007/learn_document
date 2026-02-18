# Seata 源码学习案例（深入版）

## 案例概述

本案例深入 Seata AT 模式、全局事务、RM/TM/TC 交互等核心源码。**重点：断点位置、数据结构、undo_log 机制、全局锁、基于源码的扩展实验。**

---

## 📍 断点清单（建议按顺序打断点）

### AT 模式断点
1. **`GlobalTransactionalInterceptor.invoke()`** (L89) - 全局事务拦截入口
2. **`DefaultGlobalTransaction.begin()`** (L124) - 全局事务开始
3. **`DataSourceProxy.getConnection()`** (L89) - 数据源代理获取连接
4. **`ConnectionProxy.execute()`** (L124) - 连接代理执行 SQL
5. **`UndoLogManager.insertUndoLog()`** (L89) - undo_log 插入

### 回滚断点
1. **`UndoLogManager.undo()`** (L124) - undo_log 回滚
2. **`AbstractUndoLogParser.decode()`** (L89) - undo_log 解析
3. **`SQLUndoLog.getUndoSQL()`** (L124) - 反向 SQL 生成

### TC 交互断点
1. **`TmNettyRemotingClient.sendSyncRequest()`** (L89) - TM 发送请求
2. **`RmNettyRemotingClient.sendSyncRequest()`** (L124) - RM 发送请求
3. **`DefaultCoordinator.doGlobalCommit()`** (L89) - TC 全局提交
4. **`DefaultCoordinator.doGlobalRollback()`** (L124) - TC 全局回滚

---

## 🔍 关键数据结构

### AT 模式核心数据结构

```java
// GlobalTransactionScanner.java
// 1. 全局事务扫描器
private final Map<Method, GlobalTransactional> globalTransactionalMap = new ConcurrentHashMap<>();

// DefaultGlobalTransaction.java
// 2. 全局事务对象
private String xid;
private GlobalStatus status;
private GlobalTransactionRole role;

// DataSourceProxy.java
// 3. 数据源代理
private final DataSource targetDataSource;
private final ResourceManager resourceManager;

// ConnectionProxy.java
// 4. 连接代理
private final Connection targetConnection;
private final String xid;
private final String branchId;

// UndoLogManager.java
// 5. undo_log 管理器
private final UndoLogParser undoLogParser;
```

### undo_log 核心数据结构

```java
// UndoLog.java
// 1. undo_log 对象
private long branchId;
private String xid;
private String context;
private byte[] rollbackInfo;
private int logStatus;
private Date logCreated;
private Date logModified;

// BranchUndoLog.java
// 2. 分支 undo_log
private String xid;
private long branchId;
private List<SQLUndoLog> sqlUndoLogs;

// SQLUndoLog.java
// 3. SQL undo_log
private String tableName;
private TableRecords beforeImage;
private TableRecords afterImage;
private SQLType sqlType;
```

### TC 交互核心数据结构

```java
// DefaultCoordinator.java
// 1. 全局事务映射
private final Map<String, GlobalSession> globalSessions = new ConcurrentHashMap<>();

// GlobalSession.java
// 2. 全局会话
private String xid;
private GlobalStatus status;
private List<BranchSession> branchSessions = new ArrayList<>();

// BranchSession.java
// 3. 分支会话
private String xid;
private long branchId;
private String resourceId;
private String lockKey;
```

---

## 🧵 线程模型

### AT 模式线程模型
- **事务拦截**：业务线程同步执行
- **undo_log 生成**：业务线程同步生成
- **TC 通信**：Netty 异步通信，同步等待响应

### 回滚线程模型
- **回滚触发**：TC 线程触发
- **回滚执行**：RM 线程执行
- **undo_log 解析**：回滚线程同步解析

### TC 交互线程模型
- **请求发送**：业务线程发送，同步等待
- **请求处理**：TC 线程处理，异步响应
- **状态管理**：使用 `ConcurrentHashMap`，线程安全

---

## 📚 源码追踪（深入版）

### 案例1：AT 模式一阶段（完整流程）

**完整调用链：**
```
@GlobalTransactional 方法调用
  -> GlobalTransactionScanner.wrapIfNecessary()
    -> 创建代理对象
      -> Proxy.newProxyInstance()
        -> GlobalTransactionalInterceptor.invoke() (L89)
          -> GlobalTransaction.begin() (L124)
            -> DefaultGlobalTransaction.begin()
              -> 生成 XID
                -> UUID.randomUUID().toString()
              -> TM 向 TC 注册全局事务
                -> TmNettyRemotingClient.sendSyncRequest()
                  -> TC 创建全局会话
                    -> DefaultCoordinator.begin()
                      -> GlobalSession.addSession()
          -> 执行业务 SQL
            -> DataSourceProxy.getConnection() (L89)
              -> 创建连接代理
                -> new ConnectionProxy(targetConnection, xid)
            -> ConnectionProxy.execute() (L124)
              -> ExecuteTemplate.execute()
                -> AbstractDMLBaseExecutor.execute()
                  -> 执行 SQL
                    -> targetConnection.prepareStatement(sql)
                    -> statement.executeUpdate()
                  -> 生成 undo_log
                    -> UndoLogManager.insertUndoLog()
                      -> 构建前后镜像
                        -> buildBeforeImage()
                        -> buildAfterImage()
                      -> 序列化 undo_log
                        -> undoLogParser.encode()
                      -> 插入数据库
                        -> insertUndoLog()
          -> 提交事务
            -> connection.commit()
              -> 删除 undo_log
                -> UndoLogManager.deleteUndoLog()
```

**undo_log 生成详细机制：**
```java
// UndoLogManager.insertUndoLog()
public void insertUndoLog(String xid, long branchId, String rollbackCtx, byte[] undoLogContent) {
    // 1. 构建 undo_log
    UndoLog undoLog = new UndoLog();
    undoLog.setBranchId(branchId);
    undoLog.setXid(xid);
    undoLog.setContext(rollbackCtx);
    undoLog.setRollbackInfo(undoLogContent);
    undoLog.setLogStatus(UndoLogStatus.NORMAL);
    undoLog.setLogCreated(new Date());
    undoLog.setLogModified(new Date());
    
    // 2. 插入数据库
    String sql = "INSERT INTO undo_log (branch_id, xid, context, rollback_info, log_status, log_created, log_modified) VALUES (?, ?, ?, ?, ?, ?, ?)";
    PreparedStatement ps = connection.prepareStatement(sql);
    ps.setLong(1, undoLog.getBranchId());
    ps.setString(2, undoLog.getXid());
    ps.setString(3, undoLog.getContext());
    ps.setBytes(4, undoLog.getRollbackInfo());
    ps.setInt(5, undoLog.getLogStatus());
    ps.setDate(6, new java.sql.Date(undoLog.getLogCreated().getTime()));
    ps.setDate(7, new java.sql.Date(undoLog.getLogModified().getTime()));
    ps.executeUpdate();
}
```

**前后镜像构建：**
```java
// AbstractDMLBaseExecutor.buildBeforeImage()
protected TableRecords buildBeforeImage(TableMeta tableMeta, SQLRecognizer sqlRecognizer, ArrayList<List<Object>> paramAppenderList) {
    // 1. 构建查询 SQL
    String selectSQL = buildBeforeImageSQL(tableMeta, sqlRecognizer);
    
    // 2. 执行查询
    TableRecords beforeImage = TableRecords.buildRecords(tableMeta, selectSQL, paramAppenderList);
    
    // 3. 返回前镜像
    return beforeImage;
}

// AbstractDMLBaseExecutor.buildAfterImage()
protected TableRecords buildAfterImage(TableMeta tableMeta, TableRecords beforeImage, SQLRecognizer sqlRecognizer, ArrayList<List<Object>> paramAppenderList) {
    // 1. 构建查询 SQL
    String selectSQL = buildAfterImageSQL(tableMeta, sqlRecognizer, beforeImage);
    
    // 2. 执行查询
    TableRecords afterImage = TableRecords.buildRecords(tableMeta, selectSQL, paramAppenderList);
    
    // 3. 返回后镜像
    return afterImage;
}
```

**关键类：**
- `GlobalTransactionalInterceptor`：全局事务拦截器
- `DataSourceProxy`：数据源代理
- `ConnectionProxy`：连接代理
- `UndoLogManager`：undo_log 管理器

**验证代码：** `scripts/SeataATTrace.java`
**验证数据：** `data/seata-undo_log.sql`

---

### 案例2：undo_log 生成（深入机制）

**undo_log 结构：**
```sql
CREATE TABLE undo_log (
    branch_id BIGINT NOT NULL COMMENT 'branch transaction id',
    xid VARCHAR(128) NOT NULL COMMENT 'global transaction id',
    context VARCHAR(128) NOT NULL COMMENT 'undo_log context,such as serialization',
    rollback_info LONGBLOB NOT NULL COMMENT 'rollback info',
    log_status INT NOT NULL COMMENT '0:normal status,1:defense status',
    log_created DATETIME(6) NOT NULL COMMENT 'create datetime',
    log_modified DATETIME(6) NOT NULL COMMENT 'modify datetime',
    PRIMARY KEY (branch_id),
    UNIQUE KEY ux_undo_log (xid, branch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='AT transaction mode undo table';
```

**rollback_info 序列化：**
```java
// UndoLogParser.encode()
public byte[] encode(BranchUndoLog branchUndoLog) {
    // 1. 序列化分支 undo_log
    String json = JSON.toJSONString(branchUndoLog);
    
    // 2. 压缩（可选）
    byte[] compressed = compress(json.getBytes());
    
    // 3. 返回字节数组
    return compressed;
}

// BranchUndoLog 结构
{
    "xid": "192.168.1.100:8091:1234567890",
    "branchId": 1,
    "sqlUndoLogs": [
        {
            "tableName": "user",
            "sqlType": "UPDATE",
            "beforeImage": {
                "tableName": "user",
                "rows": [
                    {"id": 1, "name": "Alice", "age": 25}
                ]
            },
            "afterImage": {
                "tableName": "user",
                "rows": [
                    {"id": 1, "name": "Bob", "age": 30}
                ]
            }
        }
    ]
}
```

**前后镜像示例：**
```java
// UPDATE user SET name='Bob', age=30 WHERE id=1

// 前镜像（beforeImage）
TableRecords beforeImage = {
    tableName: "user",
    rows: [
        {id: 1, name: "Alice", age: 25}
    ]
}

// 后镜像（afterImage）
TableRecords afterImage = {
    tableName: "user",
    rows: [
        {id: 1, name: "Bob", age: 30}
    ]
}

// 反向 SQL（回滚时生成）
// UPDATE user SET name='Alice', age=25 WHERE id=1
```

---

### 案例3：二阶段回滚（完整流程）

**完整调用链：**
```
TC 发起回滚
  -> DefaultCoordinator.doGlobalRollback() (L124)
    -> 获取全局会话
      -> GlobalSession session = globalSessions.get(xid)
    -> 更新全局状态
      -> session.changeStatus(GlobalStatus.Rollbacking)
    -> 通知 RM 回滚
      -> RmNettyRemotingClient.sendSyncRequest()
        -> RM 接收回滚请求
          -> DefaultRMHandler.handle()
            -> UndoLogManager.undo() (L124)
              -> 查询 undo_log
                -> selectUndoLog(xid, branchId)
              -> 解析 undo_log
                -> AbstractUndoLogParser.decode()
                  -> 反序列化 rollback_info
                    -> JSON.parseObject(rollbackInfo, BranchUndoLog.class)
              -> 生成反向 SQL
                -> SQLUndoLog.getUndoSQL()
                  -> 根据前后镜像生成 SQL
                    -> buildUndoSQL(beforeImage, afterImage)
              -> 执行回滚 SQL
                -> connection.prepareStatement(undoSQL)
                -> statement.executeUpdate()
              -> 删除 undo_log
                -> deleteUndoLog(xid, branchId)
    -> 更新全局状态
      -> session.changeStatus(GlobalStatus.Rollbacked)
```

**反向 SQL 生成机制：**
```java
// SQLUndoLog.getUndoSQL()
public String getUndoSQL() {
    if (sqlType == SQLType.UPDATE) {
        // UPDATE -> UPDATE（反向更新）
        return buildUpdateSQL(beforeImage, afterImage);
    } else if (sqlType == SQLType.INSERT) {
        // INSERT -> DELETE（反向删除）
        return buildDeleteSQL(afterImage);
    } else if (sqlType == SQLType.DELETE) {
        // DELETE -> INSERT（反向插入）
        return buildInsertSQL(beforeImage);
    }
    return null;
}

// buildUpdateSQL()
private String buildUpdateSQL(TableRecords beforeImage, TableRecords afterImage) {
    // 1. 构建 UPDATE SQL
    StringBuilder sql = new StringBuilder("UPDATE ");
    sql.append(beforeImage.getTableName());
    sql.append(" SET ");
    
    // 2. 设置字段（使用前镜像的值）
    List<Field> fields = beforeImage.getFields();
    for (int i = 0; i < fields.size(); i++) {
        if (i > 0) sql.append(", ");
        sql.append(fields.get(i).getName()).append("=?");
    }
    
    // 3. 设置 WHERE 条件（使用主键）
    sql.append(" WHERE ");
    List<Field> primaryKeys = beforeImage.getPrimaryKeys();
    for (int i = 0; i < primaryKeys.size(); i++) {
        if (i > 0) sql.append(" AND ");
        sql.append(primaryKeys.get(i).getName()).append("=?");
    }
    
    return sql.toString();
}
```

**全局锁机制：**
```java
// LockManager.acquireLock()
public boolean acquireLock(BranchSession branchSession) {
    // 1. 获取锁键
    String lockKey = branchSession.getLockKey();
    
    // 2. 检查锁冲突
    if (isLockConflict(lockKey, branchSession.getXid())) {
        return false;
    }
    
    // 3. 获取锁
    lockManager.addLock(lockKey, branchSession.getXid());
    
    return true;
}

// isLockConflict()
private boolean isLockConflict(String lockKey, String xid) {
    // 1. 查询锁记录
    Lock lock = lockManager.getLock(lockKey);
    
    // 2. 检查是否被其他事务锁定
    if (lock != null && !lock.getXid().equals(xid)) {
        return true;
    }
    
    return false;
}
```

---

## 🧪 基于源码扩展实验

### 实验1：自定义 UndoLogParser（自定义序列化）

**目标**：实现自定义 undo_log 序列化方式。

**实现：**
```java
@Component
public class CustomUndoLogParser implements UndoLogParser {
    @Override
    public String getName() {
        return "custom";
    }
    
    @Override
    public byte[] encode(BranchUndoLog branchUndoLog) {
        // 自定义序列化（如：使用 Protobuf）
        return ProtobufUtil.serialize(branchUndoLog);
    }
    
    @Override
    public BranchUndoLog decode(byte[] bytes) {
        // 自定义反序列化
        return ProtobufUtil.deserialize(bytes, BranchUndoLog.class);
    }
}

// 配置使用
@Configuration
public class SeataConfig {
    @Bean
    public UndoLogParser undoLogParser() {
        return new CustomUndoLogParser();
    }
}
```

**验证**：执行事务，检查 undo_log 序列化格式。

---

### 实验2：自定义 LockManager（自定义锁管理）

**目标**：实现自定义锁管理器，使用 Redis 存储锁。

**实现：**
```java
@Component
public class RedisLockManager implements LockManager {
    @Autowired
    private RedisTemplate<String, String> redisTemplate;
    
    @Override
    public boolean acquireLock(BranchSession branchSession) {
        String lockKey = branchSession.getLockKey();
        String xid = branchSession.getXid();
        
        // 使用 Redis SETNX 获取锁
        Boolean success = redisTemplate.opsForValue().setIfAbsent(lockKey, xid, 30, TimeUnit.SECONDS);
        return Boolean.TRUE.equals(success);
    }
    
    @Override
    public boolean releaseLock(BranchSession branchSession) {
        String lockKey = branchSession.getLockKey();
        String xid = branchSession.getXid();
        
        // 释放锁（只有锁的持有者才能释放）
        String value = redisTemplate.opsForValue().get(lockKey);
        if (xid.equals(value)) {
            redisTemplate.delete(lockKey);
            return true;
        }
        return false;
    }
}
```

**验证**：执行并发事务，检查锁机制是否生效。

---

### 实验3：自定义 ResourceManager（自定义资源管理）

**目标**：扩展资源管理器，支持更多数据源类型。

**实现：**
```java
@Component
public class CustomResourceManager extends AbstractResourceManager {
    @Override
    public void registerResource(Resource resource) {
        // 注册资源
        resourceManagerMap.put(resource.getResourceId(), resource);
    }
    
    @Override
    public void unregisterResource(Resource resource) {
        // 注销资源
        resourceManagerMap.remove(resource.getResourceId());
    }
    
    @Override
    public BranchStatus branchCommit(BranchType branchType, String xid, long branchId, String resourceId, String applicationData) {
        // 分支提交
        return BranchStatus.PhaseTwo_Committed;
    }
    
    @Override
    public BranchStatus branchRollback(BranchType branchType, String xid, long branchId, String resourceId, String applicationData) {
        // 分支回滚
        return BranchStatus.PhaseTwo_Rollbacked;
    }
}
```

**验证**：注册自定义资源，观察资源管理是否生效。

---

## 🐛 常见坑与排查

### 坑1：undo_log 表不存在
**现象**：事务执行失败，提示 undo_log 表不存在
**原因**：未创建 undo_log 表
**排查**：
1. 检查数据库是否有 undo_log 表
2. 执行建表 SQL：`data/seata-undo_log.sql`
3. 检查数据源配置

### 坑2：全局锁冲突
**现象**：事务执行失败，提示全局锁冲突
**原因**：多个事务同时修改同一行数据
**排查**：
1. 检查是否有并发事务
2. 检查锁键是否冲突
3. 检查全局锁配置

### 坑3：回滚失败
**现象**：回滚时失败，数据不一致
**原因**：
1. undo_log 数据损坏
2. 反向 SQL 生成错误
3. 数据库约束冲突
**排查**：
1. 检查 undo_log 数据
2. 检查反向 SQL 生成逻辑
3. 检查数据库约束

---

## 验证数据

### 事务日志

```
[INFO] Global transaction begin: xid=192.168.1.100:8091:1234567890
[INFO] Branch transaction register: branchId=1, xid=192.168.1.100:8091:1234567890
[INFO] Undo log inserted: branchId=1, xid=192.168.1.100:8091:1234567890
[INFO] Before image: {id=1, name=Alice, age=25}
[INFO] After image: {id=1, name=Bob, age=30}
[INFO] Global transaction commit: xid=192.168.1.100:8091:1234567890
```

### 回滚日志

```
[INFO] Global transaction rollback: xid=192.168.1.100:8091:1234567890
[INFO] Undo log found: branchId=1, xid=192.168.1.100:8091:1234567890
[INFO] Rollback SQL generated: UPDATE user SET name=?, age=? WHERE id=?
[INFO] Rollback parameters: [Alice, 25, 1]
[INFO] Rollback executed successfully
[INFO] Undo log deleted: branchId=1, xid=192.168.1.100:8091:1234567890
```

### 全局锁日志

```
[DEBUG] Acquiring lock: lockKey=user:1, xid=192.168.1.100:8091:1234567890
[DEBUG] Lock acquired: lockKey=user:1
[DEBUG] Lock conflict detected: lockKey=user:1, existingXid=192.168.1.100:8091:1234567891
[WARN] Global lock conflict: lockKey=user:1
```

---

## 总结

1. **AT 核心**
   - 一阶段提交业务 SQL（正常提交）
   - 生成 undo_log 记录前后镜像（回滚数据）
   - 二阶段回滚使用 undo_log（反向 SQL）

2. **事务核心**
   - TM 开启全局事务（生成 XID）
   - RM 注册分支事务（注册到 TC）
   - TC 协调提交/回滚（两阶段提交）

3. **一致性核心**
   - 全局锁保证隔离（防止脏读）
   - undo_log 保证回滚（前后镜像）
   - 幂等性保证重试（XID 唯一）

4. **扩展点**
   - `UndoLogParser`：自定义序列化
   - `LockManager`：自定义锁管理
   - `ResourceManager`：自定义资源管理
