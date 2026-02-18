# 案例2：内存问题排查

## 案例描述
学习排查 Java 应用的内存问题，包括内存溢出、内存泄漏等。

## 排查脚本

### 内存监控脚本 (monitor_memory.sh)
```bash
#!/bin/bash

echo "=== Java 应用内存监控 ==="

# ============================================
# 1. 查找 Java 进程
# ============================================

echo -e "\n1. 查找 Java 进程"
JAVA_PID=$(jps -l | grep -i "Application\|Main" | awk '{print $1}' | head -1)

if [ -z "$JAVA_PID" ]; then
    echo "未找到 Java 进程，请先启动应用"
    exit 1
fi

echo "Java 进程 PID: $JAVA_PID"

# ============================================
# 2. 查看进程内存使用
# ============================================

echo -e "\n2. 进程内存使用"
ps aux | grep $JAVA_PID | grep -v grep
echo ""
ps -o pid,rss,vsz,pmem,comm -p $JAVA_PID

# ============================================
# 3. 查看 JVM 堆内存
# ============================================

echo -e "\n3. JVM 堆内存使用"
jmap -heap $JAVA_PID 2>/dev/null | grep -A 10 "Heap Configuration\|Heap Usage"

# ============================================
# 4. 查看 GC 统计
# ============================================

echo -e "\n4. GC 统计（每5秒更新一次，共5次）"
for i in {1..5}; do
    echo "--- 第 $i 次统计 ---"
    jstat -gcutil $JAVA_PID
    sleep 5
done

# ============================================
# 5. 查看内存对象统计
# ============================================

echo -e "\n5. 内存对象统计（Top 10）"
jmap -histo $JAVA_PID 2>/dev/null | head -15

# ============================================
# 6. 生成堆转储
# ============================================

echo -e "\n6. 生成堆转储"
DUMP_FILE="output/heap_dump_$(date +%Y%m%d_%H%M%S).hprof"
jmap -dump:format=b,file=$DUMP_FILE $JAVA_PID 2>/dev/null

if [ -f "$DUMP_FILE" ]; then
    echo "堆转储已生成: $DUMP_FILE"
    echo "文件大小: $(du -h $DUMP_FILE | cut -f1)"
    echo "可以使用 jhat 或 Eclipse MAT 分析"
else
    echo "堆转储生成失败"
fi

# ============================================
# 7. 检查内存泄漏
# ============================================

echo -e "\n7. 检查内存泄漏（对比两次对象统计）"
echo "第一次统计:"
jmap -histo $JAVA_PID 2>/dev/null | head -20 > /tmp/histo1.txt
cat /tmp/histo1.txt

echo -e "\n等待10秒后再次统计..."
sleep 10

echo "第二次统计:"
jmap -histo $JAVA_PID 2>/dev/null | head -20 > /tmp/histo2.txt
cat /tmp/histo2.txt

echo -e "\n对象数量变化（重点关注持续增长的对象）:"
diff /tmp/histo1.txt /tmp/histo2.txt | grep "^>" | head -10
```

