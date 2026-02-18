# 案例1：日志分析

## 案例描述
学习如何分析 Java 应用日志，定位问题根因。

## 数据准备

### 应用日志 (application.log)
```
2024-01-15 09:00:00.123 [main] INFO  com.example.App - Application started
2024-01-15 09:00:05.456 [http-nio-8080-exec-1] INFO  com.example.Controller - Processing request: /api/users
2024-01-15 09:00:10.789 [http-nio-8080-exec-1] ERROR com.example.Service - Database connection failed
java.sql.SQLException: Connection refused
    at com.mysql.jdbc.ConnectionImpl.connectOneTryOnly(ConnectionImpl.java:2400)
    at com.mysql.jdbc.ConnectionImpl.createNewIO(ConnectionImpl.java:2300)
    at com.example.Service.getConnection(Service.java:45)
2024-01-15 09:00:15.234 [http-nio-8080-exec-2] WARN  com.example.Controller - Request timeout: /api/users
2024-01-15 09:00:20.567 [GC] INFO  - [GC (Allocation Failure) 1024M->512M, 0.123s]
2024-01-15 09:00:25.890 [http-nio-8080-exec-3] ERROR com.example.Service - OutOfMemoryError: Java heap space
java.lang.OutOfMemoryError: Java heap space
    at java.util.Arrays.copyOf(Arrays.java:3210)
    at java.util.ArrayList.grow(ArrayList.java:267)
    at com.example.Service.processData(Service.java:78)
2024-01-15 09:00:30.123 [scheduler-1] INFO  com.example.Scheduler - Scheduled task executed
2024-01-15 09:00:35.456 [http-nio-8080-exec-4] ERROR com.example.Controller - NullPointerException
java.lang.NullPointerException
    at com.example.Controller.handleRequest(Controller.java:32)
    at com.example.Controller.doGet(Controller.java:15)
2024-01-15 09:00:40.789 [http-nio-8080-exec-5] INFO  com.example.Service - Processing completed in 5000ms
```

### GC 日志 (gc.log)
```
2024-01-15T09:00:20.123+0800: 0.234: [GC (Allocation Failure) [PSYoungGen: 1024K->512K(2048K)] 1024K->512K(4096K), 0.001234 secs]
2024-01-15T09:00:25.456+0800: 5.567: [GC (Allocation Failure) [PSYoungGen: 1536K->768K(2048K)] 1536K->768K(4096K), 0.001567 secs]
2024-01-15T09:00:30.789+0800: 10.890: [Full GC (Ergonomics) [PSYoungGen: 768K->0K(2048K)] [ParOldGen: 3072K->2048K(4096K)] 3840K->2048K(6144K), 0.012345 secs]
```

## 排查脚本

