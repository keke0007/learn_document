# 自动化运维案例

## 案例概述

本案例通过实际脚本和配置演示自动化运维的实现，包括 Ansible、Terraform、自动化脚本等。

## 知识点

1. **配置管理**
   - Ansible Playbook
   - 批量操作
   - 配置同步

2. **基础设施即代码**
   - Terraform
   - 资源管理
   - 环境一致性

3. **自动化脚本**
   - 部署脚本
   - 备份脚本
   - 清理脚本

## 案例代码

### 案例1：Ansible Playbook

```yaml
# deploy.yml
- name: Deploy Java Application
  hosts: app_servers
  become: yes
  vars:
    app_name: myapp
    app_version: "1.0.0"
    app_home: "/opt/apps/{{ app_name }}"
  
  tasks:
    - name: Create application directory
      file:
        path: "{{ app_home }}"
        state: directory
        owner: appuser
        group: appgroup
        mode: '0755'
    
    - name: Create subdirectories
      file:
        path: "{{ app_home }}/{{ item }}"
        state: directory
        owner: appuser
        group: appgroup
      loop:
        - bin
        - lib
        - logs
        - config
    
    - name: Download application JAR
      get_url:
        url: "http://artifactory.example.com/{{ app_name }}/{{ app_version }}/{{ app_name }}.jar"
        dest: "{{ app_home }}/lib/{{ app_name }}.jar"
        owner: appuser
        group: appgroup
        mode: '0644'
    
    - name: Copy configuration files
      template:
        src: "{{ item }}.j2"
        dest: "{{ app_home }}/config/{{ item }}"
        owner: appuser
        group: appgroup
        mode: '0644'
      loop:
        - application.yml
        - logback.xml
    
    - name: Copy startup script
      template:
        src: start_service.sh.j2
        dest: "{{ app_home }}/bin/start_service.sh"
        owner: appuser
        group: appgroup
        mode: '0755'
    
    - name: Stop existing service
      systemd:
        name: "{{ app_name }}"
        state: stopped
      ignore_errors: yes
    
    - name: Reload systemd
      systemd:
        daemon_reload: yes
    
    - name: Start service
      systemd:
        name: "{{ app_name }}"
        state: started
        enabled: yes
    
    - name: Wait for service to be healthy
      uri:
        url: "http://localhost:8080/actuator/health"
        status_code: 200
      register: result
      until: result.status == 200
      retries: 30
      delay: 2
```

### 案例2：Terraform 配置

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "java-app-vpc"
  }
}

# Subnet
resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
  
  tags = {
    Name = "java-app-public-subnet"
  }
}

# Security Group
resource "aws_security_group" "app" {
  name        = "java-app-sg"
  description = "Security group for Java application"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "java-app-sg"
  }
}

# EC2 Instance
resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id
  
  vpc_security_group_ids = [aws_security_group.app.id]
  
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y java-11-openjdk
              # 部署脚本...
              EOF
  
  tags = {
    Name = "java-app-instance"
  }
}

# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "AMI ID"
  type        = string
}

variable "instance_type" {
  description = "Instance type"
  type        = string
  default     = "t3.medium"
}
```

### 案例3：自动化备份脚本

```bash
#!/bin/bash
# backup.sh

APP_NAME="myapp"
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# 创建备份目录
mkdir -p ${BACKUP_DIR}/${APP_NAME}

# 备份应用文件
tar -czf ${BACKUP_DIR}/${APP_NAME}/app_${DATE}.tar.gz \
    /opt/apps/${APP_NAME}/lib \
    /opt/apps/${APP_NAME}/config

# 备份数据库
mysqldump -u backup_user -p${DB_PASSWORD} myapp > \
    ${BACKUP_DIR}/${APP_NAME}/db_${DATE}.sql
gzip ${BACKUP_DIR}/${APP_NAME}/db_${DATE}.sql

# 备份日志（最近7天）
find /opt/logs -name "*.log" -mtime -7 | \
    tar -czf ${BACKUP_DIR}/${APP_NAME}/logs_${DATE}.tar.gz -T -

# 清理旧备份
find ${BACKUP_DIR}/${APP_NAME} -type f -mtime +${RETENTION_DAYS} -delete

# 上传到对象存储（可选）
# aws s3 cp ${BACKUP_DIR}/${APP_NAME}/ s3://backup-bucket/${APP_NAME}/ --recursive
```

### 案例4：自动化清理脚本

```bash
#!/bin/bash
# cleanup.sh

LOG_DIR="/opt/logs"
ARCHIVE_DIR="/opt/logs/archive"
RETENTION_DAYS=30

# 归档日志
find $LOG_DIR -name "*.log" -mtime +7 -exec gzip {} \;
find $LOG_DIR -name "*.log.gz" -exec mv {} $ARCHIVE_DIR/ \;

# 清理旧日志
find $ARCHIVE_DIR -name "*.log.gz" -mtime +${RETENTION_DAYS} -delete

# 清理临时文件
find /tmp -type f -mtime +1 -delete
find /var/tmp -type f -mtime +7 -delete

# 清理 Docker
docker system prune -f --volumes

# 清理旧镜像
docker image prune -a -f --filter "until=168h"
```

## 验证数据

### 自动化效果

| 操作 | 手动时间 | 自动化时间 | 提升 |
|-----|---------|-----------|------|
| 单服务器部署 | 30min | 5min | 83% |
| 批量部署（10台） | 5h | 15min | 95% |
| 配置同步 | 2h | 10min | 92% |

## 总结

1. **配置管理**
   - 使用 Ansible 批量操作
   - 配置版本控制
   - 环境一致性

2. **基础设施即代码**
   - 使用 Terraform 管理资源
   - 版本控制基础设施
   - 快速环境创建

3. **自动化脚本**
   - 定期备份
   - 自动清理
   - 监控和维护
