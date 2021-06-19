pipeline {
    agent any
    options {
        disableConcurrentBuilds()
    }
    stages {
        stage("关闭容器") {
            steps {
                // 当前stage报错时，设置构建结果为成功，保证后续stage继续执行
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    echo "==================关闭老版本容器=================="
                    sh label: "停止前端容器", script: "docker stop meiduo_server_1"
                    sh label: "停止后端容器", script: "docker stop meiduo_web_1"
                }
            }
        }
        stage("环境清理") {
            steps {
                // 当前stage报错时，设置构建结果为成功，保证后续stage继续执行
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    echo "==================开始环境清理工作=================="
                    sh script: "docker stop \$(docker ps -a | grep 'Exited' | awk '{print \$1 }')"
                    sh script: "docker rm \$(docker ps -a | grep 'Exited' | awk '{print \$1 }')"
                    sh script: "docker rmi \$(docker images | grep 'none' | awk '{print \$3}')"
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
        stage("启动后端服务器") {
            steps {
                echo "==================启动容器=================="
                sh label: "构建镜像", script: "docker-compose up -d"
            }
        }
    }
}
