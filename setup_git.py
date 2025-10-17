#!/usr/bin/env python3
"""
Git Setup Script for SwiftAssess QA Automation
This script helps set up git repository and initial configuration
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_git_installed():
    """Check if git is installed"""
    print("🔍 Checking if Git is installed...")
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git is not installed")
            return False
    except FileNotFoundError:
        print("❌ Git is not installed or not in PATH")
        return False

def initialize_git_repo():
    """Initialize git repository"""
    print("\n📁 Initializing Git repository...")
    
    # Check if already a git repo
    if os.path.exists(".git"):
        print("ℹ️ Git repository already exists")
        return True
    
    # Initialize git repository
    if run_command("git init", "Initializing Git repository"):
        print("✅ Git repository initialized")
        return True
    else:
        print("❌ Failed to initialize Git repository")
        return False

def setup_git_config():
    """Setup basic git configuration"""
    print("\n⚙️ Setting up Git configuration...")
    
    # Get user input for git config
    print("Please provide your Git configuration:")
    
    # Get name
    name = input("Enter your name (for Git commits): ").strip()
    if not name:
        name = "QA Automation Team"
        print(f"Using default name: {name}")
    
    # Get email
    email = input("Enter your email (for Git commits): ").strip()
    if not email:
        email = "qa-team@company.com"
        print(f"Using default email: {email}")
    
    # Set git config
    commands = [
        f'git config user.name "{name}"',
        f'git config user.email "{email}"',
        'git config core.autocrlf true',
        'git config core.safecrlf true',
        'git config pull.rebase false'
    ]
    
    for command in commands:
        if not run_command(command, f"Setting {command.split()[-1]}"):
            print(f"⚠️ Warning: Failed to set {command}")
    
    print("✅ Git configuration completed")
    return True

def add_files_to_git():
    """Add files to git repository"""
    print("\n📝 Adding files to Git repository...")
    
    # Add all files
    if run_command("git add .", "Adding files to Git"):
        print("✅ Files added to Git repository")
        return True
    else:
        print("❌ Failed to add files to Git")
        return False

def create_initial_commit():
    """Create initial commit"""
    print("\n💾 Creating initial commit...")
    
    commit_message = "Initial commit: SwiftAssess QA Automation project setup"
    
    if run_command(f'git commit -m "{commit_message}"', "Creating initial commit"):
        print("✅ Initial commit created")
        return True
    else:
        print("❌ Failed to create initial commit")
        return False

def setup_remote_repository():
    """Setup remote repository"""
    print("\n🌐 Setting up remote repository...")
    
    print("To connect to a remote repository, you have several options:")
    print("1. GitHub: https://github.com")
    print("2. GitLab: https://gitlab.com")
    print("3. Bitbucket: https://bitbucket.org")
    print("4. Azure DevOps: https://dev.azure.com")
    
    remote_url = input("\nEnter remote repository URL (or press Enter to skip): ").strip()
    
    if remote_url:
        if run_command(f"git remote add origin {remote_url}", "Adding remote origin"):
            print("✅ Remote repository added")
            
            # Ask if user wants to push
            push_now = input("Do you want to push to remote repository now? (y/n): ").strip().lower()
            if push_now in ['y', 'yes']:
                if run_command("git push -u origin main", "Pushing to remote repository"):
                    print("✅ Code pushed to remote repository")
                else:
                    print("⚠️ Failed to push to remote repository")
                    print("You can try again later with: git push -u origin main")
        else:
            print("❌ Failed to add remote repository")
    else:
        print("ℹ️ Skipping remote repository setup")
        print("You can add a remote repository later with:")
        print("git remote add origin <repository-url>")
        print("git push -u origin main")

def show_git_status():
    """Show git status"""
    print("\n📊 Git Repository Status:")
    print("=" * 40)
    
    # Show git status
    run_command("git status", "Checking Git status")
    
    # Show git log
    print("\n📝 Recent commits:")
    run_command("git log --oneline -5", "Showing recent commits")

def show_next_steps():
    """Show next steps for git usage"""
    print("\n" + "="*60)
    print("🎉 Git Setup Complete!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Create a repository on GitHub/GitLab/Bitbucket")
    print("2. Add remote repository:")
    print("   git remote add origin <repository-url>")
    print("3. Push your code:")
    print("   git push -u origin main")
    
    print("\n🔧 Common Git Commands:")
    print("• Check status: git status")
    print("• Add files: git add .")
    print("• Commit changes: git commit -m 'Your message'")
    print("• Push changes: git push")
    print("• Pull changes: git pull")
    print("• Create branch: git checkout -b feature-branch")
    print("• Switch branch: git checkout branch-name")
    print("• Merge branch: git merge branch-name")
    
    print("\n📁 Project Structure:")
    print("• Source code: All Python/JavaScript files")
    print("• Configuration: config/, pytest.ini, package.json")
    print("• Documentation: docs/, README.md")
    print("• CI/CD: Jenkinsfile, docker-compose.yml")
    print("• Reports: reports/ (generated files ignored)")
    print("• Screenshots: screenshots/ (generated files ignored)")
    print("• Logs: logs/ (generated files ignored)")

def main():
    """Main function to setup git repository"""
    print("🚀 SwiftAssess QA Automation - Git Setup")
    print("=" * 50)
    
    # Check if git is installed
    if not check_git_installed():
        print("\n❌ Git is not installed. Please install Git first:")
        print("• Windows: https://git-scm.com/download/win")
        print("• macOS: brew install git")
        print("• Linux: sudo apt-get install git")
        return
    
    # Initialize git repository
    if not initialize_git_repo():
        return
    
    # Setup git configuration
    if not setup_git_config():
        return
    
    # Add files to git
    if not add_files_to_git():
        return
    
    # Create initial commit
    if not create_initial_commit():
        return
    
    # Setup remote repository
    setup_remote_repository()
    
    # Show git status
    show_git_status()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
