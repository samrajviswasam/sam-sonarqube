pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/samrajviswasam/sam-sonarqube.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    withCredentials([
                        string(
                            credentialsId: 'sonarqube-token',
                            variable: 'SONAR_TOKEN'
                        )
                    ]) {
                        sh '''
                            docker run --rm \
                            --network devops-network \
                            -e SONAR_HOST_URL="http://sonarqube:9000" \
                            -e SONAR_TOKEN="$SONAR_TOKEN" \
                            -v "$WORKSPACE:/usr/src" \
                            -w /usr/src \
                            sonarsource/sonar-scanner-cli
                        '''
                    }
                }
            }
        }

    }
}
