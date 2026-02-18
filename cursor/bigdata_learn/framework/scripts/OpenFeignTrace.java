package com.example.trace;

import feign.Feign;
import feign.RequestInterceptor;
import feign.RequestTemplate;
import feign.codec.ErrorDecoder;

/**
 * OpenFeign 追踪示例（增强版）
 * 演示 Feign 客户端代理生成、请求构建、自定义拦截器和错误处理
 */
public class OpenFeignTrace {
    
    /**
     * Feign 客户端接口
     */
    public interface UserServiceClient {
        User getUserById(Integer id);
    }
    
    /**
     * 请求拦截器示例：添加认证信息
     */
    public static class AuthInterceptor implements RequestInterceptor {
        @Override
        public void apply(RequestTemplate template) {
            System.out.println("[TRACE] RequestInterceptor.apply() called");
            template.header("Authorization", "Bearer token123");
            System.out.println("[TRACE] Header added: Authorization");
        }
    }
    
    /**
     * 自定义错误解码器：处理特定错误码
     */
    public static class CustomErrorDecoder implements ErrorDecoder {
        private final ErrorDecoder defaultErrorDecoder = new feign.codec.ErrorDecoder.Default();
        
        @Override
        public Exception decode(String methodKey, feign.Response response) {
            System.out.println("[TRACE] ErrorDecoder.decode() called");
            System.out.println("[TRACE] Method: " + methodKey);
            System.out.println("[TRACE] Status: " + response.status());
            
            if (response.status() == 404) {
                return new NotFoundException("Resource not found: " + methodKey);
            }
            
            if (response.status() == 401) {
                return new UnauthorizedException("Unauthorized: " + methodKey);
            }
            
            return defaultErrorDecoder.decode(methodKey, response);
        }
    }
    
    /**
     * 自定义重试器：控制重试策略
     */
    public static class CustomRetryer implements feign.Retryer {
        private final int maxAttempts;
        private final long period;
        private int attempt;
        
        public CustomRetryer() {
            this.maxAttempts = 3;
            this.period = 1000L;
            this.attempt = 1;
        }
        
        @Override
        public void continueOrPropagate(feign.RetryableException e) {
            System.out.println("[TRACE] Retryer.continueOrPropagate() called, attempt: " + attempt);
            
            if (attempt++ >= maxAttempts) {
                throw e;
            }
            
            try {
                Thread.sleep(period * attempt); // 递增间隔
                System.out.println("[TRACE] Retrying after " + (period * attempt) + "ms");
            } catch (InterruptedException ignored) {
                Thread.currentThread().interrupt();
                throw e;
            }
        }
        
        @Override
        public feign.Retryer clone() {
            return new CustomRetryer();
        }
    }
    
    public static void main(String[] args) {
        System.out.println("=== OpenFeign Trace Start ===\n");
        
        System.out.println("[TRACE] Creating Feign client:");
        System.out.println("  1. FeignClientFactoryBean.getObject()");
        System.out.println("  2. Feign.Builder.build()");
        System.out.println("  3. ReflectiveFeign.newInstance()");
        System.out.println("  4. Proxy.newProxyInstance()");
        
        System.out.println("\n[TRACE] Request building flow:");
        System.out.println("  SynchronousMethodHandler.invoke()");
        System.out.println("    -> RequestTemplate.create()");
        System.out.println("    -> Contract.parseAndValidateMetadata()");
        System.out.println("    -> RequestInterceptor.apply()");
        System.out.println("    -> Encoder.encode()");
        
        System.out.println("\n[TRACE] Request execution flow:");
        System.out.println("  LoadBalancerFeignClient.execute()");
        System.out.println("    -> LoadBalancerRequest.execute()");
        System.out.println("      -> ILoadBalancer.chooseServer()");
        System.out.println("      -> HTTP request");
        System.out.println("        -> Retryer.continueOrPropagate()");
        System.out.println("        -> ErrorDecoder.decode()");
        
        // 创建 Feign 客户端（简化示例）
        UserServiceClient client = Feign.builder()
            .requestInterceptor(new AuthInterceptor())
            .errorDecoder(new CustomErrorDecoder())
            .retryer(new CustomRetryer())
            .target(UserServiceClient.class, "http://user-service");
        
        System.out.println("\n[TRACE] Client created: " + client.getClass().getName());
        System.out.println("[TRACE] Is proxy: " + java.lang.reflect.Proxy.isProxyClass(client.getClass()));
        
        System.out.println("\n=== OpenFeign Trace End ===");
    }
}

class User {
    private Integer id;
    private String name;
    
    public User(Integer id, String name) {
        this.id = id;
        this.name = name;
    }
}

class NotFoundException extends RuntimeException {
    public NotFoundException(String message) {
        super(message);
    }
}

class UnauthorizedException extends RuntimeException {
    public UnauthorizedException(String message) {
        super(message);
    }
}
