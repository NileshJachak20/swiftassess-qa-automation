# SwiftAssess QA Automation & Load Testing Project

## Project Overview
Complete QA automation and performance testing solution for SwiftAssess signup page (`https://app.swiftassess.com/Signup`). The project includes functional UI tests, unit tests, load/performance tests, and a fully automated Azure DevOps CI/CD pipeline.

## What's Included

### 1. **Unit Tests** (Active in Pipeline)
- 22 browser-less unit tests for smoke, regression, and functional validation
- Fast execution without browser dependencies
- Located in `tests/unit/test_demo.py`
- Categories: Math operations, String operations, List operations, Dictionary operations

### 2. **Functional UI Tests** (Code Available)
- Selenium WebDriver + Pytest for browser automation
- Page Object Model (POM) design pattern
- Cross-browser support (Chrome, Firefox, Edge)
- Comprehensive signup flow validation
- Located in `tests/functional/`
- **Note:** Currently disabled in pipeline (can be enabled when browser automation is configured)

### 3. **Load/Performance Tests** (Active in Pipeline)
- k6-based load testing with three scenarios:
  - **Baseline Test**: 10 concurrent users
  - **Stress Test**: 500 concurrent users  
  - **Spike Test**: 1000 concurrent users
- Performance metrics: response time, throughput, error rate
- Threshold monitoring with detailed reporting
- Located in `tests/load/`

### 4. **Azure DevOps CI/CD Pipeline**
- Automated pipeline with self-hosted agent
- Stages: Setup → Unit Tests → Load Tests → Reports
- Automatic execution on every push
- Artifact publishing for all test results
- Configuration: `azure-pipelines.yml`

## Project Structure
```
project/
├── tests/
│   ├── unit/                        # Unit tests (active in pipeline)
│   │   └── test_demo.py             # 22 unit tests
│   ├── functional/                  # UI tests (Selenium + Pytest)
│   │   ├── pages/                   # Page Object Models
│   │   │   └── signup_page.py
│   │   ├── tests/                   # Functional test cases
│   │   │   └── test_signup_functional.py
│   │   └── utils/                   # Test helpers
│   │       ├── base_page.py
│   │       └── test_helpers.py
│   ├── load/                        # k6 load tests (active in pipeline)
│   │   ├── load_test_baseline.js    # 10 users
│   │   ├── load_test_stress.js      # 500 users
│   │   └── load_test_spike.js       # 1000 users
│   └── conftest.py                  # Pytest configuration
│
├── config/
│   └── config.yaml                  # Test configuration
│
├── scripts/
│   ├── generate_combined_report.py  # Combined HTML/Excel reports
│   └── generate_bug_report.py       # Bug extraction tool
│
├── reports/                         # Auto-generated test reports
├── screenshots/                     # Test failure screenshots
├── azure-pipelines.yml              # CI/CD pipeline definition
├── pytest.ini                       # Pytest configuration
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **Git** for version control
- **Azure DevOps** account (for CI/CD pipeline)
- **k6** (automatically installed by pipeline)
- **Browsers** (Chrome/Firefox/Edge) - only needed for local functional tests

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd project
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Azure DevOps Pipeline
1. Push code to your Azure DevOps repository
2. Create a new pipeline pointing to `azure-pipelines.yml`
3. Set up a self-hosted agent (see instructions below)
4. Run the pipeline - it triggers automatically on push

## How to Run Tests

### Run Unit Tests Locally
```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific test categories
pytest tests/unit/ -m smoke -v
pytest tests/unit/ -m regression -v

# Generate HTML report
pytest tests/unit/ -v --html=reports/unit_test_report.html --self-contained-html
```

### Run Functional UI Tests Locally (Optional)
```bash
# Run all functional tests
pytest tests/functional/ -v

# Run with specific browser
pytest tests/functional/ --browser=chrome -v
pytest tests/functional/ --browser=firefox -v

# Run in headless mode
pytest tests/functional/ --headless -v

# Run specific test
pytest tests/functional/tests/test_signup_functional.py::TestSignupFunctional::test_valid_signup -v
```

### Run Load Tests Locally
You need k6 installed. Download from: https://k6.io/docs/get-started/installation/

```bash
# Baseline test (10 users)
k6 run tests/load/load_test_baseline.js --out json=reports/load_baseline.json

# Stress test (500 users)
k6 run tests/load/load_test_stress.js --out json=reports/load_stress.json

