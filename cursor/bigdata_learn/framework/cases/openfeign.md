# OpenFeign 源码学习案例（深入版）

## 案例概述

本案例深入 OpenFeign 接口代理生成、请求构建、调用链等核心源码。**重点：断点位置、数据结构、负载均衡集成、超时重试机制、基于源码的扩展实验。**

---

## 📍 断点清单（建议按顺序打断点）

### 代理生成断点
1. **`FeignClientFactoryBean.getObject()`** (L124) - Feign 客户端创建入口
2. **`Feign.Builder.build()`** (L89) - Feign 构建
3. **`ReflectiveFeign.newInstance()`** (L124) - 反射 Feign 创建
4. **`SynchronousMethodHandler.invoke()`** (L89) - 同步方法处理

### 请求构建断点
1. **`RequestTemplate.create()`** (L89) - 请求模板创建
2. **`Contract.parseAndValidateMetadata()`** (L124) - 契约解析
3. **`RequestInterceptor.apply()`** (L45) - 请求拦截器应用
4. **`Encoder.encode()`** (L89) - 请求编码

### 调用链断点
1. **`LoadBalancerFeignClient.execute()`** (L124) - 负载均衡执行
2. **`RibbonLoadBalancerClient.execute()`** (L89) - Ribbon 负载均衡
3. **`Retryer.continueOrPropagate()`** (L45) - 重试判断

---

## 🔍 关键数据结构

### 代理生成核心数据结构

```java
// FeignClientFactoryBean.java
// 1. Feign 客户端配置
private Class<?> type;
private String name;
private String url;
private String path;
private boolean decode404;
private ApplicationContext applicationContext;

// ReflectiveFeign.java
// 2. 方法处理器映射
private final Map<Method, MethodHandler> methodToHandler;

// 3. 目标类型
private final Target<T> target;

// SynchronousMethodHandler.java
// 4. 请求模板工厂
private final RequestTemplate.Factory buildTemplateFromArgs;

// 5. 请求拦截器列表
private final List<RequestInterceptor> requestInterceptors;
```

### 请求构建核心数据结构

```java
// RequestTemplate.java
// 1. 请求方法
private String method;

// 2. 请求 URL
private StringBuilder url = new StringBuilder();

// 3. 请求头映射
private Map<String, Collection<String>> headers = new LinkedHashMap<>();

// 4. 查询参数映射
private Map<String, Collection<String>> queries = new LinkedHashMap<>();

// 5. 请求体
private byte[] body;

// Contract.java
// 6. 方法元数据映射
private final Map<Method, MethodMetadata> methodMetadataCache = new ConcurrentHashMap<>();
```

### 调用链核心数据结构

```java
// LoadBalancerFeignClient.java
// 1. 负载均衡客户端
private final LoadBalancerClient loadBalancerClient;

// 2. Feign 客户端
private final Client delegate;

// Retryer.java
// 3. 重试配置
private final int maxAttempts;
private final long period;
private final long maxPeriod;
private int attempt;
```

---

## 🧵 线程模型

### 代理生成线程模型
- **代理创建**：启动时单线程创建，线程安全
- **方法调用**：多线程并发调用，线程安全
- **方法缓存**：使用 `ConcurrentHashMap`，线程安全

### 请求构建线程模型
- **请求模板**：每次调用创建新模板，线程隔离
- **请求拦截器**：同步执行，线程安全
- **编码解码**：同步执行，线程安全

### 调用链线程模型
- **负载均衡**：同步选择实例，线程安全
- **HTTP 请求**：异步执行（如果配置），支持超时
- **重试机制**：同步重试，线程安全

---

## 📚 源码追踪（深入版）

### 案例1：代理生成（完整流程）

**完整调用链：**
```
@FeignClient 接口扫描
  -> FeignClientFactoryBean.getObject() (L124)
    -> Feign.Builder.build() (L89)
      -> ReflectiveFeign.newInstance() (L124)
        -> 创建方法处理器映射
          -> parseAndValidateMetadata()
            -> Contract.parseAndValidateMetadata()
              -> SpringMvcContract.processAnnotationOnMethod()
                -> 解析 @RequestMapping/@GetMapping 等
        -> 创建动态代理
          -> Proxy.newProxyInstance()
            -> InvocationHandler.invoke()
              -> SynchronousMethodHandler.invoke() (L89)
                -> 构建请求模板
                  -> buildTemplateFromArgs.create()
                -> 应用请求拦截器
                  -> requestInterceptors.forEach(interceptor -> interceptor.apply(template))
                -> 编码请求
                  -> encoder.encode(request, bodyType)
                -> 执行请求
                  -> client.execute(request, options)
```

