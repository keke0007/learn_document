# Spring Boot 源码学习案例（深入版）

## 案例概述

本案例深入 Spring Boot 启动流程、自动配置机制、配置绑定等核心源码。**重点：断点位置、条件评估机制、自动配置过滤、配置绑定流程、基于源码的扩展实验。**

---

## 📍 断点清单（建议按顺序打断点）

### 启动流程断点
1. **`SpringApplication.run(String... args)`** (L297) - 启动入口
2. **`SpringApplication.createApplicationContext()`** (L311) - 创建应用上下文
3. **`SpringApplication.prepareContext()`** (L653) - 准备上下文
4. **`SpringApplication.refreshContext()`** (L761) - 刷新上下文
5. **`ConfigurationClassPostProcessor.postProcessBeanDefinitionRegistry()`** (L315) - 配置类后处理

### 自动配置断点
1. **`AutoConfigurationImportSelector.selectImports()`** (L108) - 选择自动配置类
2. **`SpringFactoriesLoader.loadFactoryNames()`** (L120) - 加载 spring.factories
3. **`OnClassCondition.getMatchOutcome()`** (L64) - 类路径条件评估
4. **`OnBeanCondition.getMatchOutcome()`** (L94) - Bean 条件评估
5. **`OnPropertyCondition.getMatchOutcome()`** (L52) - 属性条件评估

### 配置绑定断点
1. **`ConfigurationPropertiesBindingPostProcessor.postProcessBeforeInitialization()`** (L89) - 配置绑定入口
2. **`Binder.bind()`** (L159) - 绑定配置
3. **`ConfigurationPropertySource.from()`** (L95) - 配置源转换

---

## 🔍 关键数据结构

### 启动流程核心数据结构

```java
// SpringApplication.java
// 1. 主类
private Class<?> mainApplicationClass;

// 2. 应用上下文类型
private WebApplicationType webApplicationType;

// 3. 监听器列表
private List<ApplicationListener<?>> listeners = new ArrayList<>();

// 4. 初始化器列表
private List<ApplicationContextInitializer<?>> initializers = new ArrayList<>();

// 5. 启动参数
private Set<String> sources = new LinkedHashSet<>();
```

### 自动配置核心数据结构

```java
// AutoConfigurationImportSelector.java
// 1. 自动配置类缓存
private static final Map<String, List<String>> cache = new ConcurrentReferenceHashMap<>();

// 2. 排除的自动配置类
private static final String[] NO_IMPORTS = {};

// 3. 排除过滤器
private static final AutoConfigurationExclusionFilter exclusionFilter = getAutoConfigurationExclusionFilter();

// ConfigurationClassParser.java
// 4. 配置类集合
private final Set<ConfigurationClass> configurationClasses = new LinkedHashSet<>();

// 5. 导入的配置类
private final Map<ImportBeanDefinitionRegistrar, AnnotationMetadata> importBeanDefinitionRegistrars = new LinkedHashMap<>();
```

### 条件评估核心数据结构

```java
// ConditionEvaluator.java
// 1. 条件评估结果缓存
private final Map<ConfigurationCondition, Boolean> conditionOutcomesCache = new HashMap<>();

// OnClassCondition.java
// 2. 类加载器缓存
private static final Map<String, Boolean> classCache = new ConcurrentReferenceHashMap<>();

// OnBeanCondition.java
// 3. Bean 存在性缓存
private final Map<String, Boolean> beanExistenceCache = new ConcurrentHashMap<>();
```

### 配置绑定核心数据结构

```java
// Binder.java
// 1. 配置源列表
private final List<ConfigurationPropertySource> sources;

// 2. 转换器
private final ConversionService conversionService;

// 3. 属性名匹配器
private final PropertyNamePatternMatcher patternMatcher;

// ConfigurationPropertiesBindingPostProcessor.java
// 4. 绑定结果缓存
private final Map<ConfigurationBeanNameMetadata, ConfigurationProperties> boundConfigurationProperties = new ConcurrentHashMap<>();
```

---

## 🧵 线程模型

### 启动流程线程模型
- **单线程启动**：`run()` 在主线程执行
- **上下文创建**：同步创建，线程安全由 `ConcurrentHashMap` 保证
- **自动配置加载**：启动时单线程加载，运行时只读

### 条件评估线程模型
- **条件评估**：启动时单线程评估，结果缓存
- **类加载检查**：使用 `ConcurrentReferenceHashMap` 缓存，线程安全
- **Bean 存在性检查**：使用 `ConcurrentHashMap` 缓存

### 配置绑定线程模型
- **配置绑定**：Bean 初始化时单线程绑定
- **配置源读取**：只读操作，线程安全
- **类型转换**：使用 `ConversionService`，线程安全

