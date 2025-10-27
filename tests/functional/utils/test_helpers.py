"""
Test helper utilities for SwiftAssess testing
"""

import os
import json
import csv
import random
import string
import logging
from datetime import datetime
from faker import Faker
from typing import Dict, List, Any


class TestDataGenerator:
    """Generate test data for SwiftAssess testing"""

    def __init__(self):
        self.fake = Faker()
        self.logger = logging.getLogger(__name__)

    def generate_valid_user_data(self) -> Dict[str, Any]:
        """Generate valid user data for signup"""
        return {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.fake.email(),
            "password": self._generate_strong_password(),
            "confirm_password": "",  # Will be set to same as password
            "accept_terms": True,
            "accept_privacy": True,
        }

    def generate_invalid_user_data(self, error_type: str) -> Dict[str, Any]:
        """Generate invalid user data based on error type"""
        base_data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.fake.email(),
            "password": self._generate_strong_password(),
            "confirm_password": "",
            "accept_terms": True,
            "accept_privacy": True,
        }

        if error_type == "empty_first_name":
            base_data["first_name"] = ""
        elif error_type == "empty_last_name":
            base_data["last_name"] = ""
        elif error_type == "invalid_email":
            base_data["email"] = "invalid-email"
        elif error_type == "weak_password":
            base_data["password"] = "123"
        elif error_type == "mismatched_passwords":
            base_data["password"] = self._generate_strong_password()
            base_data["confirm_password"] = self._generate_strong_password()
        elif error_type == "no_terms":
            base_data["accept_terms"] = False
        elif error_type == "no_privacy":
            base_data["accept_privacy"] = False

        # Set confirm_password to match password if not specifically mismatched
        if error_type != "mismatched_passwords":
            base_data["confirm_password"] = base_data["password"]

        return base_data

    def _generate_strong_password(self) -> str:
        """Generate a strong password"""
        # Ensure password has uppercase, lowercase, number, and special character
        password = (
            random.choice(string.ascii_uppercase)
            + random.choice(string.ascii_lowercase)
            + random.choice(string.digits)
            + random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")
            + "".join(random.choices(string.ascii_letters + string.digits, k=8))
        )
        return "".join(random.sample(password, len(password)))

    def generate_bulk_user_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate bulk user data for load testing"""
        users = []
        for _ in range(count):
            user = self.generate_valid_user_data()
            # Ensure unique emails
            user["email"] = f"loadtest_{random.randint(10000, 99999)}@example.com"
            users.append(user)
        return users


class TestDataManager:
    """Manage test data files"""

    def __init__(self, data_dir: str = "test_data"):
        self.data_dir = data_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(data_dir, exist_ok=True)

    def save_test_data(self, data: List[Dict], filename: str, format: str = "json"):
        """Save test data to file"""
        filepath = os.path.join(self.data_dir, filename)

        if format.lower() == "json":
            with open(f"{filepath}.json", "w") as f:
                json.dump(data, f, indent=2)
        elif format.lower() == "csv":
            if data:
                with open(f"{filepath}.csv", "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)

        self.logger.info(f"Test data saved to {filepath}.{format}")

    def load_test_data(self, filename: str, format: str = "json") -> List[Dict]:
        """Load test data from file"""
        filepath = os.path.join(self.data_dir, f"{filename}.{format}")

        if not os.path.exists(filepath):
            self.logger.warning(f"Test data file not found: {filepath}")
            return []

        try:
            if format.lower() == "json":
                with open(filepath, "r") as f:
                    return json.load(f)
            elif format.lower() == "csv":
                with open(filepath, "r") as f:
                    reader = csv.DictReader(f)
                    return list(reader)
        except Exception as e:
            self.logger.error(f"Error loading test data: {e}")
            return []


class ScreenshotManager:
    """Manage screenshot capture and storage"""

    def __init__(self, screenshot_dir: str = "screenshots"):
        self.screenshot_dir = screenshot_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(screenshot_dir, exist_ok=True)

    def capture_screenshot(self, driver, test_name: str, status: str = "info"):
        """Capture screenshot with timestamp and test info"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"{test_name}_{status}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)

        try:
            driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot captured: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {e}")
            return None

    def capture_element_screenshot(
        self, driver, element, test_name: str, status: str = "info"
    ):
        """Capture screenshot of specific element"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"{test_name}_{status}_element_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)

        try:
            element.screenshot(filepath)
            self.logger.info(f"Element screenshot captured: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to capture element screenshot: {e}")
            return None


class RetryMechanism:
    """Implement retry mechanism for flaky tests"""

    def __init__(self, max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
        self.max_attempts = max_attempts
        self.delay = delay
        self.backoff = backoff
        self.logger = logging.getLogger(__name__)

    def retry(self, func, *args, **kwargs):
        """Retry function execution with exponential backoff"""
        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_attempts - 1:
                    self.logger.error(
                        f"Function failed after {self.max_attempts} attempts: {e}"
                    )
                    raise

                wait_time = self.delay * (self.backoff**attempt)
                self.logger.warning(
                    f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}"
                )
                import time

                time.sleep(wait_time)


class TestReportGenerator:
    """Generate test reports"""

    def __init__(self, report_dir: str = "reports"):
        self.report_dir = report_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(report_dir, exist_ok=True)

    def generate_html_report(self, test_results: List[Dict], filename: str = None):
        """Generate HTML test report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_report_{timestamp}.html"

        filepath = os.path.join(self.report_dir, filename)

        html_content = self._generate_html_content(test_results)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        self.logger.info(f"HTML report generated: {filepath}")
        return filepath

    def _generate_html_content(self, test_results: List[Dict]) -> str:
        """Generate HTML content for test report"""
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r.get("status") == "PASSED"])
        failed_tests = len([r for r in test_results if r.get("status") == "FAILED"])
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SwiftAssess Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ margin: 20px 0; }}
                .test-case {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 3px; }}
                .passed {{ background-color: #d4edda; }}
                .failed {{ background-color: #f8d7da; }}
                .screenshot {{ max-width: 300px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>SwiftAssess Test Report</h1>
                <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            
            <div class="summary">
                <h2>Test Summary</h2>
                <p><strong>Total Tests:</strong> {total_tests}</p>
                <p><strong>Passed:</strong> {passed_tests}</p>
                <p><strong>Failed:</strong> {failed_tests}</p>
                <p><strong>Pass Rate:</strong> {pass_rate:.1f}%</p>
            </div>
            
            <div class="test-results">
                <h2>Test Results</h2>
        """

        for result in test_results:
            status_class = "passed" if result.get("status") == "PASSED" else "failed"
            html += f"""
                <div class="test-case {status_class}">
                    <h3>{result.get('name', 'Unknown Test')}</h3>
                    <p><strong>Status:</strong> {result.get('status', 'UNKNOWN')}</p>
                    <p><strong>Duration:</strong> {result.get('duration', 'N/A')}s</p>
                    <p><strong>Description:</strong> {result.get('description', 'No description')}</p>
            """

            if result.get("error"):
                html += f"<p><strong>Error:</strong> {result.get('error')}</p>"

            if result.get("screenshot"):
                html += f'<img src="{result.get("screenshot")}" class="screenshot" alt="Screenshot">'

            html += "</div>"

        html += """
            </div>
        </body>
        </html>
        """

        return html


class DeviceManager:
    """Manage device configurations for testing"""

    def __init__(self):
        self.devices = {
            "desktop_chrome": {
                "browser": "chrome",
                "viewport": [1920, 1080],
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            },
            "desktop_firefox": {
                "browser": "firefox",
                "viewport": [1920, 1080],
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            },
            "mobile_iphone": {
                "browser": "chrome",
                "viewport": [375, 667],
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
            },
            "mobile_android": {
                "browser": "chrome",
                "viewport": [360, 640],
                "user_agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36",
            },
            "tablet_ipad": {
                "browser": "chrome",
                "viewport": [768, 1024],
                "user_agent": "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
            },
        }

    def get_device_config(self, device_name: str) -> Dict[str, Any]:
        """Get device configuration"""
        if device_name not in self.devices:
            raise ValueError(f"Unknown device: {device_name}")
        return self.devices[device_name]

    def get_all_devices(self) -> List[str]:
        """Get list of all available devices"""
        return list(self.devices.keys())
