#!/bin/bash
# monitoring.sh - 监控脚本

APP_NAME="myapp"
HEALTH_URL="http://localhost:8080/actuator/health"
METRICS_URL="http://localhost:8080/actuator/metrics"
ALERT_EMAIL="admin@example.com"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 告警函数
send_alert() {
    local level=$1
    local message=$2
    echo -e "${RED}[ALERT ${level}]${NC} $message"
    # 发送邮件告警
    # echo "$message" | mail -s "[${level}] ${APP_NAME} Alert" $ALERT_EMAIL
}

# 健康检查
check_health() {
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 $HEALTH_URL)
    
    if [ "$HTTP_CODE" = "200" ]; then
        RESPONSE=$(curl -s $HEALTH_URL)
        if echo "$RESPONSE" | grep -q '"status":"UP"'; then
            echo -e "${GREEN}✓${NC} Health check: OK"
            return 0
        fi
    fi
    
    send_alert "CRITICAL" "Health check failed (HTTP $HTTP_CODE)"
    return 1
}

# 获取 JVM 内存使用
check_memory() {
    MEMORY_USED=$(curl -s $METRICS_URL/jvm.memory.used?tag=area:heap 2>/dev/null | \
        grep -o '"value":[0-9]*' | head -1 | cut -d: -f2)
    MEMORY_MAX=$(curl -s $METRICS_URL/jvm.memory.max?tag=area:heap 2>/dev/null | \
        grep -o '"value":[0-9]*' | head -1 | cut -d: -f2)
    
    if [ -n "$MEMORY_USED" ] && [ -n "$MEMORY_MAX" ]; then
        USAGE_PERCENT=$((MEMORY_USED * 100 / MEMORY_MAX))
        echo "Memory usage: ${USAGE_PERCENT}%"
        
        if [ $USAGE_PERCENT -gt 90 ]; then
            send_alert "CRITICAL" "Memory usage is ${USAGE_PERCENT}% (above 90%)"
            return 1
        elif [ $USAGE_PERCENT -gt 80 ]; then
            send_alert "WARNING" "Memory usage is ${USAGE_PERCENT}% (above 80%)"
            return 0
        fi
    fi
    return 0
}

# 检查 CPU 使用
check_cpu() {
    CPU_USAGE=$(top -bn1 | grep "java" | awk '{print $9}' | head -1 | cut -d. -f1)
    
    if [ -n "$CPU_USAGE" ]; then
        echo "CPU usage: ${CPU_USAGE}%"
        
        if [ $CPU_USAGE -gt 80 ]; then
            send_alert "WARNING" "CPU usage is ${CPU_USAGE}% (above 80%)"
            return 1
        fi
    fi
    return 0
}

# 检查磁盘空间
check_disk() {
    DISK_USAGE=$(df -h /opt | awk 'NR==2 {print $5}' | sed 's/%//')
    echo "Disk usage: ${DISK_USAGE}%"
    
    if [ $DISK_USAGE -gt 90 ]; then
        send_alert "CRITICAL" "Disk usage is ${DISK_USAGE}% (above 90%)"
        return 1
    elif [ $DISK_USAGE -gt 80 ]; then
        send_alert "WARNING" "Disk usage is ${DISK_USAGE}% (above 80%)"
        return 0
    fi
    return 0
}

# 检查响应时间
check_response_time() {
    RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" --max-time 5 $HEALTH_URL)
    
    if [ -n "$RESPONSE_TIME" ]; then
        # 转换为毫秒
        RESPONSE_MS=$(echo "$RESPONSE_TIME * 1000" | bc | cut -d. -f1)
        echo "Response time: ${RESPONSE_MS}ms"
        
        if [ $RESPONSE_MS -gt 1000 ]; then
            send_alert "WARNING" "Response time is ${RESPONSE_MS}ms (above 1000ms)"
            return 1
        fi
    fi
    return 0
}

# 主函数
main() {
    echo "=== Monitoring Check for ${APP_NAME} ==="
    echo ""
    
    local exit_code=0
    
    check_health || exit_code=1
    echo ""
    
    check_memory || exit_code=1
    echo ""
    
    check_cpu || exit_code=1
    echo ""
    
    check_disk || exit_code=1
    echo ""
    
    check_response_time || exit_code=1
    echo ""
    
    echo "=== Monitoring Check Completed ==="
    
    exit $exit_code
}

main
