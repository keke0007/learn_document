package com.example.trace;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Spring IOC 容器追踪示例（增强版）
 * 演示 Bean 生命周期、依赖注入、BeanPostProcessor 扩展点
 */
@Configuration
public class SpringIocTrace {
    
    @Bean
    public UserService userService() {
        System.out.println("[TRACE] Creating UserService bean");
        return new UserService();
    }
    
    @Bean
    public OrderService orderService(UserService userService) {
        System.out.println("[TRACE] Creating OrderService bean with UserService dependency");
        return new OrderService(userService);
    }
    
    /**
     * 自定义 BeanPostProcessor：在 Bean 初始化后修改属性
     */
    @Bean
    public CustomBeanPostProcessor customBeanPostProcessor() {
        return new CustomBeanPostProcessor();
    }
    
    public static void main(String[] args) {
        System.out.println("=== Spring IOC Trace Start ===\n");
        
        ApplicationContext context = new AnnotationConfigApplicationContext(SpringIocTrace.class);
        
        System.out.println("\n=== Getting Bean ===");
        UserService userService = context.getBean(UserService.class);
        OrderService orderService = context.getBean(OrderService.class);
        
        System.out.println("\n=== Bean Info ===");
        System.out.println("UserService: " + userService);
        System.out.println("OrderService: " + orderService);
        System.out.println("Is singleton: " + (userService == context.getBean(UserService.class)));
        
        System.out.println("\n=== BeanPostProcessor Effect ===");
        System.out.println("UserService name after BPP: " + userService.getName());
        
        System.out.println("\n=== Spring IOC Trace End ===");
    }
}

class UserService {
    private String name;
    
    public UserService() {
        System.out.println("[TRACE] UserService constructor called");
        this.name = "OriginalName";
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
}

class OrderService {
    private final UserService userService;
    
    public OrderService(UserService userService) {
        System.out.println("[TRACE] OrderService constructor called with UserService");
        this.userService = userService;
    }
}

/**
 * 自定义 BeanPostProcessor：在初始化后修改 String 类型属性
 */
class CustomBeanPostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        System.out.println("[TRACE] BeanPostProcessor.postProcessAfterInitialization: " + beanName);
        
        // 使用反射修改 String 属性
        try {
            java.lang.reflect.Field[] fields = bean.getClass().getDeclaredFields();
            for (java.lang.reflect.Field field : fields) {
                if (field.getType() == String.class) {
                    field.setAccessible(true);
                    String value = (String) field.get(bean);
                    if (value != null && !value.startsWith("[CUSTOM]")) {
                        field.set(bean, "[CUSTOM]" + value);
                        System.out.println("[TRACE] Modified field: " + field.getName() + " = " + field.get(bean));
                    }
                }
            }
        } catch (Exception e) {
            // 忽略异常
        }
        
        return bean;
    }
}
