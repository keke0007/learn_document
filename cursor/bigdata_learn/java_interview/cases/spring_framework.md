# Spring 框架案例

## 案例概述

本案例通过实际代码演示 Spring 框架的核心功能，包括 IOC、AOP、事务管理等。

## 知识点

1. **IOC 容器**
   - Bean 生命周期
   - 依赖注入
   - Bean 作用域

2. **AOP**
   - 切面编程
   - 动态代理
   - 通知类型

3. **事务管理**
   - 声明式事务
   - 事务传播行为
   - 事务隔离级别

## 案例代码

### 案例1：Bean 生命周期

```java
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.*;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

public class LifecycleBean implements 
    BeanNameAware, 
    BeanFactoryAware, 
    ApplicationContextAware,
    InitializingBean,
    DisposableBean {
    
    private String name;
    
    // 1. 实例化
    public LifecycleBean() {
        System.out.println("1. 实例化 Bean");
    }
    
    // 2. 属性赋值
    public void setName(String name) {
        this.name = name;
        System.out.println("2. 属性赋值: " + name);
    }
    
    // 3. 设置 BeanName
    @Override
    public void setBeanName(String name) {
        System.out.println("3. 设置 BeanName: " + name);
    }
    
    // 4. 设置 BeanFactory
    @Override
    public void setBeanFactory(BeanFactory beanFactory) throws BeansException {
        System.out.println("4. 设置 BeanFactory");
    }
    
    // 5. 设置 ApplicationContext
    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        System.out.println("5. 设置 ApplicationContext");
    }
    
    // 6. BeanPostProcessor.postProcessBeforeInitialization
    
    // 7. @PostConstruct
    @PostConstruct
    public void postConstruct() {
        System.out.println("7. @PostConstruct 方法执行");
    }
    
    // 8. InitializingBean.afterPropertiesSet
    @Override
    public void afterPropertiesSet() throws Exception {
        System.out.println("8. InitializingBean.afterPropertiesSet 方法执行");
    }
    
    // 9. 自定义初始化方法
    public void customInit() {
        System.out.println("9. 自定义初始化方法执行");
    }
    
    // 10. BeanPostProcessor.postProcessAfterInitialization
    
    // 11. Bean 使用中
    
    // 12. @PreDestroy
    @PreDestroy
    public void preDestroy() {
        System.out.println("12. @PreDestroy 方法执行");
    }
    
    // 13. DisposableBean.destroy
    @Override
    public void destroy() throws Exception {
        System.out.println("13. DisposableBean.destroy 方法执行");
    }
    
    // 14. 自定义销毁方法
    public void customDestroy() {
        System.out.println("14. 自定义销毁方法执行");
    }
}
```

### 案例2：依赖注入

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

// 接口
interface UserRepository {
    void save(User user);
}

// 实现类1
@Component("jdbcUserRepository")
class JdbcUserRepository implements UserRepository {
    @Override
    public void save(User user) {
        System.out.println("JDBC 保存用户: " + user.getName());
    }
}

// 实现类2
@Component("mybatisUserRepository")
class MybatisUserRepository implements UserRepository {
    @Override
    public void save(User user) {
        System.out.println("MyBatis 保存用户: " + user.getName());
    }
}

// 服务类
@Component
class UserService {
    // 字段注入（不推荐）
    @Autowired
    @Qualifier("jdbcUserRepository")
    private UserRepository userRepository;
    
