# 案例4：线程问题排查

## 案例描述
学习排查 Java 应用的线程问题，包括死锁、线程泄漏、线程阻塞等。

## 排查脚本

### 线程监控脚本 (monitor_threads.sh)
```bash
#!/bin/bash

echo "=== Java 应用线程监控 ==="

JAVA_PID=$(jps -l | grep -i "Application\|Main" | awk '{print $1}' | head -1)

if [ -z "$JAVA_PID" ]; then
    echo "未找到 Java 进程"
    exit 1
fi

echo "监控进程: $JAVA_PID"
echo ""

# ============================================
# 1. 查看线程总数
# ============================================

echo "1. 线程总数"
THREAD_COUNT=$(ps -eLf | grep $JAVA_PID | wc -l)
echo "系统线程数: $THREAD_COUNT"

JVM_THREAD_COUNT=$(jstack $JAVA_PID | grep "java.lang.Thread.State" | wc -l)
echo "JVM 线程数: $JVM_THREAD_COUNT"

# ============================================
# 2. 线程状态统计
# ============================================

echo -e "\n2. 线程状态统计"
jstack $JAVA_PID | grep "java.lang.Thread.State" | sort | uniq -c | sort -rn

# ============================================
# 3. 检测死锁
# ============================================

echo -e "\n3. 死锁检测"
DEADLOCK=$(jstack $JAVA_PID | grep -A 10 "deadlock")
if [ ! -z "$DEADLOCK" ]; then
    echo "发现死锁！"
    jstack $JAVA_PID | grep -A 20 "deadlock"
else
    echo "未发现死锁"
fi

# ============================================
# 4. 查找 BLOCKED 线程
# ============================================

echo -e "\n4. BLOCKED 线程（可能等待锁）"
BLOCKED_COUNT=$(jstack $JAVA_PID | grep -c "BLOCKED")
if [ $BLOCKED_COUNT -gt 0 ]; then
    echo "BLOCKED 线程数: $BLOCKED_COUNT"
    jstack $JAVA_PID | grep -B 5 -A 10 "BLOCKED" | head -30
else
    echo "未发现 BLOCKED 线程"
fi

# ============================================
# 5. 查找 WAITING 线程
# ============================================

echo -e "\n5. WAITING 线程（等待条件）"
WAITING_COUNT=$(jstack $JAVA_PID | grep -c "WAITING")
if [ $WAITING_COUNT -gt 0 ]; then
    echo "WAITING 线程数: $WAITING_COUNT"
    jstack $JAVA_PID | grep -B 5 -A 10 "WAITING" | head -30
fi

# ============================================
# 6. 线程泄漏检测
# ============================================

echo -e "\n6. 线程泄漏检测（对比两次线程数）"
echo "第一次统计:"
THREAD_COUNT_1=$(jstack $JAVA_PID | grep "java.lang.Thread.State" | wc -l)
echo "线程数: $THREAD_COUNT_1"

echo -e "\n等待30秒后再次统计..."
sleep 30

THREAD_COUNT_2=$(jstack $JAVA_PID | grep "java.lang.Thread.State" | wc -l)
echo "线程数: $THREAD_COUNT_2"

THREAD_DIFF=$((THREAD_COUNT_2 - THREAD_COUNT_1))
if [ $THREAD_DIFF -gt 10 ]; then
    echo "警告: 线程数增加了 $THREAD_DIFF，可能存在线程泄漏"
else
    echo "线程数变化: $THREAD_DIFF（正常范围）"
fi

# ============================================
# 7. 生成线程转储
# ============================================

echo -e "\n7. 生成线程转储"
THREAD_DUMP_FILE="output/thread_dump_$(date +%Y%m%d_%H%M%S).txt"
jstack $JAVA_PID > $THREAD_DUMP_FILE
echo "线程转储已保存: $THREAD_DUMP_FILE"
echo "文件大小: $(du -h $THREAD_DUMP_FILE | cut -f1)"
```

### 死锁检测脚本 (detect_deadlock.sh)
```bash
#!/bin/bash

echo "=== 死锁检测 ==="

JAVA_PID=$(jps -l | grep -i "Application\|Main" | awk '{print $1}' | head -1)

if [ -z "$JAVA_PID" ]; then
    echo "未找到 Java 进程"
    exit 1
fi

echo "分析进程: $JAVA_PID"
echo ""

# ============================================
# 1. 检查死锁
# ============================================

THREAD_DUMP=$(jstack $JAVA_PID)

if echo "$THREAD_DUMP" | grep -q "deadlock"; then
    echo "发现死锁！"
    echo ""
    
    # 提取死锁信息
    echo "死锁详情:"
    echo "$THREAD_DUMP" | sed -n '/deadlock/,/Found/p'
    
    # 提取死锁线程
    echo -e "\n死锁线程:"
    echo "$THREAD_DUMP" | grep -A 20 "deadlock" | grep -E "Thread|locked|waiting"
    
    # 保存死锁信息
    DEADLOCK_FILE="output/deadlock_$(date +%Y%m%d_%H%M%S).txt"
    echo "$THREAD_DUMP" | sed -n '/deadlock/,/Found/p' > $DEADLOCK_FILE
    echo -e "\n死锁信息已保存: $DEADLOCK_FILE"
else
    echo "未发现死锁"
    
    # 检查潜在死锁（大量 BLOCKED 线程）
    BLOCKED_COUNT=$(echo "$THREAD_DUMP" | grep -c "BLOCKED")
    if [ $BLOCKED_COUNT -gt 5 ]; then
        echo "警告: 发现 $BLOCKED_COUNT 个 BLOCKED 线程，可能存在锁竞争"
        echo "BLOCKED 线程详情:"
        echo "$THREAD_DUMP" | grep -B 5 -A 10 "BLOCKED" | head -40
    fi
fi
```

