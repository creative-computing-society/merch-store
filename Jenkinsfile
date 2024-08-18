pipeline {
    agent any

    stages {
        stage('Pull Code') {
            steps {
                script {
                    sh 'sudo -u ccs git -C /home/ccs/merch-store pull'
                }
            }
        }
        stage('Build and Deploy') {
            steps {
                script {
                    sh '''
                    cd /home/ccs/merch-store
                    docker compose up --build -d
                    '''
                }
            }
        }
    }
}
