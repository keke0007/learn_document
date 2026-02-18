# Spring Cloud Gateway 源码学习案例（深入版）

## 案例概述

本案例深入 Spring Cloud Gateway 路由匹配、过滤器链、Netty 响应式模型等核心源码。**重点：断点位置、数据结构、Netty 线程模型、背压机制、基于源码的扩展实验。**

---

## 📍 断点清单（建议按顺序打断点）

### 路由匹配断点
1. **`DispatcherHandler.handle()`** (L124) - 请求处理入口
2. **`RoutePredicateHandlerMapping.getHandler()`** (L89) - 路由匹配
3. **`RouteLocator.getRoutes()`** (L45) - 获取路由列表
4. **`PathRoutePredicateFactory.apply()`** (L89) - 路径匹配
5. **`RouteDefinitionRouteLocator.convertToRoute()`** (L124) - 路由转换

### 过滤器链断点
1. **`FilteringWebHandler.handle()`** (L89) - 过滤器处理入口
2. **`DefaultGatewayFilterChain.filter()`** (L89) - 过滤器链执行
3. **`GlobalFilter.filter()`** (L45) - 全局过滤器执行
4. **`GatewayFilter.filter()`** (L45) - 路由过滤器执行

### Netty 响应式断点
1. **`ReactorHttpHandlerAdapter.apply()`** (L89) - Reactor 适配
2. **`NettyRoutingFilter.filter()`** (L200) - Netty 路由过滤
3. **`HttpClientOperations.onInboundNext()`** (L124) - HTTP 响应处理

---

## 🔍 关键数据结构

### 路由匹配核心数据结构

```java
// RouteDefinitionLocator.java
// 1. 路由定义列表（Flux）
Flux<RouteDefinition> getRouteDefinitions();

// RouteLocator.java
// 2. 路由列表（Flux）
Flux<Route> getRoutes();

// Route.java
// 3. 路由对象
private final String id;
private final URI uri;
private final int order;
private final Predicate<ServerWebExchange> predicate;
private final List<GatewayFilter> filters;

// RouteDefinitionRouteLocator.java
// 4. 路由定义映射
private final Map<String, RouteDefinition> routeDefinitions = new ConcurrentHashMap<>();
```

### 过滤器链核心数据结构

```java
// FilteringWebHandler.java
// 1. 全局过滤器列表（有序）
private final List<GlobalFilter> globalFilters;

// 2. 过滤器链构建器
private final GatewayFilterChainBuilder filterChainBuilder;

// DefaultGatewayFilterChain.java
// 3. 过滤器列表（有序）
private final List<GatewayFilter> filters;

// 4. 当前过滤器索引
private int index;

// 5. 网关过滤器工厂映射
private final Map<String, GatewayFilterFactory> gatewayFilterFactories = new HashMap<>();
```

### Netty 响应式核心数据结构

```java
// NettyRoutingFilter.java
// 1. HTTP 客户端
private final HttpClient httpClient;

// 2. 负载均衡客户端
private final LoadBalancerClient loadBalancerClient;

// ReactorHttpHandlerAdapter.java
// 3. HTTP 处理器
private final HttpHandler httpHandler;

// 4. 服务器配置
private final ServerHttpRequest request;
private final ServerHttpResponse response;
```

---

## 🧵 线程模型

### 路由匹配线程模型
- **请求处理**：Netty EventLoop 线程（非阻塞）
- **路由匹配**：响应式流处理，无阻塞
- **路由缓存**：使用 `ConcurrentHashMap`，线程安全

### 过滤器链线程模型
- **过滤器执行**：响应式流处理，支持异步
- **过滤器顺序**：通过 `Ordered` 接口控制
- **过滤器状态**：使用 `ServerWebExchange`，线程隔离

### Netty 响应式线程模型
- **EventLoopGroup**：主线程组（Boss），处理连接
- **WorkerGroup**：工作线程组（Worker），处理 I/O
- **背压处理**：通过 `onBackpressureBuffer` 自动处理
- **超时控制**：通过 `timeout()` 操作符控制

