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

     post {
        success {
            mail to: 'abakshi_be23+merch_store@thapar.edu',
                 subject: "Pipeline Succeeded: ${currentBuild.fullDisplayName}",
                 body: "The pipeline completed successfully.\n\nJob: ${env.JOB_NAME}\nBuild Number: ${env.BUILD_NUMBER}\nURL: ${env.BUILD_URL}"
        }
        failure {
            mail to: 'abakshi_be23+merch_store@thapar.edu',
                 subject: "Pipeline Failed: ${currentBuild.fullDisplayName}",
                 body: "Something went wrong. Please check the Jenkins job for more details.\n\nJob: ${env.JOB_NAME}\nBuild Number: ${env.BUILD_NUMBER}\nURL: ${env.BUILD_URL}"
        }

    }
}
