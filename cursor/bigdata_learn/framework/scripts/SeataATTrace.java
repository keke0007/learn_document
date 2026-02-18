package com.example.trace;

import io.seata.spring.annotation.GlobalTransactional;

/**
 * Seata AT 模式追踪示例（增强版）
 * 演示全局事务、undo_log 生成、回滚机制
 */
public class SeataATTrace {
    
    @GlobalTransactional
    public void businessMethod() {
        System.out.println("[TRACE] Global transaction begin");
        System.out.println("[TRACE] XID generated");
        
        // 执行业务 SQL
        System.out.println("[TRACE] Executing business SQL");
        System.out.println("[TRACE] Generating undo_log");
        System.out.println("[TRACE] Before image captured");
        System.out.println("[TRACE] After image captured");
        
        // 提交或回滚
        System.out.println("[TRACE] Transaction commit/rollback");
    }
    
    public static void main(String[] args) {
        System.out.println("=== Seata AT Trace Start ===\n");
        
        System.out.println("[TRACE] Phase 1 (Commit) Flow:");
        System.out.println("  @GlobalTransactional method call");
        System.out.println("    -> GlobalTransactionalInterceptor.invoke()");
        System.out.println("      -> GlobalTransaction.begin()");
        System.out.println("        -> TM register to TC");
        System.out.println("      -> Execute business SQL");
        System.out.println("        -> DataSourceProxy.execute()");
        System.out.println("          -> Generate undo_log");
        System.out.println("            -> UndoLogManager.insertUndoLog()");
        System.out.println("      -> Commit (Phase 1)");
        
        System.out.println("\n[TRACE] Phase 2 (Rollback) Flow:");
        System.out.println("  TC initiate rollback");
        System.out.println("    -> RM receive rollback request");
        System.out.println("      -> UndoLogManager.undo()");
        System.out.println("        -> Parse undo_log");
        System.out.println("          -> Generate reverse SQL");
        System.out.println("            -> Execute rollback SQL");
        System.out.println("              -> Delete undo_log");
        
        System.out.println("\n[TRACE] undo_log structure:");
        System.out.println("  - branch_id: Branch transaction ID");
        System.out.println("  - xid: Global transaction ID");
        System.out.println("  - rollback_info: Before/after image");
        System.out.println("  - log_status: 0=normal, 1=defense");
        
        System.out.println("\n[TRACE] Before/After Image Example:");
        System.out.println("  UPDATE user SET name='Bob', age=30 WHERE id=1");
        System.out.println("  Before: {id=1, name=Alice, age=25}");
        System.out.println("  After:  {id=1, name=Bob, age=30}");
        System.out.println("  Rollback SQL: UPDATE user SET name='Alice', age=25 WHERE id=1");
        
        System.out.println("\n=== Seata AT Trace End ===");
    }
}

/**
 * 自定义 UndoLogParser：自定义序列化方式
 */
class CustomUndoLogParser implements io.seata.rm.datasource.undo.UndoLogParser {
    @Override
    public String getName() {
        return "custom";
    }
    
    @Override
    public byte[] encode(io.seata.rm.datasource.undo.BranchUndoLog branchUndoLog) {
        System.out.println("[TRACE] CustomUndoLogParser.encode()");
        // 自定义序列化（如：使用 Protobuf）
        return com.alibaba.fastjson.JSON.toJSONBytes(branchUndoLog);
    }
    
    @Override
    public io.seata.rm.datasource.undo.BranchUndoLog decode(byte[] bytes) {
        System.out.println("[TRACE] CustomUndoLogParser.decode()");
        // 自定义反序列化
        return com.alibaba.fastjson.JSON.parseObject(bytes, io.seata.rm.datasource.undo.BranchUndoLog.class);
    }
}