---

## 📚 源码追踪（深入版）

### 案例1：路由匹配（完整流程）

**完整调用链：**
```
DispatcherHandler.handle() (L124)
  -> RoutePredicateHandlerMapping.getHandler() (L89)
    -> RouteLocator.getRoutes() (L45)
      -> RouteDefinitionRouteLocator.getRoutes()
        -> RouteDefinitionLocator.getRouteDefinitions()
          -> 获取路由定义列表
        -> convertToRoute() (L124)
          -> 路由转换
            -> 创建 Predicate
              -> PathRoutePredicateFactory.apply()
            -> 创建 GatewayFilter
              -> GatewayFilterFactory.apply()
    -> 路由匹配
      -> Route.predicate.test(exchange)
        -> PathRoutePredicate.apply()
          -> 路径匹配
            -> pathMatcher.match(pattern, path)
    -> 返回匹配的路由
      -> Mono.just(route)
```

**路由匹配详细机制：**
```java
// RoutePredicateHandlerMapping.getHandler()
public Mono<Object> getHandler(ServerWebExchange exchange) {
    return this.routeLocator.getRoutes()
        .concatMap(route -> Mono.just(route)
            .filterWhen(r -> r.getPredicate().apply(exchange))
            .doOnNext(r -> exchange.getAttributes().put(GATEWAY_ROUTE_ATTR, r))
            .then(Mono.just(r))
        )
        .next()
        .map(route -> new HandlerMethod(this, "handle", route));
}
```

**Predicate 类型：**
- **PathRoutePredicate**：路径匹配
- **HostRoutePredicate**：主机匹配
- **MethodRoutePredicate**：HTTP 方法匹配
- **HeaderRoutePredicate**：请求头匹配
- **QueryRoutePredicate**：查询参数匹配
- **CookieRoutePredicate**：Cookie 匹配
- **AfterRoutePredicate**：时间匹配（之后）
- **BeforeRoutePredicate**：时间匹配（之前）
- **BetweenRoutePredicate**：时间匹配（之间）
- **RemoteAddrRoutePredicate**：远程地址匹配
- **WeightRoutePredicate**：权重匹配

**关键类：**
- `RouteDefinitionLocator`：路由定义定位器
- `RouteLocator`：路由定位器
- `RoutePredicateHandlerMapping`：路由匹配处理器映射
- `Predicate`：断言接口

**验证代码：** `scripts/GatewayFilterTrace.java`

---

### 案例2：过滤器链（完整执行流程）

**完整调用链：**
```
FilteringWebHandler.handle() (L89)
  -> buildFilters() (L124)
    -> getFilters() (L89)
      -> 合并过滤器
        -> GlobalFilter + GatewayFilter
      -> 排序过滤器
        -> filters.sort(Comparator.comparingInt(Ordered::getOrder))
  -> DefaultGatewayFilterChain.filter() (L89)
    -> 获取当前过滤器
      -> GatewayFilter filter = filters.get(index)
    -> 执行过滤器
      -> filter.filter(exchange, this)
        -> 下一个过滤器
          -> chain.filter(exchange)
    -> 所有过滤器执行完成
      -> 返回 Mono.empty()
```

**过滤器执行详细机制：**
```java
// DefaultGatewayFilterChain.filter()
public Mono<Void> filter(ServerWebExchange exchange) {
    return Mono.defer(() -> {
        if (this.index < filters.size()) {
            GatewayFilter filter = filters.get(this.index);
            DefaultGatewayFilterChain chain = new DefaultGatewayFilterChain(this, this.index + 1);
            return filter.filter(exchange, chain);
        } else {
            return Mono.empty();
        }
    });
}
```

