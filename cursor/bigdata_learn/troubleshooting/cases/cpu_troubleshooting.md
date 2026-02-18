# 案例3：CPU 问题排查

## 案例描述
学习排查 Java 应用的 CPU 高占用问题。

## 排查脚本

### CPU 监控脚本 (monitor_cpu.sh)
```bash
#!/bin/bash

echo "=== Java 应用 CPU 监控 ==="

# ============================================
# 1. 查找 Java 进程
# ============================================

echo -e "\n1. 查找 Java 进程"
JAVA_PID=$(jps -l | grep -i "Application\|Main" | awk '{print $1}' | head -1)

if [ -z "$JAVA_PID" ]; then
    echo "未找到 Java 进程"
    exit 1
fi

echo "Java 进程 PID: $JAVA_PID"

# ============================================
# 2. 查看进程 CPU 使用
# ============================================

echo -e "\n2. 进程 CPU 使用率"
top -b -n 1 -p $JAVA_PID | tail -1

# ============================================
# 3. 查看线程 CPU 使用
# ============================================

echo -e "\n3. 线程 CPU 使用率（Top 10）"
top -H -b -n 1 -p $JAVA_PID | head -12

# ============================================
# 4. 获取高 CPU 线程 ID
# ============================================

echo -e "\n4. 高 CPU 线程（转换为16进制）"
HIGH_CPU_THREAD=$(top -H -b -n 1 -p $JAVA_PID | awk 'NR>7 && $9>10 {print $1; exit}')

if [ ! -z "$HIGH_CPU_THREAD" ]; then
    HEX_THREAD_ID=$(printf "%x" $HIGH_CPU_THREAD)
    echo "线程 ID (10进制): $HIGH_CPU_THREAD"
    echo "线程 ID (16进制): 0x$HEX_THREAD_ID"
    
    # ============================================
    # 5. 查看线程堆栈
    # ============================================
    
    echo -e "\n5. 高 CPU 线程堆栈"
    jstack $JAVA_PID | grep -A 20 "$HEX_THREAD_ID"
else
    echo "未发现高 CPU 线程"
fi

# ============================================
# 6. 查看所有线程状态
# ============================================

echo -e "\n6. 线程状态统计"
jstack $JAVA_PID | grep "java.lang.Thread.State" | sort | uniq -c | sort -rn

# ============================================
# 7. 查找 RUNNABLE 线程
# ============================================

echo -e "\n7. RUNNABLE 线程详情（可能消耗 CPU）"
jstack $JAVA_PID | grep -B 5 "RUNNABLE" | head -30

# ============================================
# 8. 系统 CPU 使用
# ============================================

echo -e "\n8. 系统 CPU 使用率"
top -b -n 1 | head -5
echo ""
vmstat 1 3

# ============================================
# 9. 生成 CPU 分析报告
# ============================================

echo -e "\n9. 生成 CPU 分析报告"
REPORT_FILE="output/cpu_report_$(date +%Y%m%d_%H%M%S).txt"

cat > $REPORT_FILE << EOF
=== CPU 分析报告 ===
生成时间: $(date)

进程 CPU 使用:
$(top -b -n 1 -p $JAVA_PID | tail -1)

线程 CPU Top 10:
$(top -H -b -n 1 -p $JAVA_PID | head -12)

线程状态统计:
$(jstack $JAVA_PID | grep "java.lang.Thread.State" | sort | uniq -c | sort -rn)

系统 CPU:
$(top -b -n 1 | head -5)
EOF

echo "报告已生成: $REPORT_FILE"
```

