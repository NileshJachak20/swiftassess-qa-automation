# Azure DevOps Pipeline - Complete Test Cases Reference

## Overview
This document provides a comprehensive list of all test cases included in the Azure DevOps pipeline for the SwiftAssess QA Automation project.

**Total Test Cases**: 22  
**Pipeline Stages**: 6  
**Parallel Jobs**: 10  
**Estimated Execution Time**: 45-60 minutes

---

## Test Execution Summary

### Stage 1: Setup & Code Quality
**Purpose**: Environment setup and code quality validation  
**Duration**: ~3-5 minutes  
**Jobs**: 1

#### Tasks
- ✅ Python 3.11 installation
- ✅ Node.js 16.x installation
- ✅ Python dependencies installation (requirements.txt)
- ✅ Node.js dependencies installation (package.json)
- ✅ Pylint code quality checks
- ✅ Black formatting checks

---

## Stage 2: Functional Tests
**Purpose**: Validate signup page functionality  
**Duration**: ~15-20 minutes  
**Jobs**: 3 (Parallel Execution)  
**Total Test Cases**: 12

### Job 2.1: Smoke Tests
**Marker**: `@pytest.mark.smoke`  
**Browser**: Chrome (Headless)  
**Test Cases**: 1

| # | Test Case | Description | Expected Result |
|---|-----------|-------------|-----------------|
| 1 | `test_valid_signup` | Test valid signup with all required fields | User successfully signs up with valid data |

**Artifacts**:
- `smoke_test_report.html`
- `smoke_results.json`
- Allure results

---

### Job 2.2: Regression Tests
**Marker**: `@pytest.mark.regression`  
**Browser**: Chrome (Headless)  
**Test Cases**: Multiple

All functional tests marked as regression tests are executed in this job.

**Artifacts**:
- `regression_test_report.html`
- `regression_results.json`
- Allure results

---

### Job 2.3: All Functional Tests
**Marker**: `@pytest.mark.functional`  
**Browser**: Chrome (Headless)  
**Test Cases**: 12

| # | Test Case | Description | Validation Type | Expected Result |
|---|-----------|-------------|-----------------|-----------------|
| 1 | `test_valid_signup` | Valid signup with all fields | Positive | Successful signup |
| 2 | `test_empty_first_name_validation` | Empty first name field | Negative | Error: "First name is required" |
| 3 | `test_empty_last_name_validation` | Empty last name field | Negative | Error: "Last name is required" |
| 4 | `test_invalid_email_validation` | Invalid email format | Negative | Error: "Invalid email format" |
| 5 | `test_weak_password_validation` | Weak password | Negative | Error: "Password too weak" |
| 6 | `test_mismatched_passwords_validation` | Passwords don't match | Negative | Error: "Passwords do not match" |
| 7 | `test_terms_and_conditions_required` | Terms not accepted | Negative | Error: "Terms must be accepted" |
| 8 | `test_privacy_policy_required` | Privacy policy not accepted | Negative | Error: "Privacy policy must be accepted" |
| 9 | `test_duplicate_email_handling` | Email already exists | Negative | Error or success based on system |
| 10 | `test_form_field_requirements` | All required fields marked | UI Validation | All required fields have indicators |
| 11 | `test_password_strength_indicator` | Password strength indicator | UI Validation | Strength indicator shows correct level |
| 12 | `test_form_clear_functionality` | Clear form functionality | UI Validation | All fields cleared successfully |

**Artifacts**:
- `functional_test_report.html`
- `functional_results.json`
- Screenshots (on failure)
- Allure results

---

## Stage 3: Device Compatibility Tests
**Purpose**: Validate cross-browser and cross-device compatibility  
**Duration**: ~20-30 minutes  
**Jobs**: 4 (Parallel Execution)  
**Total Test Cases**: 10

### Job 3.1: Desktop Browser Tests
**Test Cases**: 3

| # | Test Case | Browser | Resolution | Expected Result |
|---|-----------|---------|------------|-----------------|
| 1 | `test_desktop_chrome_compatibility` | Chrome | 1920x1080 | Signup form fully functional |
| 2 | `test_desktop_firefox_compatibility` | Firefox | 1920x1080 | Signup form fully functional |
| 3 | `test_desktop_edge_compatibility` | Edge | 1920x1080 | Signup form fully functional |

**Validations**:
- Page loads correctly
- Form elements visible and accessible
- Form can be filled and submitted
- All fields retain entered values