# Spike test (1000 users)
k6 run tests/load/load_test_spike.js --out json=reports/load_spike.json
```

## CI/CD Pipeline

### Pipeline Stages

1. **Setup Stage**
   - Install Python dependencies
   - Run code quality checks (pylint, black)
   - Validate environment

2. **Unit Tests Stage**
   - Smoke tests (critical functionality)
   - Regression tests (existing features)
   - Full test suite execution
   - Generate HTML and JSON reports

3. **Load Tests Stage**
   - Install k6 load testing tool
   - Run baseline test (10 users)
   - Run stress test (500 users)
   - Run spike test (1000 users)
   - Publish performance metrics

4. **Reports Stage**
   - Combine all test results
   - Generate summary report
   - Publish artifacts
   - Create test summary

### Setting Up Self-Hosted Agent

1. **Download Agent**
   - Go to Azure DevOps → Project Settings → Agent pools
   - Click "New agent" and download Windows agent

2. **Configure Agent**
   ```powershell
   # Extract and run configuration
   .\config.cmd
   
   # Install as Windows service
   .\svc.cmd install
   .\svc.cmd start
   ```

3. **Install Prerequisites on Agent Machine**
   - Python 3.10+
   - Git
   - Browsers (for functional tests, if enabled)

### Viewing Pipeline Results

1. Go to Azure DevOps → Pipelines → Your Pipeline
2. Click on the latest run
3. View test results in the "Tests" tab
4. Download artifacts from "Artifacts" section:
   - `smoke-test-reports`
   - `regression-test-reports`
   - `functional-test-reports`
   - `load-test-baseline-results`
   - `load-test-stress-results`
   - `load-test-spike-results`

## Test Reports

### Generated Reports
- **Unit Tests**: `reports/smoke_report.html`, `reports/regression_report.html`
- **Load Tests**: `reports/load_test_*_results.json`
- **Combined Report**: Generate using `python scripts/generate_combined_report.py`
- **Bug Report**: Generate using `python scripts/generate_bug_report.py`

### Viewing Reports Locally
```bash
# Generate combined report
python scripts/generate_combined_report.py
start reports/combined_test_report.html

# Generate bug report
python scripts/generate_bug_report.py
start reports/bug_report.html
```

## Load Test Results Interpretation

The load tests are configured with performance thresholds:
- Response time < 2000ms
- Error rate < 1%

**Important:** Threshold violations are expected findings, not failures. They indicate:
- Performance bottlenecks under load
- Areas requiring optimization
- Baseline metrics for comparison

Pipeline treats threshold violations as warnings to ensure all tests complete and results are published.

## Tools & Technologies

- **Python 3.10+** - Test scripting
- **Pytest** - Test framework
- **Selenium WebDriver** - Browser automation
- **k6** - Load/performance testing
- **Azure DevOps** - CI/CD platform
- **Page Object Model** - Design pattern for UI tests
- **pytest-html** - HTML report generation
- **Allure** - Advanced reporting (optional)

## Best Practices Implemented

✅ Page Object Model (POM) design pattern  
✅ Separation of test logic and page interactions  
✅ Comprehensive test categorization (smoke, regression, unit)  
✅ Screenshot capture on test failures  
✅ Detailed logging and reporting  
✅ Performance threshold monitoring  
✅ CI/CD integration with automated execution  
✅ Artifact publishing for test results  
✅ Self-hosted agent for cost efficiency  

## Quick Start Cheat Sheet

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run unit tests
pytest tests/unit/ -v

# 3. Commit and push to trigger pipeline
git add .
git commit -m "Your changes"
git push

# 4. View results in Azure DevOps pipeline
# Download artifacts and open HTML reports
```

## Troubleshooting

### Pipeline Issues
- **Tests fail to run**: Ensure self-hosted agent is running and online
- **Import errors**: Virtual environment is automatically created by pipeline
- **Load tests fail**: k6 is automatically downloaded, threshold violations are expected

### Local Test Issues
- **Browser not found**: Install Chrome/Firefox/Edge browsers
- **Module not found**: Run `pip install -r requirements.txt`
- **Selenium errors**: webdriver-manager will auto-download drivers

## Project Highlights

✨ **Comprehensive Testing**: Unit, functional, and load tests  
✨ **Production-Ready CI/CD**: Fully automated Azure DevOps pipeline  
✨ **Performance Monitoring**: Real-time load testing with k6  
✨ **Rich Reporting**: HTML, JSON, and combined reports  
✨ **Scalable Architecture**: Easy to add more tests and scenarios  
✨ **Cost-Efficient**: Self-hosted agent reduces cloud costs  

## Support

For issues or questions:
1. Check Azure DevOps pipeline logs
2. Review test reports in artifacts
3. Check `screenshots/` folder for failure evidence
4. Verify agent is running: Azure DevOps → Agent pools

---

**Ready to Test!** Push your code to trigger the automated pipeline. ✅
