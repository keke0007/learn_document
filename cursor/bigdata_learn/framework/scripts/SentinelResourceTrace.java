package com.example.trace;

import com.alibaba.csp.sentinel.Entry;
import com.alibaba.csp.sentinel.EntryType;
import com.alibaba.csp.sentinel.SphU;
import com.alibaba.csp.sentinel.slots.block.BlockException;
import com.alibaba.csp.sentinel.slots.block.flow.FlowRule;
import com.alibaba.csp.sentinel.slots.block.flow.FlowRuleManager;

import java.util.ArrayList;
import java.util.List;

/**
 * Sentinel 资源追踪示例（增强版）
 * 演示 SlotChain 执行、规则检查、自定义 Slot
 */
public class SentinelResourceTrace {
    
    public static void main(String[] args) {
        System.out.println("=== Sentinel Resource Trace Start ===\n");
        
        System.out.println("[TRACE] Entry creation flow:");
        System.out.println("  SphU.entry()");
        System.out.println("    -> Env.sph.entry()");
        System.out.println("      -> CtSph.entry()");
        System.out.println("        -> Entry.new()");
        System.out.println("          -> SlotChain.entry()");
        
        System.out.println("\n[TRACE] SlotChain execution order:");
        System.out.println("  1. NodeSelectorSlot.entry()      // Select node");
        System.out.println("  2. ClusterBuilderSlot.entry()    // Cluster build");
        System.out.println("  3. LogSlot.entry()                // Log");
        System.out.println("  4. StatisticSlot.entry()          // Statistics");
        System.out.println("  5. SystemSlot.entry()             // System rules");
        System.out.println("  6. AuthoritySlot.entry()          // Authorization");
        System.out.println("  7. FlowSlot.entry()               // Flow control");
        System.out.println("  8. DegradeSlot.entry()            // Circuit breaker");
        
        // 示例：动态添加流控规则
        System.out.println("\n[TRACE] Adding flow rule dynamically");
        addFlowRule("userService", 100);
        
        // 示例：资源保护
        String resource = "userService";
        try (Entry entry = SphU.entry(resource, EntryType.IN)) {
            System.out.println("\n[TRACE] Resource protected: " + resource);
            System.out.println("[TRACE] Business logic executed");
        } catch (BlockException e) {
            System.out.println("\n[TRACE] Blocked by flow control: " + resource);
        }
        
        System.out.println("\n=== Sentinel Resource Trace End ===");
    }
    
    /**
     * 动态添加流控规则
     */
    private static void addFlowRule(String resource, int qps) {
        FlowRule rule = new FlowRule();
        rule.setResource(resource);
        rule.setGrade(com.alibaba.csp.sentinel.slots.block.flow.FlowRuleConstant.FLOW_GRADE_QPS);
        rule.setCount(qps);
        
        List<FlowRule> rules = new ArrayList<>();
        rules.add(rule);
        FlowRuleManager.loadRules(rules);
        
        System.out.println("[TRACE] Flow rule added: resource=" + resource + ", qps=" + qps);
    }
}

/**
 * 自定义 Slot：自定义限流逻辑
 */
class CustomSlot extends com.alibaba.csp.sentinel.slotchain.AbstractLinkedProcessorSlot<com.alibaba.csp.sentinel.context.Context> {
    @Override
    public void entry(com.alibaba.csp.sentinel.context.Context context, com.alibaba.csp.sentinel.node.DefaultNode node, int count, boolean prioritized, Object... args) throws Throwable {
        // 自定义限流逻辑
        String resourceName = context.getCurEntry().getResourceWrapper().getName();
        if (shouldBlock(resourceName)) {
            throw new BlockException("Custom block");
        }
        
        // 调用下一个 Slot
        fireEntry(context, node, count, prioritized, args);
    }
    
    @Override
    public void exit(com.alibaba.csp.sentinel.context.Context context, com.alibaba.csp.sentinel.node.DefaultNode node, int count, Object... args) {
        // 退出处理
        fireExit(context, node, count, args);
    }
    
    private boolean shouldBlock(String resourceName) {
        // 自定义限流逻辑
        return false;
    }
}
