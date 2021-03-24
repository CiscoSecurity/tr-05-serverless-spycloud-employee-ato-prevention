pipeline {
  agent any
  stages {
    stage('build&test') {
      steps {
        sh 'docker build -t tr-05-spycloud-employee-ato-prevention .'
        sh 'docker run -d -p 9090:9090 --name tr-05-spycloud-employee-ato-prevention tr-05-spycloud-employee-ato-prevention'
        sh 'while true; do if docker logs tr-05-spycloud-employee-ato-prevention | grep "entered RUNNING state"; then break; else sleep 1; fi done'
        sh 'curl -X POST -sSLi http://localhost:9090 | grep "200 OK"'
      }
    }
  }
}