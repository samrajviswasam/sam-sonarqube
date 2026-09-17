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

        stage('Docker Run Test') {
            steps {
                sh '''
                    echo "Removing old test container if it exists..."

                    docker rm -f sonarqube-demo-test 2>/dev/null || true

                    echo "Starting Docker container..."

                    docker run -d \
                        --name sonarqube-demo-test \
                        --network devops-network \
                        sonarqube-demo:1.0

                    echo "Waiting for application to start..."

                    sleep 5

                    echo "Testing application..."

                    curl -f http://sonarqube-demo-test:5000/health

                    echo ""
                    echo "Docker application test successful!"

                    echo "Stopping test container..."

                    docker rm -f sonarqube-demo-test

                    echo "Docker Run Test completed successfully!"
                '''
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                sh '''
                    echo "Checking Kubernetes connection..."

                    kubectl version --client

                    kubectl get nodes

                    echo "Deploying application..."

                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml

                    echo "Kubernetes deployment completed!"

                    echo "Checking Deployment..."

                    kubectl get deployment sonarqube-demo

                    echo "Checking Pods..."

                    kubectl get pods -l app=sonarqube-demo

                    echo "Checking Service..."

                    kubectl get service sonarqube-demo-service
                '''
            }
        }

    }
}
