# Azure DevOps Pipeline Deployment Checklist

## Pre-Deployment Checklist

### ✅ Repository Setup
- [ ] Repository is committed to Git
- [ ] All test files are present and committed
- [ ] `azure-pipelines.yml` is in repository root
- [ ] `.gitignore` is configured properly
- [ ] No sensitive data in repository

### ✅ File Verification
Run the validation script to verify all files:
```bash
python validate_pipeline.py
```

Expected output: `✅ Pipeline validation PASSED - Ready for Azure DevOps deployment`

### ✅ Required Files Present
- [ ] `azure-pipelines.yml` - Pipeline configuration
- [ ] `requirements.txt` - Python dependencies
- [ ] `package.json` - Node.js dependencies
- [ ] `pytest.ini` - Pytest configuration
- [ ] `config/config.yaml` - Test configuration
- [ ] Test files in `tests/` directory
- [ ] Report generation scripts in `scripts/` directory

### ✅ Azure DevOps Account Setup
- [ ] Azure DevOps organization exists
- [ ] Project created in Azure DevOps
- [ ] You have necessary permissions (Build Administrator or higher)
- [ ] Repository is connected to Azure DevOps

---

## Deployment Steps

### Step 1: Connect Repository to Azure DevOps
1. [ ] Navigate to Azure DevOps project
2. [ ] Go to **Project Settings** → **Repositories**
3. [ ] Add repository connection:
   - GitHub: Install Azure Pipelines app
   - Azure Repos: Already integrated
   - Bitbucket: Use service connection
4. [ ] Authorize access to repository
5. [ ] Verify connection successful

### Step 2: Create Pipeline
1. [ ] Navigate to **Pipelines** section
2. [ ] Click **New Pipeline** or **Create Pipeline**
3. [ ] Select repository source:
   - GitHub
   - Azure Repos Git
   - Bitbucket
   - Other Git
4. [ ] Authenticate if required
5. [ ] Select your repository from the list

### Step 3: Configure Pipeline
1. [ ] Choose **Existing Azure Pipelines YAML file**
2. [ ] Select branch: `main` or `develop`
3. [ ] Select file path: `/azure-pipelines.yml`
4. [ ] Click **Continue**

### Step 4: Review Pipeline Configuration
1. [ ] Review the YAML content displayed
2. [ ] Verify all stages are present:
   - Setup & Code Quality
   - Functional Tests
   - Device Tests
   - Load Tests
   - Reports
   - Notification
3. [ ] Check trigger configuration matches requirements
4. [ ] Verify pool selection (windows-latest recommended)

### Step 5: Configure Variables (Optional)
1. [ ] Click **Variables** (if needed to override defaults)
2. [ ] Add/modify variables:
   - `pythonVersion` (default: 3.11)
   - `nodeVersion` (default: 16.x)
   - `testEnv` (default: staging)
   - `browser` (default: chrome)
   - `headless` (default: true)
3. [ ] Mark sensitive variables as secret if needed
4. [ ] Save variables

### Step 6: Save and Run Pipeline
1. [ ] Click **Save and Run** button
2. [ ] Add commit message (e.g., "Add Azure DevOps pipeline")
3. [ ] Choose to commit to:
   - [ ] Main branch (production)
   - [ ] New branch (recommended for first run)
4. [ ] Click **Save and Run** to start first build

---

## First Run Verification

### ✅ Monitor First Run
1. [ ] Pipeline run starts automatically
2. [ ] Monitor execution in real-time
3. [ ] Check each stage completes successfully:
   - [ ] Setup & Code Quality (3-5 min)
   - [ ] Functional Tests (15-20 min)
   - [ ] Device Tests (20-30 min)
   - [ ] Load Tests (15-20 min)
   - [ ] Reports (3-5 min)
   - [ ] Notification (1 min)

### ✅ Review Logs
If any stage fails:
1. [ ] Click on failed stage
2. [ ] Click on failed job
3. [ ] Review error logs
4. [ ] Check screenshots in artifacts
5. [ ] Fix issues and retry

### ✅ Verify Artifacts
After successful run:
1. [ ] Go to **Artifacts** tab
2. [ ] Verify all artifacts are present (14 artifacts expected)
3. [ ] Download and review key reports:
   - [ ] `functional-test-reports/functional_test_report.html`
   - [ ] `combined-reports/combined_test_report.html`
   - [ ] `test-summary/test_summary.md`
4. [ ] Check screenshots if any tests failed

---

