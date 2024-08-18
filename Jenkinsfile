pipeline {
    agent any

    stages {
        stage('Stash Local Changes') {
            steps {
                script {
                    sh 'sudo -u ccs git -C /home/ccs/merch-store stash'
                }
            }
        }
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
                    cd /home/ccs/merch-store/backend
                    sudo docker compose up --build -d
                    '''
                }
            }
        }
    }
}
