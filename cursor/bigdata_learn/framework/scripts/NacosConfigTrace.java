package com.example.trace;

import com.alibaba.nacos.api.config.ConfigService;
import com.alibaba.nacos.api.config.listener.Listener;
import com.alibaba.nacos.api.naming.NamingService;
import com.alibaba.nacos.api.naming.listener.Event;
import com.alibaba.nacos.api.naming.listener.EventListener;
import com.alibaba.nacos.api.naming.listener.NamingEvent;

/**
 * Nacos 配置和注册发现追踪示例（增强版）
 * 演示配置拉取、服务注册、自定义监听器
 */
public class NacosConfigTrace {
    
    public static void main(String[] args) {
        System.out.println("=== Nacos Trace Start ===\n");
        
        System.out.println("[TRACE] Service Registration Flow:");
        System.out.println("  NacosServiceRegistry.register()");
        System.out.println("    -> NamingService.registerInstance()");
        System.out.println("      -> NacosNamingService.registerInstance()");
        System.out.println("        -> NamingProxy.registerService()");
        System.out.println("          -> HTTP POST /nacos/v1/ns/instance");
        System.out.println("            -> InstanceController.register()");
        System.out.println("              -> ServiceManager.registerInstance()");
        
        System.out.println("\n[TRACE] Config Pull Flow:");
        System.out.println("  NacosConfigService.getConfig()");
        System.out.println("    -> ClientWorker.getServerConfig()");
        System.out.println("      -> HttpAgent.httpGet()");
        System.out.println("        -> LocalConfigInfoProcessor.saveSnapshot()");
        
        System.out.println("\n[TRACE] Long Polling Flow:");
        System.out.println("  ClientWorker.checkUpdateDataIds()");
        System.out.println("    -> LongPollingRunnable.run()");
        System.out.println("      -> HttpAgent.httpPost() (30s timeout)");
        System.out.println("        -> Config change push");
        System.out.println("          -> LocalConfigInfoProcessor.saveSnapshot()");
        
        System.out.println("\n[TRACE] Service Discovery Flow:");
        System.out.println("  NacosServiceDiscovery.getInstances()");
        System.out.println("    -> NamingService.selectInstances()");
        System.out.println("      -> HostReactor.getServiceInfo()");
        System.out.println("        -> Get from cache");
        System.out.println("        -> Scheduled update cache");
        
        System.out.println("\n=== Nacos Trace End ===");
    }
}

/**
 * 自定义配置监听器：配置变更时执行自定义逻辑
 */
class CustomConfigListener implements Listener {
    @Override
    public void receiveConfigInfo(String configInfo) {
        System.out.println("[TRACE] Config changed: " + configInfo);
        // 自定义逻辑：重新加载配置、刷新 Bean 等
        refreshConfiguration(configInfo);
    }
    
    private void refreshConfiguration(String configInfo) {
        System.out.println("[TRACE] Refreshing configuration...");
        // 解析配置并更新应用配置
    }
}

/**
 * 自定义服务监听器：服务列表变更时执行自定义逻辑
 */
class CustomServiceListener implements EventListener {
    @Override
    public void onEvent(Event event) {
        if (event instanceof NamingEvent) {
            NamingEvent namingEvent = (NamingEvent) event;
            System.out.println("[TRACE] Service list changed: " + namingEvent.getServiceName());
            System.out.println("[TRACE] Instances: " + namingEvent.getInstances().size());
            
            // 自定义逻辑：更新负载均衡器、刷新服务列表等
            updateLoadBalancer(namingEvent);
        }
    }
    
    private void updateLoadBalancer(NamingEvent event) {
        System.out.println("[TRACE] Updating load balancer...");
        // 更新负载均衡器服务列表
    }
}
