pipeline {
    agent any

    stages {
        stage('Pull Code') {
            steps {
                script {
                    // Switch to the ccs user
                    sh 'sudo su - ccs -c "cd /home/ccs/merch-store && git pull"'
                }
            }
        }
        stage('Build and Deploy') {
            steps {
                script {
                    // Build and deploy using Docker Compose
                    sh 'sudo docker compose up --build -d'
                }
            }
        }
    }
}
