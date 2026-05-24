pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: slave
spec:
  serviceAccountName: jenkins
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 80
        preference:
          matchExpressions:
          - key: workload-type
            operator: In
            values: ["ci"]
  containers:
  - name: kaniko
    image: gcr.m.daocloud.io/kaniko-project/executor:debug
    imagePullPolicy: IfNotPresent
    command: [sleep]
    args: ["99999"]
    volumeMounts:
    - name: registry-credentials
      mountPath: /kaniko/.docker
  - name: kubectl
    image: docker.m.daocloud.io/bitnami/kubectl:latest
    imagePullPolicy: IfNotPresent
    command: [sleep]
    args: ["99999"]
    securityContext:
      runAsUser: 0
  volumes:
  - name: registry-credentials
    secret:
      secretName: registry-credentials
      items:
      - key: .dockerconfigjson
        path: config.json
"""
        }
    }

    environment {
        REGISTRY = "172.20.55.169:31500"
        IMAGE = "172.20.55.169:31500/demo-app"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "构建号: ${BUILD_NUMBER}"'
            }
        }

        stage('Build & Push') {
            steps {
                container('kaniko') {
                    sh """
                        /kaniko/executor \
                          --context=dir://${WORKSPACE} \
                          --dockerfile=${WORKSPACE}/Dockerfile \
                          --destination=${IMAGE}:${BUILD_NUMBER} \
                          --destination=${IMAGE}:latest \
                          --insecure \
                          --skip-tls-verify \
                          --cache=false
                    """
                }
            }
        }

        stage('Deploy to Dev') {
            steps {
                container('kubectl') {
                    sh """
                        kubectl set image deployment/demo-app \
                          app=${IMAGE}:${BUILD_NUMBER} \
                          -n dev
                        kubectl rollout status deployment/demo-app \
                          -n dev --timeout=120s
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ 部署成功: ${IMAGE}:${BUILD_NUMBER}"
        }
        failure {
            echo "❌ 部署失败，请检查日志"
        }
    }
}
