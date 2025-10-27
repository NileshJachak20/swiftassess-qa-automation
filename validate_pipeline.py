"""
Azure DevOps Pipeline Validation Script
Validates that all required files and configurations are in place for the pipeline to run successfully
"""

import os
import sys
import json
from pathlib import Path

# Try to import yaml, but continue without it if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("Warning: PyYAML not installed. YAML validation will be limited.")

class PipelineValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.project_root = Path(__file__).parent
        
    def validate(self):
        """Run all validation checks"""
        print("=" * 80)
        print("Azure DevOps Pipeline Validation")
        print("=" * 80)
        print()
        
        self.check_pipeline_file()
        self.check_requirements_file()
        self.check_package_json()
        self.check_test_files()
        self.check_config_files()
        self.check_script_files()
        self.check_directory_structure()
        self.check_pytest_config()
        
        self.print_summary()
        
        return len(self.errors) == 0
    
    def check_pipeline_file(self):
        """Check if azure-pipelines.yml exists and is valid"""
        print("✓ Checking azure-pipelines.yml...")
        
        pipeline_file = self.project_root / "azure-pipelines.yml"
        
        if not pipeline_file.exists():
            self.errors.append("azure-pipelines.yml not found")
            return
        
        try:
            with open(pipeline_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic validation without YAML parsing
            required_keywords = ['trigger', 'variables', 'stages', 'jobs', 'steps']
            for keyword in required_keywords:
                if keyword not in content:
                    self.warnings.append(f"Keyword '{keyword}' not found in pipeline file")
            
            # Check for expected stage names
            expected_stages = [
                'Setup',
                'Functional_Tests',
                'Device_Tests',
                'Load_Tests',
                'Reports',
                'Notification'
            ]
            
            for stage in expected_stages:
                if stage not in content:
                    self.warnings.append(f"Expected stage not found: {stage}")
            
            # If YAML is available, do full validation
            if HAS_YAML:
                with open(pipeline_file, 'r', encoding='utf-8') as f:
                    try:
                        pipeline_config = yaml.safe_load(f)
                        print(f"  ✓ Pipeline YAML is valid")
                    except yaml.YAMLError as e:
                        self.errors.append(f"Invalid YAML syntax: {e}")
                        return
            else:
                print(f"  ✓ Pipeline file exists (basic validation only)")
                        
            print(f"  ✓ Pipeline file contains expected content")
            
        except Exception as e:
            self.errors.append(f"Error reading pipeline file: {e}")
    
    def check_requirements_file(self):
        """Check if requirements.txt exists and contains required packages"""
        print("✓ Checking requirements.txt...")
        
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            self.errors.append("requirements.txt not found")
            return
        
        required_packages = [
            'pytest',
            'selenium',
            'pytest-html',
            'pytest-json-report',
            'allure-pytest',
            'webdriver-manager'
        ]
        
        with open(requirements_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for package in required_packages:
            if package not in content:
                self.warnings.append(f"Required package not found: {package}")
        
        print(f"  ✓ Requirements file is valid")
    
    def check_package_json(self):
        """Check if package.json exists and contains required scripts"""
        print("✓ Checking package.json...")
        
        package_file = self.project_root / "package.json"
        
        if not package_file.exists():
            self.errors.append("package.json not found")
            return
        
        try:
            with open(package_file, 'r', encoding='utf-8') as f:
                package_config = json.load(f)
            
            # Check required scripts
            required_scripts = [
                'load:baseline',
                'load:stress',
                'load:spike'
            ]
            
            scripts = package_config.get('scripts', {})
            for script in required_scripts:
                if script not in scripts:
                    self.errors.append(f"Required npm script not found: {script}")
            
            print(f"  ✓ Package.json is valid")
            
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON syntax in package.json: {e}")
        except Exception as e:
            self.errors.append(f"Error reading package.json: {e}")
    
    def check_test_files(self):
        """Check if test files exist"""
        print("✓ Checking test files...")
        
        test_files = [
            "tests/functional/tests/test_signup_functional.py",
            "tests/device/test_device_compatibility.py",
            "tests/load/load_test_baseline.js",
            "tests/load/load_test_stress.js",
            "tests/load/load_test_spike.js"
        ]
        
        for test_file in test_files:
            file_path = self.project_root / test_file
            if not file_path.exists():
                self.errors.append(f"Test file not found: {test_file}")
            else:
                print(f"  ✓ Found: {test_file}")
    
    def check_config_files(self):
        """Check if configuration files exist"""
        print("✓ Checking configuration files...")
        
        config_files = [
            "config/config.yaml",
            "pytest.ini"
        ]
        
        for config_file in config_files:
            file_path = self.project_root / config_file
            if not file_path.exists():
                self.errors.append(f"Configuration file not found: {config_file}")
            else:
                print(f"  ✓ Found: {config_file}")
    
    def check_script_files(self):
        """Check if report generation scripts exist"""
        print("✓ Checking script files...")
        
        script_files = [
            "scripts/generate_combined_report.py",
            "scripts/generate_bug_report.py"
        ]
        
        for script_file in script_files:
            file_path = self.project_root / script_file
            if not file_path.exists():
                self.warnings.append(f"Script file not found: {script_file}")
            else:
                print(f"  ✓ Found: {script_file}")
    
    def check_directory_structure(self):
        """Check if required directories exist"""
        print("✓ Checking directory structure...")
        
        required_dirs = [
            "tests",
            "tests/functional",
            "tests/device",
            "tests/load",
            "config",
            "scripts",
            "reports",
            "screenshots"
        ]
        
        for directory in required_dirs:
            dir_path = self.project_root / directory
            if not dir_path.exists():
                print(f"  ! Creating missing directory: {directory}")
                dir_path.mkdir(parents=True, exist_ok=True)
            else:
                print(f"  ✓ Found: {directory}/")
    
    def check_pytest_config(self):
        """Check pytest.ini configuration"""
        print("✓ Checking pytest.ini configuration...")
        
        pytest_file = self.project_root / "pytest.ini"
        
        if not pytest_file.exists():
            self.errors.append("pytest.ini not found")
            return
        
        try:
            with open(pytest_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_markers = ['smoke', 'regression', 'functional', 'device']
            for marker in required_markers:
                if marker not in content:
                    self.warnings.append(f"Pytest marker not found: {marker}")
            
            print(f"  ✓ Pytest configuration is valid")
            
        except Exception as e:
            self.errors.append(f"Error reading pytest.ini: {e}")
    
    def print_summary(self):
        """Print validation summary"""
        print()
        print("=" * 80)
        print("Validation Summary")
        print("=" * 80)
        
        if not self.errors and not self.warnings:
            print("✅ All validation checks passed!")
            print("✅ Pipeline is ready to run on Azure DevOps")
        else:
            if self.errors:
                print(f"\n❌ ERRORS ({len(self.errors)}):")
                for i, error in enumerate(self.errors, 1):
                    print(f"  {i}. {error}")
            
            if self.warnings:
                print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"  {i}. {warning}")
        
        print()
        print("=" * 80)
        
        if self.errors:
            print("❌ Pipeline validation FAILED - Please fix errors before proceeding")
            print("=" * 80)
        else:
            print("✅ Pipeline validation PASSED - Ready for Azure DevOps deployment")
            print("=" * 80)

def main():
    """Main function"""
    validator = PipelineValidator()
    success = validator.validate()
    
    if not success:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()