    // 构造器注入（推荐）
    @Autowired
    public UserService(@Qualifier("jdbcUserRepository") UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    // Setter 注入
    @Autowired
    public void setUserRepository(@Qualifier("jdbcUserRepository") UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public void saveUser(User user) {
        userRepository.save(user);
    }
}

// 用户实体
class User {
    private String name;
    
    public User(String name) {
        this.name = name;
    }
    
    public String getName() {
        return name;
    }
}
```

### 案例3：AOP 切面

```java
import org.aspectj.lang.annotation.*;
import org.aspectj.lang.ProceedingJoinPoint;
import org.springframework.stereotype.Component;

// 切面类
@Aspect
@Component
public class LoggingAspect {
    
    // 定义切点
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceMethods() {}
    
    // 前置通知
    @Before("serviceMethods()")
    public void beforeAdvice() {
        System.out.println("Before: 方法执行前");
    }
    
    // 后置通知
    @AfterReturning(pointcut = "serviceMethods()", returning = "result")
    public void afterReturningAdvice(Object result) {
        System.out.println("AfterReturning: 方法正常返回，返回值: " + result);
    }
    
    // 异常通知
    @AfterThrowing(pointcut = "serviceMethods()", throwing = "ex")
    public void afterThrowingAdvice(Exception ex) {
        System.out.println("AfterThrowing: 方法抛出异常: " + ex.getMessage());
    }
    
    // 最终通知
    @After("serviceMethods()")
    public void afterAdvice() {
        System.out.println("After: 方法执行后（无论是否异常）");
    }
    
    // 环绕通知
    @Around("serviceMethods()")
    public Object aroundAdvice(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("Around: 方法执行前");
        try {
            Object result = joinPoint.proceed();
            System.out.println("Around: 方法执行后");
            return result;
        } catch (Exception e) {
            System.out.println("Around: 方法抛出异常");
            throw e;
        }
    }
}

// 服务类
@Service
class OrderService {
    public void createOrder(Order order) {
        System.out.println("创建订单: " + order.getId());
    }
    
    public void cancelOrder(String orderId) {
        System.out.println("取消订单: " + orderId);
        throw new RuntimeException("取消订单失败");
    }
}
```

### 案例4：事务管理

```java
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;

@Service
public class TransactionService {
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private OrderRepository orderRepository;
    
    /**
     * 事务传播行为：REQUIRED（默认）
     * 如果存在事务则加入，否则创建新事务
     */
    @Transactional(propagation = Propagation.REQUIRED)
    public void createOrderWithUser(Order order, User user) {
        userRepository.save(user);
        orderRepository.save(order);
        // 如果这里抛出异常，两个操作都会回滚
    }
    
    /**
     * 事务传播行为：REQUIRES_NEW
     * 创建新事务，如果存在事务则挂起
     */
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void createOrderInNewTransaction(Order order) {
        orderRepository.save(order);
        // 这个事务独立于外部事务
    }
    
    /**
     * 事务隔离级别：READ_COMMITTED
     * 读已提交，避免脏读
     */
    @Transactional(isolation = Isolation.READ_COMMITTED)
    public User getUser(Long id) {
        return userRepository.findById(id);
    }
    
    /**
     * 只读事务
     * 优化性能，不允许修改数据
     */
    @Transactional(readOnly = true)
    public List<Order> getAllOrders() {
        return orderRepository.findAll();
    }
    
    /**
     * 回滚指定异常
     */
    @Transactional(rollbackFor = {RuntimeException.class, Exception.class})
    public void updateOrder(Order order) {
        orderRepository.update(order);
        // RuntimeException 和 Exception 都会触发回滚
    }
    
    /**
     * 不回滚指定异常
     */
    @Transactional(noRollbackFor = {IllegalArgumentException.class})
    public void deleteOrder(String orderId) {
        orderRepository.delete(orderId);
        // IllegalArgumentException 不会触发回滚
    }
}
```

### 案例5：Spring Boot 自动配置

```java
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

// 配置属性类
@ConfigurationProperties(prefix = "custom")
class CustomProperties {
    private String name;
    private int age;
    
    // getters and setters
}

// 自动配置类
@Configuration
@ConditionalOnClass(CustomService.class)
@EnableConfigurationProperties(CustomProperties.class)
public class CustomAutoConfiguration {
    
    @Bean
    @ConditionalOnMissingBean
    public CustomService customService(CustomProperties properties) {
        return new CustomService(properties.getName(), properties.getAge());
    }
}

// 服务类
class CustomService {
    private String name;
    private int age;
    
    public CustomService(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

// application.yml
// custom:
//   name: "Spring Boot"
//   age: 10
```

## 验证数据

### Bean 生命周期执行顺序

```
1. 实例化 Bean
2. 属性赋值: test
3. 设置 BeanName: lifecycleBean
4. 设置 BeanFactory
5. 设置 ApplicationContext
6. BeanPostProcessor.postProcessBeforeInitialization
7. @PostConstruct 方法执行
8. InitializingBean.afterPropertiesSet 方法执行
9. 自定义初始化方法执行
10. BeanPostProcessor.postProcessAfterInitialization
11. Bean 使用中
12. @PreDestroy 方法执行
13. DisposableBean.destroy 方法执行
14. 自定义销毁方法执行
```

### AOP 执行顺序

```
Around: 方法执行前
Before: 方法执行前
方法执行中...
AfterReturning: 方法正常返回，返回值: result
After: 方法执行后（无论是否异常）
Around: 方法执行后
```

### 事务测试结果

| 传播行为 | 外部事务 | 内部事务 | 结果 |
|---------|---------|---------|------|
| REQUIRED | 有 | 有 | 加入外部事务 |
| REQUIRED | 无 | 有 | 创建新事务 |
| REQUIRES_NEW | 有 | 有 | 创建新事务 |
| REQUIRES_NEW | 无 | 有 | 创建新事务 |

## 总结

1. **IOC 容器**
   - 控制反转，依赖注入
   - Bean 生命周期管理
   - 多种注入方式

2. **AOP**
   - 面向切面编程
   - 动态代理实现
   - 多种通知类型

3. **事务管理**
   - 声明式事务
   - 多种传播行为
   - 不同隔离级别

4. **Spring Boot**
   - 自动配置
   - 约定优于配置
   - Starter 机制
