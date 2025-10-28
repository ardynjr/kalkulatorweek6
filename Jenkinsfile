pipeline {
  agent any
  environment {
    IMAGE_NAME = 'ardyndocker/calc-app'
    REGISTRY  = 'https://index.docker.io/v1/'
    REGISTRY_CREDENTIALS = 'dockerhub-kalkulator'
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Install Dependencies') {
      steps {
        bat 'python --version'
        bat 'python -m pip install --upgrade pip'
        bat 'python -m pip install -r requirements.txt'
        bat 'python -m pip install pytest'
      }
    }

    stage('Unit Test') {
      steps {
        bat 'pytest -q'
      }
    }

    stage('Build Docker Image') {
      when { expression { currentBuild.currentResult == 'SUCCESS' } }
      steps {
        bat 'docker version'
        bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
      }
    }

    stage('Push Docker Image') {
      when { expression { currentBuild.currentResult == 'SUCCESS' } }
      steps {
        withCredentials([usernamePassword(credentialsId: env.REGISTRY_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          bat 'docker login -u %USER% -p %PASS%'
          bat 'docker push %IMAGE_NAME%:%BUILD_NUMBER%'
          bat 'docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest'
          bat 'docker push %IMAGE_NAME%:latest'
          bat 'docker logout'
        }
      }
    }
  }

  post {
    always { echo "Pipeline selesai: ${currentBuild.currentResult}" }
  }
}
