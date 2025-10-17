pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.8'
        NODE_VERSION = '16'
        TEST_ENV = 'staging'
        BROWSER = 'chrome'
        HEADLESS = 'true'
    }
    
    options {
        timeout(time: 60, unit: 'MINUTES')
        timestamps()
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            parallel {
                stage('Python Setup') {
                    steps {
                        echo 'Setting up Python environment...'
                        sh '''
                            python --version
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
                
                stage('Node.js Setup') {
                    steps {
                        echo 'Setting up Node.js environment...'
                        sh '''
                            node --version
                            npm --version
                            npm install
                        '''
                    }
                }
            }
        }
        
        stage('Code Quality') {
            steps {
                echo 'Running code quality checks...'
                sh '''
                    pylint tests/ --disable=C0114,C0116 || true
                    black --check tests/ || true
                '''
            }
        }
        
        stage('Functional Tests') {
            parallel {
                stage('Smoke Tests') {
                    steps {
                        echo 'Running smoke tests...'
                        sh '''
                            pytest tests/functional/ -m smoke \
                                --html=reports/smoke_test_report.html \
                                --self-contained-html \
                                --json-report \
                                --json-report-file=reports/smoke_results.json \
                                --alluredir=reports/allure-results/smoke \
                                -v
                        '''
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'reports',
                                reportFiles: 'smoke_test_report.html',
                                reportName: 'Smoke Test Report'
                            ])
                        }
                    }
                }
                
                stage('Regression Tests') {
                    steps {
                        echo 'Running regression tests...'
                        sh '''
                            pytest tests/functional/ -m regression \
                                --html=reports/regression_test_report.html \
                                --self-contained-html \
                                --json-report \
                                --json-report-file=reports/regression_results.json \
                                --alluredir=reports/allure-results/regression \
                                -v
                        '''
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'reports',
                                reportFiles: 'regression_test_report.html',
                                reportName: 'Regression Test Report'
                            ])
                        }
                    }
                }
            }
        }
        
        stage('Device Tests') {
            parallel {
                stage('Desktop Tests') {
                    steps {
                        echo 'Running desktop browser tests...'
                        sh '''
                            pytest tests/device/ -m "chrome or firefox or edge" \
                                --html=reports/desktop_test_report.html \
                                --self-contained-html \
                                --json-report \
                                --json-report-file=reports/desktop_results.json \
                                --alluredir=reports/allure-results/desktop \
                                -v
                        '''
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'reports',
                                reportFiles: 'desktop_test_report.html',
                                reportName: 'Desktop Test Report'
                            ])
                        }
                    }
                }
                
                stage('Mobile Tests') {
                    steps {
                        echo 'Running mobile device tests...'
                        sh '''
                            pytest tests/device/ -m mobile \
                                --html=reports/mobile_test_report.html \
                                --self-contained-html \
                                --json-report \
                                --json-report-file=reports/mobile_results.json \
                                --alluredir=reports/allure-results/mobile \
                                -v
                        '''
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'reports',
                                reportFiles: 'mobile_test_report.html',
                                reportName: 'Mobile Test Report'
                            ])
                        }
                    }
                }
                
                stage('Tablet Tests') {
                    steps {
                        echo 'Running tablet device tests...'
                        sh '''
                            pytest tests/device/ -m tablet \
                                --html=reports/tablet_test_report.html \
                                --self-contained-html \
                                --json-report \
                                --json-report-file=reports/tablet_results.json \
                                --alluredir=reports/allure-results/tablet \
                                -v
                        '''
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'reports',
                                reportFiles: 'tablet_test_report.html',
                                reportName: 'Tablet Test Report'
                            ])
                        }
                    }
                }
            }
        }
        
        stage('Load Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                    changeRequest()
                }
            }
            steps {
                echo 'Running load tests...'
                script {
                    try {
                        sh '''
                            echo "Running baseline load test..."
                            k6 run tests/load/load_test_baseline.js
                        '''
                    } catch (Exception e) {
                        echo "Baseline load test failed: ${e.getMessage()}"
                        currentBuild.result = 'UNSTABLE'
                    }
                    
                    try {
                        sh '''
                            echo "Running stress load test..."
                            k6 run tests/load/load_test_stress.js
                        '''
                    } catch (Exception e) {
                        echo "Stress load test failed: ${e.getMessage()}"
                        currentBuild.result = 'UNSTABLE'
                    }
                    
                    try {
                        sh '''
                            echo "Running spike load test..."
                            k6 run tests/load/load_test_spike.js
                        '''
                    } catch (Exception e) {
                        echo "Spike load test failed: ${e.getMessage()}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'baseline_test_summary.html',
                        reportName: 'Baseline Load Test Report'
                    ])
                    
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'stress_test_summary.html',
                        reportName: 'Stress Load Test Report'
                    ])
                    
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'spike_test_summary.html',
                        reportName: 'Spike Load Test Report'
                    ])
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                echo 'Generating comprehensive test reports...'
                sh '''
                    # Generate Allure report
                    allure generate reports/allure-results --clean -o reports/allure-report
                    
                    # Generate combined HTML report
                    python scripts/generate_combined_report.py
                    
                    # Generate bug report
                    python scripts/generate_bug_report.py
                '''
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'allure-report/index.html',
                        reportName: 'Allure Test Report'
                    ])
                    
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'combined_test_report.html',
                        reportName: 'Combined Test Report'
                    ])
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh '''
                # Archive screenshots
                tar -czf screenshots_${BUILD_NUMBER}.tar.gz screenshots/ || true
                
                # Archive reports
                tar -czf reports_${BUILD_NUMBER}.tar.gz reports/ || true
            '''
            
            archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
            archiveArtifacts artifacts: 'screenshots/**/*', fingerprint: true
            
            // Clean workspace
            cleanWs()
        }
        
        success {
            echo 'Pipeline completed successfully!'
            emailext (
                subject: "✅ SwiftAssess QA Pipeline - SUCCESS (Build #${BUILD_NUMBER})",
                body: """
                <h2>SwiftAssess QA Pipeline - SUCCESS</h2>
                <p><strong>Build:</strong> #${BUILD_NUMBER}</p>
                <p><strong>Status:</strong> ✅ SUCCESS</p>
                <p><strong>Duration:</strong> ${currentBuild.durationString}</p>
                <p><strong>Branch:</strong> ${env.BRANCH_NAME}</p>
                
                <h3>Test Results:</h3>
                <ul>
                    <li>Functional Tests: ✅ Passed</li>
                    <li>Device Tests: ✅ Passed</li>
                    <li>Load Tests: ✅ Passed</li>
                </ul>
                
                <p><a href="${BUILD_URL}">View Build Details</a></p>
                <p><a href="${BUILD_URL}allure/">View Allure Report</a></p>
                """,
                mimeType: 'text/html',
                to: 'qa-team@company.com'
            )
        }
        
        failure {
            echo 'Pipeline failed!'
            emailext (
                subject: "❌ SwiftAssess QA Pipeline - FAILED (Build #${BUILD_NUMBER})",
                body: """
                <h2>SwiftAssess QA Pipeline - FAILED</h2>
                <p><strong>Build:</strong> #${BUILD_NUMBER}</p>
                <p><strong>Status:</strong> ❌ FAILED</p>
                <p><strong>Duration:</strong> ${currentBuild.durationString}</p>
                <p><strong>Branch:</strong> ${env.BRANCH_NAME}</p>
                
                <h3>Test Results:</h3>
                <ul>
                    <li>Functional Tests: ❌ Failed</li>
                    <li>Device Tests: ❌ Failed</li>
                    <li>Load Tests: ❌ Failed</li>
                </ul>
                
                <p><a href="${BUILD_URL}">View Build Details</a></p>
                <p><a href="${BUILD_URL}console">View Console Output</a></p>
                """,
                mimeType: 'text/html',
                to: 'qa-team@company.com'
            )
        }
        
        unstable {
            echo 'Pipeline completed with warnings!'
            emailext (
                subject: "⚠️ SwiftAssess QA Pipeline - UNSTABLE (Build #${BUILD_NUMBER})",
                body: """
                <h2>SwiftAssess QA Pipeline - UNSTABLE</h2>
                <p><strong>Build:</strong> #${BUILD_NUMBER}</p>
                <p><strong>Status:</strong> ⚠️ UNSTABLE</p>
                <p><strong>Duration:</strong> ${currentBuild.durationString}</p>
                <p><strong>Branch:</strong> ${env.BRANCH_NAME}</p>
                
                <h3>Test Results:</h3>
                <ul>
                    <li>Functional Tests: ⚠️ Some failures</li>
                    <li>Device Tests: ⚠️ Some failures</li>
                    <li>Load Tests: ⚠️ Some failures</li>
                </ul>
                
                <p><a href="${BUILD_URL}">View Build Details</a></p>
                <p><a href="${BUILD_URL}allure/">View Allure Report</a></p>
                """,
                mimeType: 'text/html',
                to: 'qa-team@company.com'
            )
        }
    }
}