### 线程分析脚本 (analyze_threads.sh)
```bash
#!/bin/bash

echo "=== 线程分析 ==="

JAVA_PID=$(jps -l | grep -i "Application\|Main" | awk '{print $1}' | head -1)

if [ -z "$JAVA_PID" ]; then
    echo "未找到 Java 进程"
    exit 1
fi

THREAD_DUMP_FILE="output/thread_dump_$(date +%Y%m%d_%H%M%S).txt"
jstack $JAVA_PID > $THREAD_DUMP_FILE

echo "线程转储已保存: $THREAD_DUMP_FILE"
echo ""

# ============================================
# 1. 线程统计
# ============================================

echo "1. 线程统计"
echo "总线程数: $(grep -c "java.lang.Thread.State" $THREAD_DUMP_FILE)"
echo ""

echo "线程状态分布:"
grep "java.lang.Thread.State" $THREAD_DUMP_FILE | sort | uniq -c | sort -rn

# ============================================
# 2. 线程组统计
# ============================================

echo -e "\n2. 线程组统计（Top 10）"
grep '"' $THREAD_DUMP_FILE | grep "prio=" | awk -F'"' '{print $2}' | \
    awk '{print $1}' | sort | uniq -c | sort -rn | head -10

# ============================================
# 3. 等待的锁
# ============================================

echo -e "\n3. 等待的锁（Top 10）"
grep "waiting to lock" $THREAD_DUMP_FILE | awk -F'<' '{print $2}' | \
    awk -F'>' '{print $1}' | sort | uniq -c | sort -rn | head -10

# ============================================
# 4. 持有的锁
# ============================================

echo -e "\n4. 持有的锁（Top 10）"
grep "locked" $THREAD_DUMP_FILE | awk -F'<' '{print $2}' | \
    awk -F'>' '{print $1}' | sort | uniq -c | sort -rn | head -10

# ============================================
# 5. 线程执行的方法
# ============================================

echo -e "\n5. 线程执行的方法（Top 10）"
grep "at " $THREAD_DUMP_FILE | awk '{print $2}' | cut -d'(' -f1 | \
    sort | uniq -c | sort -rn | head -10

# ============================================
# 6. 生成分析报告
# ============================================

REPORT_FILE="output/thread_analysis_$(date +%Y%m%d_%H%M%S).txt"

cat > $REPORT_FILE << EOF
=== 线程分析报告 ===
生成时间: $(date)

线程统计:
总线程数: $(grep -c "java.lang.Thread.State" $THREAD_DUMP_FILE)

线程状态分布:
$(grep "java.lang.Thread.State" $THREAD_DUMP_FILE | sort | uniq -c | sort -rn)

线程组 Top 10:
$(grep '"' $THREAD_DUMP_FILE | grep "prio=" | awk -F'"' '{print $2}' | awk '{print $1}' | sort | uniq -c | sort -rn | head -10)

等待的锁 Top 10:
$(grep "waiting to lock" $THREAD_DUMP_FILE | awk -F'<' '{print $2}' | awk -F'>' '{print $1}' | sort | uniq -c | sort -rn | head -10)
EOF

echo -e "\n分析报告已生成: $REPORT_FILE"
```

## 运行方式

```bash
# 创建输出目录
mkdir -p output

# 添加执行权限
chmod +x monitor_threads.sh detect_deadlock.sh analyze_threads.sh

# 运行脚本（需要 Java 应用运行中）
./monitor_threads.sh
./detect_deadlock.sh
./analyze_threads.sh
```

## 预期结果

### 线程状态统计
```
45 RUNNABLE
12 TIMED_WAITING
8  WAITING
3  BLOCKED
```

### 死锁检测
```
发现死锁！

死锁线程:
"Thread-1" waiting for lock <0x000000076ab622d0>
"Thread-2" waiting for lock <0x000000076ab622e0>
```

### 线程组统计
```
15 http-nio-8080-exec
8  pool-1-thread
5  main
3  GC task thread
```

## 学习要点

1. **线程监控**：线程数、线程状态
2. **死锁检测**：jstack 死锁检测
3. **线程泄漏**：线程数趋势分析
4. **锁分析**：等待的锁、持有的锁
5. **线程转储**：生成和分析线程转储
6. **问题定位**：BLOCKED、WAITING 线程分析
