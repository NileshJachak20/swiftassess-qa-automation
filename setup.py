#!/usr/bin/env python3
"""
Setup script for SwiftAssess QA Automation project
"""
import os
import sys
import subprocess
import platform
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

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    print("🟢 Checking Node.js version...")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✅ Node.js {version} is installed")
        return True
    except FileNotFoundError:
        print("❌ Node.js is not installed")
        print("Please install Node.js 16+ from https://nodejs.org/")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def install_node_dependencies():
    """Install Node.js dependencies"""
    return run_command("npm install", "Installing Node.js dependencies")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = [
        "reports",
        "screenshots", 
        "test_data",
        "logs",
        "reports/allure-results",
        "reports/allure-report"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_environment():
    """Setup environment configuration"""
    print("⚙️ Setting up environment configuration...")
    
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            run_command("cp env.example .env", "Creating .env file from template")
            print("✅ Environment file created. Please update .env with your configuration.")
        else:
            print("⚠️ env.example file not found. Please create .env manually.")
    else:
        print("✅ .env file already exists")

def setup_git_hooks():
    """Setup git hooks for code quality"""
    print("🔧 Setting up git hooks...")
    
    # Pre-commit hook
    pre_commit_hook = """#!/bin/sh
# Pre-commit hook for SwiftAssess QA Automation

echo "Running pre-commit checks..."

# Run linting
pylint tests/ --disable=C0114,C0116 || true

# Run formatting check
black --check tests/ || true

# Run tests
pytest tests/functional/ -m smoke -v || true

echo "Pre-commit checks completed"
"""
    
    with open(".git/hooks/pre-commit", "w") as f:
        f.write(pre_commit_hook)
    
    # Make executable
    os.chmod(".git/hooks/pre-commit", 0o755)
    print("✅ Git hooks configured")

def verify_installation():
    """Verify installation"""
    print("🔍 Verifying installation...")
    
    # Check Python packages
    python_packages = ["pytest", "selenium", "pandas", "openpyxl"]
    for package in python_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
    
    # Check Node.js packages
    try:
        result = subprocess.run(["npm", "list", "k6"], capture_output=True, text=True)
        if "k6" in result.stdout:
            print("✅ k6 is installed")
        else:
            print("❌ k6 is not installed")
    except:
        print("❌ Could not verify k6 installation")

def run_sample_tests():
    """Run sample tests to verify setup"""
    print("🧪 Running sample tests...")
    
    # Run a simple test
    success = run_command("pytest tests/functional/ -m smoke --tb=short", "Running sample smoke tests")
    
    if success:
        print("✅ Sample tests passed")
    else:
        print("⚠️ Sample tests failed - this is normal for initial setup")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 SwiftAssess QA Automation Setup Complete!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Update .env file with your configuration")
    print("2. Run functional tests: pytest tests/functional/ -v")
    print("3. Run device tests: pytest tests/device/ -v")
    print("4. Run load tests: npm run load:baseline")
    print("5. Generate reports: python scripts/generate_combined_report.py")
    print("\n📚 Documentation:")
    print("- Test Plan: docs/TestPlan.md")
    print("- Test Report: docs/TestReport.md")
    print("- Load Test Report: docs/LoadTestReport.md")
    print("\n🔧 CI/CD Pipeline:")
    print("- Jenkinsfile: Configure Jenkins pipeline")
    print("- Docker: docker-compose up for containerized testing")
    print("\n📞 Support:")
    print("- Check README.md for detailed instructions")
    print("- Review test logs in logs/ directory")
    print("- Screenshots saved in screenshots/ directory")
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🚀 SwiftAssess QA Automation Setup")
    print("="*50)
    
    # Check system requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        print("⚠️ Node.js not found. Some features may not work.")
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    # Install dependencies
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    if not install_node_dependencies():
        print("⚠️ Failed to install Node.js dependencies")
    
    # Setup git hooks
    if os.path.exists(".git"):
        setup_git_hooks()
    
    # Verify installation
    verify_installation()
    
    # Run sample tests
    run_sample_tests()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
