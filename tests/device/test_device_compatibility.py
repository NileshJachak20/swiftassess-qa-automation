"""
Device compatibility tests for SwiftAssess signup page
"""
import pytest
import logging
import time
from tests.functional.pages.signup_page import SignupPage
from tests.functional.utils.test_helpers import (
    TestDataGenerator, 
    ScreenshotManager, 
    DeviceManager
)

class TestDeviceCompatibility:
    """Device compatibility test cases"""
    
    @pytest.fixture(autouse=True)
    def setup(self, request):
        """Setup for each test"""
        self.logger = logging.getLogger(__name__)
        self.data_generator = TestDataGenerator()
        self.screenshot_manager = ScreenshotManager()
        self.device_manager = DeviceManager()
        
        # Get device from pytest parameter
        device_name = getattr(request.config.option, 'device', 'desktop_chrome')
        device_config = self.device_manager.get_device_config(device_name)
        
        # Initialize signup page with device configuration
        self.signup_page = SignupPage(
            browser=device_config['browser'], 
            headless=False
        )
        
        # Set viewport size
        self.signup_page.driver.set_window_size(
            device_config['viewport'][0], 
            device_config['viewport'][1]
        )
        
        # Navigate to signup page
        self.signup_page.navigate_to_signup()
        
        yield
        
        # Cleanup
        if hasattr(self, 'signup_page'):
            self.signup_page.close_browser()
    
    @pytest.mark.device
    @pytest.mark.chrome
    def test_desktop_chrome_compatibility(self):
        """Test signup page on desktop Chrome browser"""
        test_name = "test_desktop_chrome_compatibility"
        
        try:
            # Verify page loads correctly
            assert self.signup_page.is_signup_form_visible(), "Signup form should be visible on desktop Chrome"
            
            # Test form functionality
            user_data = self.data_generator.generate_valid_user_data()
            user_data['confirm_password'] = user_data['password']
            
            # Fill form
            self.signup_page.fill_signup_form(user_data)
            
            # Verify all fields are filled
            assert self.signup_page.get_field_value('first_name') == user_data['first_name']
            assert self.signup_page.get_field_value('last_name') == user_data['last_name']
            assert self.signup_page.get_field_value('email') == user_data['email']
            
            # Test form submission
            self.signup_page.click_signup_button()
            
            # Wait for response
            time.sleep(2)
            
            self.logger.info("Desktop Chrome compatibility test passed")
            
        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, 'failed'
            )
            self.logger.error(f"Desktop Chrome compatibility test failed: {e}")
            raise
    
    @pytest.mark.device
    @pytest.mark.firefox
    def test_desktop_firefox_compatibility(self):
        """Test signup page on desktop Firefox browser"""
        test_name = "test_desktop_firefox_compatibility"
        
        try:
            # Verify page loads correctly
            assert self.signup_page.is_signup_form_visible(), "Signup form should be visible on desktop Firefox"
            
            # Test form functionality
            user_data = self.data_generator.generate_valid_user_data()
            user_data['confirm_password'] = user_data['password']
            
            # Fill form
            self.signup_page.fill_signup_form(user_data)
            
            # Verify all fields are filled
            assert self.signup_page.get_field_value('first_name') == user_data['first_name']
            assert self.signup_page.get_field_value('last_name') == user_data['last_name']
            assert self.signup_page.get_field_value('email') == user_data['email']
            
            # Test form submission
            self.signup_page.click_signup_button()
            
            # Wait for response
            time.sleep(2)
            
            self.logger.info("Desktop Firefox compatibility test passed")
            
        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, 'failed'
            )
            self.logger.error(f"Desktop Firefox compatibility test failed: {e}")
            raise
    
    @pytest.mark.device
    @pytest.mark.edge
    def test_desktop_edge_compatibility(self):
        """Test signup page on desktop Edge browser"""
        test_name = "test_desktop_edge_compatibility"
        
        try:
            # Verify page loads correctly
            assert self.signup_page.is_signup_form_visible(), "Signup form should be visible on desktop Edge"
            
            # Test form functionality
            user_data = self.data_generator.generate_valid_user_data()
            user_data['confirm_password'] = user_data['password']
            
            # Fill form
            self.signup_page.fill_signup_form(user_data)
            
            # Verify all fields are filled
            assert self.signup_page.get_field_value('first_name') == user_data['first_name']
            assert self.signup_page.get_field_value('last_name') == user_data['last_name']
            assert self.signup_page.get_field_value('email') == user_data['email']
            
            # Test form submission
            self.signup_page.click_signup_button()
            
            # Wait for response
            time.sleep(2)
            
            self.logger.info("Desktop Edge compatibility test passed")
            
        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, 'failed'
            )
            self.logger.error(f"Desktop Edge compatibility test failed: {e}")
            raise
    
    @pytest.mark.device
    @pytest.mark.mobile
    def test_mobile_iphone_compatibility(self):
        """Test signup page on mobile iPhone"""
        test_name = "test_mobile_iphone_compatibility"
        
        try:
            # Verify page loads correctly
            assert self.signup_page.is_signup_form_visible(), "Signup form should be visible on mobile iPhone"
            
            # Test responsive design
            page_title = self.signup_page.get_page_title()
            assert page_title, "Page should have a title on mobile iPhone"
            
            # Test form functionality
            user_data = self.data_generator.generate_valid_user_data()
            user_data['confirm_password'] = user_data['password']
            
            # Fill form
            self.signup_page.fill_signup_form(user_data)
            
            # Verify all fields are filled
            assert self.signup_page.get_field_value('first_name') == user_data['first_name']
            assert self.signup_page.get_field_value('last_name') == user_data['last_name']
            assert self.signup_page.get_field_value('email') == user_data['email']
            
            # Test form submission
            self.signup_page.click_signup_button()
            
            # Wait for response
            time.sleep(2)
            
            self.logger.info("Mobile iPhone compatibility test passed")
            
        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, 'failed'
            )
            self.logger.error(f"Mobile iPhone compatibility test failed: {e}")
            raise
    
    @pytest.mark.device
    @pytest.mark.mobile
    def test_mobile_android_compatibility(self):
        """Test signup page on mobile Android"""
        test_name = "test_mobile_android_compatibility"
        
        try:
            # Verify page loads correctly
            assert self.signup_page.is_signup_form_visible(), "Signup form should be visible on mobile Android"
            
            # Test responsive design
            page_title = self.signup_page.get_page_title()
            assert page_title, "Page should have a title on mobile Android"
            
            # Test form functionality
            user_data = self.data_generator.generate_valid_user_data()
            user_data['confirm_password'] = user_data['password']
            
            # Fill form
            self.signup_page.fill_signup_form(user_data)
            
            # Verify all fields are filled
            assert self.signup_page.get_field_value('first_name') == user_data['first_name']
            assert self.signup_page.get_field_value('last_name') == user_data['last_name']
            assert self.signup_page.get_field_value('email') == user_data['email']
            
            # Test form submission
            self.signup_page.click_signup_button()
            
            # Wait for response
            time.sleep(2)
            
            self.logger.info("Mobile Android compatibility test passed")
            
        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, 'failed'
            )
            self.logger.error(f"Mobile Android compatibility test failed: {e}")
            raise
    
    @pytest.mark.device
    @pytest.mark.tablet
    def test_tablet_ipad_compatibility(self):
        """Test signup page on tablet iPad"""
        test_name = "test_tablet_ipad_compatibility"
        
        try:
            # Verify page loads correctly
            assert self.signup_page.is_signup_form_visible(), "Signup form should be visible on tablet iPad"
            
            # Test responsive design
            page_title = self.signup_page.get_page_title()
            assert page_title, "Page should have a title on tablet iPad"
            
            # Test form functionality
            user_data = self.data_generator.generate_valid_user_data()
            user_data['confirm_password'] = user_data['password']
            
            # Fill form
            self.signup_page.fill_signup_form(user_data)
            
            # Verify all fields are filled
            assert self.signup_page.get_field_value('first_name') == user_data['first_name']
            assert self.signup_page.get_field_value('last_name') == user_data['last_name']
            assert self.signup_page.get_field_value('email') == user_data['email']
            
            # Test form submission
            self.signup_page.click_signup_button()
            
            # Wait for response
            time.sleep(2)
            
            self.logger.info("Tablet iPad compatibility test passed")
            
        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, 'failed'
            )
            self.logger.error(f"Tablet iPad compatibility test failed: {e}")
            raise
    
    @pytest.mark.device
    def test_responsive_design_validation(self):
        """Test responsive design across different viewport sizes"""
        test_name = "test_responsive_design_validation"
        
        try:
            # Test different viewport sizes
            viewports = [
                (1920, 1080),  # Desktop
                (1366, 768),   # Laptop
                (1024, 768),   # Tablet landscape
                (768, 1024),   # Tablet portrait
                (375, 667),    # Mobile portrait
                (667, 375)     # Mobile landscape
            ]
            
            for width, height in viewports:
                # Set viewport size
                self.signup_page.driver.set_window_size(width, height)
                time.sleep(1)  # Wait for resize
                
                # Verify page loads correctly
                assert self.signup_page.is_signup_form_visible(), f"Signup form should be visible at {width}x{height}"
                
                # Test form elements are accessible
                assert self.signup_page.is_element_visible(self.signup_page.FIRST_NAME_INPUT), f"First name input should be visible at {width}x{height}"
                assert self.signup_page.is_element_visible(self.signup_page.LAST_NAME_INPUT), f"Last name input should be visible at {width}x{height}"
                assert self.signup_page.is_element_visible(self.signup_page.EMAIL_INPUT), f"Email input should be visible at {width}x{height}"
                assert self.signup_page.is_element_visible(self.signup_page.PASSWORD_INPUT), f"Password input should be visible at {width}x{height}"
                assert self.signup_page.is_element_visible(self.signup_page.SIGNUP_BUTTON), f"Signup button should be visible at {width}x{height}"
                
                self.logger.info(f"Responsive design test passed for {width}x{height}")
            
            self.logger.info("Responsive design validation test passed")
            
        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, 'failed'
            )
            self.logger.error(f"Responsive design validation test failed: {e}")
            raise
    
    @pytest.mark.device
    def test_touch_interactions(self):
        """Test touch interactions on mobile devices"""
        test_name = "test_touch_interactions"
        
        try:
            # Test touch interactions (simulated with mouse events)
            user_data = self.data_generator.generate_valid_user_data()
            user_data['confirm_password'] = user_data['password']
            
            # Test touch on form fields
            self.signup_page.click_element(self.signup_page.FIRST_NAME_INPUT)
            self.signup_page.enter_first_name(user_data['first_name'])
            
            self.signup_page.click_element(self.signup_page.LAST_NAME_INPUT)
            self.signup_page.enter_last_name(user_data['last_name'])
            
            self.signup_page.click_element(self.signup_page.EMAIL_INPUT)
            self.signup_page.enter_email(user_data['email'])
            
            self.signup_page.click_element(self.signup_page.PASSWORD_INPUT)
            self.signup_page.enter_password(user_data['password'])
            
            self.signup_page.click_element(self.signup_page.CONFIRM_PASSWORD_INPUT)
            self.signup_page.enter_confirm_password(user_data['confirm_password'])
            
            # Test touch on checkboxes
            self.signup_page.click_element(self.signup_page.TERMS_CHECKBOX)
            self.signup_page.click_element(self.signup_page.PRIVACY_CHECKBOX)
            
            # Test touch on submit button
            self.signup_page.click_element(self.signup_page.SIGNUP_BUTTON)
            
            # Wait for response
            time.sleep(2)
            
            self.logger.info("Touch interactions test passed")
            
        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, 'failed'
            )
            self.logger.error(f"Touch interactions test failed: {e}")
            raise
    
    @pytest.mark.device
    def test_mobile_keyboard_handling(self):
        """Test mobile keyboard handling"""
        test_name = "test_mobile_keyboard_handling"
        
        try:
            # Test keyboard input on mobile
            user_data = self.data_generator.generate_valid_user_data()
            user_data['confirm_password'] = user_data['password']
            
            # Test input with mobile keyboard
            self.signup_page.enter_first_name(user_data['first_name'])
            self.signup_page.enter_last_name(user_data['last_name'])
            self.signup_page.enter_email(user_data['email'])
            self.signup_page.enter_password(user_data['password'])
            self.signup_page.enter_confirm_password(user_data['confirm_password'])
            
            # Verify inputs are correctly entered
            assert self.signup_page.get_field_value('first_name') == user_data['first_name']
            assert self.signup_page.get_field_value('last_name') == user_data['last_name']
            assert self.signup_page.get_field_value('email') == user_data['email']
            
            self.logger.info("Mobile keyboard handling test passed")
            
        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, 'failed'
            )
            self.logger.error(f"Mobile keyboard handling test failed: {e}")
            raise
    
    @pytest.mark.device
    def test_cross_browser_consistency(self):
        """Test consistency across different browsers"""
        test_name = "test_cross_browser_consistency"
        
        try:
            # Test that form elements are consistent across browsers
            user_data = self.data_generator.generate_valid_user_data()
            user_data['confirm_password'] = user_data['password']
            
            # Fill form
            self.signup_page.fill_signup_form(user_data)
            
            # Verify form state is consistent
            assert self.signup_page.get_field_value('first_name') == user_data['first_name']
            assert self.signup_page.get_field_value('last_name') == user_data['last_name']
            assert self.signup_page.get_field_value('email') == user_data['email']
            
            # Verify checkboxes are checked
            assert self.signup_page.is_checkbox_checked(self.signup_page.TERMS_CHECKBOX)
            assert self.signup_page.is_checkbox_checked(self.signup_page.PRIVACY_CHECKBOX)
            
            # Test form submission
            self.signup_page.click_signup_button()
            
            # Wait for response
            time.sleep(2)
            
            self.logger.info("Cross-browser consistency test passed")
            
        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, 'failed'
            )
            self.logger.error(f"Cross-browser consistency test failed: {e}")
            raise
