pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['smoke', 'regression', 'all'],
            description: 'Which test suite to run'
        )
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox'],
            description: 'Browser to run tests against'
        )
        string(
            name: 'BASE_URL',
            defaultValue: 'https://www.saucedemo.com',
            description: 'Application URL under test'
        )
    }

    environment {
        PYTHON = 'python3.12'
        VENV = '.venv'
        HEADLESS = 'true'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    ${PYTHON} -m venv ${VENV}
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . ${VENV}/bin/activate

                    if [ "${TEST_SUITE}" = "all" ]; then
                        MARKER_FLAG=""
                    else
                        MARKER_FLAG="-m ${TEST_SUITE}"
                    fi

                    BASE_URL=${BASE_URL} \
                    HEADLESS=${HEADLESS} \
                    pytest ${MARKER_FLAG} \
                        --browser=${BROWSER} \
                        -n 2 \
                        --reruns 1 \
                        --alluredir=allure-results \
                        --junitxml=reports/junit.xml \
                        || true
                '''
            }
        }
    }

    post {
        always {
            // Archive test artifacts even on failure
            archiveArtifacts artifacts: 'reports/**, screenshots/**, allure-results/**',
                           allowEmptyArchive: true,
                           fingerprint: true

            // Publish JUnit results so Jenkins shows pass/fail trends
            junit testResults: 'reports/junit.xml', allowEmptyResults: true

            // Publish the HTML report
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Pytest HTML Report'
            ])
        }
        success {
            echo '✅ All tests passed!'
        }
        failure {
            echo '❌ Build failed. Check test report and screenshots.'
        }
        cleanup {
            // Clean the workspace so next build starts fresh
            cleanWs()
        }
    }
}