**过滤器类型：**
- **GlobalFilter**：全局过滤器（所有路由生效）
- **GatewayFilter**：路由过滤器（特定路由生效）
- **GatewayFilterFactory**：过滤器工厂（创建过滤器）

**常见全局过滤器：**
- **LoadBalancerClientFilter**：负载均衡
- **NettyRoutingFilter**：Netty 路由
- **NettyWriteResponseFilter**：Netty 响应写入
- **RouteToRequestUrlFilter**：路由转请求 URL
- **WebSocketRoutingFilter**：WebSocket 路由
- **ForwardRoutingFilter**：转发路由

**过滤器执行顺序：**
- 通过 `@Order` 或 `Ordered` 接口控制
- 数值越小越先执行
- 全局过滤器默认顺序：-2147483648 到 2147483647

**验证数据：** `data/gateway-trace-sample.log`

---

### 案例3：Netty 响应式模型（深入机制）

**完整响应式流程：**
```
ReactorHttpHandlerAdapter.apply() (L89)
  -> 创建 ServerHttpRequest
    -> 创建 ServerHttpResponse
      -> 调用 HttpHandler
        -> FilteringWebHandler.handle()
          -> 过滤器链执行
            -> NettyRoutingFilter.filter() (L200)
              -> 创建 HTTP 请求
                -> HttpClientOperations.send()
                  -> 发送请求
                    -> 等待响应
                      -> onInboundNext() (L124)
                        -> 处理响应
                          -> 写入响应
                            -> NettyWriteResponseFilter.filter()
```

**Netty 线程模型：**
```java
// NettyRoutingFilter.filter()
public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
    // 1. 获取请求 URI
    URI requestUrl = exchange.getRequiredAttribute(GATEWAY_REQUEST_URL_ATTR);
    
    // 2. 创建 HTTP 请求
    HttpRequest request = buildHttpRequest(exchange);
    
    // 3. 发送请求（响应式）
    return this.httpClient.request(request)
        .doOnNext(response -> {
            // 4. 处理响应
            ServerHttpResponse serverHttpResponse = exchange.getResponse();
            serverHttpResponse.setStatusCode(response.status());
            // ... 设置响应头、响应体
        })
        .then();
}
```

**背压处理：**
```java
// 背压自动处理
return this.httpClient.request(request)
    .onBackpressureBuffer(1000)  // 缓冲 1000 个元素
    .timeout(Duration.ofSeconds(30))  // 30 秒超时
    .doOnError(TimeoutException.class, e -> {
        // 超时处理
    })
    .then();
```

**关键组件：**
- `HttpServer`：Netty HTTP 服务器
- `ReactorHttpHandlerAdapter`：Reactor 适配器
- `Mono/Flux`：响应式流
- `EventLoopGroup`：事件循环组

---

## 🧪 基于源码扩展实验

### 实验1：自定义 GlobalFilter（请求日志记录）

**目标**：记录所有请求的详细信息。

**实现：**
```java
@Component
@Order(-100)
public class RequestLoggingFilter implements GlobalFilter {
    private static final Logger log = LoggerFactory.getLogger(RequestLoggingFilter.class);
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        long startTime = System.currentTimeMillis();
        
        return chain.filter(exchange).then(Mono.fromRunnable(() -> {
            long duration = System.currentTimeMillis() - startTime;
            log.info("Request: {} {} - Status: {} - Duration: {}ms",
                request.getMethod(),
                request.getURI(),
                exchange.getResponse().getStatusCode(),
                duration
            );
        }));
    }
}
```

**验证**：发送请求，观察日志输出。

---

### 实验2：自定义 GatewayFilterFactory（请求头添加）

**目标**：创建自定义过滤器工厂，添加请求头。

