package com.example.trace;

import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

/**
 * Spring Cloud Gateway 过滤器追踪示例（增强版）
 * 演示全局过滤器、自定义过滤器工厂、过滤器链执行
 */
public class GatewayFilterTrace {
    
    /**
     * 全局过滤器示例：认证过滤器
     */
    public static class AuthFilter implements GlobalFilter, Ordered {
        @Override
        public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
            System.out.println("[TRACE] AuthFilter executed: order=" + getOrder());
            System.out.println("[TRACE] Request path: " + exchange.getRequest().getPath());
            
            // 检查认证信息
            String token = exchange.getRequest().getHeaders().getFirst("Authorization");
            if (token == null || !token.startsWith("Bearer ")) {
                System.out.println("[TRACE] AuthFilter: Unauthorized");
                exchange.getResponse().setStatusCode(org.springframework.http.HttpStatus.UNAUTHORIZED);
                return exchange.getResponse().setComplete();
            }
            
            // 添加请求头
            exchange.getRequest().mutate()
                .header("X-Auth-User", "admin")
                .build();
            
            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                System.out.println("[TRACE] AuthFilter post-processing");
            }));
        }
        
        @Override
        public int getOrder() {
            return -100; // 高优先级
        }
    }
    
    /**
     * 全局过滤器示例：日志过滤器
     */
    public static class LogFilter implements GlobalFilter, Ordered {
        @Override
        public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
            System.out.println("[TRACE] LogFilter executed: order=" + getOrder());
            
            long startTime = System.currentTimeMillis();
            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                long duration = System.currentTimeMillis() - startTime;
                System.out.println("[TRACE] Request processed in " + duration + "ms");
                System.out.println("[TRACE] Response status: " + exchange.getResponse().getStatusCode());
            }));
        }
        
        @Override
        public int getOrder() {
            return 100; // 低优先级
        }
    }
    
    /**
     * 自定义过滤器工厂示例：添加自定义请求头
     */
    public static class AddCustomHeaderGatewayFilterFactory extends org.springframework.cloud.gateway.filter.factory.AbstractGatewayFilterFactory<AddCustomHeaderGatewayFilterFactory.Config> {
        public AddCustomHeaderGatewayFilterFactory() {
            super(Config.class);
        }
        
        @Override
        public org.springframework.cloud.gateway.filter.GatewayFilter apply(Config config) {
            return (exchange, chain) -> {
                System.out.println("[TRACE] AddCustomHeader filter: " + config.getName() + "=" + config.getValue());
                
                org.springframework.http.server.reactive.ServerHttpRequest request = exchange.getRequest().mutate()
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
    
    public static void main(String[] args) {
        System.out.println("=== Gateway Filter Trace Start ===\n");
        
        System.out.println("[TRACE] Filter execution order:");
        System.out.println("  1. AuthFilter (order=-100)");
        System.out.println("  2. Route filters");
        System.out.println("  3. LogFilter (order=100)");
        
        System.out.println("\n[TRACE] Filter chain flow:");
        System.out.println("  FilteringWebHandler.handle()");
        System.out.println("    -> buildFilters()");
        System.out.println("    -> DefaultGatewayFilterChain.filter()");
        System.out.println("      -> GatewayFilter.filter()");
        System.out.println("        -> next.filter()");
        
        System.out.println("\n[TRACE] Netty routing flow:");
        System.out.println("  NettyRoutingFilter.filter()");
        System.out.println("    -> HttpClient.request()");
        System.out.println("      -> onInboundNext()");
        System.out.println("        -> NettyWriteResponseFilter.filter()");
        
        System.out.println("\n=== Gateway Filter Trace End ===");
    }
}