### CPU 问题定位脚本 (locate_cpu_issue.sh)
```bash
#!/bin/bash

echo "=== CPU 问题定位 ==="

JAVA_PID=$(jps -l | grep -i "Application\|Main" | awk '{print $1}' | head -1)

if [ -z "$JAVA_PID" ]; then
    echo "未找到 Java 进程"
    exit 1
fi

echo "监控进程: $JAVA_PID"
echo "每5秒采样一次，共10次"
echo ""

# ============================================
# 持续监控 CPU 使用
# ============================================

for i in {1..10}; do
    echo "=== 采样 $i ($(date +%H:%M:%S)) ==="
    
    # 进程 CPU
    CPU_USAGE=$(top -b -n 1 -p $JAVA_PID | tail -1 | awk '{print $9}')
    echo "进程 CPU: ${CPU_USAGE}%"
    
    # 高 CPU 线程
    HIGH_THREAD=$(top -H -b -n 1 -p $JAVA_PID | awk 'NR>7 && $9>5 {print $1, $9, $NF; exit}')
    if [ ! -z "$HIGH_THREAD" ]; then
        THREAD_ID=$(echo $HIGH_THREAD | awk '{print $1}')
        THREAD_CPU=$(echo $HIGH_THREAD | awk '{print $2}')
        THREAD_NAME=$(echo $HIGH_THREAD | awk '{print $3}')
        HEX_ID=$(printf "%x" $THREAD_ID)
        
        echo "高 CPU 线程: PID=$THREAD_ID (0x$HEX_ID), CPU=${THREAD_CPU}%, NAME=$THREAD_NAME"
        
        # 获取线程堆栈
        echo "线程堆栈:"
        jstack $JAVA_PID | grep -A 15 "0x$HEX_ID" | head -10
    fi
    
    echo ""
    sleep 5
done

# ============================================
# 分析总结
# ============================================

echo "=== 分析总结 ==="
echo "1. 如果 CPU 持续高，检查线程堆栈中的代码"
echo "2. 关注 RUNNABLE 状态的线程"
echo "3. 检查是否有死循环或频繁计算"
echo "4. 检查 GC 是否频繁（可能导致 CPU 高）"
```

### 死循环检测脚本 (detect_loop.sh)
```bash
#!/bin/bash

echo "=== 死循环检测 ==="

JAVA_PID=$(jps -l | grep -i "Application\|Main" | awk '{print $1}' | head -1)

if [ -z "$JAVA_PID" ]; then
    echo "未找到 Java 进程"
    exit 1
fi

echo "分析进程: $JAVA_PID"
echo ""

# ============================================
# 1. 查找 RUNNABLE 线程
# ============================================

echo "1. RUNNABLE 线程（可能正在执行）"
jstack $JAVA_PID | grep -B 5 "RUNNABLE" | grep -E "Thread|RUNNABLE|at " | head -30

# ============================================
# 2. 查找常见死循环模式
# ============================================

echo -e "\n2. 检查常见死循环模式"
THREAD_DUMP=$(jstack $JAVA_PID)

# 检查 while(true)
if echo "$THREAD_DUMP" | grep -q "while.*true"; then
    echo "发现 while(true) 循环"
    echo "$THREAD_DUMP" | grep -B 3 -A 3 "while.*true"
fi

# 检查 for(;;)
if echo "$THREAD_DUMP" | grep -q "for.*;;"; then
    echo "发现 for(;;) 循环"
    echo "$THREAD_DUMP" | grep -B 3 -A 3 "for.*;;"
fi

# ============================================
# 3. 分析线程执行的方法
# ============================================

echo -e "\n3. RUNNABLE 线程执行的方法"
jstack $JAVA_PID | grep -A 10 "RUNNABLE" | grep "at " | head -20

# ============================================
# 4. 统计方法调用频率
# ============================================

echo -e "\n4. 方法调用频率（Top 10）"
jstack $JAVA_PID | grep "at " | awk '{print $2}' | cut -d'(' -f1 | sort | uniq -c | sort -rn | head -10
```

## 运行方式

```bash
# 创建输出目录
mkdir -p output

# 添加执行权限
chmod +x monitor_cpu.sh locate_cpu_issue.sh detect_loop.sh

# 运行脚本（需要 Java 应用运行中）
./monitor_cpu.sh
./locate_cpu_issue.sh
./detect_loop.sh
```

## 预期结果

### 线程 CPU 使用
```
PID    USER  PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
12345  user  20   0  8.5g   2.1g  123m R 85.5  5.2   1:23.45 java
```

### 线程状态统计
```
45 RUNNABLE
12 TIMED_WAITING
8  WAITING
3  BLOCKED
```

### 高 CPU 线程堆栈
```
"http-nio-8080-exec-5" #45 daemon prio=5 os_prio=0 tid=0x00007f8b1c001000 nid=0x1234 runnable [0x00007f8b0c001000]
   java.lang.Thread.State: RUNNABLE
        at com.example.Service.processData(Service.java:45)
        at com.example.Controller.handleRequest(Controller.java:32)
```

## 学习要点

1. **CPU 监控**：top、htop、vmstat
2. **线程分析**：jstack、线程状态
3. **问题定位**：高 CPU 线程、堆栈分析
4. **死循环检测**：线程堆栈模式识别
5. **性能分析**：方法调用频率
6. **工具使用**：strace、perf
