pipeline {
    agent any
    options {
        disableConcurrentBuilds()
    }
    environment {
        PATH = "$PATH:/usr/local/bin"
    }
    stages {
        stage("关闭容器") {
            steps {
                // 当前stage报错时，设置构建结果为成功，保证后续stage继续执行
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    echo "==================关闭老版本容器=================="
                    sh label: "停止后端容器", script: "docker-compose down"
                }
            }
        }
        stage("环境清理") {
            steps {
                // 当前stage报错时，设置构建结果为成功，保证后续stage继续执行
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    echo "==================清理环境=================="
                    sh script: "docker rmi \$(docker images | grep 'none' | awk '{print \$3}')"
                    sh script: "docker stop \$(docker ps -a | grep 'Exited' | awk '{print \$1 }')"
                    sh script: "docker rm \$(docker ps -a | grep 'Exited' | awk '{print \$1 }')"
                }
            }
        }
        stage("收集后端静态文件") {
            steps {
                // 当前stage报错时，设置构建结果为成功，保证后续stage继续执行
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    echo "==================收集后端静态文件=================="
                    sh label: "构建镜像", script: "cd meiduo_mall && python3 manage.py collectstatic --noinput"
                }
            }
        }
        stage("构建容器") {
            steps {
                echo "==================构建后端服务器=================="
                // 在子目构建时，要用&&链接cd 的命令，因为每一个sh执行完之后，都会回到默认工作目录
                sh label: "构建镜像", script: "cd meiduo_mall && docker build -t meiduo_server:latest ."

                echo "==================构建前端服务器=================="
                sh label: "构建镜像", script: "cd meiduo_mall_frontend && docker build -t meiduo_web:latest ."
            }
        }
        stage("启动服务") {
            steps {
                echo "==================启动容器=================="
                sh label: "构建镜像", script: "docker-compose up -d"
            }
        }
    }
}