**Feign.Builder 配置：**
```java
// Feign.Builder.build()
public Feign build() {
    // 1. 设置编码器
    Encoder encoder = this.encoder != null ? this.encoder : new Encoder.Default();
    
    // 2. 设置解码器
    Decoder decoder = this.decoder != null ? this.decoder : new Decoder.Default();
    
    // 3. 设置契约
    Contract contract = this.contract != null ? this.contract : new Contract.Default();
    
    // 4. 设置请求拦截器
    List<RequestInterceptor> requestInterceptors = new ArrayList<>(this.requestInterceptors);
    
    // 5. 设置重试器
    Retryer retryer = this.retryer != null ? this.retryer : Retryer.NEVER_RETRY;
    
    // 6. 设置日志级别
    Logger logger = this.logger != null ? this.logger : new NoOpLogger();
    
    // 7. 创建 Feign 实例
    return new ReflectiveFeign(contract, methodToHandler, invocationHandlerFactory, decoder, encoder, errorDecoder, logger, retryer, requestInterceptors);
}
```

**关键类：**
- `FeignClientFactoryBean`：Feign 客户端工厂 Bean
- `ReflectiveFeign`：反射 Feign
- `SynchronousMethodHandler`：同步方法处理器

**验证代码：** `scripts/OpenFeignTrace.java`

---

### 案例2：请求构建（详细机制）

**请求模板构建流程：**
```
RequestTemplate.create() (L89)
  -> Contract.parseAndValidateMetadata()
    -> SpringMvcContract.processAnnotationOnMethod()
      -> 解析方法注解
        -> @RequestMapping -> 解析路径、方法、请求头等
        -> @GetMapping -> 解析 GET 请求
        -> @PostMapping -> 解析 POST 请求
        -> @RequestParam -> 解析查询参数
        -> @PathVariable -> 解析路径参数
        -> @RequestBody -> 解析请求体
  -> 构建请求模板
    -> 设置请求方法
    -> 设置请求 URL
    -> 设置请求头
    -> 设置查询参数
    -> 设置请求体
```

**SpringMvcContract 解析机制：**
```java
// SpringMvcContract.processAnnotationOnMethod()
protected void processAnnotationOnMethod(MethodMetadata data, Annotation methodAnnotation, Method method) {
    if (methodAnnotation instanceof RequestMapping) {
        RequestMapping requestMapping = (RequestMapping) methodAnnotation;
        // 解析路径
        String[] paths = requestMapping.value();
        if (paths.length > 0) {
            data.template().uri(paths[0]);
        }
        // 解析方法
        RequestMethod[] methods = requestMapping.method();
        if (methods.length > 0) {
            data.template().method(RequestMethod.toHttpMethod(methods[0].name()));
        }
        // 解析请求头
        String[] headers = requestMapping.headers();
        // ... 解析其他属性
    } else if (methodAnnotation instanceof GetMapping) {
        // 解析 GET 请求
    } else if (methodAnnotation instanceof PostMapping) {
        // 解析 POST 请求
    }
    // ... 解析其他注解
}
```

**请求拦截器应用：**
```java
// SynchronousMethodHandler.invoke()
Request targetRequest(RequestTemplate template) {
    // 1. 应用请求拦截器
    for (RequestInterceptor interceptor : requestInterceptors) {
        interceptor.apply(template);
    }
    
    // 2. 构建请求
    return target.apply(template);
}
```

**编码机制：**
```java
// Encoder.encode()
void encode(Object object, Type bodyType, RequestTemplate template) {
    if (bodyType == String.class) {
        template.body(object.toString());
    } else if (bodyType == byte[].class) {
        template.body((byte[]) object);
    } else {
        // 使用 Jackson 序列化
        ObjectMapper mapper = new ObjectMapper();
        template.body(mapper.writeValueAsBytes(object));
    }
}
```

**关键类：**
- `Contract`：契约接口
- `SpringMvcContract`：Spring MVC 契约实现
- `RequestInterceptor`：请求拦截器
- `Encoder/Decoder`：编解码器

---

### 案例3：调用链（负载均衡与重试）