**Artifacts**:
- `desktop_chrome_report.html`
- `desktop_firefox_report.html`
- `desktop_edge_report.html`
- JSON results for each browser

---

### Job 3.2: Mobile Device Tests
**Test Cases**: 4

| # | Test Case | Device | Viewport | Expected Result |
|---|-----------|--------|----------|-----------------|
| 1 | `test_mobile_iphone_compatibility` | iPhone | 390x844 | Responsive design works correctly |
| 2 | `test_mobile_android_compatibility` | Android | 360x800 | Responsive design works correctly |
| 3 | `test_touch_interactions` | Mobile | Variable | Touch events work correctly |
| 4 | `test_mobile_keyboard_handling` | Mobile | Variable | Keyboard input works correctly |

**Validations**:
- Mobile-optimized layout
- Touch-friendly controls
- Virtual keyboard handling
- Form submission on mobile

**Artifacts**:
- `mobile_iphone_report.html`
- `mobile_android_report.html`
- `touch_interactions_report.html`
- `mobile_keyboard_report.html`
- JSON results

---

### Job 3.3: Tablet Device Tests
**Test Cases**: 1

| # | Test Case | Device | Viewport | Expected Result |
|---|-----------|--------|----------|-----------------|
| 1 | `test_tablet_ipad_compatibility` | iPad | 768x1024 | Tablet layout works correctly |

**Validations**:
- Tablet-optimized layout
- Form elements sized appropriately
- Touch and keyboard input work
- Portrait and landscape modes

**Artifacts**:
- `tablet_ipad_report.html`
- `tablet_ipad_results.json`

---

### Job 3.4: Responsive Design Tests
**Test Cases**: 2

| # | Test Case | Viewports Tested | Expected Result |
|---|-----------|------------------|-----------------|
| 1 | `test_responsive_design_validation` | 1920x1080, 1366x768, 1024x768, 768x1024, 375x667, 667x375 | All viewports render correctly |
| 2 | `test_cross_browser_consistency` | Chrome, Firefox, Edge | Consistent behavior across browsers |

**Validations**:
- Form visible at all resolutions
- No horizontal scrolling issues
- Elements properly aligned
- Text readable at all sizes
- Buttons accessible
- Consistent styling across browsers

**Artifacts**:
- `responsive_design_report.html`
- `cross_browser_report.html`
- Screenshots at multiple resolutions
- JSON results

---

## Stage 4: Load & Performance Tests
**Purpose**: Validate application performance under load  
**Duration**: ~15-20 minutes  
**Jobs**: 3 (Parallel Execution)  
**Test Scripts**: 3

### Job 4.1: Baseline Load Test
**Script**: `tests/load/load_test_baseline.js`

| Parameter | Value |
|-----------|-------|
| Virtual Users | 10 |
| Duration | 5 minutes |
| Ramp-up Time | 1 minute |

**Thresholds**:
- Response Time (p95) < 2 seconds
- Error Rate < 1%
- Throughput > 100 req/s

**Artifacts**:
- `baseline-load-test-reports` (JSON)

---

### Job 4.2: Stress Load Test
**Script**: `tests/load/load_test_stress.js`

| Parameter | Value |
|-----------|-------|
| Virtual Users | 500 |
| Duration | 10 minutes |
| Ramp-up Time | 2 minutes |

**Purpose**: Test system behavior under sustained high load

**Thresholds**:
- Response Time (p95) < 3 seconds
- Error Rate < 5%
- System remains stable

**Artifacts**:
- `stress-load-test-reports` (JSON)

---

### Job 4.3: Spike Load Test
**Script**: `tests/load/load_test_spike.js`

| Parameter | Value |
|-----------|-------|
| Virtual Users | 1000 |
| Duration | 5 minutes |
| Ramp-up Time | 30 seconds |

**Purpose**: Test system behavior under sudden traffic spike

**Thresholds**:
- System doesn't crash
- Graceful degradation
- Recovery after spike

**Artifacts**:
- `spike-load-test-reports` (JSON)

---

## Stage 5: Report Generation & Publishing
**Purpose**: Generate and publish comprehensive test reports  
**Duration**: ~3-5 minutes  
**Jobs**: 1

### Reports Generated

