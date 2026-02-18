# 案例4：系统管理

## 案例描述
学习 Shell 脚本在系统管理中的应用，包括进程管理、系统监控、定时任务等。

## 脚本示例

### 1. 进程管理 (process_management.sh)
```bash
#!/bin/bash

# ============================================
# 查看进程
# ============================================

echo "=== 查看所有进程 ==="
ps aux | head -n 5

# ============================================
# 查找特定进程
# ============================================

echo -e "\n=== 查找bash进程 ==="
ps aux | grep bash | grep -v grep

# ============================================
# 进程数量统计
# ============================================

echo -e "\n=== 进程统计 ==="
echo "总进程数: $(ps aux | wc -l)"
echo "用户进程数: $(ps aux | grep $USER | wc -l)"

# ============================================
# 后台运行进程
# ============================================

echo -e "\n=== 后台运行 ==="
sleep 5 &
echo "后台进程PID: $!"

# ============================================
# 等待进程完成
# ============================================

wait
echo "所有后台进程完成"
```

### 2. 系统监控 (system_monitor.sh)
```bash
#!/bin/bash

# ============================================
# CPU 使用率
# ============================================

echo "=== CPU 使用率 ==="
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1

# ============================================
# 内存使用情况
# ============================================

echo -e "\n=== 内存使用情况 ==="
free -h

# ============================================
# 磁盘使用情况
# ============================================

echo -e "\n=== 磁盘使用情况 ==="
df -h | head -n 5

# ============================================
# 系统负载
# ============================================

echo -e "\n=== 系统负载 ==="
uptime

# ============================================
# 生成监控报告
# ============================================

generate_report() {
    local report_file="output/system_report_$(date +%Y%m%d_%H%M%S).txt"
    
    cat > "$report_file" << EOF
=== 系统监控报告 ===
生成时间: $(date)

CPU 使用率:
$(top -bn1 | grep "Cpu(s)")

内存使用:
$(free -h)

磁盘使用:
$(df -h)

系统负载:
$(uptime)
EOF
    
    echo "报告已生成: $report_file"
}

generate_report
```

### 3. 文件系统操作 (filesystem.sh)
```bash
#!/bin/bash

# ============================================
# 查找大文件
# ============================================

echo "=== 查找大于10MB的文件 ==="
find . -type f -size +10M 2>/dev/null | head -n 5

# ============================================
# 查找空文件
# ============================================

echo -e "\n=== 查找空文件 ==="
find . -type f -empty 2>/dev/null | head -n 5

# ============================================
# 查找最近修改的文件
# ============================================

echo -e "\n=== 最近24小时修改的文件 ==="
find . -type f -mtime -1 2>/dev/null | head -n 5

# ============================================
# 统计文件类型
# ============================================

echo -e "\n=== 统计文件类型 ==="
echo "Shell脚本: $(find . -name "*.sh" 2>/dev/null | wc -l)"
echo "文本文件: $(find . -name "*.txt" 2>/dev/null | wc -l)"
echo "CSV文件: $(find . -name "*.csv" 2>/dev/null | wc -l)"

# ============================================
# 清理临时文件
# ============================================

cleanup_temp() {
    echo "=== 清理临时文件 ==="
    find . -name "*.tmp" -type f -delete 2>/dev/null
    find . -name "*~" -type f -delete 2>/dev/null
    echo "清理完成"
}

cleanup_temp
```

### 4. 日志管理 (log_management.sh)
```bash
#!/bin/bash

mkdir -p output/logs

# ============================================
# 日志轮转
# ============================================

rotate_log() {
    local log_file=$1
    local max_size=1000  # KB
    
    if [ -f "$log_file" ]; then
        local size=$(du -k "$log_file" | cut -f1)
        if [ $size -gt $max_size ]; then
            mv "$log_file" "${log_file}.$(date +%Y%m%d)"
            touch "$log_file"
            echo "日志已轮转: $log_file"
        fi
    fi
}

# ============================================
# 分析日志
# ============================================

analyze_log() {
    local log_file=$1
    
    if [ ! -f "$log_file" ]; then
        echo "日志文件不存在: $log_file"
        return
    fi
    
    echo "=== 日志分析: $log_file ==="
    echo "总行数: $(wc -l < $log_file)"
    echo "ERROR数量: $(grep -c ERROR $log_file)"
    echo "WARN数量: $(grep -c WARN $log_file)"
    echo "INFO数量: $(grep -c INFO $log_file)"
}

# ============================================
# 提取错误日志
# ============================================

extract_errors() {
    local log_file=$1
    local output_file="output/logs/errors_$(date +%Y%m%d).txt"
    
    grep "ERROR" "$log_file" > "$output_file"
    echo "错误日志已提取到: $output_file"
}

# 使用示例
if [ -f "data/log.txt" ]; then
    analyze_log "data/log.txt"
    extract_errors "data/log.txt"
fi
```

### 5. 定时任务示例 (cron_example.sh)
```bash
#!/bin/bash

# ============================================
# 定时任务脚本示例
# ============================================

# 这个脚本可以添加到 crontab
# crontab -e
# 添加: */5 * * * * /path/to/cron_example.sh

LOG_FILE="output/cron.log"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查磁盘空间
check_disk() {
    local usage=$(df -h / | awk 'NR==2 {print $5}' | cut -d'%' -f1)
    if [ $usage -gt 80 ]; then
        log_message "警告: 磁盘使用率超过80%"
    fi
}

# 检查内存
check_memory() {
    local mem_usage=$(free | awk 'NR==2 {printf "%.0f", $3*100/$2}')
    if [ $mem_usage -gt 90 ]; then
        log_message "警告: 内存使用率超过90%"
    fi
}

# 执行检查
log_message "开始系统检查"
check_disk
check_memory
log_message "系统检查完成"
```

## 运行方式

```bash
# 创建输出目录
mkdir -p output/logs

# 添加执行权限
chmod +x process_management.sh system_monitor.sh filesystem.sh log_management.sh cron_example.sh

# 运行脚本
./process_management.sh
./system_monitor.sh
./filesystem.sh
./log_management.sh
./cron_example.sh
```

## crontab 配置示例

```bash
# 编辑 crontab
crontab -e

# 添加以下内容：
# 每5分钟执行一次
*/5 * * * * /path/to/cron_example.sh

# 每天凌晨2点执行
0 2 * * * /path/to/system_monitor.sh

# 每周一执行
0 0 * * 1 /path/to/log_management.sh
```

## 学习要点

1. **进程管理**：ps、grep、后台运行、wait
2. **系统监控**：top、free、df、uptime
3. **文件系统**：find、du、文件统计
4. **日志管理**：日志轮转、日志分析、错误提取
5. **定时任务**：crontab、定时执行
