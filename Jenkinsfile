pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install pytest-playwright allure-pytest
                    playwright install chromium
                '''
            }
        }

        stage('Run Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest test_saucedemo.py --alluredir=allure-results || true
                '''
            }
        }
    }

    post {
        always {
            // Esto va a compilar los resultados binarios en HTML interactivo
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
