# 案例5：综合故障排查

## 案例描述
学习综合故障排查流程，包括问题确认、信息收集、问题定位、解决方案。

## 故障场景

### 场景1：应用响应慢
- **现象**：接口响应时间超过5秒
- **影响**：用户体验差，部分请求超时

### 场景2：应用频繁重启
- **现象**：应用每隔几分钟重启一次
- **影响**：服务不稳定，数据丢失

### 场景3：内存持续增长
- **现象**：内存使用率持续上升，最终 OOM
- **影响**：应用崩溃，需要重启

## 排查脚本

### 综合排查脚本 (comprehensive_check.sh)
```bash
#!/bin/bash

echo "=== Java 应用综合故障排查 ==="

JAVA_PID=$(jps -l | grep -i "Application\|Main" | awk '{print $1}' | head -1)

if [ -z "$JAVA_PID" ]; then
    echo "未找到 Java 进程"
    exit 1
fi

echo "分析进程: $JAVA_PID"
REPORT_FILE="output/comprehensive_report_$(date +%Y%m%d_%H%M%S).txt"

# ============================================
# 1. 基本信息收集
# ============================================

echo -e "\n1. 基本信息收集"
echo "进程 PID: $JAVA_PID"
echo "启动时间: $(ps -o lstart= -p $JAVA_PID)"
echo "运行时长: $(ps -o etime= -p $JAVA_PID)"

# ============================================
# 2. 系统资源检查
# ============================================

echo -e "\n2. 系统资源检查"
echo "--- CPU 使用率 ---"
top -b -n 1 | head -5

echo -e "\n--- 内存使用 ---"
free -h

echo -e "\n--- 磁盘使用 ---"
df -h | head -5

echo -e "\n--- 负载 ---"
uptime

# ============================================
# 3. 进程资源使用
# ============================================

echo -e "\n3. 进程资源使用"
ps aux | grep $JAVA_PID | grep -v grep

# ============================================
# 4. JVM 信息
# ============================================

echo -e "\n4. JVM 信息"
echo "JVM 参数:"
jps -v | grep $JAVA_PID

echo -e "\n堆内存使用:"
jmap -heap $JAVA_PID 2>/dev/null | grep -A 5 "Heap Usage" | head -10

# ============================================
# 5. GC 统计
# ============================================

echo -e "\n5. GC 统计"
jstat -gcutil $JAVA_PID

# ============================================
# 6. 线程统计
# ============================================

echo -e "\n6. 线程统计"
THREAD_COUNT=$(jstack $JAVA_PID | grep -c "java.lang.Thread.State")
echo "线程总数: $THREAD_COUNT"

echo "线程状态:"
jstack $JAVA_PID | grep "java.lang.Thread.State" | sort | uniq -c | sort -rn

# ============================================
# 7. 死锁检测
# ============================================

echo -e "\n7. 死锁检测"
if jstack $JAVA_PID | grep -q "deadlock"; then
    echo "发现死锁！"
    jstack $JAVA_PID | grep -A 20 "deadlock"
else
    echo "未发现死锁"
fi

# ============================================
# 8. 错误日志检查
# ============================================

echo -e "\n8. 错误日志检查"
if [ -f "data/application.log" ]; then
    ERROR_COUNT=$(grep -c " ERROR " data/application.log)
    echo "错误日志数: $ERROR_COUNT"
    
    if [ $ERROR_COUNT -gt 0 ]; then
        echo "最近5条错误:"
        grep " ERROR " data/application.log | tail -5
    fi
fi

# ============================================
# 9. 网络连接检查
# ============================================

echo -e "\n9. 网络连接检查"
echo "监听端口:"
netstat -tuln | grep $JAVA_PID || ss -tuln | grep $JAVA_PID

echo -e "\n连接数:"
ESTABLISHED=$(netstat -an | grep ESTABLISHED | wc -l)
echo "ESTABLISHED 连接: $ESTABLISHED"

# ============================================
# 10. 生成综合报告
# ============================================

cat > $REPORT_FILE << EOF
=== Java 应用综合故障排查报告 ===
生成时间: $(date)

=== 1. 基本信息 ===
进程 PID: $JAVA_PID
启动时间: $(ps -o lstart= -p $JAVA_PID)
运行时长: $(ps -o etime= -p $JAVA_PID)

=== 2. 系统资源 ===
$(top -b -n 1 | head -5)

内存:
$(free -h)

磁盘:
$(df -h | head -5)

负载:
$(uptime)

=== 3. 进程资源 ===
$(ps aux | grep $JAVA_PID | grep -v grep)

=== 4. JVM 信息 ===
$(jps -v | grep $JAVA_PID)

=== 5. GC 统计 ===
$(jstat -gcutil $JAVA_PID)

=== 6. 线程统计 ===
线程总数: $THREAD_COUNT
$(jstack $JAVA_PID | grep "java.lang.Thread.State" | sort | uniq -c | sort -rn)

=== 7. 死锁检测 ===
$(if jstack $JAVA_PID | grep -q "deadlock"; then
    jstack $JAVA_PID | grep -A 20 "deadlock"
else
    echo "未发现死锁"
fi)

=== 8. 错误日志 ===
$(if [ -f "data/application.log" ]; then
    echo "错误数: $(grep -c " ERROR " data/application.log)"
    echo "最近错误:"
    grep " ERROR " data/application.log | tail -5
fi)

=== 9. 网络连接 ===
$(netstat -tuln | grep $JAVA_PID || ss -tuln | grep $JAVA_PID)
EOF

echo -e "\n综合报告已生成: $REPORT_FILE"
```

