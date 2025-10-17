"""
Signup Page Object Model for SwiftAssess
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from tests.functional.utils.base_page import BasePage

class SignupPage(BasePage):
    """Signup page object model"""
    
    # Locators
    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirmPassword")
    TERMS_CHECKBOX = (By.ID, "terms")
    PRIVACY_CHECKBOX = (By.ID, "privacy")
    SIGNUP_BUTTON = (By.ID, "signupButton")
    
    # Error message locators
    FIRST_NAME_ERROR = (By.ID, "firstNameError")
    LAST_NAME_ERROR = (By.ID, "lastNameError")
    EMAIL_ERROR = (By.ID, "emailError")
    PASSWORD_ERROR = (By.ID, "passwordError")
    CONFIRM_PASSWORD_ERROR = (By.ID, "confirmPasswordError")
    TERMS_ERROR = (By.ID, "termsError")
    GENERAL_ERROR = (By.CLASS_NAME, "error-message")
    
    # Success message locator
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    
    # Page elements
    PAGE_TITLE = (By.TAG_NAME, "h1")
    SIGNUP_FORM = (By.ID, "signupForm")
    
    def __init__(self, driver=None, browser='chrome', headless=False):
        """Initialize signup page"""
        super().__init__(driver, browser, headless)
        self.logger = logging.getLogger(__name__)
    
    def navigate_to_signup(self, url=None):
        """
        Navigate to signup page
        
        Args:
            url: Signup page URL (optional)
        """
        if not url:
            url = self.config.get('urls', {}).get('production', 'https://app.swiftassess.com/Signup')
        
        self.navigate_to(url)
        self.wait_for_page_load()
        self.logger.info("Navigated to signup page")
    
    def wait_for_page_load(self, timeout=10):
        """
        Wait for signup page to load
        
        Args:
            timeout: Wait timeout in seconds
        """
        try:
            # Wait for signup form to be visible
            self.wait.until(EC.visibility_of_element_located(self.SIGNUP_FORM))
            self.logger.info("Signup page loaded successfully")
        except TimeoutException:
            self.logger.error("Signup page failed to load within timeout")
            raise
    
    def get_page_title(self):
        """Get signup page title"""
        try:
            return self.get_text(self.PAGE_TITLE)
        except TimeoutException:
            return "Signup Page"
    
    def is_signup_form_visible(self):
        """Check if signup form is visible"""
        return self.is_element_visible(self.SIGNUP_FORM)
    
    def enter_first_name(self, first_name):
        """
        Enter first name
        
        Args:
            first_name: First name to enter
        """
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.logger.info(f"Entered first name: {first_name}")
    
    def enter_last_name(self, last_name):
        """
        Enter last name
        
        Args:
            last_name: Last name to enter
        """
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.logger.info(f"Entered last name: {last_name}")
    
    def enter_email(self, email):
        """
        Enter email address
        
        Args:
            email: Email address to enter
        """
        self.send_keys(self.EMAIL_INPUT, email)
        self.logger.info(f"Entered email: {email}")
    
    def enter_password(self, password):
        """
        Enter password
        
        Args:
            password: Password to enter
        """
        self.send_keys(self.PASSWORD_INPUT, password)
        self.logger.info("Entered password")
    
    def enter_confirm_password(self, confirm_password):
        """
        Enter confirm password
        
        Args:
            confirm_password: Confirm password to enter
        """
        self.send_keys(self.CONFIRM_PASSWORD_INPUT, confirm_password)
        self.logger.info("Entered confirm password")
    
    def check_terms_and_conditions(self):
        """Check terms and conditions checkbox"""
        if not self.is_checkbox_checked(self.TERMS_CHECKBOX):
            self.click_element(self.TERMS_CHECKBOX)
            self.logger.info("Checked terms and conditions")
    
    def check_privacy_policy(self):
        """Check privacy policy checkbox"""
        if not self.is_checkbox_checked(self.PRIVACY_CHECKBOX):
            self.click_element(self.PRIVACY_CHECKBOX)
            self.logger.info("Checked privacy policy")
    
    def is_checkbox_checked(self, locator):
        """
        Check if checkbox is checked
        
        Args:
            locator: Checkbox locator
            
        Returns:
            Boolean
        """
        try:
            element = self.find_element(locator)
            return element.is_selected()
        except (TimeoutException, NoSuchElementException):
            return False
    
    def click_signup_button(self):
        """Click signup button"""
        self.click_element(self.SIGNUP_BUTTON)
        self.logger.info("Clicked signup button")
    
    def fill_signup_form(self, user_data):
        """
        Fill complete signup form
        
        Args:
            user_data: Dictionary containing user data
        """
        self.logger.info("Filling signup form with user data")
        
        # Fill form fields
        if 'first_name' in user_data:
            self.enter_first_name(user_data['first_name'])
        
        if 'last_name' in user_data:
            self.enter_last_name(user_data['last_name'])
        
        if 'email' in user_data:
            self.enter_email(user_data['email'])
        
        if 'password' in user_data:
            self.enter_password(user_data['password'])
        
        if 'confirm_password' in user_data:
            self.enter_confirm_password(user_data['confirm_password'])
        
        # Check terms and privacy if required
        if user_data.get('accept_terms', True):
            self.check_terms_and_conditions()
        
        if user_data.get('accept_privacy', True):
            self.check_privacy_policy()
    
    def submit_signup_form(self, user_data):
        """
        Fill and submit signup form
        
        Args:
            user_data: Dictionary containing user data
            
        Returns:
            Boolean indicating success
        """
        try:
            self.fill_signup_form(user_data)
            self.click_signup_button()
            
            # Wait for response (success or error)
            time.sleep(2)
            
            # Check for success or error
            if self.is_signup_successful():
                self.logger.info("Signup successful")
                return True
            else:
                self.logger.warning("Signup failed - errors present")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during signup: {str(e)}")
            return False
    
    def is_signup_successful(self):
        """
        Check if signup was successful
        
        Returns:
            Boolean
        """
        try:
            # Check for success message
            if self.is_element_visible(self.SUCCESS_MESSAGE):
                return True
            
            # Check if we're redirected to a different page
            current_url = self.get_current_url()
            if 'signup' not in current_url.lower():
                return True
            
            # Check for absence of error messages
            return not self.has_validation_errors()
            
        except Exception:
            return False
    
    def has_validation_errors(self):
        """
        Check if there are validation errors
        
        Returns:
            Boolean
        """
        error_locators = [
            self.FIRST_NAME_ERROR,
            self.LAST_NAME_ERROR,
            self.EMAIL_ERROR,
            self.PASSWORD_ERROR,
            self.CONFIRM_PASSWORD_ERROR,
            self.TERMS_ERROR,
            self.GENERAL_ERROR
        ]
        
        for locator in error_locators:
            if self.is_element_visible(locator, timeout=2):
                return True
        
        return False
    
    def get_validation_errors(self):
        """
        Get all validation error messages
        
        Returns:
            List of error messages
        """
        errors = []
        error_locators = [
            (self.FIRST_NAME_ERROR, "First name error"),
            (self.LAST_NAME_ERROR, "Last name error"),
            (self.EMAIL_ERROR, "Email error"),
            (self.PASSWORD_ERROR, "Password error"),
            (self.CONFIRM_PASSWORD_ERROR, "Confirm password error"),
            (self.TERMS_ERROR, "Terms error"),
            (self.GENERAL_ERROR, "General error")
        ]
        
        for locator, error_type in error_locators:
            try:
                if self.is_element_visible(locator, timeout=1):
                    error_text = self.get_text(locator)
                    if error_text:
                        errors.append(f"{error_type}: {error_text}")
            except Exception:
                continue
        
        return errors
    
    def get_field_value(self, field_name):
        """
        Get value from form field
        
        Args:
            field_name: Name of the field
            
        Returns:
            Field value
        """
        field_locators = {
            'first_name': self.FIRST_NAME_INPUT,
            'last_name': self.LAST_NAME_INPUT,
            'email': self.EMAIL_INPUT,
            'password': self.PASSWORD_INPUT,
            'confirm_password': self.CONFIRM_PASSWORD_INPUT
        }
        
        if field_name in field_locators:
            try:
                return self.get_attribute(field_locators[field_name], 'value')
            except Exception:
                return ""
        else:
            raise ValueError(f"Unknown field name: {field_name}")
    
    def clear_form(self):
        """Clear all form fields"""
        fields = [
            self.FIRST_NAME_INPUT,
            self.LAST_NAME_INPUT,
            self.EMAIL_INPUT,
            self.PASSWORD_INPUT,
            self.CONFIRM_PASSWORD_INPUT
        ]
        
        for field in fields:
            try:
                element = self.find_element(field, timeout=2)
                element.clear()
            except Exception:
                continue
        
        # Uncheck checkboxes
        try:
            if self.is_checkbox_checked(self.TERMS_CHECKBOX):
                self.click_element(self.TERMS_CHECKBOX)
        except Exception:
            pass
        
        try:
            if self.is_checkbox_checked(self.PRIVACY_CHECKBOX):
                self.click_element(self.PRIVACY_CHECKBOX)
        except Exception:
            pass
        
        self.logger.info("Form cleared")
    
    def is_field_required(self, field_name):
        """
        Check if field is marked as required
        
        Args:
            field_name: Name of the field
            
        Returns:
            Boolean
        """
        field_locators = {
            'first_name': self.FIRST_NAME_INPUT,
            'last_name': self.LAST_NAME_INPUT,
            'email': self.EMAIL_INPUT,
            'password': self.PASSWORD_INPUT,
            'confirm_password': self.CONFIRM_PASSWORD_INPUT
        }
        
        if field_name in field_locators:
            try:
                element = self.find_element(field_locators[field_name])
                return element.get_attribute('required') is not None
            except Exception:
                return False
        else:
            raise ValueError(f"Unknown field name: {field_name}")
    
    def get_password_strength_indicator(self):
        """
        Get password strength indicator value
        
        Returns:
            Password strength level
        """
        try:
            strength_element = (By.CLASS_NAME, "password-strength")
            if self.is_element_visible(strength_element):
                return self.get_text(strength_element)
            return None
        except Exception:
            return None
    
    def wait_for_signup_completion(self, timeout=30):
        """
        Wait for signup process to complete
        
        Args:
            timeout: Wait timeout in seconds
            
        Returns:
            Boolean indicating success
        """
        try:
            # Wait for either success message or error
            WebDriverWait(self.driver, timeout).until(
                lambda driver: (
                    self.is_element_visible(self.SUCCESS_MESSAGE) or
                    self.has_validation_errors() or
                    'signup' not in self.get_current_url().lower()
                )
            )
            return self.is_signup_successful()
        except TimeoutException:
            self.logger.error("Signup completion timeout")
            return False
