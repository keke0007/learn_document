#!/bin/bash
# deploy.sh - Java 应用部署脚本

set -e  # 遇到错误立即退出

# 配置变量
APP_NAME="myapp"
APP_VERSION="${1:-latest}"
APP_HOME="/opt/apps/${APP_NAME}"
JAR_FILE="${APP_NAME}.jar"
PID_FILE="/var/run/${APP_NAME}.pid"
LOG_FILE="${APP_HOME}/logs/deploy.log"
BACKUP_DIR="${APP_HOME}/backups"
JAVA_HOME="/usr/lib/jvm/java-11-openjdk"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

# 检查服务是否运行
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null 2>&1; then
            return 0
        else
            rm -f $PID_FILE
            return 1
        fi
    fi
    return 1
}

# 停止服务
stop_service() {
    if ! is_running; then
        log_info "Service is not running"
        return 0
    fi
    
    PID=$(cat $PID_FILE)
    log_info "Stopping service (PID: $PID)..."
    
    # 优雅停止
    kill $PID
    
    # 等待停止
    for i in {1..30}; do
        if ! ps -p $PID > /dev/null 2>&1; then
            rm -f $PID_FILE
            log_info "Service stopped successfully"
            return 0
        fi
        sleep 1
    done
    
    # 强制停止
    log_warn "Force stopping service..."
    kill -9 $PID
    rm -f $PID_FILE
    log_info "Service force stopped"
}

# 备份当前版本
backup_current() {
    if [ -f "${APP_HOME}/lib/${JAR_FILE}" ]; then
        log_info "Backing up current version..."
        mkdir -p $BACKUP_DIR
        BACKUP_FILE="${BACKUP_DIR}/${JAR_FILE}.$(date +%Y%m%d_%H%M%S)"
        cp "${APP_HOME}/lib/${JAR_FILE}" "$BACKUP_FILE"
        log_info "Backup saved to $BACKUP_FILE"
    fi
}

# 下载新版本
download_version() {
    log_info "Downloading version ${APP_VERSION}..."
    
    # 从 Artifactory 下载
    DOWNLOAD_URL="http://artifactory.example.com/${APP_NAME}/${APP_VERSION}/${JAR_FILE}"
    
    if curl -f -o "${APP_HOME}/lib/${JAR_FILE}.new" "$DOWNLOAD_URL"; then
        mv "${APP_HOME}/lib/${JAR_FILE}.new" "${APP_HOME}/lib/${JAR_FILE}"
        log_info "Download completed"
        return 0
    else
        log_error "Download failed"
        return 1
    fi
}

# 启动服务
start_service() {
    log_info "Starting service..."
    
    # JVM 参数
    JAVA_OPTS="-Xms2g -Xmx4g"
    JAVA_OPTS="$JAVA_OPTS -XX:+UseG1GC"
    JAVA_OPTS="$JAVA_OPTS -XX:MaxGCPauseMillis=200"
    JAVA_OPTS="$JAVA_OPTS -XX:+HeapDumpOnOutOfMemoryError"
    JAVA_OPTS="$JAVA_OPTS -XX:HeapDumpPath=${APP_HOME}/logs/heapdump.hprof"
    
    # Spring Boot 参数
    SPRING_OPTS="--spring.profiles.active=prod"
    SPRING_OPTS="$SPRING_OPTS --server.port=8080"
    
    # 启动
    cd ${APP_HOME}
    nohup ${JAVA_HOME}/bin/java $JAVA_OPTS \
        -jar ${APP_HOME}/lib/${JAR_FILE} \
        $SPRING_OPTS \
        > ${APP_HOME}/logs/app.log 2>&1 &
    
    echo $! > $PID_FILE
    PID=$(cat $PID_FILE)
    log_info "Service started with PID $PID"
    
    # 等待启动
    sleep 5
    
    # 健康检查
    for i in {1..30}; do
        if curl -f http://localhost:8080/actuator/health > /dev/null 2>&1; then
            log_info "Service is healthy"
            return 0
        fi
        sleep 2
    done
    
    log_error "Health check failed"
    return 1
}

# 回滚
rollback() {
    log_info "Rolling back..."
    
    # 查找最新的备份
    LATEST_BACKUP=$(ls -t ${BACKUP_DIR}/${JAR_FILE}.* 2>/dev/null | head -1)
    
    if [ -z "$LATEST_BACKUP" ]; then
        log_error "No backup found for rollback"
        return 1
    fi
    
    log_info "Restoring from $LATEST_BACKUP"
    cp "$LATEST_BACKUP" "${APP_HOME}/lib/${JAR_FILE}"
    
    start_service
}

# 主部署流程
deploy() {
    log_info "Starting deployment of ${APP_NAME} version ${APP_VERSION}"
    
    # 1. 停止服务
    stop_service
    
    # 2. 备份当前版本
    backup_current
    
    # 3. 下载新版本
    if ! download_version; then
        log_error "Deployment failed: download error"
        rollback
        exit 1
    fi
    
    # 4. 启动服务
    if ! start_service; then
        log_error "Deployment failed: start error"
        rollback
        exit 1
    fi
    
    log_info "Deployment completed successfully"
}

# 主逻辑
case "$1" in
    deploy)
        deploy
        ;;
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        stop_service
        sleep 2
        start_service
        ;;
    status)
        if is_running; then
            PID=$(cat $PID_FILE)
            echo "Service is running (PID: $PID)"
            curl -s http://localhost:8080/actuator/health | jq .
        else
            echo "Service is not running"
        fi
        ;;
    rollback)
        stop_service
        rollback
        ;;
    *)
        echo "Usage: $0 {deploy [version]|start|stop|restart|status|rollback}"
        exit 1
        ;;
esac
