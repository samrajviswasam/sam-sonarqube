pipeline {
    agent any

    stages {

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
                            echo "Checking project files..."
                            ls -la

                            echo "Checking app.py..."
                            ls -l app.py

                            echo "Running SonarQube Scanner..."

                            docker run --rm \
                            --network devops-network \
                            -e SONAR_HOST_URL="http://sonarqube:9000" \
                            -e SONAR_TOKEN="$SONAR_TOKEN" \
                            -v "$WORKSPACE:/usr/src" \
                            -w /usr/src \
                            sonarsource/sonar-scanner-cli \
                            -Dsonar.projectKey=sonarqube-demo \
                            -Dsonar.projectName=sonarqube-demo \
                            -Dsonar.sources=. \
                            -Dsonar.exclusions=venv/**,__pycache__/**,*.pyc \
                            -Dsonar.python.version=3.12
                        '''
                    }
                }
            }
        }

    }
}
