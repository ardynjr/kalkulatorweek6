pipeline {
  agent any
  environment {
    IMAGE_NAME = 'ardyndocker/calc-app'
    REGISTRY  = 'https://index.docker.io/v1/'
    REGISTRY_CREDENTIALS = 'dockerhub-kalkulator'
  }
  stages {
    stage('Checkout'){ steps { checkout scm } }

    stage('Unit Test'){
      steps {
        sh 'python -V'
        sh 'pip install -r requirements.txt'
        sh 'pip install pytest'
        sh 'pytest -q'
      }
    }

    stage('Build Docker Image'){
      when { expression { currentBuild.currentResult == 'SUCCESS' } }
      steps {
        script { docker.build("${IMAGE_NAME}:${env.BUILD_NUMBER}") }
      }
    }

    stage('Push Docker Image'){
      when { expression { currentBuild.currentResult == 'SUCCESS' } }
      steps {
        script {
          docker.withRegistry(REGISTRY, REGISTRY_CREDENTIALS) {
            def tag = "${IMAGE_NAME}:${env.BUILD_NUMBER}"
            docker.image(tag).push()
            docker.image(tag).push('latest')
          }
        }
      }
    }
  }
  post {
    always { echo "Pipeline selesai: ${currentBuild.currentResult}" }
  }
}
