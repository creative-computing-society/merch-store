pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/creative-computing-society/merch-store.git', branch: 'main'
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    dir('/home/ccs/merch_store') {
                        sh 'sudo docker compose up --build -d'
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
        success {
            echo 'Pipeline succeeded'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
