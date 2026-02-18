# Java 服务故障排查学习知识点

## 目录
1. [故障排查基础](#1-故障排查基础)
2. [日志分析](#2-日志分析)
3. [进程和线程排查](#3-进程和线程排查)
4. [内存问题排查](#4-内存问题排查)
5. [CPU 问题排查](#5-cpu-问题排查)
6. [网络问题排查](#6-网络问题排查)
7. [JVM 问题排查](#7-jvm-问题排查)
8. [性能问题排查](#8-性能问题排查)
9. [案例与验证数据](#9-案例与验证数据)

---

## 1. 故障排查基础

### 1.1 故障排查流程
1. **问题确认**：确认问题现象和影响范围
2. **信息收集**：收集日志、监控数据、系统信息
3. **问题定位**：分析日志、检查资源、定位根因
4. **解决方案**：制定解决方案并实施
5. **验证和总结**：验证修复效果，总结经验

### 1.2 常用排查工具
- **系统工具**：top、htop、ps、netstat、ss
- **JVM 工具**：jps、jstack、jmap、jstat、jinfo
- **日志工具**：tail、grep、awk、sed
- **网络工具**：tcpdump、wireshark、curl
- **性能工具**：strace、perf、vmstat、iostat

### 1.3 排查原则
- 先看日志，再看监控
- 先看系统资源，再看应用
- 先看整体，再看细节
- 记录排查过程

---

## 2. 日志分析

### 2.1 日志位置
- **应用日志**：`/var/log/app/`、`logs/`
- **系统日志**：`/var/log/messages`、`/var/log/syslog`
- **JVM 日志**：GC 日志、JVM 崩溃日志

### 2.2 日志分析工具
```bash
# 实时查看日志
tail -f application.log

# 搜索错误
grep -i error application.log

# 统计错误数量
grep -c error application.log

# 查看最近100行
tail -n 100 application.log

# 按时间范围查看
grep "2024-01-15" application.log
```

### 2.3 常见日志模式
- **异常堆栈**：Exception、Error、Stack trace
- **性能问题**：slow query、timeout
- **资源问题**：OutOfMemoryError、Thread limit

---

## 3. 进程和线程排查

### 3.1 进程查看
```bash
# 查看 Java 进程
ps aux | grep java
jps -lvm

# 查看进程详情
ps -ef | grep java
top -p <pid>
```

### 3.2 线程排查
```bash
# 查看线程数
ps -eLf | grep java | wc -l

# JVM 线程转储
jstack <pid> > thread_dump.txt

# 查看线程状态
jstack <pid> | grep "java.lang.Thread.State"
```

### 3.3 线程问题
- **线程死锁**：使用 jstack 检测
- **线程泄漏**：线程数持续增长
- **线程阻塞**：大量线程处于 BLOCKED 状态

---

## 4. 内存问题排查

### 4.1 内存查看
```bash
# 查看进程内存
ps aux | grep java
top -p <pid>

# JVM 内存转储
jmap -dump:format=b,file=heap.hprof <pid>

# 查看堆内存使用
jmap -heap <pid>
jstat -gc <pid> 1000
```

### 4.2 内存问题类型
- **堆内存溢出**：OutOfMemoryError: Java heap space
- **方法区溢出**：OutOfMemoryError: Metaspace
- **直接内存溢出**：OutOfMemoryError: Direct buffer memory
- **内存泄漏**：内存持续增长

### 4.3 GC 分析
```bash
# 查看 GC 统计
jstat -gcutil <pid> 1000

# 分析 GC 日志
grep "GC" gc.log | tail -20
```

---

## 5. CPU 问题排查

### 5.1 CPU 查看
```bash
# 查看 CPU 使用率
top
htop
ps aux --sort=-%cpu | head

# 查看 Java 进程 CPU
top -p <pid>
```

### 5.2 CPU 高占用排查
```bash
# 查看线程 CPU 使用
top -H -p <pid>

# 线程转储分析
jstack <pid> | grep -A 10 "RUNNABLE"

# 查看系统调用
strace -p <pid>
```

### 5.3 CPU 问题原因
- **死循环**：代码逻辑问题
- **频繁 GC**：内存配置不当
- **线程竞争**：锁竞争激烈
- **计算密集**：算法效率低

---

## 6. 网络问题排查

### 6.1 网络连接查看
```bash
# 查看端口监听
netstat -tuln | grep java
ss -tuln | grep java

# 查看连接数
netstat -an | grep ESTABLISHED | wc -l
ss -s

# 查看网络统计
netstat -s
```

### 6.2 网络问题排查
```bash
# 抓包分析
tcpdump -i eth0 port 8080 -w capture.pcap

# 测试连接
telnet host port
curl -v http://host:port

# 查看防火墙
iptables -L
firewall-cmd --list-all
```

### 6.3 常见网络问题
- **连接超时**：网络不通、防火墙
- **连接数过多**：连接池配置
- **端口占用**：端口冲突
- **DNS 解析**：域名解析失败

---

## 7. JVM 问题排查

### 7.1 JVM 参数查看
```bash
# 查看 JVM 参数
jinfo <pid>
jps -v

# 查看系统属性
jinfo -sysprops <pid>
```

### 7.2 JVM 调优参数
```bash
# 堆内存
-Xms2g -Xmx2g

# 元空间
-XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=256m

# GC 参数
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200

# GC 日志
-Xloggc:gc.log -XX:+PrintGCDetails
```

### 7.3 JVM 崩溃分析
```bash
# 查看崩溃日志
cat hs_err_pid*.log

# 分析崩溃原因
grep -i "fatal" hs_err_pid*.log
```

---

## 8. 性能问题排查

### 8.1 性能指标
- **响应时间**：接口响应时间
- **吞吐量**：QPS、TPS
- **资源使用**：CPU、内存、IO
- **错误率**：4xx、5xx 错误

### 8.2 性能分析工具
```bash
# 系统性能
vmstat 1
iostat -x 1
sar -u 1

# 应用性能
jprofiler
arthas
```

### 8.3 性能优化
- **代码优化**：算法优化、减少循环
- **JVM 调优**：GC 优化、内存调优
- **数据库优化**：SQL 优化、索引
- **缓存优化**：Redis、本地缓存

---

## 9. 案例与验证数据

详见以下文件：
- [案例1：日志分析](cases/log_analysis.md)
- [案例2：内存问题排查](cases/memory_troubleshooting.md)
- [案例3：CPU 问题排查](cases/cpu_troubleshooting.md)
- [案例4：线程问题排查](cases/thread_troubleshooting.md)
- [案例5：综合故障排查](cases/comprehensive_troubleshooting.md)
- [验证数据文件](data/)
