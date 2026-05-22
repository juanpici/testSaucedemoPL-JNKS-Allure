pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Navegador para Playwright')
        choice(name: 'K6_VUS', choices: ['3', '5', '10'], description: 'Usuarios virtuales concurrentes para K6')
    }

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
                    pip install pytest-playwright allure-pytest flake8
                    playwright install chromium firefox webkit
                '''
            }
        }

        stage('Code Quality (Lint)') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 .
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh """
                    . venv/bin/activate
                    pytest test_saucedemo.py --browser=${params.BROWSER} --alluredir=allure-results || true
                """
            }
        }

        stage('Run Performance Tests (k6)') {
            steps {
                sh "k6 run -u ${params.K6_VUS} test_perf.js"
            }
        }
    }

    post {
        always {
            // Reporte visual interactivo de Playwright
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            
            // Gráficos de tendencias históricas de rendimiento
            perfReport sourceDataFiles: 'k6-report.xml'
        }
    }
}