| Report Type | File Name | Format | Content |
|-------------|-----------|--------|---------|
| Combined Report | `combined_test_report.html` | HTML | All test results combined |
| Bug Report | `bug_report_*.html` | HTML/Excel | Failed tests with details |
| Allure Report | `allure-report/index.html` | HTML | Interactive test report |
| Test Summary | `test_summary.md` | Markdown | Build and test summary |

### Artifacts Published

| Artifact Name | Contents |
|---------------|----------|
| `smoke-test-reports` | Smoke test HTML and JSON reports |
| `regression-test-reports` | Regression test reports |
| `functional-test-reports` | All functional test reports |
| `desktop-test-reports` | Desktop browser test reports |
| `mobile-test-reports` | Mobile device test reports |
| `tablet-test-reports` | Tablet device test reports |
| `responsive-test-reports` | Responsive design test reports |
| `baseline-load-test-reports` | Baseline load test results |
| `stress-load-test-reports` | Stress load test results |
| `spike-load-test-reports` | Spike load test results |
| `combined-reports` | Combined test reports (all formats) |
| `functional-screenshots` | Functional test failure screenshots |
| `device-screenshots` | Device test failure screenshots |
| `all-screenshots` | All screenshots combined |
| `test-summary` | Test execution summary markdown |

---

## Stage 6: Notification & Cleanup
**Purpose**: Send notifications and cleanup  
**Duration**: ~1 minute  
**Jobs**: 1

### Tasks
- Display build status
- Send email notifications (configured in Azure DevOps)
- Archive artifacts
- Cleanup temporary files

---

## Test Execution Matrix

### Summary by Category

| Category | Test Cases | Browsers/Devices | Duration |
|----------|-----------|------------------|----------|
| Functional | 12 | Chrome | 15-20 min |
| Desktop Compatibility | 3 | Chrome, Firefox, Edge | 8-10 min |
| Mobile Compatibility | 4 | iPhone, Android | 10-12 min |
| Tablet Compatibility | 1 | iPad | 3-5 min |
| Responsive Design | 2 | Multiple viewports | 8-10 min |
| Load Testing | 3 | N/A | 15-20 min |
| **Total** | **25** | **Multiple** | **45-60 min** |

---

## Pipeline Triggers

### Automatic Triggers
- **Push to branches**: `main`, `develop`, `feature/*`
- **Pull requests to**: `main`, `develop`

### Conditional Execution
- **Load Tests**: Only run on `main`, `develop`, or Pull Requests
- **All Stages**: Can be triggered manually

---

## Test Data Management

### Valid Test Data
- First Name: Generated by Faker
- Last Name: Generated by Faker
- Email: Generated by Faker (unique)
- Password: Strong password (meets all requirements)

### Invalid Test Data
Test cases cover various invalid scenarios:
- Empty fields
- Invalid email formats
- Weak passwords
- Mismatched passwords
- Unchecked required checkboxes

---

## Failure Handling

### Test Failures
- **Continue on Error**: Tests continue even if some fail
- **Screenshots**: Captured automatically on failure
- **Logs**: Detailed logs available in Azure DevOps
- **Retry**: Pytest configured to retry flaky tests (2 retries)

### Build Status
- **Success**: All critical tests pass
- **Partial Success**: Some non-critical tests fail
- **Failure**: Critical tests fail

---

## Viewing Test Results

### Azure DevOps Portal
1. Navigate to **Pipelines**
2. Select the pipeline run
3. View **Tests** tab for summary
4. View **Artifacts** tab for detailed reports
5. Download and open HTML reports in browser

### Test Reports Include
- ✅ Pass/Fail status for each test
- ⏱️ Execution time
- 📊 Test trends over time
- 📸 Screenshots on failure
- 📝 Detailed error messages
- 📈 Historical data

---

## Continuous Improvement

### Metrics Tracked
- Test execution time
- Pass/fail rates
- Flaky test detection
- Code coverage (if configured)
- Performance trends

### Regular Reviews
- Weekly: Review failed tests
- Bi-weekly: Update test data
- Monthly: Review test coverage
- Quarterly: Update dependencies

---

## Contact Information

For questions or issues with the test pipeline:

- **QA Team**: qa-team@company.com
- **DevOps Team**: devops-team@company.com
- **Documentation**: See [AZURE_DEVOPS_SETUP.md](AZURE_DEVOPS_SETUP.md)

---

**Last Updated**: October 2025  
**Pipeline Version**: 1.0.0  
**Total Test Cases**: 22  
**Maintained By**: QA Automation Team