**完整调用流程：**
```
SynchronousMethodHandler.invoke() (L89)
  -> 构建请求
    -> targetRequest(template)
  -> 执行请求
    -> client.execute(request, options)
      -> LoadBalancerFeignClient.execute() (L124)
        -> 解析服务名
          -> URI uri = request.url().toURI();
          -> String serviceId = uri.getHost();
        -> 负载均衡选择实例
          -> ServiceInstance instance = loadBalancerClient.choose(serviceId);
        -> 构建实际请求 URL
          -> String url = "http://" + instance.getHost() + ":" + instance.getPort() + uri.getPath();
        -> 执行 HTTP 请求
          -> delegate.execute(request, options)
            -> 超时控制
              -> options.readTimeout()
            -> 重试机制
              -> retryer.continueOrPropagate(e)
                -> 判断是否重试
                  -> attempt < maxAttempts
                -> 等待后重试
                  -> Thread.sleep(period)
```

**负载均衡集成：**
```java
// LoadBalancerFeignClient.execute()
public Response execute(Request request, Request.Options options) throws IOException {
    // 1. 解析服务名
    URI uri = URI.create(request.url());
    String serviceId = uri.getHost();
    
    // 2. 负载均衡选择实例
    ServiceInstance instance = loadBalancerClient.choose(serviceId);
    if (instance == null) {
        throw new IllegalStateException("No instances available for " + serviceId);
    }
    
    // 3. 构建实际请求 URL
    String url = "http://" + instance.getHost() + ":" + instance.getPort() + uri.getPath();
    Request newRequest = Request.create(request.method(), url, request.headers(), request.body(), request.charset());
    
    // 4. 执行 HTTP 请求
    return delegate.execute(newRequest, options);
}
```

**重试机制：**
```java
// Retryer.continueOrPropagate()
public void continueOrPropagate(RetryableException e) {
    if (attempt++ >= maxAttempts) {
        throw e;
    }
    
    long interval = period;
    if (interval > maxPeriod) {
        interval = maxPeriod;
    }
    
    try {
        Thread.sleep(interval);
    } catch (InterruptedException ignored) {
        Thread.currentThread().interrupt();
        throw e;
    }
}
```

**超时控制：**
```java
// Request.Options
public static class Options {
    private final int connectTimeoutMillis;
    private final int readTimeoutMillis;
    
    public Options(int connectTimeoutMillis, int readTimeoutMillis) {
        this.connectTimeoutMillis = connectTimeoutMillis;
        this.readTimeoutMillis = readTimeoutMillis;
    }
}
```

**集成点：**
- 负载均衡：Ribbon/Spring Cloud LoadBalancer
- 超时：Feign Client 配置
- 重试：Retryer
- 熔断：Sentinel/Resilience4j

---

## 🧪 基于源码扩展实验

### 实验1：自定义 RequestInterceptor（请求头添加）

**目标**：在所有 Feign 请求中添加自定义请求头。

**实现：**
```java
@Component
public class CustomRequestInterceptor implements RequestInterceptor {
    @Override
    public void apply(RequestTemplate template) {
        // 添加自定义请求头
        template.header("X-Custom-Header", "custom-value");
        template.header("X-Request-Id", UUID.randomUUID().toString());
        
        // 添加认证信息
        String token = getToken();
        template.header("Authorization", "Bearer " + token);
    }
    
    private String getToken() {
        // 获取认证 token
        return "token123";
    }
}

// 配置使用
@FeignClient(name = "user-service", configuration = FeignConfig.class)
public interface UserServiceClient {
    @GetMapping("/users/{id}")
    User getUserById(@PathVariable("id") Long id);
}

@Configuration
public class FeignConfig {
    @Bean
    public RequestInterceptor customRequestInterceptor() {
        return new CustomRequestInterceptor();
    }
}
```

**验证**：发送 Feign 请求，检查请求头是否添加。

---

### 实验2：自定义 ErrorDecoder（错误处理）

**目标**：自定义 Feign 错误解码器，处理特定错误码。

