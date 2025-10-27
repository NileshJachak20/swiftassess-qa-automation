"""
Functional test cases for SwiftAssess signup page
"""

import pytest
import logging
import time
from tests.functional.pages.signup_page import SignupPage
from tests.functional.utils.test_helpers import (
    TestDataGenerator,
    ScreenshotManager,
    RetryMechanism,
    TestReportGenerator,
)


class TestSignupFunctional:
    """Functional test cases for signup page"""

    @pytest.fixture(autouse=True)
    def setup(self, request):
        """Setup for each test"""
        self.logger = logging.getLogger(__name__)
        self.data_generator = TestDataGenerator()
        self.screenshot_manager = ScreenshotManager()
        self.retry_mechanism = RetryMechanism()
        self.report_generator = TestReportGenerator()

        # Get browser from pytest parameter
        browser = getattr(request.config.option, "browser", "chrome")
        headless = getattr(request.config.option, "headless", False)

        # Initialize signup page
        self.signup_page = SignupPage(browser=browser, headless=headless)

        # Navigate to signup page
        self.signup_page.navigate_to_signup()

        yield

        # Cleanup
        if hasattr(self, "signup_page"):
            self.signup_page.close_browser()

    @pytest.mark.smoke
    @pytest.mark.functional
    def test_valid_signup(self):
        """Test valid signup with all required fields"""
        test_name = "test_valid_signup"
        start_time = time.time()

        try:
            # Generate valid user data
            user_data = self.data_generator.generate_valid_user_data()
            user_data["confirm_password"] = user_data["password"]

            # Fill and submit signup form
            success = self.signup_page.submit_signup_form(user_data)

            # Wait for signup completion
            success = self.signup_page.wait_for_signup_completion()

            # Verify success
            assert success, "Signup should be successful with valid data"

            # Check for success indicators
            assert (
                self.signup_page.is_signup_successful()
            ), "Signup should show success indicators"

            self.logger.info("Valid signup test passed")

        except Exception as e:
            # Capture screenshot on failure
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Valid signup test failed: {e}")
            raise

        finally:
            duration = time.time() - start_time
            self.logger.info(f"Test duration: {duration:.2f} seconds")

    @pytest.mark.functional
    def test_empty_first_name_validation(self):
        """Test validation for empty first name"""
        test_name = "test_empty_first_name_validation"

        try:
            # Generate user data with empty first name
            user_data = self.data_generator.generate_invalid_user_data(
                "empty_first_name"
            )

            # Fill form and submit
            self.signup_page.fill_signup_form(user_data)
            self.signup_page.click_signup_button()

            # Check for validation error
            assert (
                self.signup_page.has_validation_errors()
            ), "Should show validation errors for empty first name"

            errors = self.signup_page.get_validation_errors()
            assert any(
                "first name" in error.lower() for error in errors
            ), "Should show first name error"

            self.logger.info("Empty first name validation test passed")

        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Empty first name validation test failed: {e}")
            raise

    @pytest.mark.functional
    def test_empty_last_name_validation(self):
        """Test validation for empty last name"""
        test_name = "test_empty_last_name_validation"

        try:
            # Generate user data with empty last name
            user_data = self.data_generator.generate_invalid_user_data(
                "empty_last_name"
            )

            # Fill form and submit
            self.signup_page.fill_signup_form(user_data)
            self.signup_page.click_signup_button()

            # Check for validation error
            assert (
                self.signup_page.has_validation_errors()
            ), "Should show validation errors for empty last name"

            errors = self.signup_page.get_validation_errors()
            assert any(
                "last name" in error.lower() for error in errors
            ), "Should show last name error"

            self.logger.info("Empty last name validation test passed")

        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Empty last name validation test failed: {e}")
            raise

    @pytest.mark.functional
    def test_invalid_email_validation(self):
        """Test validation for invalid email format"""
        test_name = "test_invalid_email_validation"

        try:
            # Generate user data with invalid email
            user_data = self.data_generator.generate_invalid_user_data("invalid_email")

            # Fill form and submit
            self.signup_page.fill_signup_form(user_data)
            self.signup_page.click_signup_button()

            # Check for validation error
            assert (
                self.signup_page.has_validation_errors()
            ), "Should show validation errors for invalid email"

            errors = self.signup_page.get_validation_errors()
            assert any(
                "email" in error.lower() for error in errors
            ), "Should show email error"

            self.logger.info("Invalid email validation test passed")

        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Invalid email validation test failed: {e}")
            raise

    @pytest.mark.functional
    def test_weak_password_validation(self):
        """Test validation for weak password"""
        test_name = "test_weak_password_validation"

        try:
            # Generate user data with weak password
            user_data = self.data_generator.generate_invalid_user_data("weak_password")

            # Fill form and submit
            self.signup_page.fill_signup_form(user_data)
            self.signup_page.click_signup_button()

            # Check for validation error
            assert (
                self.signup_page.has_validation_errors()
            ), "Should show validation errors for weak password"

            errors = self.signup_page.get_validation_errors()
            assert any(
                "password" in error.lower() for error in errors
            ), "Should show password error"

            self.logger.info("Weak password validation test passed")

        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Weak password validation test failed: {e}")
            raise

    @pytest.mark.functional
    def test_mismatched_passwords_validation(self):
        """Test validation for mismatched passwords"""
        test_name = "test_mismatched_passwords_validation"

        try:
            # Generate user data with mismatched passwords
            user_data = self.data_generator.generate_invalid_user_data(
                "mismatched_passwords"
            )

            # Fill form and submit
            self.signup_page.fill_signup_form(user_data)
            self.signup_page.click_signup_button()

            # Check for validation error
            assert (
                self.signup_page.has_validation_errors()
            ), "Should show validation errors for mismatched passwords"

            errors = self.signup_page.get_validation_errors()
            assert any(
                "password" in error.lower() or "match" in error.lower()
                for error in errors
            ), "Should show password mismatch error"

            self.logger.info("Mismatched passwords validation test passed")

        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Mismatched passwords validation test failed: {e}")
            raise

    @pytest.mark.functional
    def test_terms_and_conditions_required(self):
        """Test that terms and conditions acceptance is required"""
        test_name = "test_terms_and_conditions_required"

        try:
            # Generate user data without accepting terms
            user_data = self.data_generator.generate_invalid_user_data("no_terms")

            # Fill form and submit
            self.signup_page.fill_signup_form(user_data)
            self.signup_page.click_signup_button()

            # Check for validation error
            assert (
                self.signup_page.has_validation_errors()
            ), "Should show validation errors for not accepting terms"

            errors = self.signup_page.get_validation_errors()
            assert any(
                "terms" in error.lower() for error in errors
            ), "Should show terms error"

            self.logger.info("Terms and conditions required test passed")

        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Terms and conditions required test failed: {e}")
            raise

    @pytest.mark.functional
    def test_privacy_policy_required(self):
        """Test that privacy policy acceptance is required"""
        test_name = "test_privacy_policy_required"

        try:
            # Generate user data without accepting privacy policy
            user_data = self.data_generator.generate_invalid_user_data("no_privacy")

            # Fill form and submit
            self.signup_page.fill_signup_form(user_data)
            self.signup_page.click_signup_button()

            # Check for validation error
            assert (
                self.signup_page.has_validation_errors()
            ), "Should show validation errors for not accepting privacy policy"

            errors = self.signup_page.get_validation_errors()
            assert any(
                "privacy" in error.lower() for error in errors
            ), "Should show privacy error"

            self.logger.info("Privacy policy required test passed")

        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Privacy policy required test failed: {e}")
            raise

    @pytest.mark.functional
    def test_duplicate_email_handling(self):
        """Test handling of duplicate email addresses"""
        test_name = "test_duplicate_email_handling"

        try:
            # Use a fixed email that might already exist
            user_data = self.data_generator.generate_valid_user_data()
            user_data["email"] = "test@example.com"
            user_data["confirm_password"] = user_data["password"]

            # Fill form and submit
            self.signup_page.fill_signup_form(user_data)
            self.signup_page.click_signup_button()

            # Wait for response
            time.sleep(2)

            # Check if duplicate email is handled (either success or specific error)
            if not self.signup_page.is_signup_successful():
                errors = self.signup_page.get_validation_errors()
                # Should show some error for duplicate email
                assert len(errors) > 0, "Should show error for duplicate email"

            self.logger.info("Duplicate email handling test passed")

        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Duplicate email handling test failed: {e}")
            raise

    @pytest.mark.functional
    def test_form_field_requirements(self):
        """Test that all required fields are marked as required"""
        test_name = "test_form_field_requirements"

        try:
            # Check if fields are marked as required
            required_fields = [
                "first_name",
                "last_name",
                "email",
                "password",
                "confirm_password",
            ]

            for field in required_fields:
                is_required = self.signup_page.is_field_required(field)
                assert is_required, f"Field {field} should be marked as required"

            self.logger.info("Form field requirements test passed")

        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Form field requirements test failed: {e}")
            raise

    @pytest.mark.functional
    def test_password_strength_indicator(self):
        """Test password strength indicator functionality"""
        test_name = "test_password_strength_indicator"

        try:
            # Test with weak password
            self.signup_page.enter_password("123")
            weak_strength = self.signup_page.get_password_strength_indicator()

            # Test with strong password
            self.signup_page.enter_password("StrongPass123!")
            strong_strength = self.signup_page.get_password_strength_indicator()

            # If strength indicator exists, it should show different values
            if weak_strength and strong_strength:
                assert (
                    weak_strength != strong_strength
                ), "Password strength should change with different passwords"

            self.logger.info("Password strength indicator test passed")

        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Password strength indicator test failed: {e}")
            raise

    @pytest.mark.functional
    def test_form_clear_functionality(self):
        """Test form clear functionality"""
        test_name = "test_form_clear_functionality"

        try:
            # Fill form with data
            user_data = self.data_generator.generate_valid_user_data()
            self.signup_page.fill_signup_form(user_data)

            # Clear form
            self.signup_page.clear_form()

            # Verify all fields are empty
            assert (
                self.signup_page.get_field_value("first_name") == ""
            ), "First name should be empty"
            assert (
                self.signup_page.get_field_value("last_name") == ""
            ), "Last name should be empty"
            assert (
                self.signup_page.get_field_value("email") == ""
            ), "Email should be empty"
            assert (
                self.signup_page.get_field_value("password") == ""
            ), "Password should be empty"
            assert (
                self.signup_page.get_field_value("confirm_password") == ""
            ), "Confirm password should be empty"

            # Verify checkboxes are unchecked
            assert not self.signup_page.is_checkbox_checked(
                self.signup_page.TERMS_CHECKBOX
            ), "Terms checkbox should be unchecked"
            assert not self.signup_page.is_checkbox_checked(
                self.signup_page.PRIVACY_CHECKBOX
            ), "Privacy checkbox should be unchecked"

            self.logger.info("Form clear functionality test passed")

        except Exception as e:
            self.screenshot_manager.capture_screenshot(
                self.signup_page.driver, test_name, "failed"
            )
            self.logger.error(f"Form clear functionality test failed: {e}")
            raise
