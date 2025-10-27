# Azure DevOps Pipeline Setup Guide

## Overview
This document provides detailed instructions for setting up and running the Azure DevOps pipeline for SwiftAssess QA Automation project.

## Pipeline Architecture

The pipeline consists of **6 main stages**:

### 1. Setup & Code Quality
- Environment setup (Python 3.11, Node.js 16.x)
- Dependency installation
- Code quality checks (Pylint, Black)

### 2. Functional Tests
- **Smoke Tests**: Critical path testing
- **Regression Tests**: Full feature regression
- **All Functional Tests**: Complete functional test suite

**Test Cases Included:**
- ✅ test_valid_signup (Smoke)
- ✅ test_empty_first_name_validation
- ✅ test_empty_last_name_validation
- ✅ test_invalid_email_validation
- ✅ test_weak_password_validation
- ✅ test_mismatched_passwords_validation
- ✅ test_terms_and_conditions_required
- ✅ test_privacy_policy_required
- ✅ test_duplicate_email_handling
- ✅ test_form_field_requirements
- ✅ test_password_strength_indicator
- ✅ test_form_clear_functionality

### 3. Device Compatibility Tests
- **Desktop Tests**: Chrome, Firefox, Edge
- **Mobile Tests**: iPhone, Android, Touch Interactions, Keyboard Handling
- **Tablet Tests**: iPad compatibility
- **Responsive Tests**: Multiple viewport sizes, Cross-browser consistency

**Test Cases Included:**
- ✅ test_desktop_chrome_compatibility
- ✅ test_desktop_firefox_compatibility
- ✅ test_desktop_edge_compatibility
- ✅ test_mobile_iphone_compatibility
- ✅ test_mobile_android_compatibility
- ✅ test_tablet_ipad_compatibility
- ✅ test_responsive_design_validation
- ✅ test_touch_interactions
- ✅ test_mobile_keyboard_handling
- ✅ test_cross_browser_consistency

### 4. Load & Performance Tests
- **Baseline Load Test**: 10 concurrent users
- **Stress Load Test**: 500 concurrent users
- **Spike Load Test**: 1000 concurrent users

### 5. Report Generation & Publishing
- Combined test reports (HTML/JSON/Excel)
- Bug reports
- Allure reports
- Screenshot archives
- Test summary markdown

### 6. Notification & Cleanup
- Build status notifications
- Artifact publishing
- Cleanup operations

## Prerequisites

### Azure DevOps Setup
1. **Azure DevOps Account**: Ensure you have an Azure DevOps organization and project
2. **Repository**: Repository must be connected to Azure DevOps
3. **Agent Pool**: Use Microsoft-hosted agents (windows-latest)

### Required Service Connections (Optional)
- Email notification service (for build alerts)
- External reporting tools (if used)

## Setup Instructions

### Step 1: Create Azure DevOps Project
1. Navigate to your Azure DevOps organization
2. Create a new project or use an existing one
3. Name: `SwiftAssess-QA-Automation`

### Step 2: Connect Repository
1. Go to **Project Settings** → **Repositories**
2. Connect your Git repository
3. Ensure the repository contains the `azure-pipelines.yml` file

### Step 3: Create Pipeline
1. Navigate to **Pipelines** → **New Pipeline**
2. Select your repository source (GitHub, Azure Repos, Bitbucket, etc.)
3. Choose **Existing Azure Pipelines YAML file**
4. Select the `azure-pipelines.yml` file
5. Review and click **Run**

### Step 4: Configure Pipeline Variables (Optional)
Go to **Pipeline** → **Edit** → **Variables** and configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `pythonVersion` | 3.11 | Python version to use |
| `nodeVersion` | 16.x | Node.js version to use |
| `testEnv` | staging | Test environment (staging/production) |
| `browser` | chrome | Default browser for tests |
| `headless` | true | Run tests in headless mode |

### Step 5: Configure Triggers
The pipeline is configured to trigger on:
- Push to `main`, `develop`, or `feature/*` branches
- Pull requests to `main` or `develop`

To modify triggers, edit the `trigger` and `pr` sections in `azure-pipelines.yml`.

