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
                    pip install pytest-playwright allure-pytest flake8 bandit pip-audit
                    playwright install chromium
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

        stage('Security - Bandit') {
            steps {
                sh '''
                    . venv/bin/activate
                    bandit -r . -x ./venv -f txt -o bandit-report.txt || true
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.txt', allowEmptyArchive: true
                }
            }
        }

        stage('Security - pip-audit') {
            steps {
                sh '''
                    . venv/bin/activate
                    sh 'pip-audit --local -f text -o pip-audit-report.txt'
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'pip-audit-report.txt', allowEmptyArchive: true
                }
            }
        }

        stage('Security - OWASP ZAP') {
            steps {
                sh 'docker run --user root --rm -v $(pwd):/zap/wrk/:rw ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t https://www.saucedemo.com -r zap_report.html || true'
            }
            post {
                always {
                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: '.', reportFiles: 'zap_report.html', reportName: 'OWASP ZAP Report', reportTitles: ''])
                }
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest test_saucedemo.py --browser=chromium --alluredir=allure-results
                '''
            }
        }

        stage('Run Performance Tests (k6)') {
            steps {
                sh 'k6 run -u 3 test_perf.js'
            }
        }
    }

   post {
        always {
            // Reporte de Allure
            allure includeProperties: false, jdk: '', properties: [], reportBuildPolicy: 'ALWAYS', results: [[path: 'allure-results']]
            
            // Reporte de k6 simplificado
            perfReport sourceDataFiles: 'k6-report.xml'
        }
    }
}