### 内存分析脚本 (analyze_memory.sh)
```bash
#!/bin/bash

echo "=== 内存问题分析 ==="

# ============================================
# 1. 检查 OutOfMemoryError
# ============================================

echo -e "\n1. 检查日志中的 OutOfMemoryError"
if [ -f "data/application.log" ]; then
    OOM_COUNT=$(grep -c "OutOfMemoryError" data/application.log)
    if [ $OOM_COUNT -gt 0 ]; then
        echo "发现 $OOM_COUNT 次 OutOfMemoryError"
        echo "错误详情:"
        grep -A 3 "OutOfMemoryError" data/application.log | head -20
    else
        echo "未发现 OutOfMemoryError"
    fi
fi

# ============================================
# 2. 分析 GC 日志
# ============================================

echo -e "\n2. 分析 GC 日志"
if [ -f "data/gc.log" ]; then
    echo "GC 次数: $(grep -c '\[GC' data/gc.log)"
    echo "Full GC 次数: $(grep -c '\[Full GC' data/gc.log)"
    
    echo -e "\nGC 时间统计:"
    grep "\[GC" data/gc.log | awk -F'secs\]' '{print $1}' | awk '{print $NF}' | \
        awk '{sum+=$1; count++; if($1>max) max=$1} END {
            if(count>0) {
                print "总GC时间:", sum, "秒"
                print "平均GC时间:", sum/count, "秒"
                print "最大GC时间:", max, "秒"
                print "GC次数:", count
            }
        }'
    
    echo -e "\nFull GC 详情:"
    grep "\[Full GC" data/gc.log | tail -5
fi

# ============================================
# 3. 检查系统内存
# ============================================

echo -e "\n3. 系统内存使用"
free -h

echo -e "\n4. 内存使用 Top 10 进程"
ps aux --sort=-%mem | head -11

# ============================================
# 4. 生成内存报告
# ============================================

echo -e "\n5. 生成内存分析报告"
REPORT_FILE="output/memory_report_$(date +%Y%m%d_%H%M%S).txt"

cat > $REPORT_FILE << EOF
=== 内存分析报告 ===
生成时间: $(date)

系统内存:
$(free -h)

Java 进程内存使用:
$(ps aux | grep java | grep -v grep | head -5)

GC 统计:
$(if [ -f "data/gc.log" ]; then
    echo "GC次数: $(grep -c '\[GC' data/gc.log)"
    echo "Full GC次数: $(grep -c '\[Full GC' data/gc.log)"
fi)
EOF

echo "报告已生成: $REPORT_FILE"
```

### 内存泄漏检测脚本 (detect_memory_leak.sh)
```bash
#!/bin/bash

echo "=== 内存泄漏检测 ==="

JAVA_PID=$(jps -l | grep -i "Application\|Main" | awk '{print $1}' | head -1)

if [ -z "$JAVA_PID" ]; then
    echo "未找到 Java 进程"
    exit 1
fi

echo "监控进程: $JAVA_PID"
echo "每30秒统计一次，共10次"
echo ""

# 记录初始内存
INITIAL_MEM=$(jmap -heap $JAVA_PID 2>/dev/null | grep "used" | head -1 | awk '{print $3}')

for i in {1..10}; do
    echo "=== 第 $i 次统计 ($(date +%H:%M:%S)) ==="
    
    # 当前内存
    CURRENT_MEM=$(jmap -heap $JAVA_PID 2>/dev/null | grep "used" | head -1 | awk '{print $3}')
    
    # GC 统计
    jstat -gcutil $JAVA_PID | awk 'NR==2 {
        printf "堆使用: %.2f%% | 老年代: %.2f%% | 元空间: %.2f%% | GC次数: %d\n", 
        $3, $4, $5, $7+$8
    }'
    
    # 对象统计（Top 5）
    echo "Top 5 对象:"
    jmap -histo $JAVA_PID 2>/dev/null | head -8 | tail -5
    
    echo ""
    sleep 30
done

echo "检测完成"
echo "如果内存持续增长且没有下降，可能存在内存泄漏"
```

## 运行方式

```bash
# 创建输出目录
mkdir -p output

# 添加执行权限
chmod +x monitor_memory.sh analyze_memory.sh detect_memory_leak.sh

# 运行脚本（需要 Java 应用运行中）
./monitor_memory.sh
./analyze_memory.sh
./detect_memory_leak.sh
```

## 预期结果

### 堆内存使用
```
Heap Configuration:
   MinHeapFreeRatio = 40
   MaxHeapFreeRatio = 70
   Heap Usage:
PS Young Generation
   used = 512M
   free = 1536M
```

### GC 统计
```
S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT
0.00   0.00  75.00  45.00  85.00  80.00     10     0.123     2     0.456    0.579
```

### 内存对象统计
```
num     #instances         #bytes  class name
----------------------------------------------
1:          1234         12345678  [B
2:           567          5678901  java.lang.String
3:           234          2345678  java.util.HashMap$Node
```

## 学习要点

1. **内存监控**：jmap、jstat、ps
2. **堆转储**：生成和分析堆转储
3. **GC 分析**：GC 日志分析、GC 统计
4. **内存泄漏**：对象统计对比、内存趋势
5. **问题定位**：OutOfMemoryError 分析
6. **工具使用**：jhat、Eclipse MAT