### Step 6: Configure Notifications
1. Go to **Project Settings** → **Notifications**
2. Add notification rules:
   - **Build completes**: Notify QA team
   - **Build fails**: Notify QA team and developers
   - **Build partially succeeds**: Notify QA team

### Step 7: Set Up Branch Policies (Recommended)
1. Go to **Project Settings** → **Repositories** → **Branches**
2. Select `main` branch → **Branch Policies**
3. Enable:
   - ✅ Require a minimum number of reviewers
   - ✅ Check for linked work items
   - ✅ Build validation (select the pipeline)

## Running the Pipeline

### Manual Run
1. Navigate to **Pipelines**
2. Select the pipeline
3. Click **Run pipeline**
4. Select branch and commit
5. (Optional) Add runtime variables
6. Click **Run**

### Automatic Triggers
The pipeline automatically runs on:
- Code push to configured branches
- Pull request creation/update
- Scheduled runs (if configured)

## Understanding Pipeline Execution

### Stage Execution Flow
```
Setup & Code Quality
    ↓
[Parallel Execution]
    ├─→ Functional Tests (Smoke, Regression, All)
    └─→ Device Tests (Desktop, Mobile, Tablet, Responsive)
         ↓
    Load Tests (Baseline, Stress, Spike)
         ↓
    Report Generation & Publishing
         ↓
    Notification & Cleanup
```

### Job Parallelization
- **Functional Tests**: 3 parallel jobs (Smoke, Regression, All)
- **Device Tests**: 4 parallel jobs (Desktop, Mobile, Tablet, Responsive)
- **Load Tests**: 3 parallel jobs (Baseline, Stress, Spike)

This reduces total execution time significantly.

## Viewing Test Results

### During Execution
1. Navigate to **Pipelines** → Select running pipeline
2. Click on the build number
3. View real-time logs for each stage/job

### After Completion
1. **Test Results Tab**: View test execution summary
2. **Artifacts Tab**: Download generated reports
   - Smoke test reports
   - Regression test reports
   - Functional test reports
   - Desktop test reports
   - Mobile test reports
   - Tablet test reports
   - Responsive test reports
   - Load test reports
   - Combined reports
   - Screenshots
   - Test summary

### Downloading Reports
1. Go to completed pipeline run
2. Click **Artifacts** (top right)
3. Download desired artifact (ZIP format)
4. Extract and view HTML reports in browser

## Artifacts Generated

Each pipeline run generates the following artifacts:

| Artifact Name | Contents | Format |
|---------------|----------|--------|
| `smoke-test-reports` | Smoke test results | HTML, JSON |
| `regression-test-reports` | Regression test results | HTML, JSON |
| `functional-test-reports` | All functional test results | HTML, JSON |
| `desktop-test-reports` | Desktop browser test results | HTML, JSON |
| `mobile-test-reports` | Mobile device test results | HTML, JSON |
| `tablet-test-reports` | Tablet device test results | HTML, JSON |
| `responsive-test-reports` | Responsive design test results | HTML, JSON |
| `baseline-load-test-reports` | Baseline load test results | JSON, HTML |
| `stress-load-test-reports` | Stress load test results | JSON, HTML |
| `spike-load-test-reports` | Spike load test results | JSON, HTML |
| `combined-reports` | Combined test report | HTML, Excel, JSON |
| `functional-screenshots` | Functional test screenshots | PNG |
| `device-screenshots` | Device test screenshots | PNG |
| `all-screenshots` | All screenshots combined | PNG |
| `test-summary` | Test execution summary | Markdown |

## Troubleshooting

### Common Issues

#### Issue 1: Pipeline Not Triggering
**Solution:**
- Check branch name matches trigger configuration
- Verify repository is connected properly
- Check if pipeline is disabled

#### Issue 2: Dependencies Installation Fails
**Solution:**
- Verify `requirements.txt` and `package.json` are valid
- Check if packages are available in public repositories
- Add retry logic for transient failures

#### Issue 3: Tests Failing
**Solution:**
- Check test logs in Azure DevOps
- Review screenshots in artifacts
- Verify test environment is accessible
- Check if test data is valid

#### Issue 4: Browser Driver Issues
**Solution:**
- Ensure `webdriver-manager` is in requirements.txt
- Add browser installation steps if needed
- Use headless mode for Azure agents

