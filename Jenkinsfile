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
        // Ensure Homebrew tools (Python, git, chromedriver) are findable.
        // Covers Apple Silicon (/opt/homebrew) and Intel (/usr/local) Macs.
        PATH = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
        VENV = '.venv'
    }

    stages {
        stage('Verify Environment') {
            steps {
                sh '''
                    echo "=== PATH ==="
                    echo $PATH
                    echo "=== Which Python ==="
                    which python3 || echo "python3 not found"
                    python3 --version || echo "python3 --version failed"
                    echo "=== Chrome check ==="
                    ls -la "/Applications/Google Chrome.app" 2>/dev/null || echo "Chrome not at default path"
                '''
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv ${VENV}
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip list
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
                    pytest ${MARKER_FLAG} \
                        --browser=${BROWSER} \
                        --headless \
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
            archiveArtifacts artifacts: 'reports/**, screenshots/**, allure-results/**',
                           allowEmptyArchive: true,
                           fingerprint: true

            junit testResults: 'reports/junit.xml', allowEmptyResults: true

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
            cleanWs()
        }
    }
}