**实现：**
```java
@Component
public class AddCustomHeaderGatewayFilterFactory extends AbstractGatewayFilterFactory<AddCustomHeaderGatewayFilterFactory.Config> {
    public AddCustomHeaderGatewayFilterFactory() {
        super(Config.class);
    }
    
    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            ServerHttpRequest request = exchange.getRequest().mutate()
                .header(config.getName(), config.getValue())
                .build();
            return chain.filter(exchange.mutate().request(request).build());
        };
    }
    
    public static class Config {
        private String name;
        private String value;
        // getters/setters
    }
}
```

**配置使用：**
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: custom-route
          uri: lb://user-service
          filters:
            - AddCustomHeader=name,X-Custom-Value
```

**验证**：发送请求，检查请求头是否添加。

---

### 实验3：自定义 RoutePredicateFactory（自定义断言）

**目标**：创建自定义路由断言，根据请求参数匹配。

**实现：**
```java
@Component
public class CustomParamRoutePredicateFactory extends AbstractRoutePredicateFactory<CustomParamRoutePredicateFactory.Config> {
    public CustomParamRoutePredicateFactory() {
        super(Config.class);
    }
    
    @Override
    public Predicate<ServerWebExchange> apply(Config config) {
        return exchange -> {
            String paramValue = exchange.getRequest().getQueryParams().getFirst(config.getParamName());
            return config.getParamValue().equals(paramValue);
        };
    }
    
    public static class Config {
        private String paramName;
        private String paramValue;
        // getters/setters
    }
}
```

**配置使用：**
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: custom-predicate-route
          uri: lb://user-service
          predicates:
            - CustomParam=key,value
```

**验证**：发送带参数的请求，观察路由匹配。

---

## 🐛 常见坑与排查

### 坑1：路由不匹配
**现象**：请求未匹配到路由
**原因**：
1. 路径不匹配
2. 断言条件不满足
3. 路由顺序问题
**排查**：
1. 检查路径配置
2. 检查断言条件
3. 检查路由顺序（order）

### 坑2：过滤器不执行
**现象**：过滤器未执行
**原因**：
1. 过滤器顺序错误
2. 过滤器未注册
3. 过滤器短路返回
**排查**：
1. 检查过滤器顺序
2. 检查过滤器是否注册为 Bean
3. 检查过滤器逻辑

### 坑3：响应式流阻塞
**现象**：请求超时或阻塞
**原因**：
1. 同步阻塞操作
2. 背压未处理
3. 超时未设置
**排查**：
1. 检查是否有阻塞操作
2. 检查背压处理
3. 检查超时配置

---

## 验证数据

### 路由匹配日志

```
[DEBUG] Route matched: route1
[DEBUG] Predicate matched: Path=/api/**
[DEBUG] Filters applied: [AddRequestHeader, Retry]
[DEBUG] Forwarding to: http://backend-service/api/users
```

### 过滤器执行日志

```
[DEBUG] GlobalFilter[AuthFilter] executed: order=-100
[DEBUG] GatewayFilter[AddRequestHeader] executed: order=0
[DEBUG] GatewayFilter[Retry] executed: order=100
[DEBUG] Response received: 200 OK
```

### Netty 响应式日志

```
[DEBUG] NettyRoutingFilter: Sending request to http://backend-service/api/users
[DEBUG] NettyRoutingFilter: Response received: 200 OK
[DEBUG] NettyWriteResponseFilter: Writing response
```

---

## 总结

1. **路由核心**
   - RouteDefinition 定义路由（配置）
   - RouteLocator 定位路由（运行时）
   - Predicate 匹配请求（条件判断）

2. **过滤器核心**
   - GlobalFilter 全局生效（所有路由）
   - GatewayFilter 路由级别（特定路由）
   - 有序执行，支持短路（责任链模式）

3. **响应式核心**
   - Reactor 响应式编程（Mono/Flux）
   - Netty 异步非阻塞（EventLoop）
   - 背压自动处理（onBackpressureBuffer）

4. **扩展点**
   - `GlobalFilter`：全局过滤器
   - `GatewayFilterFactory`：过滤器工厂
   - `RoutePredicateFactory`：路由断言工厂