### 日志分析脚本 (analyze_logs.sh)
```bash
#!/bin/bash

LOG_FILE="data/application.log"
GC_LOG="data/gc.log"

echo "=== Java 应用日志分析 ==="

# ============================================
# 1. 查看日志基本信息
# ============================================

echo -e "\n1. 日志基本信息"
echo "总行数: $(wc -l < $LOG_FILE)"
echo "文件大小: $(du -h $LOG_FILE | cut -f1)"

# ============================================
# 2. 统计日志级别
# ============================================

echo -e "\n2. 日志级别统计"
echo "INFO: $(grep -c " INFO " $LOG_FILE)"
echo "WARN: $(grep -c " WARN " $LOG_FILE)"
echo "ERROR: $(grep -c " ERROR " $LOG_FILE)"

# ============================================
# 3. 查找错误日志
# ============================================

echo -e "\n3. 错误日志列表"
grep " ERROR " $LOG_FILE | head -10

# ============================================
# 4. 查找异常堆栈
# ============================================

echo -e "\n4. 异常类型统计"
grep -o "java\.[a-z.]*Exception\|java\.[a-z.]*Error" $LOG_FILE | sort | uniq -c | sort -rn

# ============================================
# 5. 查找特定错误
# ============================================

echo -e "\n5. OutOfMemoryError 详情"
grep -A 5 "OutOfMemoryError" $LOG_FILE

echo -e "\n6. NullPointerException 详情"
grep -A 5 "NullPointerException" $LOG_FILE

# ============================================
# 7. 按时间范围分析
# ============================================

echo -e "\n7. 09:00:00-09:00:30 时间段的错误"
grep "09:00:0[0-3]" $LOG_FILE | grep " ERROR "

# ============================================
# 8. 统计错误频率
# ============================================

echo -e "\n8. 错误频率统计（按分钟）"
grep " ERROR " $LOG_FILE | awk '{print $1, $2}' | cut -d: -f1-2 | uniq -c

# ============================================
# 9. 查找慢请求
# ============================================

echo -e "\n9. 慢请求（>1000ms）"
grep -E "completed in [0-9]{4,}ms\|timeout" $LOG_FILE

# ============================================
# 10. GC 日志分析
# ============================================

if [ -f "$GC_LOG" ]; then
    echo -e "\n10. GC 统计"
    echo "GC 次数: $(grep -c "\[GC" $GC_LOG)"
    echo "Full GC 次数: $(grep -c "\[Full GC" $GC_LOG)"
    
    echo -e "\n11. GC 时间统计"
    grep "\[GC" $GC_LOG | awk -F'secs\]' '{print $1}' | awk '{print $NF}' | awk '{sum+=$1; count++} END {print "平均GC时间:", sum/count, "秒"}'
fi

# ============================================
# 12. 生成错误报告
# ============================================

echo -e "\n12. 生成错误报告"
REPORT_FILE="output/error_report_$(date +%Y%m%d_%H%M%S).txt"

cat > $REPORT_FILE << EOF
=== 错误分析报告 ===
生成时间: $(date)

总错误数: $(grep -c " ERROR " $LOG_FILE)
警告数: $(grep -c " WARN " $LOG_FILE)

主要错误类型:
$(grep -o "java\.[a-z.]*Exception\|java\.[a-z.]*Error" $LOG_FILE | sort | uniq -c | sort -rn | head -5)

最近10条错误:
$(grep " ERROR " $LOG_FILE | tail -10)
EOF

echo "报告已生成: $REPORT_FILE"
cat $REPORT_FILE
```

### 实时监控脚本 (monitor_logs.sh)
```bash
#!/bin/bash

LOG_FILE="data/application.log"

echo "=== 实时日志监控 ==="
echo "监控文件: $LOG_FILE"
echo "按 Ctrl+C 停止监控"
echo ""

# 实时监控错误
tail -f $LOG_FILE | while read line; do
    if echo "$line" | grep -q " ERROR "; then
        echo "[ERROR] $line"
    elif echo "$line" | grep -q " WARN "; then
        echo "[WARN]  $line"
    fi
done
```

## 运行方式

```bash
# 创建输出目录
mkdir -p output

# 添加执行权限
chmod +x analyze_logs.sh monitor_logs.sh

# 运行分析脚本
./analyze_logs.sh

# 运行监控脚本（实时）
./monitor_logs.sh
```

## 预期结果

### 日志级别统计
```
INFO: 4
WARN: 1
ERROR: 3
```

### 异常类型统计
```
2 OutOfMemoryError
1 NullPointerException
1 SQLException
```

### 错误报告
```
=== 错误分析报告 ===
总错误数: 3
警告数: 1

主要错误类型:
2 OutOfMemoryError
1 NullPointerException
1 SQLException
```

## 学习要点

1. **日志查看**：tail、grep、awk
2. **错误统计**：计数、分类、排序
3. **异常分析**：堆栈跟踪、异常类型
4. **时间分析**：按时间范围筛选
5. **性能分析**：慢请求、GC 分析
6. **报告生成**：自动化错误报告
