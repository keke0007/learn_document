package com.example.trace;

import org.springframework.aop.framework.ProxyFactory;
import org.springframework.aop.support.AopUtils;
import org.springframework.transaction.annotation.Transactional;

import java.lang.reflect.Method;

/**
 * Spring AOP 和事务追踪示例（增强版）
 * 演示代理创建、事务拦截、自定义切面
 */
public class SpringAopTxTrace {
    
    public static void main(String[] args) {
        System.out.println("=== Spring AOP & Transaction Trace Start ===\n");
        
        // 创建目标对象
        UserService target = new UserService();
        System.out.println("[TRACE] Target object created: " + target);
        System.out.println("[TRACE] Is proxy: " + AopUtils.isAopProxy(target));
        
        // 创建代理工厂
        ProxyFactory proxyFactory = new ProxyFactory();
        proxyFactory.setTarget(target);
        proxyFactory.addInterface(IUserService.class);
        
        // 添加自定义切面
        CustomAspect customAspect = new CustomAspect();
        proxyFactory.addAdvice(customAspect);
        
        // 创建代理对象
        IUserService proxy = (IUserService) proxyFactory.getProxy();
        System.out.println("[TRACE] Proxy object created: " + proxy);
        System.out.println("[TRACE] Proxy class: " + proxy.getClass().getName());
        System.out.println("[TRACE] Is proxy: " + AopUtils.isAopProxy(proxy));
        System.out.println("[TRACE] Is JDK proxy: " + AopUtils.isJdkDynamicProxy(proxy));
        System.out.println("[TRACE] Is CGLIB proxy: " + AopUtils.isCglibProxy(proxy));
        
        // 调用代理方法
        System.out.println("\n=== Calling Proxy Method ===");
        User user = proxy.getUserById(1);
        System.out.println("[TRACE] Result: " + user);
        
        System.out.println("\n=== Spring AOP & Transaction Trace End ===");
    }
}

interface IUserService {
    @Transactional
    User getUserById(Integer id);
}

class UserService implements IUserService {
    @Override
    @Transactional
    public User getUserById(Integer id) {
        System.out.println("[TRACE] getUserById called with id: " + id);
        System.out.println("[TRACE] TransactionInterceptor would intercept here");
        return new User(id, "Alice");
    }
}

class User {
    private Integer id;
    private String name;
    
    public User(Integer id, String name) {
        this.id = id;
        this.name = name;
    }
    
    @Override
    public String toString() {
        return "User{id=" + id + ", name='" + name + "'}";
    }
}

/**
 * 自定义切面：记录方法执行时间
 */
class CustomAspect implements org.aopalliance.intercept.MethodInterceptor {
    @Override
    public Object invoke(org.aopalliance.intercept.MethodInvocation invocation) throws Throwable {
        long start = System.currentTimeMillis();
        System.out.println("[TRACE] Before advice: " + invocation.getMethod().getName());
        
        try {
            Object result = invocation.proceed();
            long duration = System.currentTimeMillis() - start;
            System.out.println("[TRACE] After advice: " + invocation.getMethod().getName() + " executed in " + duration + "ms");
            return result;
        } catch (Throwable e) {
            System.out.println("[TRACE] Exception advice: " + e.getMessage());
            throw e;
        }
    }
}