## Post-Deployment Configuration

### ✅ Configure Branch Policies
1. [ ] Go to **Project Settings** → **Repositories**
2. [ ] Select repository → **Branches**
3. [ ] Select `main` branch → **Branch policies**
4. [ ] Enable policies:
   - [ ] Require minimum number of reviewers (recommended: 1)
   - [ ] Check for linked work items
   - [ ] Build validation:
     - [ ] Select the pipeline
     - [ ] Policy requirement: Required
     - [ ] Build expiration: Immediately
     - [ ] Display name: "CI Build"
5. [ ] Save policies

### ✅ Configure Notifications
1. [ ] Go to **Project Settings** → **Notifications**
2. [ ] Create notification rules:
   - [ ] Build completes successfully
     - Target: QA Team
     - Deliver via: Email
   - [ ] Build fails
     - Target: QA Team + Dev Team
     - Deliver via: Email
   - [ ] Build partially succeeds
     - Target: QA Team
     - Deliver via: Email
3. [ ] Test notification by running pipeline
4. [ ] Verify emails received

### ✅ Set Up Scheduled Builds (Optional)
1. [ ] Edit pipeline → **Triggers**
2. [ ] Add scheduled trigger:
   - [ ] Days: Select days (e.g., Daily)
   - [ ] Time: Select time (e.g., 00:00 UTC)
   - [ ] Branch: `main` or `develop`
   - [ ] Always run: Yes
3. [ ] Save scheduled trigger
4. [ ] Verify next scheduled run time

### ✅ Configure Retention Policies
1. [ ] Go to **Project Settings** → **Pipelines** → **Retention**
2. [ ] Set artifact retention:
   - [ ] Days to keep: 30 (recommended)
   - [ ] Minimum to keep: 10
   - [ ] Days to keep pull request runs: 10
3. [ ] Save settings

---

## Testing the Pipeline

### ✅ Test Manual Trigger
1. [ ] Navigate to **Pipelines**
2. [ ] Select pipeline
3. [ ] Click **Run pipeline**
4. [ ] Select branch: `develop`
5. [ ] Click **Run**
6. [ ] Verify pipeline runs successfully

### ✅ Test Automatic Trigger (Push)
1. [ ] Create test branch: `git checkout -b test/pipeline-trigger`
2. [ ] Make minor change (e.g., update README)
3. [ ] Commit: `git commit -m "Test pipeline trigger"`
4. [ ] Push: `git push origin test/pipeline-trigger`
5. [ ] Verify pipeline runs automatically
6. [ ] Check **Pipelines** page for new run

### ✅ Test Pull Request Trigger
1. [ ] Create pull request from test branch to `main`
2. [ ] Verify pipeline runs automatically
3. [ ] Check PR shows pipeline status
4. [ ] Review test results in PR
5. [ ] Complete or abandon PR

### ✅ Test Load Test Conditional Execution
1. [ ] Push to feature branch
2. [ ] Verify Load Tests are skipped (feature branch)
3. [ ] Push to `main` or `develop`
4. [ ] Verify Load Tests run (main/develop branch)

---

## Troubleshooting Common Issues

### ❌ Issue: Dependencies Installation Fails
**Solution:**
- [ ] Verify `requirements.txt` is valid
- [ ] Check `package.json` syntax
- [ ] Ensure packages are available in public registries
- [ ] Check agent has internet access

### ❌ Issue: Test Execution Fails
**Solution:**
- [ ] Review test logs in Azure DevOps
- [ ] Check if test environment (app.swiftassess.com) is accessible
- [ ] Verify test data is valid
- [ ] Check screenshots in artifacts
- [ ] Run tests locally to reproduce issue

### ❌ Issue: Browser/WebDriver Issues
**Solution:**
- [ ] Verify `webdriver-manager` in requirements.txt
- [ ] Check `headless` mode is enabled (recommended for CI)
- [ ] Ensure browser drivers are compatible
- [ ] Add browser installation step if needed

### ❌ Issue: Load Tests Not Running
**Solution:**
- [ ] Check branch condition (main/develop only)
- [ ] Verify k6 installation in npm packages
- [ ] Check load test script paths
- [ ] Verify target URL is accessible

### ❌ Issue: Pipeline Timeout
**Solution:**
- [ ] Increase timeout in YAML (default: 60 minutes)
- [ ] Optimize slow tests
- [ ] Use parallel execution (already configured)
- [ ] Consider using self-hosted agents

