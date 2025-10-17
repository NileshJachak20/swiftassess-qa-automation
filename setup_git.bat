@echo off
echo 🚀 SwiftAssess QA Automation - Git Setup
echo ================================================

echo.
echo 🔍 Checking Git installation...
git --version
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first:
    echo • Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git is installed

echo.
echo 📁 Initializing Git repository...
if exist .git (
    echo ℹ️ Git repository already exists
) else (
    git init
    if %errorlevel% neq 0 (
        echo ❌ Failed to initialize Git repository
        pause
        exit /b 1
    )
    echo ✅ Git repository initialized
)

echo.
echo ⚙️ Setting up Git configuration...
set /p git_name="Enter your name (for Git commits): "
if "%git_name%"=="" set git_name=QA Automation Team

set /p git_email="Enter your email (for Git commits): "
if "%git_email%"=="" set git_email=qa-team@company.com

git config user.name "%git_name%"
git config user.email "%git_email%"
git config core.autocrlf true
git config core.safecrlf true
git config pull.rebase false

echo ✅ Git configuration completed

echo.
echo 📝 Adding files to Git repository...
git add .
if %errorlevel% neq 0 (
    echo ❌ Failed to add files to Git
    pause
    exit /b 1
)
echo ✅ Files added to Git repository

echo.
echo 💾 Creating initial commit...
git commit -m "Initial commit: SwiftAssess QA Automation project setup"
if %errorlevel% neq 0 (
    echo ❌ Failed to create initial commit
    pause
    exit /b 1
)
echo ✅ Initial commit created

echo.
echo 🌐 Setting up remote repository...
set /p remote_url="Enter remote repository URL (or press Enter to skip): "
if not "%remote_url%"=="" (
    git remote add origin "%remote_url%"
    if %errorlevel% neq 0 (
        echo ❌ Failed to add remote repository
    ) else (
        echo ✅ Remote repository added
        set /p push_now="Do you want to push to remote repository now? (y/n): "
        if /i "%push_now%"=="y" (
            git push -u origin main
            if %errorlevel% neq 0 (
                echo ⚠️ Failed to push to remote repository
                echo You can try again later with: git push -u origin main
            ) else (
                echo ✅ Code pushed to remote repository
            )
        )
    )
) else (
    echo ℹ️ Skipping remote repository setup
    echo You can add a remote repository later with:
    echo git remote add origin ^<repository-url^>
    echo git push -u origin main
)

echo.
echo 📊 Git Repository Status:
echo ========================================
git status

echo.
echo 📝 Recent commits:
git log --oneline -5

echo.
echo ================================================
echo 🎉 Git Setup Complete!
echo ================================================

echo.
echo 📋 Next Steps:
echo 1. Create a repository on GitHub/GitLab/Bitbucket
echo 2. Add remote repository:
echo    git remote add origin ^<repository-url^>
echo 3. Push your code:
echo    git push -u origin main

echo.
echo 🔧 Common Git Commands:
echo • Check status: git status
echo • Add files: git add .
echo • Commit changes: git commit -m "Your message"
echo • Push changes: git push
echo • Pull changes: git pull
echo • Create branch: git checkout -b feature-branch
echo • Switch branch: git checkout branch-name
echo • Merge branch: git merge branch-name

echo.
echo 📁 Project Structure:
echo • Source code: All Python/JavaScript files
echo • Configuration: config/, pytest.ini, package.json
echo • Documentation: docs/, README.md
echo • CI/CD: Jenkinsfile, docker-compose.yml
echo • Reports: reports/ (generated files ignored)
echo • Screenshots: screenshots/ (generated files ignored)
echo • Logs: logs/ (generated files ignored)

echo.
pause
