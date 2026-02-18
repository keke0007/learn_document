# MyBatis 源码学习案例（深入版）

## 案例概述

本案例深入 MyBatis Mapper 动态代理、SQL 执行链、插件机制等核心源码。**重点：断点位置、数据结构、执行链机制、插件拦截原理、基于源码的扩展实验。**

---

## 📍 断点清单（建议按顺序打断点）

### Mapper 代理断点
1. **`SqlSession.getMapper(Class<T> type)`** (L56) - Mapper 获取入口
2. **`MapperRegistry.getMapper()`** (L54) - Mapper 注册表获取
3. **`MapperProxyFactory.newInstance()`** (L25) - 代理工厂创建
4. **`MapperProxy.invoke()`** (L59) - 代理方法调用
5. **`MapperMethod.execute()`** (L115) - Mapper 方法执行

### SQL 执行链断点
1. **`Executor.query()`** (L82) - 执行器查询入口
2. **`CachingExecutor.query()`** (L60) - 二级缓存查询
3. **`BaseExecutor.queryFromDatabase()`** (L320) - 数据库查询
4. **`PreparedStatementHandler.query()`** (L87) - 预处理语句查询
5. **`DefaultResultSetHandler.handleResultSets()`** (L152) - 结果集处理

### 插件机制断点
1. **`InterceptorChain.pluginAll()`** (L33) - 插件链包装
2. **`Plugin.wrap()`** (L60) - 插件包装
3. **`Plugin.invoke()`** (L95) - 插件拦截执行

---

## 🔍 关键数据结构

### Mapper 代理核心数据结构

```java
// MapperRegistry.java
// 1. Mapper 代理工厂映射
private final Map<Class<?>, MapperProxyFactory<?>> knownMappers = new HashMap<>();

// MapperProxyFactory.java
// 2. Mapper 接口
private final Class<T> mapperInterface;

// 3. 方法缓存
private final Map<Method, MapperMethod> methodCache = new ConcurrentHashMap<>();

// MapperProxy.java
// 4. SqlSession（线程安全）
private final SqlSession sqlSession;

// 5. Mapper 接口
private final Class<T> mapperInterface;

// 6. 方法缓存
private final Map<Method, MapperMethod> methodCache;
```

### SQL 执行链核心数据结构

```java
// Configuration.java
// 1. MappedStatement 映射（SQL 语句元数据）
protected final Map<String, MappedStatement> mappedStatements = new StrictMap<>("Mapped Statements collection");

// 2. Executor 类型
protected ExecutorType defaultExecutorType = ExecutorType.SIMPLE;

// BaseExecutor.java
// 3. 一级缓存（PerpetualCache）
protected PerpetualCache localCache;

// 4. 本地输出参数缓存
protected PerpetualCache localOutputParameterCache;

// CachingExecutor.java
// 5. 二级缓存（TransactionalCacheManager）
private final TransactionalCacheManager tcm = new TransactionalCacheManager();
```

### 插件机制核心数据结构

```java
// InterceptorChain.java
// 1. 拦截器列表（有序）
private final List<Interceptor> interceptors = new ArrayList<>();

// Plugin.java
// 2. 目标对象
private final Object target;

// 3. 拦截器
private final Interceptor interceptor;

// 4. 拦截方法映射
private final Map<Class<?>, Set<Method>> signatureMap;

// 5. 拦截方法缓存
private final Class<?>[] interfaces;
```

---

## 🧵 线程模型

### Mapper 代理线程模型
- **代理创建**：单例模式，线程安全
- **方法调用**：多线程并发调用，`SqlSession` 线程安全
- **方法缓存**：使用 `ConcurrentHashMap`，线程安全

### SQL 执行线程模型
- **Executor**：每个 `SqlSession` 一个 `Executor`，线程隔离
- **一级缓存**：`SqlSession` 级别，线程隔离
- **二级缓存**：`Mapper` 级别，多线程共享，需要事务管理

### 插件线程模型
- **插件包装**：启动时单线程包装
- **插件执行**：多线程并发执行，需要线程安全

---

## 📚 源码追踪（深入版）

### 案例1：Mapper 动态代理（完整机制）

**完整调用链：**
```
SqlSession.getMapper(Class<T> type) (L56)
  -> MapperRegistry.getMapper() (L54)
    -> MapperProxyFactory.newInstance() (L25)
      -> Proxy.newProxyInstance()
        -> MapperProxy.invoke() (L59)
          -> 缓存检查
            -> methodCache.get(method)
          -> MapperMethod.execute() (L115)
            -> 判断命令类型
              ├─ SELECT -> sqlSession.selectOne/selectList()
              ├─ INSERT -> sqlSession.insert()
              ├─ UPDATE -> sqlSession.update()
              └─ DELETE -> sqlSession.delete()
```

