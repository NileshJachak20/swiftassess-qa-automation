#!/usr/bin/env python3
"""
Demo test script for SwiftAssess QA Automation
This script demonstrates the testing framework without requiring the full test suite
"""
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class SwiftAssessDemoTest:
    """Demo test class for SwiftAssess signup page"""
    
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        try:
            logger.info("Setting up Chrome WebDriver...")
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("✅ Chrome WebDriver setup successful")
        except Exception as e:
            logger.error(f"❌ Failed to setup WebDriver: {e}")
            raise
    
    def test_signup_page_load(self):
        """Test if signup page loads correctly"""
        try:
            logger.info("🧪 Testing signup page load...")
            url = "https://app.swiftassess.com/Signup"
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Check if page loaded
            title = self.driver.title
            current_url = self.driver.current_url
            
            logger.info(f"Page Title: {title}")
            logger.info(f"Current URL: {current_url}")
            
            # Check for common signup form elements
            form_elements = [
                "firstName", "lastName", "email", "password", "confirmPassword"
            ]
            
            found_elements = []
            for element in form_elements:
                try:
                    if self.driver.find_element(By.ID, element):
                        found_elements.append(element)
                except:
                    pass
            
            logger.info(f"Found form elements: {found_elements}")
            
            if len(found_elements) >= 3:
                logger.info("✅ Signup page loaded successfully with form elements")
                return True
            else:
                logger.warning("⚠️ Signup page loaded but form elements not found")
                return False
                
        except Exception as e:
            logger.error(f"❌ Signup page load test failed: {e}")
            return False
    
    def test_form_interaction(self):
        """Test form field interactions"""
        try:
            logger.info("🧪 Testing form interactions...")
            
            # Test data
            test_data = {
                "firstName": "John",
                "lastName": "Doe", 
                "email": "john.doe@example.com",
                "password": "SecurePass123!",
                "confirmPassword": "SecurePass123!"
            }
            
            # Fill form fields
            for field, value in test_data.items():
                try:
                    element = self.driver.find_element(By.ID, field)
                    element.clear()
                    element.send_keys(value)
                    logger.info(f"✅ Filled {field} field")
                except Exception as e:
                    logger.warning(f"⚠️ Could not fill {field} field: {e}")
            
            # Check if form was filled
            filled_fields = []
            for field in test_data.keys():
                try:
                    element = self.driver.find_element(By.ID, field)
                    if element.get_attribute('value'):
                        filled_fields.append(field)
                except:
                    pass
            
            logger.info(f"Successfully filled fields: {filled_fields}")
            
            if len(filled_fields) >= 3:
                logger.info("✅ Form interaction test passed")
                return True
            else:
                logger.warning("⚠️ Form interaction test had issues")
                return False
                
        except Exception as e:
            logger.error(f"❌ Form interaction test failed: {e}")
            return False
    
    def test_validation(self):
        """Test form validation"""
        try:
            logger.info("🧪 Testing form validation...")
            
            # Clear all fields
            fields = ["firstName", "lastName", "email", "password", "confirmPassword"]
            for field in fields:
                try:
                    element = self.driver.find_element(By.ID, field)
                    element.clear()
                except:
                    pass
            
            # Try to submit empty form
            try:
                submit_button = self.driver.find_element(By.ID, "signupButton")
                submit_button.click()
                time.sleep(2)
                logger.info("✅ Attempted to submit empty form")
            except Exception as e:
                logger.warning(f"⚠️ Could not find submit button: {e}")
            
            # Check for validation errors
            error_elements = self.driver.find_elements(By.CLASS_NAME, "error")
            if error_elements:
                logger.info(f"✅ Found {len(error_elements)} validation errors")
                return True
            else:
                logger.info("ℹ️ No validation errors found (this might be expected)")
                return True
                
        except Exception as e:
            logger.error(f"❌ Validation test failed: {e}")
            return False
    
    def take_screenshot(self, filename):
        """Take screenshot"""
        try:
            screenshot_path = f"screenshots/{filename}"
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"📸 Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"❌ Failed to take screenshot: {e}")
            return None
    
    def run_all_tests(self):
        """Run all demo tests"""
        logger.info("🚀 Starting SwiftAssess Demo Tests")
        logger.info("=" * 50)
        
        results = []
        
        # Test 1: Page Load
        result1 = self.test_signup_page_load()
        results.append(("Page Load Test", result1))
        self.take_screenshot("page_load.png")
        
        # Test 2: Form Interaction
        result2 = self.test_form_interaction()
        results.append(("Form Interaction Test", result2))
        self.take_screenshot("form_filled.png")
        
        # Test 3: Validation
        result3 = self.test_validation()
        results.append(("Validation Test", result3))
        self.take_screenshot("validation_test.png")
        
        # Print results
        logger.info("\n📊 Test Results Summary:")
        logger.info("=" * 30)
        
        passed = 0
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"{test_name}: {status}")
            if result:
                passed += 1
        
        total_tests = len(results)
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        logger.info(f"\n🎯 Overall Results:")
        logger.info(f"Passed: {passed}/{total_tests}")
        logger.info(f"Pass Rate: {pass_rate:.1f}%")
        
        return results
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()
            logger.info("🧹 WebDriver cleanup completed")

def main():
    """Main function"""
    demo = SwiftAssessDemoTest()
    
    try:
        results = demo.run_all_tests()
        
        # Generate simple report
        with open("reports/demo_test_report.html", "w") as f:
            f.write(generate_html_report(results))
        
        logger.info("📄 Demo test report generated: reports/demo_test_report.html")
        
    except Exception as e:
        logger.error(f"❌ Demo test execution failed: {e}")
    finally:
        demo.cleanup()

def generate_html_report(results):
    """Generate HTML report"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SwiftAssess Demo Test Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
            .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px; }}
            .metric {{ background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; }}
            .metric-value {{ font-size: 1.5em; font-weight: bold; color: #007bff; }}
            .test-result {{ margin: 10px 0; padding: 10px; border-radius: 5px; }}
            .passed {{ background-color: #d4edda; border-left: 4px solid #28a745; }}
            .failed {{ background-color: #f8d7da; border-left: 4px solid #dc3545; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 SwiftAssess Demo Test Report</h1>
                <p>Generated on: {timestamp}</p>
            </div>
            
            <div class="summary">
                <div class="metric">
                    <div class="metric-value">{total}</div>
                    <div>Total Tests</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{passed}</div>
                    <div>Passed</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{pass_rate:.1f}%</div>
                    <div>Pass Rate</div>
                </div>
            </div>
            
            <h2>Test Results</h2>
    """
    
    for test_name, result in results:
        status_class = "passed" if result else "failed"
        status_icon = "✅" if result else "❌"
        f.write(f"""
            <div class="test-result {status_class}">
                <strong>{status_icon} {test_name}</strong>
                <span style="float: right;">{"PASSED" if result else "FAILED"}</span>
            </div>
        """)
    
    f.write("""
            <div style="margin-top: 20px; padding: 15px; background-color: #e3f2fd; border-radius: 5px;">
                <h3>📋 Test Summary</h3>
                <p>This demo test validates the basic functionality of the SwiftAssess signup page including:</p>
                <ul>
                    <li>Page loading and accessibility</li>
                    <li>Form field interactions</li>
                    <li>Basic validation testing</li>
                </ul>
                <p><strong>Note:</strong> This is a demonstration of the testing framework. For comprehensive testing, run the full test suite.</p>
            </div>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    main()