---

## 📚 源码追踪（深入版）

### 案例1：启动流程（完整链路）

**完整调用链：**
```
SpringApplication.run(String... args) (L297)
  -> run(new Class<?>[]{primarySource}, args)
    -> createApplicationContext() (L311)
      -> 根据 webApplicationType 创建上下文
        ├─ SERVLET -> AnnotationConfigServletWebServerApplicationContext
        ├─ REACTIVE -> AnnotationConfigReactiveWebServerApplicationContext
        └─ NONE -> AnnotationConfigApplicationContext
    -> prepareContext() (L653)
      -> postProcessApplicationContext()      // 后处理上下文
      -> applyInitializers()                  // 应用初始化器
      -> listeners.contextPrepared()         // 发布 ContextPreparedEvent
      -> load()                              // 加载 BeanDefinition
    -> refreshContext() (L761)
      -> AbstractApplicationContext.refresh()
        -> invokeBeanFactoryPostProcessors()
          -> ConfigurationClassPostProcessor.postProcessBeanDefinitionRegistry()
            -> processConfigBeanDefinitions()
              -> ConfigurationClassParser.parse()
                -> processImports()           // 处理 @Import
                  -> AutoConfigurationImportSelector.selectImports()
                    -> getAutoConfigurationEntry()
                      -> getCandidateConfigurations()
                        -> SpringFactoriesLoader.loadFactoryNames()
                          -> loadSpringFactories()  // 加载 META-INF/spring.factories
    -> afterRefresh()                         // 后处理刷新
    -> listeners.started()                    // 发布 ApplicationStartedEvent
    -> callRunners()                          // 调用 ApplicationRunner/CommandLineRunner
```

**关键源码位置：**
- `SpringApplication.run()` - `spring-boot-2.x.x.jar`
- `AutoConfigurationImportSelector.selectImports()` - `spring-boot-autoconfigure-2.x.x.jar`
- `SpringFactoriesLoader.loadFactoryNames()` - `spring-core-5.x.x.jar`

**Web 应用类型推断：**
```java
// SpringApplication.deduceWebApplicationType()
static WebApplicationType deduceWebApplicationType() {
    if (ClassUtils.isPresent("org.springframework.web.reactive.DispatcherHandler", null)
            && !ClassUtils.isPresent("org.springframework.web.servlet.DispatcherServlet", null)
            && !ClassUtils.isPresent("org.glassfish.jersey.servlet.ServletContainer", null)) {
        return WebApplicationType.REACTIVE;
    }
    for (String className : SERVLET_INDICATOR_CLASSES) {
        if (!ClassUtils.isPresent(className, null)) {
            return WebApplicationType.NONE;
        }
    }
    return WebApplicationType.SERVLET;
}
```

---

### 案例2：自动配置机制（深入过滤流程）

**完整自动配置流程：**
```
AutoConfigurationImportSelector.selectImports() (L108)
  -> getAutoConfigurationEntry() (L123)
    -> getCandidateConfigurations() (L178)
      -> SpringFactoriesLoader.loadFactoryNames()
        -> loadSpringFactories()              // 加载所有自动配置类
    -> filter()                               // 【关键】过滤自动配置类
      -> getAutoConfigurationExclusions()     // 排除配置
      -> getConfigurationClassFilter().filter() // 条件过滤
        -> OnClassCondition.getMatchOutcome()  // 类路径条件
        -> OnBeanCondition.getMatchOutcome()  // Bean 条件
        -> OnPropertyCondition.getMatchOutcome() // 属性条件
    -> fireAutoConfigurationImportEvents()    // 发布事件
```

**条件评估详细流程：**

**1. OnClassCondition（类路径条件）**
```java
// OnClassCondition.getMatchOutcome()
public ConditionOutcome getMatchOutcome(ConditionContext context, AnnotatedTypeMetadata metadata) {
    // 1. 获取 @ConditionalOnClass 注解
    List<String> onClasses = getCandidates(metadata, ConditionalOnClass.class);
    
    // 2. 检查类是否存在
    List<String> missing = filter(onClasses, ClassNameFilter.MISSING, context.getClassLoader());
    
    // 3. 返回结果
    if (!missing.isEmpty()) {
        return ConditionOutcome.noMatch(ConditionMessage.forCondition(ConditionalOnClass.class)
                .didNotFind("required class", "required classes").items(Style.QUOTE, missing));
    }
    return ConditionOutcome.match();
}
```

