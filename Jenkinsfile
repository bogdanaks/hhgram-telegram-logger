pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                sh 'git pull origin master'
            }
        }
        stage('Prepare') {
            steps {
                sh 'cp /opt/hhgram/telegram-logger/.env /var/lib/jenkins/workspace/hhgram-telegram-logger/'
                sh 'cp /opt/hhgram/telegram-logger/1002359715140.session /var/lib/jenkins/workspace/hhgram-telegram-logger/'
            }
        }
        stage('Run docker-compose') {
            steps {
                script {
                    sh 'docker-compose stop'
                    sh 'docker-compose up --build -d'
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline finished'
        }
    }
}