**MapperMethod 详细机制：**
```java
// MapperMethod.execute()
public Object execute(SqlSession sqlSession, Object[] args) {
    Object result;
    switch (command.getType()) {
        case INSERT: {
            Object param = method.convertArgsToSqlCommandParam(args);
            result = rowCountResult(sqlSession.insert(command.getName(), param));
            break;
        }
        case UPDATE: {
            Object param = method.convertArgsToSqlCommandParam(args);
            result = rowCountResult(sqlSession.update(command.getName(), param));
            break;
        }
        case DELETE: {
            Object param = method.convertArgsToSqlCommandParam(args);
            result = rowCountResult(sqlSession.delete(command.getName(), param));
            break;
        }
        case SELECT:
            if (method.returnsVoid() && method.hasResultHandler()) {
                executeWithHandler(sqlSession, args);
                result = null;
            } else if (method.returnsMany()) {
                result = executeForMany(sqlSession, args);
            } else if (method.returnsMap()) {
                result = executeForMap(sqlSession, args);
            } else if (method.returnsCursor()) {
                result = executeForCursor(sqlSession, args);
            } else {
                Object param = method.convertArgsToSqlCommandParam(args);
                result = sqlSession.selectOne(command.getName(), param);
            }
            break;
        default:
            throw new BindingException("Unknown execution method for: " + command.getName());
    }
    return result;
}
```

**关键类：**
- `MapperProxy`：代理类
- `MapperMethod`：方法封装
- `SqlCommand`：SQL 命令类型
- `MethodSignature`：方法签名

**验证代码：** `scripts/MyBatisMapperProxyTrace.java`

---

### 案例2：SQL 执行链（完整流程）

**完整执行流程：**
```
Executor.query() (L82)
  -> CachingExecutor.query() (L60)  // 二级缓存
    -> 检查二级缓存
      -> tcm.getObject(cache, key)
    -> BaseExecutor.query() (L145)
      -> 检查一级缓存
        -> localCache.getObject(key)
      -> queryFromDatabase() (L320)
        -> SimpleExecutor.doQuery() (L63)
          -> prepareStatement() (L87)
            -> StatementHandler.prepare() (L87)
              -> connection.prepareStatement(sql)
            -> StatementHandler.parameterize() (L87)
              -> ParameterHandler.setParameters()
            -> StatementHandler.query() (L87)
              -> statement.execute()
              -> ResultSetHandler.handleResultSets() (L152)
                -> 结果集映射
                  -> createResultObject()
                  -> applyPropertyMappings()
        -> 放入一级缓存
          -> localCache.putObject(key, value)
    -> 放入二级缓存
      -> tcm.putObject(cache, key, value)
```

**Executor 类型：**
- **SimpleExecutor**：简单执行器，每次执行都创建新的 Statement
- **ReuseExecutor**：重用执行器，重用 Statement
- **BatchExecutor**：批量执行器，批量执行 SQL
- **CachingExecutor**：缓存执行器，二级缓存装饰器

**StatementHandler 类型：**
- **SimpleStatementHandler**：简单语句处理器
- **PreparedStatementHandler**：预处理语句处理器（常用）
- **CallableStatementHandler**：存储过程语句处理器

**ResultSetHandler 机制：**
```java
// DefaultResultSetHandler.handleResultSets()
public List<Object> handleResultSets(Statement stmt) throws SQLException {
    // 1. 获取结果集
    ResultSet rs = stmt.getResultSet();
    
    // 2. 获取结果映射
    List<ResultMap> resultMaps = mappedStatement.getResultMaps();
    
    // 3. 处理结果集
    List<Object> multipleResults = new ArrayList<>();
    int resultSetCount = 0;
    ResultSetWrapper rsw = new ResultSetWrapper(rs, configuration);
    
    while (rsw != null && resultMaps.size() > resultSetCount) {
        ResultMap resultMap = resultMaps.get(resultSetCount);
        handleResultSet(rsw, resultMap, multipleResults, null);
        rsw = getNextResultSet(stmt);
        resultSetCount++;
    }
    
    return collapseSingleResultList(multipleResults);
}
```