**2. OnBeanCondition（Bean 条件）**
```java
// OnBeanCondition.getMatchOutcome()
public ConditionOutcome getMatchOutcome(ConditionContext context, AnnotatedTypeMetadata metadata) {
    // 1. 获取 @ConditionalOnMissingBean 注解
    Spec<ConditionalOnMissingBean> missingBeanSpec = getSpec(metadata, ConditionalOnMissingBean.class);
    
    // 2. 检查 Bean 是否存在
    List<String> missing = missingBeanSpec.collectNames(context, metadata);
    
    // 3. 返回结果
    if (!missing.isEmpty()) {
        return ConditionOutcome.noMatch(ConditionMessage.forCondition(ConditionalOnMissingBean.class)
                .didNotFind("bean", "beans").items(Style.QUOTE, missing));
    }
    return ConditionOutcome.match();
}
```

**3. OnPropertyCondition（属性条件）**
```java
// OnPropertyCondition.getMatchOutcome()
public ConditionOutcome getMatchOutcome(ConditionContext context, AnnotatedTypeMetadata metadata) {
    // 1. 获取 @ConditionalOnProperty 注解
    Spec<ConditionalOnProperty> propertySpec = getSpec(metadata, ConditionalOnProperty.class);
    
    // 2. 检查属性值
    List<String> missingProperties = propertySpec.collectProperties(context, metadata);
    
    // 3. 返回结果
    if (!missingProperties.isEmpty()) {
        return ConditionOutcome.noMatch(ConditionMessage.forCondition(ConditionalOnProperty.class)
                .didNotFind("property", "properties").items(Style.QUOTE, missingProperties));
    }
    return ConditionOutcome.match();
}
```

**自动配置类示例：**
```java
@Configuration
@ConditionalOnClass(DataSource.class)                    // 类路径条件
@ConditionalOnMissingBean(DataSource.class)              // Bean 条件
@ConditionalOnProperty(prefix = "spring.datasource", name = "url") // 属性条件
@EnableConfigurationProperties(DataSourceProperties.class)
public class DataSourceAutoConfiguration {
    @Bean
    public DataSource dataSource(DataSourceProperties properties) {
        return properties.initializeDataSourceBuilder().build();
    }
}
```

**验证数据：** `data/application-sample.yml`

---

### 案例3：配置绑定（深入绑定流程）

**完整绑定流程：**
```
ConfigurationPropertiesBindingPostProcessor.postProcessBeforeInitialization() (L89)
  -> bind() (L105)
    -> Binder.bind() (L159)
      -> bindObject() (L200)
        -> bindBean() (L250)
          -> bindProperty() (L300)
            -> convertValue() (L350)
              -> ConversionService.convert()
                -> 类型转换
          -> validate() (L400)
            -> Validator.validate()
```

**配置绑定详细机制：**

**1. PropertySource 解析**
```java
// Binder.bind()
public <T> BindResult<T> bind(ConfigurationPropertyName name, Bindable<T> target) {
    // 1. 查找配置源
    ConfigurationPropertySource source = findPropertySource(name);
    
    // 2. 获取配置值
    Object value = source.getConfigurationProperty(name).getValue();
    
    // 3. 类型转换
    T result = convert(value, target);
    
    // 4. 返回结果
    return BindResult.of(result);
}
```

**2. 类型转换**
```java
// Binder.convertValue()
private <T> T convertValue(Object value, Bindable<T> target) {
    // 1. 获取目标类型
    ResolvableType type = target.getType();
    
    // 2. 使用 ConversionService 转换
    return (T) this.conversionService.convert(value, type.resolve());
}
```

**3. 嵌套绑定**
```java
// Binder.bindBean()
private <T> void bindBean(ConfigurationPropertyName name, Bindable<T> target, BeanPropertyBinder propertyBinder) {
    // 1. 获取 Bean 属性
    BeanDescription description = getBeanDescription(target.getType());
    
    // 2. 遍历属性
    for (BeanProperty property : description.getProperties()) {
        // 3. 递归绑定嵌套属性
        bindProperty(name.append(property.getName()), property, propertyBinder);
    }
}
```

**配置类示例：**
```java
@ConfigurationProperties(prefix = "app")
public class AppProperties {
    private String name;
    private int port;
    private Nested nested;
    
    // getters/setters
    
    public static class Nested {
        private String value;
        // getters/setters
    }
}
```

**配置文件：**
```yaml
app:
  name: demo-app
  port: 8080
  nested:
    value: nested-value
```

---

## 🧪 基于源码扩展实验

### 实验1：自定义 Starter（完整实现）

**目标**：创建一个自定义 Starter，自动配置一个服务。

