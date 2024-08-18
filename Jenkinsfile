pipeline {
    agent any

    environment {
        WORKSPACE_DIR = '/home/ccs/merch_store'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    // Ensure the workspace directory exists and pull latest changes
                    dir(WORKSPACE_DIR) {
                        if (!fileExists('.git')) {
                            // Clone the repository if the .git directory does not exist
                            sh 'git clone https://github.com/creative-computing-society/merch-store.git .'
                        } else {
                            // Pull latest changes if the repository already exists
                            sh 'git pull origin main'
                        }
                    }
                }
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    // Change directory to the workspace and run docker compose
                    dir(WORKSPACE_DIR) {
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