### ❌ Issue: Artifacts Not Published
**Solution:**
- [ ] Check artifact paths in YAML
- [ ] Verify directories exist before publishing
- [ ] Check if previous stages completed
- [ ] Review logs for artifact publication errors

---

## Performance Optimization

### ✅ Speed Up Pipeline Execution
- [ ] Enable dependency caching (optional)
- [ ] Reduce test scope for PR builds
- [ ] Use self-hosted agents for faster execution
- [ ] Optimize slow tests
- [ ] Consider splitting into multiple pipelines

### ✅ Resource Management
- [ ] Monitor agent pool usage
- [ ] Set up alerts for long-running builds
- [ ] Review and optimize resource usage
- [ ] Consider agent scaling strategies

---

## Security Best Practices

### ✅ Secure Sensitive Data
- [ ] Never commit passwords or API keys
- [ ] Use Azure Key Vault for secrets
- [ ] Mark pipeline variables as secret
- [ ] Restrict access to pipeline variables
- [ ] Enable audit logging

### ✅ Access Control
- [ ] Set up proper permissions
- [ ] Use service connections for external services
- [ ] Enable approval gates for production
- [ ] Review and update permissions regularly

---

## Monitoring and Maintenance

### ✅ Set Up Monitoring Dashboard
1. [ ] Go to **Dashboards**
2. [ ] Create new dashboard: "QA Automation"
3. [ ] Add widgets:
   - [ ] Build history
   - [ ] Test results trend
   - [ ] Pass rate
   - [ ] Build duration
4. [ ] Share dashboard with team

### ✅ Regular Maintenance Tasks
- [ ] Weekly: Review failed tests
- [ ] Bi-weekly: Update test data
- [ ] Monthly: Update dependencies
- [ ] Monthly: Review and optimize slow tests
- [ ] Quarterly: Update documentation
- [ ] Quarterly: Review security settings

---

## Rollback Plan

### If Pipeline Fails Completely
1. [ ] Disable automatic triggers
2. [ ] Fix issues in feature branch
3. [ ] Test locally: `python validate_pipeline.py`
4. [ ] Test in separate test pipeline
5. [ ] Re-enable triggers after verification

---

## Success Criteria

### ✅ Pipeline Deployment Success
- [x] Pipeline created in Azure DevOps
- [x] First run completed successfully
- [x] All stages executed
- [x] Artifacts published (14 artifacts)
- [x] Test reports generated
- [x] Notifications configured
- [x] Branch policies set up
- [x] Team has access to results

### ✅ Pipeline Health Indicators
- [ ] Pass rate > 90%
- [ ] Execution time < 60 minutes
- [ ] No flaky tests (consistent results)
- [ ] All critical tests passing
- [ ] Reports generated successfully

---

## Next Steps

### After Successful Deployment
1. [ ] Document pipeline URL and share with team
2. [ ] Train team on viewing results
3. [ ] Set up weekly review meetings
4. [ ] Create backlog items for test improvements
5. [ ] Monitor pipeline health metrics
6. [ ] Plan for continuous improvement

### Continuous Improvement
1. [ ] Add more test cases as needed
2. [ ] Optimize slow tests
3. [ ] Add code coverage reporting
4. [ ] Implement test parallelization improvements
5. [ ] Set up advanced monitoring

---

## Support Resources

### Documentation
- [ ] [AZURE_DEVOPS_SETUP.md](AZURE_DEVOPS_SETUP.md) - Detailed setup guide
- [ ] [AZURE_PIPELINE_TEST_CASES.md](AZURE_PIPELINE_TEST_CASES.md) - Complete test case reference
- [ ] [README.md](README.md) - Project overview

### External Resources
- [ ] [Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [ ] [YAML Schema Reference](https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/)
- [ ] [Pytest Documentation](https://docs.pytest.org/)
- [ ] [k6 Load Testing Documentation](https://k6.io/docs/)

### Contact Support
- QA Team: qa-team@company.com
- DevOps Team: devops-team@company.com
- Azure DevOps Support: [https://azure.microsoft.com/support/devops/](https://azure.microsoft.com/support/devops/)

---

## Completion Sign-off

**Pipeline Deployed By**: ___________________________  
**Date**: ___________________________  
**Pipeline Status**: ⬜ Successful ⬜ Issues (documented)  
**Verified By**: ___________________________  
**Date**: ___________________________  

**Notes/Comments**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

**Last Updated**: October 2025  
**Document Version**: 1.0.0  
**Maintained By**: QA Automation Team

