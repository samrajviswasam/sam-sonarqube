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

                            echo "Running SonarQube Scanner..."

                            docker run --rm \
                            --network devops-network \
                            -e SONAR_HOST_URL="http://sonarqube:9000" \
                            -e SONAR_TOKEN="$SONAR_TOKEN" \
                            -v "/var/lib/docker/volumes/jenkins_home/_data/workspace/sonarqube-demo-pipeline:/usr/src" \
                            -w /usr/src \
                            sonarsource/sonar-scanner-cli \
                            -Dsonar.projectKey=sonarqube-demo \
                            -Dsonar.projectName=sonarqube-demo \
                            -Dsonar.sources=. \
                            -Dsonar.exclusions=venv/**,__pycache__/**,*.pyc \
                            -Dsonar.python.version=3.12 \
                            -Dsonar.working.directory=/usr/src/.scannerwork

                            echo "Preparing SonarQube report for Jenkins..."

                            if [ -f .scannerwork/report-task.txt ]; then
                                cp .scannerwork/report-task.txt report-task.txt
                                echo "report-task.txt created successfully"
                            else
                                echo "ERROR: report-task.txt was not created"
                                exit 1
                            fi

                            ls -la report-task.txt
                        '''
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    echo "Building Docker image..."

                    docker build -t sonarqube-demo:1.0 .

                    echo "Docker image built successfully!"

                    docker images | grep sonarqube-demo
                '''
            }
        }

    }
}
