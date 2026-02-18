# 监控和日志案例

## 案例概述

本案例通过实际配置演示监控和日志系统的搭建，包括 Prometheus、Grafana、ELK Stack 等。

## 知识点

1. **监控系统**
   - Prometheus 配置
   - Grafana 仪表板
   - 告警规则

2. **日志管理**
   - 日志收集
   - 日志聚合
   - 日志分析

## 案例代码

### 案例1：Prometheus 配置

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    environment: 'prod'

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'java-app'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['app:8080']
        labels:
          app: 'java-app'
          version: 'v1.0.0'
  
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
  
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
  
  - job_name: 'mysql-exporter'
    static_configs:
      - targets: ['mysql-exporter:9104']
```

### 案例2：告警规则

```yaml
# alerts.yml
groups:
  - name: java_app_alerts
    interval: 30s
    rules:
      - alert: HighMemoryUsage
        expr: jvm_memory_used_bytes{area="heap"} / jvm_memory_max_bytes{area="heap"} > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 90% for 5 minutes"
      
      - alert: HighCPUUsage
        expr: process_cpu_usage > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80% for 5 minutes"
      
      - alert: ApplicationDown
        expr: up{job="java-app"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Application is down"
          description: "Java application is not responding"
      
      - alert: HighErrorRate
        expr: rate(http_server_requests_seconds_count{status=~"5.."}[5m]) > 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate"
          description: "Error rate is above 10 requests/second"
```

### 案例3：日志收集配置

```yaml
# filebeat.yml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /opt/logs/*.log
    fields:
      app: java-app
      environment: production
    fields_under_root: true
    multiline.pattern: '^\d{4}-\d{2}-\d{2}'
    multiline.negate: true
    multiline.match: after

output.logstash:
  hosts: ["logstash:5044"]

# logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  if [app] == "java-app" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
    }
    date {
      match => [ "timestamp", "yyyy-MM-dd HH:mm:ss.SSS" ]
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "java-app-%{+YYYY.MM.dd}"
  }
}
```

### 案例4：监控脚本

```bash
#!/bin/bash
# monitoring.sh

APP_NAME="myapp"
HEALTH_URL="http://localhost:8080/actuator/health"
METRICS_URL="http://localhost:8080/actuator/metrics"

# 健康检查
check_health() {
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)
    if [ "$HTTP_CODE" = "200" ]; then
        echo "Health check: OK"
        return 0
    else
        echo "Health check: FAILED (HTTP $HTTP_CODE)"
        return 1
    fi
}

# 获取 JVM 内存使用
get_memory_usage() {
    MEMORY_USED=$(curl -s $METRICS_URL/jvm.memory.used | grep -o '"value":[0-9]*' | head -1 | cut -d: -f2)
    MEMORY_MAX=$(curl -s $METRICS_URL/jvm.memory.max | grep -o '"value":[0-9]*' | head -1 | cut -d: -f2)
    
    if [ -n "$MEMORY_USED" ] && [ -n "$MEMORY_MAX" ]; then
        USAGE_PERCENT=$((MEMORY_USED * 100 / MEMORY_MAX))
        echo "Memory usage: ${USAGE_PERCENT}%"
        
        if [ $USAGE_PERCENT -gt 90 ]; then
            echo "WARNING: Memory usage is above 90%"
            return 1
        fi
    fi
    return 0
}

# 获取 CPU 使用
get_cpu_usage() {
    CPU_USAGE=$(top -bn1 | grep "java" | awk '{print $9}' | head -1)
    if [ -n "$CPU_USAGE" ]; then
        echo "CPU usage: ${CPU_USAGE}%"
        
        CPU_INT=${CPU_USAGE%.*}
        if [ $CPU_INT -gt 80 ]; then
            echo "WARNING: CPU usage is above 80%"
            return 1
        fi
    fi
    return 0
}

# 检查磁盘空间
check_disk_space() {
    DISK_USAGE=$(df -h /opt | awk 'NR==2 {print $5}' | sed 's/%//')
    echo "Disk usage: ${DISK_USAGE}%"
    
    if [ $DISK_USAGE -gt 90 ]; then
        echo "WARNING: Disk usage is above 90%"
        return 1
    fi
    return 0
}

# 主函数
main() {
    echo "=== Monitoring Check for ${APP_NAME} ==="
    echo ""
    
    check_health
    echo ""
    
    get_memory_usage
    echo ""
    
    get_cpu_usage
    echo ""
    
    check_disk_space
    echo ""
    
    echo "=== Monitoring Check Completed ==="
}

main
```

## 验证数据

### 监控指标

| 指标 | 正常值 | 警告阈值 | 严重阈值 |
|-----|--------|---------|---------|
| CPU 使用率 | <70% | 70-80% | >80% |
| 内存使用率 | <80% | 80-90% | >90% |
| 响应时间 | <200ms | 200-500ms | >500ms |
| 错误率 | <1% | 1-5% | >5% |

### 日志统计

```
日志量：10GB/天
日志保留：30天
查询响应时间：<2s
```

## 总结

1. **监控系统**
   - 关键指标监控
   - 告警规则配置
   - 仪表板设计

2. **日志管理**
   - 集中收集
   - 结构化存储
   - 快速检索

3. **最佳实践**
   - 设置合理的告警阈值
   - 日志轮转和清理
   - 监控和日志联动
