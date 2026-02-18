package com.example.trace;

import com.xxl.job.core.handler.annotation.XxlJob;
import com.xxl.job.core.handler.IJobHandler;
import com.xxl.job.core.biz.model.ReturnT;

/**
 * XXL-JOB 任务处理器追踪示例（增强版）
 * 演示任务触发、执行器注册、自定义路由策略和任务处理器
 */
public class XxlJobHandlerTrace {
    
    @XxlJob("userJobHandler")
    public ReturnT<String> execute(String param) {
        System.out.println("[TRACE] Job handler executed");
        System.out.println("[TRACE] Job param: " + param);
        System.out.println("[TRACE] Business logic executed");
        return ReturnT.SUCCESS;
    }
    
    public static void main(String[] args) {
        System.out.println("=== XXL-JOB Trace Start ===\n");
        
        System.out.println("[TRACE] Job Trigger Flow:");
        System.out.println("  JobScheduleHelper.run()");
        System.out.println("    -> JobTriggerPoolHelper.trigger()");
        System.out.println("      -> XxlJobTrigger.trigger()");
        System.out.println("        -> Select executor by route strategy");
        System.out.println("          -> Send HTTP request to executor");
        System.out.println("            -> ExecutorBiz.run()");
        System.out.println("              -> JobThread.run()");
        System.out.println("                -> JobHandler.execute()");
        
        System.out.println("\n[TRACE] Executor Registration Flow:");
        System.out.println("  XxlJobSpringExecutor.start()");
        System.out.println("    -> ExecutorRegistryThread.run()");
        System.out.println("      -> ExecutorRegistryRegistry.registry()");
        System.out.println("        -> AdminBiz.registry()");
        System.out.println("          -> Send registry request to admin");
        System.out.println("            -> Admin update executor list");
        
        System.out.println("\n[TRACE] Route Strategies:");
        System.out.println("  - FIRST: First executor");
        System.out.println("  - LAST: Last executor");
        System.out.println("  - ROUND: Round robin");
        System.out.println("  - RANDOM: Random");
        System.out.println("  - CONSISTENT_HASH: Consistent hash");
        System.out.println("  - FAILOVER: Failover");
        System.out.println("  - BUSYOVER: Busy transfer");
        System.out.println("  - SHARDING_BROADCAST: Sharding broadcast");
        
        System.out.println("\n=== XXL-JOB Trace End ===");
    }
}

/**
 * 自定义任务处理器：实现复杂业务逻辑
 */
class CustomJobHandler extends IJobHandler {
    @Override
    public ReturnT<String> execute(String param) throws Exception {
        System.out.println("[TRACE] CustomJobHandler.execute()");
        
        // 解析任务参数
        com.alibaba.fastjson.JSONObject params = com.alibaba.fastjson.JSON.parseObject(param);
        String taskType = params.getString("taskType");
        
        // 根据任务类型执行不同逻辑
        switch (taskType) {
            case "dataSync":
                return executeDataSync(params);
            case "report":
                return executeReport(params);
            default:
                return ReturnT.FAIL;
        }
    }
    
    private ReturnT<String> executeDataSync(com.alibaba.fastjson.JSONObject params) {
        System.out.println("[TRACE] Executing data sync");
        // 数据同步逻辑
        return ReturnT.SUCCESS;
    }
    
    private ReturnT<String> executeReport(com.alibaba.fastjson.JSONObject params) {
        System.out.println("[TRACE] Executing report generation");
        // 报表生成逻辑
        return ReturnT.SUCCESS;
    }
}

/**
 * 自定义路由策略：根据任务参数选择执行器
 */
class CustomRouteStrategy implements com.xxl.job.core.router.ExecutorRouter {
    @Override
    public ReturnT<String> route(com.xxl.job.core.biz.model.TriggerParam triggerParam, java.util.List<String> addressList) {
        System.out.println("[TRACE] CustomRouteStrategy.route()");
        
        // 解析任务参数
        String jobParam = triggerParam.getExecutorParam();
        
        // 根据参数选择执行器（如：根据地域选择）
        String selectedAddress = selectExecutorByRegion(jobParam, addressList);
        
        return new ReturnT<String>(selectedAddress);
    }
    
    private String selectExecutorByRegion(String jobParam, java.util.List<String> addressList) {
        // 自定义路由逻辑
        if (jobParam.contains("region=beijing")) {
            return addressList.stream()
                .filter(addr -> addr.contains("beijing"))
                .findFirst()
                .orElse(addressList.get(0));
        }
        return addressList.get(0);
    }
}