#### Issue 5: Load Tests Not Running
**Solution:**
- Verify k6 is installed via npm
- Check if load test scripts exist
- Ensure k6 scripts have correct URLs
- Verify branch condition for load tests

#### Issue 6: Reports Not Generated
**Solution:**
- Check if report generation scripts exist
- Verify Python dependencies are installed
- Check if previous test data exists
- Review script logs for errors

### Debug Mode
To enable detailed logging:
1. Edit pipeline YAML
2. Add to variables section:
```yaml
variables:
  system.debug: true
```
3. Save and run pipeline

## Performance Optimization

### Reduce Pipeline Execution Time
1. **Use Parallel Jobs**: Already configured
2. **Cache Dependencies**:
```yaml
- task: Cache@2
  inputs:
    key: 'pip | "$(Agent.OS)" | requirements.txt'
    path: $(Pipeline.Workspace)/.pip
```
3. **Skip Unnecessary Stages**: Use conditions
4. **Reduce Test Scope**: Run critical tests only on PR

### Resource Management
- Windows agents: Suitable for Selenium tests
- Linux agents: Consider for better performance (modify YAML)
- Self-hosted agents: For sensitive data or specific requirements

## Best Practices

### 1. Branching Strategy
- Use feature branches for development
- Merge to `develop` for integration testing
- Merge to `main` for production testing

### 2. Test Strategy
- Run smoke tests on every commit
- Run full regression on PR to main
- Run load tests only on main/develop

### 3. Artifact Management
- Retain artifacts for 30 days (configurable)
- Download critical reports before expiration
- Archive important test results

### 4. Monitoring
- Set up Azure DevOps dashboards
- Track test pass rates over time
- Monitor pipeline execution duration
- Review failure trends

### 5. Security
- Use Azure Key Vault for secrets
- Don't commit sensitive data
- Use service principals for external services
- Regularly update dependencies

## Advanced Configuration

### Scheduled Runs
Add to `azure-pipelines.yml`:
```yaml
schedules:
- cron: "0 0 * * *"  # Daily at midnight
  displayName: Daily regression test
  branches:
    include:
    - main
  always: true
```

### Multi-Environment Testing
Add environment-specific variables:
```yaml
- stage: Test_Staging
  variables:
    testEnv: 'staging'
    baseUrl: 'https://app-stg.swiftassess.com'
    
- stage: Test_Production
  variables:
    testEnv: 'production'
    baseUrl: 'https://app.swiftassess.com'
```

### Matrix Testing
Test multiple configurations:
```yaml
strategy:
  matrix:
    Chrome:
      browser: 'chrome'
    Firefox:
      browser: 'firefox'
    Edge:
      browser: 'edge'
```

## Support and Maintenance

### Regular Maintenance Tasks
- [ ] Update dependencies monthly
- [ ] Review and optimize slow tests
- [ ] Clean up old artifacts
- [ ] Update browser drivers
- [ ] Review and update test data

### Documentation
- Keep this guide updated
- Document pipeline changes
- Maintain test case documentation
- Update README.md

## Contacts
- **QA Team**: qa-team@company.com
- **DevOps Team**: devops-team@company.com
- **Project Owner**: project-owner@company.com

## Additional Resources
- [Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [Pytest Documentation](https://docs.pytest.org/)
- [k6 Documentation](https://k6.io/docs/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)

---

## Quick Reference Commands

### Local Testing (Before Pipeline)
```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Run smoke tests locally
pytest tests/functional/ -m smoke -v

# Run all functional tests
pytest tests/functional/ -v

# Run device tests
pytest tests/device/ -v

# Run load tests
npm run load:baseline

# Generate reports
python scripts/generate_combined_report.py
```

### Pipeline Management
```bash
# Clone repository
git clone <repository-url>
cd project

# Create feature branch
git checkout -b feature/new-tests

# Make changes and commit
git add .
git commit -m "Add new test cases"

# Push to trigger pipeline
git push origin feature/new-tests

# Create pull request (triggers pipeline)
```

---

**Last Updated**: October 2025  
**Pipeline Version**: 1.0.0  
**Maintained By**: QA Automation Team

