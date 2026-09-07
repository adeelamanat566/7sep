
pipeline {

    agent any

    environment {
        IMAGE = 'adeelamanat56/guest-book'
        TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t $IMAGE:$TAG .'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                        -u "$DOCKER_USER" \
                        --password-stdin
                    '''
                }
            }
        }

        stage('Push') {
            steps {
                sh 'docker push $IMAGE:$TAG'
            }
        }

        stage('Run') {
            steps {
                sh '''
                    docker stop guest-book || true
                    docker rm guest-book || true

                    docker run -d \
                        --name guest-book \
                        -p 5000:5000 \
                        $IMAGE:$TAG
                '''
            }
        }
    }
}

