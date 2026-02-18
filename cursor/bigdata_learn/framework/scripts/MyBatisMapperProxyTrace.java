package com.example.trace;

import org.apache.ibatis.executor.Executor;
import org.apache.ibatis.mapping.MappedStatement;
import org.apache.ibatis.plugin.*;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import java.io.InputStream;
import java.lang.reflect.Proxy;
import java.util.Properties;

/**
 * MyBatis Mapper 动态代理追踪示例（增强版）
 * 演示 Mapper 代理、插件拦截、自定义 Interceptor
 */
public class MyBatisMapperProxyTrace {
    
    public static void main(String[] args) {
        System.out.println("=== MyBatis Mapper Proxy Trace Start ===\n");
        
        // 创建 SqlSessionFactory（简化示例）
        System.out.println("[TRACE] Creating SqlSessionFactory");
        SqlSessionFactory sqlSessionFactory = createSqlSessionFactory();
        
        // 获取 SqlSession
        System.out.println("[TRACE] Opening SqlSession");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            
            // 获取 Mapper（这里会创建动态代理）
            System.out.println("[TRACE] Getting Mapper from SqlSession");
            UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
            
            System.out.println("[TRACE] Mapper class: " + userMapper.getClass().getName());
            System.out.println("[TRACE] Is proxy: " + Proxy.isProxyClass(userMapper.getClass()));
            
            // 调用 Mapper 方法（会触发代理）
            System.out.println("\n=== Calling Mapper Method ===");
            System.out.println("[TRACE] Calling getUserById(1)");
            // User user = userMapper.getUserById(1);
            // System.out.println("[TRACE] Result: " + user);
            
            System.out.println("\n[TRACE] Call flow:");
            System.out.println("  1. MapperProxy.invoke()");
            System.out.println("  2. MapperMethod.execute()");
            System.out.println("  3. SqlSession.selectOne()");
            System.out.println("  4. Executor.query()");
            System.out.println("  5. StatementHandler.query()");
        }
        
        System.out.println("\n=== MyBatis Mapper Proxy Trace End ===");
    }
    
    private static SqlSessionFactory createSqlSessionFactory() {
        // 简化示例，实际应从配置文件创建
        return new SqlSessionFactoryBuilder().build((InputStream) null);
    }
}

interface UserMapper {
    User getUserById(Integer id);
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
 * 自定义 MyBatis 插件：统计 SQL 执行时间
 */
@Intercepts({
    @Signature(type = Executor.class, method = "query", args = {MappedStatement.class, Object.class, org.apache.ibatis.session.RowBounds.class, org.apache.ibatis.session.ResultHandler.class})
})
class PerformanceInterceptor implements Interceptor {
    @Override
    public Object intercept(Invocation invocation) throws Throwable {
        long start = System.currentTimeMillis();
        System.out.println("[TRACE] Plugin intercepting: Executor.query");
        
        try {
            Object result = invocation.proceed();
            long duration = System.currentTimeMillis() - start;
            
            MappedStatement ms = (MappedStatement) invocation.getArgs()[0];
            System.out.println("[TRACE] SQL executed: " + ms.getId() + " in " + duration + "ms");
            
            return result;
        } catch (Throwable e) {
            System.out.println("[TRACE] SQL execution failed: " + e.getMessage());
            throw e;
        }
    }
    
    @Override
    public Object plugin(Object target) {
        System.out.println("[TRACE] Plugin.wrap: wrapping " + target.getClass().getName());
        return Plugin.wrap(target, this);
    }
    
    @Override
    public void setProperties(Properties properties) {
        System.out.println("[TRACE] Plugin properties: " + properties);
    }
}