**实现：**
```java
@Component
public class CustomErrorDecoder implements ErrorDecoder {
    private final ErrorDecoder defaultErrorDecoder = new Default();
    
    @Override
    public Exception decode(String methodKey, Response response) {
        // 1. 检查状态码
        if (response.status() == 404) {
            return new NotFoundException("Resource not found: " + methodKey);
        }
        
        if (response.status() == 401) {
            return new UnauthorizedException("Unauthorized: " + methodKey);
        }
        
        if (response.status() == 500) {
            return new ServerException("Server error: " + methodKey);
        }
        
        // 2. 使用默认解码器
        return defaultErrorDecoder.decode(methodKey, response);
    }
}

// 配置使用
@Configuration
public class FeignConfig {
    @Bean
    public ErrorDecoder errorDecoder() {
        return new CustomErrorDecoder();
    }
}
```

**验证**：模拟错误响应，观察错误处理。

---

### 实验3：自定义 Retryer（重试策略）

**目标**：自定义重试策略，控制重试次数和间隔。

**实现：**
```java
@Component
public class CustomRetryer implements Retryer {
    private final int maxAttempts;
    private final long period;
    private int attempt;
    
    public CustomRetryer() {
        this.maxAttempts = 3;
        this.period = 1000L;
        this.attempt = 1;
    }
    
    @Override
    public void continueOrPropagate(RetryableException e) {
        if (attempt++ >= maxAttempts) {
            throw e;
        }
        
        try {
            Thread.sleep(period * attempt);  // 递增间隔
        } catch (InterruptedException ignored) {
            Thread.currentThread().interrupt();
            throw e;
        }
    }
    
    @Override
    public Retryer clone() {
        return new CustomRetryer();
    }
}

// 配置使用
@Configuration
public class FeignConfig {
    @Bean
    public Retryer retryer() {
        return new CustomRetryer();
    }
}
```

**验证**：模拟请求失败，观察重试行为。

---

## 🐛 常见坑与排查

### 坑1：Feign 客户端未创建
**现象**：Feign 客户端 Bean 未创建
**原因**：
1. 未启用 Feign：`@EnableFeignClients`
2. 包扫描路径错误
3. 接口未标注 `@FeignClient`
**排查**：
1. 检查 `@EnableFeignClients` 注解
2. 检查包扫描路径
3. 检查 `@FeignClient` 注解

### 坑2：请求超时
**现象**：Feign 请求超时
**原因**：
1. 超时配置过短
2. 服务响应慢
3. 网络问题
**排查**：
1. 检查超时配置：`feign.client.config.default.readTimeout`
2. 检查服务响应时间
3. 检查网络连接

### 坑3：负载均衡不生效
**现象**：请求未负载均衡
**原因**：
1. 未配置负载均衡客户端
2. 服务实例未注册
3. URL 使用 IP 而非服务名
**排查**：
1. 检查负载均衡配置
2. 检查服务注册
3. 检查 Feign URL 配置

---

## 验证数据

### Feign 调用日志

```
[DEBUG] Feign client method: getUserById
[DEBUG] Request URL: http://user-service/api/users/1
[DEBUG] Request headers: {Content-Type=[application/json], X-Custom-Header=[custom-value]}
[DEBUG] Response status: 200
[DEBUG] Response body: {"id":1,"name":"Alice"}
```

### 负载均衡日志

```
[DEBUG] LoadBalancer: Choosing server for user-service
[DEBUG] LoadBalancer: Selected server: 192.168.1.100:8080
[DEBUG] Request forwarded to: http://192.168.1.100:8080/api/users/1
```

### 重试日志

```
[DEBUG] Feign request failed: Connection timeout
[DEBUG] Retrying request (attempt 1/3)
[DEBUG] Retrying request (attempt 2/3)
[DEBUG] Request succeeded after 2 retries
```

---

## 总结

1. **代理核心**
   - FeignClientFactoryBean 创建代理（启动时）
   - 动态代理实现接口调用（运行时）
   - SynchronousMethodHandler 处理调用（请求时）

2. **请求核心**
   - Contract 解析注解（SpringMVC 注解）
   - RequestInterceptor 增强请求（添加请求头等）
   - Encoder/Decoder 处理数据（JSON 序列化/反序列化）

3. **调用核心**
   - 负载均衡选择实例（Ribbon/LoadBalancer）
   - 超时重试保证可靠性（Request.Options/Retryer）
   - 熔断降级保护服务（Sentinel/Resilience4j）

4. **扩展点**
   - `RequestInterceptor`：请求拦截器
   - `ErrorDecoder`：错误解码器
   - `Retryer`：重试策略
   - `Contract`：契约解析
   - `Encoder/Decoder`：编解码器