**关键类：**
- `Executor`：执行器接口
- `SimpleExecutor`：简单执行器
- `PreparedStatementHandler`：预处理语句处理器
- `DefaultResultSetHandler`：结果集处理器

---

### 案例3：插件机制（深入拦截原理）

**插件包装流程：**
```
InterceptorChain.pluginAll() (L33)
  -> 遍历所有拦截器
    -> Plugin.wrap() (L60)
      -> 获取拦截方法
        -> getSignatureMap(interceptor)
      -> 创建代理对象
        -> Proxy.newProxyInstance()
          -> Plugin.invoke() (L95)
            -> 检查是否需要拦截
              -> signatureMap.get(target.getClass())
            -> 拦截方法
              -> interceptor.intercept()
            -> 非拦截方法
              -> method.invoke(target, args)
```

**Plugin.wrap() 详细机制：**
```java
// Plugin.wrap()
public static Object wrap(Object target, Interceptor interceptor) {
    // 1. 获取拦截方法映射
    Map<Class<?>, Set<Method>> signatureMap = getSignatureMap(interceptor);
    
    // 2. 获取目标类实现的接口
    Class<?> type = target.getClass();
    Class<?>[] interfaces = getAllInterfaces(type, signatureMap);
    
    // 3. 如果没有需要拦截的接口，直接返回目标对象
    if (interfaces.length > 0) {
        return Proxy.newProxyInstance(
            type.getClassLoader(),
            interfaces,
            new Plugin(target, interceptor, signatureMap)
        );
    }
    return target;
}

// Plugin.invoke()
public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
    try {
        // 1. 获取拦截方法集合
        Set<Method> methods = signatureMap.get(method.getDeclaringClass());
        
        // 2. 检查是否需要拦截
        if (methods != null && methods.contains(method)) {
            // 3. 执行拦截器
            return interceptor.intercept(new Invocation(target, method, args));
        }
        
        // 4. 非拦截方法，直接调用
        return method.invoke(target, args);
    } catch (Exception e) {
        throw ExceptionUtil.unwrapThrowable(e);
    }
}
```

**插件实现示例：**
```java
@Intercepts({
    @Signature(type = Executor.class, method = "query", args = {MappedStatement.class, Object.class, RowBounds.class, ResultHandler.class})
})
public class MyPlugin implements Interceptor {
    @Override
    public Object intercept(Invocation invocation) throws Throwable {
        // 前置处理
        System.out.println("Before query");
        
        // 执行目标方法
        Object result = invocation.proceed();
        
        // 后置处理
        System.out.println("After query");
        
        return result;
    }
    
    @Override
    public Object plugin(Object target) {
        return Plugin.wrap(target, this);
    }
    
    @Override
    public void setProperties(Properties properties) {
        // 设置插件属性
    }
}
```

**插件执行顺序：**
- 插件按配置顺序包装（后配置的在外层）
- 执行顺序：外层 -> 内层 -> 目标对象
- 返回顺序：目标对象 -> 内层 -> 外层

**验证数据：**
```xml
<plugins>
    <plugin interceptor="com.example.MyPlugin">
        <property name="property1" value="value1"/>
    </plugin>
</plugins>
```

---

## 🧪 基于源码扩展实验

### 实验1：自定义 Interceptor（SQL 执行时间统计）

**目标**：统计所有 SQL 执行时间。

**实现：**
```java
@Intercepts({
    @Signature(type = Executor.class, method = "query", args = {MappedStatement.class, Object.class, RowBounds.class, ResultHandler.class}),
    @Signature(type = Executor.class, method = "update", args = {MappedStatement.class, Object.class})
})
public class PerformanceInterceptor implements Interceptor {
    @Override
    public Object intercept(Invocation invocation) throws Throwable {
        long start = System.currentTimeMillis();
        try {
            return invocation.proceed();
        } finally {
            long duration = System.currentTimeMillis() - start;
            MappedStatement ms = (MappedStatement) invocation.getArgs()[0];
            System.out.println("SQL: " + ms.getId() + " executed in " + duration + "ms");
        }
    }
    
    @Override
    public Object plugin(Object target) {
        return Plugin.wrap(target, this);
    }
}
```

**验证**：执行 SQL，观察执行时间日志。

---

### 实验2：自定义 TypeHandler（自定义类型转换）

**目标**：实现自定义类型的数据库映射。

