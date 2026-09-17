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

                            echo "Finding files in workspace..."
                            find "$WORKSPACE" -maxdepth 2 -type f -print

                            echo "Checking SonarQube configuration..."
                            cat sonar-project.properties

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
                            -Dsonar.inclusions=app.py
                        '''
                    }
                }
            }
        }

    }
}
