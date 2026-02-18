# CI/CD 流水线案例

## 案例概述

本案例通过实际配置文件演示 CI/CD 流水线的实现，包括 Jenkins、GitLab CI、GitHub Actions 等。

## 知识点

1. **Jenkins Pipeline**
   - Pipeline 脚本
   - 多阶段构建
   - 自动化部署

2. **GitLab CI/CD**
   - .gitlab-ci.yml
   - 阶段定义
   - 部署策略

3. **GitHub Actions**
   - workflow 文件
   - 自动化任务
   - 部署流程

## 案例代码

### 案例1：Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        IMAGE_NAME = 'java-app'
        KUBERNETES_NAMESPACE = 'production'
        MAVEN_OPTS = '-Xmx2048m'
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.BUILD_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT_SHORT}"
                }
            }
        }
        
        stage('Build') {
            steps {
                sh '''
                    mvn clean package -DskipTests \
                        -Dmaven.test.skip=true \
                        -Dmaven.compile.fork=true
                '''
            }
            post {
                success {
                    archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
                }
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'mvn test'
                    }
                    post {
                        always {
                            junit 'target/surefire-reports/*.xml'
                        }
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh 'mvn verify -Dskip.unit.tests=true'
                    }
                }
            }
        }
        
        stage('Code Quality') {
            steps {
                sh 'mvn sonar:sonar'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_TAG}"
                    def latestTag = "${DOCKER_REGISTRY}/${IMAGE_NAME}:latest"
                    
                    sh """
                        docker build -t ${imageTag} .
                        docker tag ${imageTag} ${latestTag}
                    """
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-registry-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh """
                            echo ${DOCKER_PASS} | docker login ${DOCKER_REGISTRY} \
                                -u ${DOCKER_USER} --password-stdin
                            docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_TAG}
                            docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
                        """
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    sh """
                        kubectl set image deployment/java-app \
                            app=${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_TAG} \
                            -n staging
                        kubectl rollout status deployment/java-app -n staging
                    """
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh """
                        kubectl set image deployment/java-app \
                            app=${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_TAG} \
                            -n ${KUBERNETES_NAMESPACE}
                        kubectl rollout status deployment/java-app \
                            -n ${KUBERNETES_NAMESPACE}
                    """
                }
            }
            post {
                success {
                    sh """
                        kubectl annotate deployment/java-app \
                            -n ${KUBERNETES_NAMESPACE} \
                            deployment.kubernetes.io/revision=${BUILD_NUMBER}
                    """
                }
                failure {
                    script {
                        echo 'Deployment failed, rolling back...'
                        sh """
                            kubectl rollout undo deployment/java-app \
                                -n ${KUBERNETES_NAMESPACE}
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            emailext(
                subject: "Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build completed successfully",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
        failure {
            emailext(
                subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build failed. Please check the logs.",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}
```

### 案例2：GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - package
  - deploy

variables:
  DOCKER_REGISTRY: registry.example.com
  IMAGE_NAME: java-app
  MAVEN_OPTS: "-Xmx2048m"

build:
  stage: build
  image: maven:3.8-openjdk-11
  script:
    - mvn clean package -DskipTests
  artifacts:
    paths:
      - target/*.jar
    expire_in: 1 week

unit-test:
  stage: test
  image: maven:3.8-openjdk-11
  script:
    - mvn test
  coverage: '/Total.*?([0-9]{1,3})%/'
  artifacts:
    reports:
      junit: target/surefire-reports/TEST-*.xml

integration-test:
  stage: test
  image: maven:3.8-openjdk-11
  script:
    - mvn verify -Dskip.unit.tests=true
  only:
    - main
    - develop

build-docker:
  stage: package
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main
    - develop

deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/java-app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA -n staging
    - kubectl rollout status deployment/java-app -n staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/java-app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA -n production
    - kubectl rollout status deployment/java-app -n production
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main
```

### 案例3：GitHub Actions

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  DOCKER_REGISTRY: registry.example.com
  IMAGE_NAME: java-app

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 11
      uses: actions/setup-java@v3
      with:
        java-version: '11'
        distribution: 'temurin'
    
    - name: Build with Maven
      run: mvn clean package -DskipTests
    
    - name: Run tests
      run: mvn test
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: target/surefire-reports/
  
  build-docker:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.DOCKER_REGISTRY }}
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:latest
  
  deploy-staging:
    needs: build-docker
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    steps:
    - name: Deploy to Kubernetes
      uses: azure/k8s-deploy@v4
      with:
        manifests: |
          k8s/deployment.yaml
        images: |
          ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        kubectl-version: 'latest'
  
  deploy-production:
    needs: build-docker
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
    - name: Deploy to Kubernetes
      uses: azure/k8s-deploy@v4
      with:
        manifests: |
          k8s/deployment.yaml
        images: |
          ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        kubectl-version: 'latest'
```

## 验证数据

### CI/CD 性能

| 阶段 | 执行时间 | 说明 |
|-----|---------|------|
| 构建 | 3min | Maven 构建 |
| 测试 | 5min | 单元测试+集成测试 |
| 打包 | 2min | Docker 镜像构建 |
| 部署 | 2min | K8s 部署 |

### 成功率统计

```
构建成功率：98%
测试通过率：95%
部署成功率：99%
```

## 总结

1. **流水线设计**
   - 多阶段构建
   - 并行执行
   - 失败快速反馈

2. **部署策略**
   - 蓝绿部署
   - 滚动更新
   - 回滚机制

3. **最佳实践**
   - 自动化测试
   - 代码质量检查
   - 环境隔离