**步骤1：创建自动配置模块**
```java
// my-starter-autoconfigure/src/main/java/com/example/autoconfigure/MyServiceAutoConfiguration.java
@Configuration
@ConditionalOnClass(MyService.class)
@ConditionalOnMissingBean(MyService.class)
@EnableConfigurationProperties(MyServiceProperties.class)
public class MyServiceAutoConfiguration {
    @Bean
    public MyService myService(MyServiceProperties properties) {
        return new MyService(properties);
    }
}
```

**步骤2：创建配置属性类**
```java
// MyServiceProperties.java
@ConfigurationProperties(prefix = "my.service")
public class MyServiceProperties {
    private String name = "default";
    private int timeout = 5000;
    // getters/setters
}
```

**步骤3：创建 spring.factories**
```properties
# my-starter-autoconfigure/src/main/resources/META-INF/spring.factories
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
com.example.autoconfigure.MyServiceAutoConfiguration
```

**步骤4：创建 Starter 模块**
```xml
<!-- my-starter/pom.xml -->
<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>my-starter-autoconfigure</artifactId>
    </dependency>
</dependencies>
```

**验证**：在其他项目中引入 Starter，观察 MyService 是否自动创建。

---

### 实验2：自定义 Condition（环境条件）

**目标**：根据环境变量决定是否启用某个功能。

**实现：**
```java
// 自定义 Condition
public class EnvironmentCondition implements Condition {
    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        Environment env = context.getEnvironment();
        String envName = env.getProperty("spring.profiles.active");
        return "prod".equals(envName);
    }
}

// 使用 Condition
@Configuration
public class ProductionConfiguration {
    @Bean
    @Conditional(EnvironmentCondition.class)
    public ProductionService productionService() {
        return new ProductionService();
    }
}
```

**验证**：设置 `spring.profiles.active=prod`，观察 Bean 是否创建。

---

### 实验3：自定义 ApplicationListener（启动监听）

**目标**：在应用启动后执行自定义逻辑。

**实现：**
```java
@Component
public class CustomApplicationListener implements ApplicationListener<ContextRefreshedEvent> {
    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        System.out.println("Application context refreshed!");
        // 自定义逻辑
    }
}
```

**验证**：启动应用，观察日志输出。

---

## 🐛 常见坑与排查

### 坑1：自动配置不生效
**现象**：Starter 的自动配置类没有被加载
**原因**：
1. spring.factories 路径错误
2. 条件不满足
3. 被排除
**排查**：
1. 检查 `META-INF/spring.factories` 路径
2. 启用 debug 日志：`debug=true`
3. 检查自动配置报告

### 坑2：配置绑定失败
**现象**：`@ConfigurationProperties` 属性为 null
**原因**：
1. 前缀不匹配
2. 属性名不匹配
3. 类型转换失败
**排查**：
1. 检查配置前缀
2. 检查属性名（支持 kebab-case）
3. 检查类型转换器

### 坑3：条件评估缓存问题
**现象**：修改条件后，Bean 仍然创建/不创建
**原因**：条件评估结果被缓存
**排查**：
1. 重启应用
2. 清除条件缓存（需要修改源码）

---

## 验证数据

### 启动日志

```
[INFO] Starting SpringApplication on host with PID 12345
[INFO] The following profiles are active: dev
[INFO] Auto-configuration report:
[INFO]   Positive matches:
[INFO]     - MyAutoConfiguration matched
[INFO]   Negative matches:
[INFO]     - OtherAutoConfiguration did not match
[INFO]     -   Reason: @ConditionalOnClass did not find required class 'com.example.OtherService'
```

### 自动配置报告（debug=true）

```
============================
CONDITIONS EVALUATION REPORT
============================

Positive matches:
-----------------
   MyServiceAutoConfiguration matched
      - @ConditionalOnClass found required class 'com.example.MyService'
      - @ConditionalOnMissingBean did not find any bean of type 'com.example.MyService'

Negative matches:
-----------------
   OtherAutoConfiguration did not match
      - @ConditionalOnClass did not find required class 'com.example.OtherService'
```

---

## 总结

1. **启动核心**
   - `SpringApplication.run()` 是入口
   - `SpringFactoriesLoader` 加载自动配置
   - 条件装配决定是否生效

2. **自动配置核心**
   - `spring.factories` 声明配置类
   - `AutoConfigurationImportSelector` 选择配置类
   - 条件评估过滤配置类

3. **配置绑定核心**
   - `@ConfigurationProperties` 绑定配置
   - `Binder` 进行类型转换
   - 支持嵌套、集合、Map

4. **扩展点**
   - `@Conditional`：条件装配
   - `ApplicationListener`：事件监听
   - `ApplicationRunner`：启动后执行
