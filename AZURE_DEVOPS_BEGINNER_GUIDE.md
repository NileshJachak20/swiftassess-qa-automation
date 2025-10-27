# 🎓 Azure DevOps Setup for Complete Beginners

## 📚 Overview

This guide will walk you through **every single step** to set up Azure DevOps and run your test pipeline - even if you've never used Azure before!

**Time Required**: 15-20 minutes  
**Cost**: $0 (100% Free)  
**Difficulty**: Beginner-friendly  

---

## 🎯 What We'll Do

1. ✅ Create a free Azure DevOps account
2. ✅ Set up your organization and project
3. ✅ Connect your code repository
4. ✅ Create the pipeline
5. ✅ Run your first test
6. ✅ View the results

Let's get started! 🚀

---

## 📝 **PART 1: Create Azure DevOps Account (5 minutes)**

### Step 1.1: Go to Azure DevOps Website

1. Open your web browser
2. Go to: **[https://dev.azure.com](https://dev.azure.com)**
3. You'll see a blue "Start free" button

### Step 1.2: Sign Up

**Option A: If you have a Microsoft account (Outlook, Hotmail, Xbox, etc.)**
1. Click **"Start free"**
2. Click **"Sign in"**
3. Enter your Microsoft email and password
4. Click **"Next"**
5. ✅ You're signed in!

**Option B: If you have a GitHub account**
1. Click **"Start free"**
2. Click **"Sign in with GitHub"**
3. Authorize Azure DevOps to access your GitHub
4. ✅ You're signed in!

**Option C: If you don't have either**
1. Click **"Start free"**
2. Click **"Create a Microsoft account"**
3. Follow the prompts to create a free account (use any email)
4. Verify your email
5. Return to [https://dev.azure.com](https://dev.azure.com)
6. Sign in with your new account
7. ✅ You're signed in!

### Step 1.3: Create Your Organization

After signing in, you'll see a page asking to create an organization:

1. **Organization name**: Enter a name (e.g., "MyCompanyQA" or "TestAutomation")
   - This is like your workspace name
   - Use letters, numbers, hyphens only
   - Example: `swiftassess-qa`

2. **Choose region**: Select closest to you
   - United States
   - Europe
   - Asia Pacific
   - Australia

3. Enter the **CAPTCHA** (verify you're human)

4. Click **"Continue"**

✅ **Your organization is created!**

---

## 📁 **PART 2: Create Your First Project (2 minutes)**

After creating your organization, you'll see a screen to create a project:

### Step 2.1: Project Details

Fill in these fields:

1. **Project name**: `SwiftAssess-QA-Automation`
   - This is your project name
   - Can use spaces and special characters

2. **Description** (optional): 
   ```
   QA Automation and Load Testing for SwiftAssess Signup Page
   ```

3. **Visibility**: 
   - Select **"Private"** (recommended)
   - Only you and invited people can see it
   - You get unlimited private projects for free!

4. **Advanced** (click to expand):
   - **Version control**: Select **"Git"** (recommended)
   - **Work item process**: Select **"Agile"** (default is fine)

5. Click **"Create project"**

⏳ Wait 5-10 seconds while it creates...

✅ **Your project is ready!**

You'll now see your project dashboard with several tabs:
- Overview
- Boards
- Repos
- Pipelines ← We'll use this!
- Test Plans
- Artifacts

---

## 🔗 **PART 3: Upload Your Code (3 minutes)**

You have two options: Use Azure Repos or Connect External Repository

### Option A: Use Azure Repos (Recommended for Beginners)

#### Step 3A.1: Navigate to Repos

1. Click **"Repos"** in the left menu
2. You'll see options to initialize a repository

#### Step 3A.2: Initialize Repository

1. Make sure **"Add a README"** is checked
2. Add **.gitignore**: Select **"Python"**
3. Click **"Initialize"**

✅ Your repository is created!

#### Step 3A.3: Upload Your Files

**Method 1: Using Git (if you have Git installed)**

1. On the Repos page, look for the **"Clone"** button (top right)
2. Copy the clone URL (it looks like: `https://dev.azure.com/yourorg/yourproject/_git/yourrepo`)
3. Open Command Prompt or Terminal
4. Navigate to your project folder:
   ```bash
   cd C:\Users\DELL\Desktop\project
   ```
5. Initialize git (if not already done):
   ```bash
   git init
   ```
6. Add Azure DevOps as remote:
   ```bash
   git remote add azure YOUR_CLONE_URL_HERE
   ```
7. Add all files:
   ```bash
   git add .
   ```
8. Commit:
   ```bash
   git commit -m "Initial commit with Azure DevOps pipeline"
   ```
9. Push:
   ```bash
   git push azure main
   ```
   Or if that doesn't work:
   ```bash
   git push azure master
   ```

**Method 2: Upload via Web (Easier if you don't know Git)**

1. In Azure Repos, click **"Upload file(s)"** button
2. Click **"Browse"** and select all your files
3. **Important**: You need to upload these files:
   - `azure-pipelines.yml`
   - `requirements.txt`
   - `package.json`
   - `pytest.ini`
   - All folders: `tests/`, `config/`, `scripts/`
4. Add commit message: "Add test automation files"
5. Click **"Commit"**
6. Repeat for folders (upload folder contents)

✅ Your code is now in Azure DevOps!

---

### Option B: Connect GitHub Repository (If Your Code is Already on GitHub)

#### Step 3B.1: Navigate to Project Settings

1. Click **"Project settings"** (bottom left, gear icon)
2. Scroll down to **"Pipelines"** section
3. Click **"Service connections"**

#### Step 3B.2: Create Service Connection

1. Click **"Create service connection"**
2. Select **"GitHub"**
3. Click **"Next"**
4. Choose authentication method:
   - **Grant authorization** (easier)
   - Or use **Personal access token**
5. Click **"Authorize"** and log in to GitHub
6. Give it a name: "GitHub-Connection"
7. Click **"Save"**

✅ GitHub is now connected!

---

## 🔧 **PART 4: Create Your Pipeline (3 minutes)**

Now for the exciting part - creating the automated test pipeline!

### Step 4.1: Navigate to Pipelines

1. Click **"Pipelines"** in the left menu
2. You'll see an empty state with "Create Pipeline" button
3. Click **"Create Pipeline"** or **"New pipeline"**

### Step 4.2: Select Repository Source

You'll see: **"Where is your code?"**

**If you used Azure Repos (Option A above):**
1. Click **"Azure Repos Git"**
2. Select your repository (should be `SwiftAssess-QA-Automation`)

**If you connected GitHub (Option B above):**
1. Click **"GitHub"**
2. Select your repository from the list
3. Authorize if prompted

### Step 4.3: Configure Pipeline

You'll see: **"Configure your pipeline"**

1. Scroll down and click **"Existing Azure Pipelines YAML file"**
   - Don't click "Starter pipeline" or other templates!

2. A panel will slide out from the right

3. Select:
   - **Branch**: `main` (or `master` if that's your default)
   - **Path**: `/azure-pipelines.yml`

4. Click **"Continue"**

### Step 4.4: Review Pipeline

You'll now see the contents of your `azure-pipelines.yml` file displayed:

1. **Review it**: Scroll through to see the stages
   - Setup & Code Quality
   - Functional Tests
   - Device Tests
   - Load Tests
   - Reports
   - Notification

2. You'll see a blue **"Run"** button in the top right

3. Click the **dropdown arrow** next to "Run"
4. Select **"Save"** (for now, don't run yet)

5. A dialog will appear: "Save pipeline and commit file"
6. Add commit message: "Add Azure DevOps pipeline"
7. Click **"Save"**

✅ **Your pipeline is created!**

---

## ⚙️ **PART 5: Configure Pipeline Variables (Optional but Recommended) (2 minutes)**

Before running, let's set up some configuration:

### Step 5.1: Access Variables

1. You should now be on the pipeline view
2. Click **"Edit"** button (top right)
3. Click **"Variables"** button (top right, next to "Run")
4. Click **"New variable"**

### Step 5.2: Add Variables (Optional)

Add these variables one by one:

| Variable Name | Value | Keep as Secret? |
|---------------|-------|-----------------|
| `pythonVersion` | `3.11` | No |
| `nodeVersion` | `16.x` | No |
| `testEnv` | `staging` | No |
| `browser` | `chrome` | No |
| `headless` | `true` | No |

**How to add each variable:**
1. Click **"New variable"**
2. Name: Enter variable name (e.g., `pythonVersion`)
3. Value: Enter value (e.g., `3.11`)
4. Keep "Let users override..." checked
5. Click **"OK"**
6. Repeat for other variables

When done, click **"Save"** (top right)

✅ Variables configured!

---

## 🚀 **PART 6: Run Your First Pipeline! (2 minutes)**

Now let's run the pipeline and see the magic happen!

### Step 6.1: Start the Pipeline

1. Make sure you're on the Pipelines page
2. Click on your pipeline name (if not already open)
3. Click the blue **"Run pipeline"** button (top right)

4. A panel will slide out asking for details:
   - **Branch/tag**: Select `main` (or your default branch)
   - **Variables**: Use the defaults (or override if needed)
   - Click **"Run"**

### Step 6.2: Monitor Execution

You'll see the pipeline start running! 🎉

**What you'll see:**

1. **Pipeline view** with stages:
   ```
   ⏳ Setup (Running...)
      Functional_Tests (Waiting...)
      Device_Tests (Waiting...)
      Load_Tests (Waiting...)
      Reports (Waiting...)
      Notification (Waiting...)
   ```

2. Each stage will show:
   - ⏳ Orange = Running
   - ✅ Green = Success
   - ❌ Red = Failed
   - ⚪ Gray = Not started yet

### Step 6.3: View Real-Time Logs

To see what's happening:

1. Click on any stage (e.g., "Setup")
2. Click on a job name
3. You'll see real-time logs scrolling
4. Watch as it:
   - Installs Python
   - Installs dependencies
   - Runs tests
   - Generates reports

**Expected Duration**: 45-60 minutes for complete run

**☕ Time for coffee!** The first run takes longer because it downloads everything.

---

## 📊 **PART 7: View Your Results (3 minutes)**

After the pipeline completes (or while it's running):

### Step 7.1: View Test Results

1. Click on the **"Tests"** tab (top menu)
2. You'll see:
   - Total tests run
   - Passed tests (green)
   - Failed tests (red)
   - Pass rate percentage
   - Test duration

3. Click on any test to see details:
   - Test name
   - Duration
   - Error messages (if failed)
   - Stack trace

### Step 7.2: Download Reports and Artifacts

1. Click on the **"Summary"** tab
2. Scroll down to find **"Artifacts"** section (right side)
3. You'll see 14 published artifacts:
   - smoke-test-reports
   - functional-test-reports
   - device-test-reports
   - combined-reports
   - And more...

4. Click on any artifact name
5. Click **"Download"** button
6. Extract the ZIP file
7. Open `*.html` files in your browser

**Example**: 
- Download `functional-test-reports`
- Extract ZIP
- Open `functional_test_report.html`
- See beautiful test report with charts!

### Step 7.3: View Screenshots (if tests failed)

If any tests failed:
1. Download `functional-screenshots` or `device-screenshots`
2. Extract ZIP
3. View PNG images showing exactly what happened

---

## 🎉 **SUCCESS! You're Done!**

Congratulations! 🎊 You've successfully:
- ✅ Created Azure DevOps account
- ✅ Set up organization and project
- ✅ Uploaded your code
- ✅ Created automated pipeline
- ✅ Run tests in the cloud
- ✅ Viewed results and reports

---

## 🔄 **What Happens Next? (Automatic Testing)**

Now that your pipeline is set up, here's the magic:

### Automatic Triggers

**Every time you push code to GitHub/Azure Repos:**
1. Pipeline automatically starts
2. Runs all 22 tests
3. Generates reports
4. Publishes results
5. **You get notified** (we'll set this up next)

**For Pull Requests:**
1. Pipeline runs automatically
2. Shows results in the PR
3. Blocks merge if tests fail (optional)

---

## 🔔 **BONUS: Set Up Email Notifications (2 minutes)**

Get notified when builds complete or fail:

### Step 1: Navigate to Notifications

1. Click your profile icon (top right)
2. Click **"User settings"**
3. Click **"Notifications"**

### Step 2: Enable Build Notifications

1. Look for **"Build completes"**
2. Click the toggle to **ON** (blue)
3. Repeat for:
   - ✅ **"Build fails"**
   - ✅ **"Build completes"**
   - ✅ **"Build partially succeeds"**

4. Click **"Save"**

✅ You'll now get emails when builds run!

---

## 🛡️ **BONUS: Set Up Branch Protection (3 minutes)**

Require tests to pass before merging code:

### Step 1: Navigate to Branch Policies

1. Click **"Project settings"** (bottom left)
2. Click **"Repositories"** under "Repos" section
3. Click your repository name
4. Click **"Policies"** tab
5. Click **"Branch Policies"**
6. Click on **"main"** branch (or your default branch)

### Step 2: Enable Policies

Enable these policies:

1. **Require a minimum number of reviewers**
   - Toggle **ON**
   - Minimum reviewers: `1`
   - Allow requestors to approve: Your choice

2. **Build Validation**
   - Click **"+ (Add build policy)"**
   - Select your pipeline
   - **Policy requirement**: Required
   - **Build expiration**: Immediately
   - **Display name**: "CI Build"
   - Click **"Save"**

✅ Now tests must pass before code can be merged!

---

## 🎓 **Understanding Your Pipeline**

### What Each Stage Does:

1. **Setup & Code Quality** (3-5 min)
   - Installs Python 3.11
   - Installs Node.js 16.x
   - Installs all dependencies
   - Runs code quality checks

2. **Functional Tests** (15-20 min)
   - Runs 12 functional tests
   - Tests signup form validation
   - Tests user registration
   - Captures screenshots on failure

3. **Device Tests** (20-30 min)
   - Tests on Chrome, Firefox, Edge
   - Tests on mobile devices (iPhone, Android)
   - Tests on tablet (iPad)
   - Tests responsive design

4. **Load Tests** (15-20 min)
   - Baseline: 10 concurrent users
   - Stress: 500 concurrent users
   - Spike: 1000 concurrent users

5. **Reports** (3-5 min)
   - Generates HTML reports
   - Generates Allure reports
   - Creates combined summary
   - Publishes all artifacts

6. **Notification** (1 min)
   - Shows build status
   - Cleans up temporary files

---

## 🆘 **Troubleshooting Common Issues**

### Issue 1: "Pipeline not found" or "File not found"

**Solution:**
- Make sure `azure-pipelines.yml` is in the **root** of your repository
- Check the file name is exactly `azure-pipelines.yml` (not `.yaml`)
- Make sure you selected the correct branch

### Issue 2: "Failed to install dependencies"

**Solution:**
- This is usually temporary - click **"Run new"** to retry
- Check if `requirements.txt` exists in repository
- Check if `package.json` exists in repository

### Issue 3: "Tests are failing"

**Solution:**
- Don't worry! This might be expected if:
  - Test environment is not accessible
  - Test data needs updating
  - Tests need configuration
- Download screenshots to see what happened
- Review logs for error messages

### Issue 4: "Pipeline is taking too long"

**Solution:**
- First run is always slower (downloads everything)
- Expected time: 45-60 minutes
- Subsequent runs will be faster
- This is normal for comprehensive testing

### Issue 5: "Can't push to repository"

**Solution:**
- Make sure you're authenticated
- In Azure Repos: Use Git credential manager
- In GitHub: Use personal access token or SSH key
- Try the web upload method instead

---

## 📞 **Getting Help**

### Resources in This Project:

1. **Quick Start**: `QUICK_START_GUIDE.md`
2. **Detailed Setup**: `AZURE_DEVOPS_SETUP.md`
3. **Test Cases**: `AZURE_PIPELINE_TEST_CASES.md`
4. **Validation**: Run `python validate_pipeline.py`

### External Resources:

- **Azure DevOps Docs**: [https://docs.microsoft.com/azure/devops/](https://docs.microsoft.com/azure/devops/)
- **Azure DevOps Support**: [https://azure.microsoft.com/support/devops/](https://azure.microsoft.com/support/devops/)
- **Community Forums**: [https://developercommunity.visualstudio.com/](https://developercommunity.visualstudio.com/)

### Questions to Ask:

- "How do I..." - Check the detailed setup guide
- "What does this error mean..." - Check troubleshooting section
- "How do I view..." - Check Part 7 of this guide

---

## ✅ **Success Checklist**

Mark each as you complete:

- [ ] Created Azure DevOps account
- [ ] Created organization
- [ ] Created project
- [ ] Uploaded code to repository
- [ ] Created pipeline from `azure-pipelines.yml`
- [ ] Configured variables (optional)
- [ ] Ran pipeline successfully
- [ ] Viewed test results
- [ ] Downloaded and viewed reports
- [ ] Set up email notifications (optional)
- [ ] Set up branch protection (optional)

---

## 🎯 **What You've Achieved**

By completing this guide, you now have:

✅ **Professional CI/CD Pipeline**
- Automated testing on every code change
- 22 test cases running automatically
- Cross-browser and cross-device testing
- Load and performance testing
- Professional test reports

✅ **Azure DevOps Skills**
- Know how to create projects
- Know how to create pipelines
- Know how to view results
- Know how to configure settings

✅ **Quality Assurance Automation**
- Tests run automatically
- No manual testing needed
- Catch bugs before production
- Professional reporting

---

## 🚀 **Next Steps**

Now that you're set up:

1. **Customize the tests**: Add more test cases as needed
2. **Schedule runs**: Set up nightly test runs
3. **Integrate with Slack**: Get notifications in Slack
4. **Add more environments**: Test staging and production
5. **Invite team members**: Share access with your team

---

## 🎓 **You're Now an Azure DevOps User!**

Congratulations! You've successfully set up a professional CI/CD pipeline from scratch. This is a valuable skill for any QA engineer or developer.

**Remember**: 
- Pipeline runs automatically on code changes
- Check results regularly
- Update tests as application changes
- Review reports to find issues early

**You did it!** 🎉🎊🥳

---

**Guide Version**: 1.0.0  
**Last Updated**: October 27, 2025  
**Difficulty**: Beginner  
**Time to Complete**: 15-20 minutes  
**Cost**: $0 (Free)

---

**Questions?** Re-read the relevant section or check the troubleshooting guide. You've got this! 💪

