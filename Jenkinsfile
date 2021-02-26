pipeline {
    agent { docker { image 'python:3.7' } }
    stages {
        stage('test') {
            steps {
                sh 'echo "print(123)" | python'
                }
            }
        }
}