### 快速诊断脚本 (quick_diagnosis.sh)
```bash
#!/bin/bash

echo "=== 快速诊断 ==="

JAVA_PID=$(jps -l | grep -i "Application\|Main" | awk '{print $1}' | head -1)

if [ -z "$JAVA_PID" ]; then
    echo "❌ 未找到 Java 进程"
    exit 1
fi

echo "✓ Java 进程运行中: PID=$JAVA_PID"
echo ""

# ============================================
# 快速检查项
# ============================================

# 1. CPU 检查
CPU_USAGE=$(top -b -n 1 -p $JAVA_PID | tail -1 | awk '{print $9}')
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "⚠ CPU 使用率过高: ${CPU_USAGE}%"
else
    echo "✓ CPU 使用率正常: ${CPU_USAGE}%"
fi

# 2. 内存检查
MEM_USAGE=$(ps aux | grep $JAVA_PID | grep -v grep | awk '{print $4}')
if (( $(echo "$MEM_USAGE > 80" | bc -l) )); then
    echo "⚠ 内存使用率过高: ${MEM_USAGE}%"
else
    echo "✓ 内存使用率正常: ${MEM_USAGE}%"
fi

# 3. 线程检查
THREAD_COUNT=$(jstack $JAVA_PID | grep -c "java.lang.Thread.State")
if [ $THREAD_COUNT -gt 500 ]; then
    echo "⚠ 线程数过多: $THREAD_COUNT"
else
    echo "✓ 线程数正常: $THREAD_COUNT"
fi

# 4. 死锁检查
if jstack $JAVA_PID | grep -q "deadlock"; then
    echo "❌ 发现死锁！"
else
    echo "✓ 未发现死锁"
fi

# 5. GC 检查
FULL_GC_COUNT=$(jstat -gcutil $JAVA_PID | awk 'NR==2 {print $9}')
if [ ! -z "$FULL_GC_COUNT" ] && [ "$FULL_GC_COUNT" != "0.00" ]; then
    echo "⚠ Full GC 次数: $FULL_GC_COUNT"
else
    echo "✓ GC 正常"
fi

# 6. 错误日志检查
if [ -f "data/application.log" ]; then
    RECENT_ERRORS=$(grep " ERROR " data/application.log | tail -1)
    if [ ! -z "$RECENT_ERRORS" ]; then
        echo "⚠ 最近有错误日志"
        echo "   $RECENT_ERRORS"
    else
        echo "✓ 无最近错误日志"
    fi
fi

echo ""
echo "详细诊断请运行: ./comprehensive_check.sh"
```

## 运行方式

```bash
# 创建输出目录
mkdir -p output

# 添加执行权限
chmod +x comprehensive_check.sh quick_diagnosis.sh

# 运行脚本
./quick_diagnosis.sh
./comprehensive_check.sh
```

## 预期结果

### 快速诊断输出
```
✓ Java 进程运行中: PID=12345
✓ CPU 使用率正常: 25.5%
⚠ 内存使用率过高: 85.2%
✓ 线程数正常: 45
✓ 未发现死锁
⚠ Full GC 次数: 5
⚠ 最近有错误日志
   2024-01-15 09:00:00 ERROR Service - Database connection failed
```

### 综合报告
```
=== Java 应用综合故障排查报告 ===
生成时间: 2024-01-15 09:30:00

=== 1. 基本信息 ===
进程 PID: 12345
启动时间: Mon Jan 15 08:00:00 2024
运行时长: 01:30:00

=== 2. 系统资源 ===
...
```

## 学习要点

1. **系统化排查**：按流程收集信息
2. **多维度分析**：CPU、内存、线程、网络
3. **问题定位**：结合多个指标定位问题
4. **报告生成**：自动化生成排查报告
5. **快速诊断**：关键指标快速检查
6. **最佳实践**：建立排查流程和模板