**实现：**
```java
// 自定义类型
public class Status {
    private String value;
    // getters/setters
}

// 自定义 TypeHandler
@MappedTypes(Status.class)
@MappedJdbcTypes(JdbcType.VARCHAR)
public class StatusTypeHandler extends BaseTypeHandler<Status> {
    @Override
    public void setNonNullParameter(PreparedStatement ps, int i, Status parameter, JdbcType jdbcType) throws SQLException {
        ps.setString(i, parameter.getValue());
    }
    
    @Override
    public Status getNullableResult(ResultSet rs, String columnName) throws SQLException {
        String value = rs.getString(columnName);
        return value == null ? null : new Status(value);
    }
    
    @Override
    public Status getNullableResult(ResultSet rs, int columnIndex) throws SQLException {
        String value = rs.getString(columnIndex);
        return value == null ? null : new Status(value);
    }
    
    @Override
    public Status getNullableResult(CallableStatement cs, int columnIndex) throws SQLException {
        String value = cs.getString(columnIndex);
        return value == null ? null : new Status(value);
    }
}
```

**验证**：在 Mapper 中使用 Status 类型，观察类型转换。

---

### 实验3：自定义 ResultHandler（结果集处理）

**目标**：自定义结果集处理逻辑。

**实现：**
```java
// 自定义 ResultHandler
public class CustomResultHandler implements ResultHandler<Object> {
    private final List<Object> results = new ArrayList<>();
    
    @Override
    public void handleResult(ResultContext<? extends Object> resultContext) {
        Object resultObject = resultContext.getResultObject();
        // 自定义处理逻辑
        if (resultObject instanceof User) {
            User user = (User) resultObject;
            user.setProcessed(true);
        }
        results.add(resultObject);
    }
    
    public List<Object> getResults() {
        return results;
    }
}

// 使用 ResultHandler
public void selectUsers(ResultHandler<User> handler) {
    sqlSession.select("selectUsers", null, handler);
}
```

**验证**：使用自定义 ResultHandler 查询数据，观察处理结果。

---

## 🐛 常见坑与排查

### 坑1：一级缓存导致数据不一致
**现象**：同一 SqlSession 中查询结果不一致
**原因**：一级缓存未清除
**排查**：
1. 检查是否有更新操作未提交
2. 检查是否需要清除缓存：`sqlSession.clearCache()`
3. 检查是否使用了不同的 SqlSession

### 坑2：二级缓存导致数据不一致
**现象**：不同 SqlSession 查询结果不一致
**原因**：二级缓存未更新
**排查**：
1. 检查更新操作是否提交事务
2. 检查 Mapper 是否启用二级缓存：`<cache/>`
3. 检查缓存配置是否正确

### 坑3：插件拦截失效
**现象**：插件不执行
**原因**：
1. 拦截方法签名不匹配
2. 目标对象未被代理
3. 插件配置错误
**排查**：
1. 检查 `@Signature` 注解配置
2. 检查目标对象类型
3. 检查插件配置

---

## 验证数据

### Mapper 调用日志

```
[DEBUG] ==>  Preparing: SELECT * FROM user WHERE id = ?
[DEBUG] ==> Parameters: 1(Integer)
[DEBUG] <==      Total: 1
[DEBUG] Mapper method 'com.example.UserMapper.selectById' executed
```

### 插件拦截日志

```
[DEBUG] Plugin intercepting: Executor.query
[DEBUG] Before intercept: MappedStatement=selectUser
[DEBUG] After intercept: Result=User{id=1, name='Alice'}
```

### 执行链日志

```
[DEBUG] Executor.query: MappedStatement=selectUser
[DEBUG] Cache hit: key=selectUser:1
[DEBUG] Statement prepared: SELECT * FROM user WHERE id = ?
[DEBUG] Parameters set: 1
[DEBUG] ResultSet handled: 1 row
```

---

## 总结

1. **Mapper 核心**
   - 动态代理实现接口调用（`MapperProxy`）
   - MapperMethod 封装方法信息（SQL、参数、返回类型）
   - SqlSession 执行 SQL（线程安全）

2. **执行链核心**
   - Executor 负责执行（Simple/Reuse/Batch）
   - StatementHandler 负责语句（PreparedStatement）
   - ResultSetHandler 负责结果映射（反射 + 类型转换）

3. **插件核心**
   - Interceptor 接口定义（intercept/plugin/setProperties）
   - Plugin.wrap 创建代理（JDK 动态代理）
   - 责任链模式串联（多层代理）

4. **扩展点**
   - `Interceptor`：SQL 拦截
   - `TypeHandler`：类型转换
   - `ResultHandler`：结果处理
   - `KeyGenerator`：主键生成
