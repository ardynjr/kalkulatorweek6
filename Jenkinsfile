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

    stage('Run Unit Tests in Docker') {
      steps {
        // Gunakan Dockerfile.test untuk install deps dan menjalankan pytest
        bat '''
          docker build -t calc-test -f Dockerfile.test .
          docker run --rm calc-test
        '''
      }
    }

    stage('Build Production Image') {
      when { expression { currentBuild.currentResult == 'SUCCESS' } }
      steps {
        script {
          docker.build("${IMAGE_NAME}:${env.BUILD_NUMBER}")
        }
      }
    }

    stage('Push Docker Image') {
      when { expression { currentBuild.currentResult == 'SUCCESS' } }
      steps {
        script {
          docker.withRegistry(env.REGISTRY, env.REGISTRY_CREDENTIALS) {
            def tag = "${IMAGE_NAME}:${env.BUILD_NUMBER}"
            docker.image(tag).push()
            docker.image(tag).push('latest')
          }
        }
      }
    }
  }

  post {
    always { echo 'Pipeline selesai dijalankan' }
    success { echo 'Build dan push berhasil!' }
    failure { echo 'Pipeline gagal! Periksa log untuk detail error.' }
  }
}
