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
                    pip install pytest-playwright allure-playwright
                    playwright install --with-deps chromium
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
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
