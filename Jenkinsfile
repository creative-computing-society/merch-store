pipeline {
    agent any

    stages {
        stage('Pull Code') {
            steps {
                script {
                    // Switch to ccs user and pull the latest code
                    sh 'sudo -u ccs git -C /home/ccs/merch-store pull'
                }
            }
        }
        stage('Build and Deploy') {
            steps {
                script {
                    // Build and deploy using Docker Compose
                    sh 'docker compose up --build -d'
                }
            }
        }
    }
}
