# SwiftAssess Signup Page - QA Automation & Load Testing

## Project Overview
This project provides comprehensive QA automation and load testing for the SwiftAssess signup page, including functional testing, device testing, and performance testing scenarios.

## Project Structure
```
project/
├── docs/
│   ├── TestPlan.md
│   ├── TestReport.md
│   └── LoadTestReport.md
├── tests/
│   ├── functional/
│   │   ├── pages/
│   │   ├── tests/
│   │   └── utils/
│   ├── device/
│   └── load/
├── config/
├── reports/
├── screenshots/
├── requirements.txt
├── pytest.ini
├── docker-compose.yml
└── Jenkinsfile
```

## Features
- **Functional Testing**: Automated test cases for signup page functionality
- **Device Testing**: Cross-device compatibility testing
- **Load Testing**: Performance testing with baseline, stress, and spike scenarios
- **Retry Mechanism**: Automatic retry on test failures
- **Screenshot Capture**: Visual evidence on test failures
- **CI/CD Integration**: DevOps pipeline configuration
- **Comprehensive Reporting**: Detailed test reports with metrics

## Test Scenarios

### Functional Tests
- Valid signup with all required fields
- Invalid email format validation
- Password strength validation
- Required field validation
- Duplicate email handling
- Terms and conditions acceptance

### Device Tests
- Desktop browser testing
- Mobile device testing
- Tablet device testing
- Cross-browser compatibility

### Load Tests
- **Baseline Test**: 10 concurrent users
- **Stress Test**: 500 concurrent users  
- **Spike Test**: Sudden jump to 1000 users

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker (optional)
- Chrome/Firefox browsers

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd project

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies for load testing
npm install

# Set up environment variables
cp .env.example .env
```

### Running Tests

#### Functional Tests
```bash
# Run all functional tests
pytest tests/functional/ -v

# Run with specific browser
pytest tests/functional/ --browser=chrome

# Run with retry mechanism
pytest tests/functional/ --retry=3
```

#### Device Tests
```bash
# Run device tests
pytest tests/device/ -v
```

#### Load Tests
```bash
# Run baseline test
npm run load:baseline

# Run stress test
npm run load:stress

# Run spike test
npm run load:spike
```

## CI/CD Pipeline
The project includes Jenkins pipeline configuration for automated testing:
- Automated test execution on code changes
- Parallel test execution
- Test result reporting
- Artifact collection

## Reports
- **Functional Test Report**: `reports/functional_test_report.html`
- **Load Test Report**: `reports/load_test_report.html`
- **Screenshots**: `screenshots/` directory
- **Bug Report**: `reports/bug_report.xlsx`

## Best Practices Implemented
- Page Object Model (POM) design pattern
- BDD framework integration
- Retry mechanisms for flaky tests
- Screenshot capture on failures
- Comprehensive logging
- Data-driven testing
- Cross-browser testing
- Mobile device testing
- Performance monitoring

## Contact
For questions or issues, please contact the QA team.
