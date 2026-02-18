// Jenkinsfile - CI/CD Pipeline

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
        ansiColor('xterm')
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
