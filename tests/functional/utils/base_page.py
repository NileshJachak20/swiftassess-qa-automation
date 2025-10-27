"""
Base Page Object Model class for SwiftAssess testing
"""

import yaml
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os
from datetime import datetime


class BasePage:
    """Base page class that all page objects inherit from"""

    def __init__(self, driver=None, browser="chrome", headless=False):
        """
        Initialize the base page

        Args:
            driver: WebDriver instance
            browser: Browser type (chrome, firefox, edge)
            headless: Run browser in headless mode
        """
        self.driver = driver or self._setup_driver(browser, headless)
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(self.driver)
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from YAML file"""
        try:
            with open("config/config.yaml", "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            self.logger.warning("Config file not found, using default values")
            return {}

    def _setup_driver(self, browser="chrome", headless=False):
        """
        Set up WebDriver instance

        Args:
            browser: Browser type
            headless: Run in headless mode

        Returns:
            WebDriver instance
        """
        if browser.lower() == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")

            # Add common options
            for option in (
                self.config.get("browsers", {}).get("chrome", {}).get("options", [])
            ):
                options.add_argument(option)

            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        elif browser.lower() == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")

            for option in (
                self.config.get("browsers", {}).get("firefox", {}).get("options", [])
            ):
                options.add_argument(option)

            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)

        elif browser.lower() == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless")

            for option in (
                self.config.get("browsers", {}).get("edge", {}).get("options", [])
            ):
                options.add_argument(option)

            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser}")

        # Set window size
        window_size = (
            self.config.get("browsers", {})
            .get(browser, {})
            .get("window_size", [1920, 1080])
        )
        driver.set_window_size(window_size[0], window_size[1])

        return driver

    def find_element(self, locator, timeout=10):
        """
        Find element with explicit wait

        Args:
            locator: Tuple of (By, value)
            timeout: Wait timeout in seconds

        Returns:
            WebElement
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise

    def find_elements(self, locator, timeout=10):
        """
        Find multiple elements with explicit wait

        Args:
            locator: Tuple of (By, value)
            timeout: Wait timeout in seconds

        Returns:
            List of WebElements
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            self.logger.error(f"Elements not found: {locator}")
            return []

    def click_element(self, locator, timeout=10):
        """
        Click element with retry mechanism

        Args:
            locator: Tuple of (By, value)
            timeout: Wait timeout in seconds
        """
        max_attempts = self.config.get("retry", {}).get("max_attempts", 3)

        for attempt in range(max_attempts):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                self.logger.info(f"Successfully clicked element: {locator}")
                return
            except (
                ElementClickInterceptedException,
                StaleElementReferenceException,
            ) as e:
                if attempt == max_attempts - 1:
                    self.logger.error(
                        f"Failed to click element after {max_attempts} attempts: {locator}"
                    )
                    raise
                time.sleep(1)

    def send_keys(self, locator, text, timeout=10, clear_first=True):
        """
        Send keys to element

        Args:
            locator: Tuple of (By, value)
            text: Text to send
            timeout: Wait timeout in seconds
            clear_first: Clear field before sending keys
        """
        element = self.find_element(locator, timeout)

        if clear_first:
            element.clear()

        element.send_keys(text)
        self.logger.info(f"Sent keys to element: {locator}")

    def get_text(self, locator, timeout=10):
        """
        Get text from element

        Args:
            locator: Tuple of (By, value)
            timeout: Wait timeout in seconds

        Returns:
            Element text
        """
        element = self.find_element(locator, timeout)
        return element.text

    def get_attribute(self, locator, attribute, timeout=10):
        """
        Get attribute value from element

        Args:
            locator: Tuple of (By, value)
            attribute: Attribute name
            timeout: Wait timeout in seconds

        Returns:
            Attribute value
        """
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)

    def is_element_present(self, locator, timeout=10):
        """
        Check if element is present

        Args:
            locator: Tuple of (By, value)
            timeout: Wait timeout in seconds

        Returns:
            Boolean
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator, timeout=10):
        """
        Check if element is visible

        Args:
            locator: Tuple of (By, value)
            timeout: Wait timeout in seconds

        Returns:
            Boolean
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_to_disappear(self, locator, timeout=10):
        """
        Wait for element to disappear

        Args:
            locator: Tuple of (By, value)
            timeout: Wait timeout in seconds
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.warning(
                f"Element did not disappear within {timeout} seconds: {locator}"
            )

    def select_dropdown_option(self, locator, option_text, timeout=10):
        """
        Select option from dropdown

        Args:
            locator: Tuple of (By, value)
            option_text: Option text to select
            timeout: Wait timeout in seconds
        """
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(option_text)
        self.logger.info(f"Selected option '{option_text}' from dropdown: {locator}")

    def scroll_to_element(self, locator, timeout=10):
        """
        Scroll to element

        Args:
            locator: Tuple of (By, value)
            timeout: Wait timeout in seconds
        """
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Small delay for scroll animation

    def hover_element(self, locator, timeout=10):
        """
        Hover over element

        Args:
            locator: Tuple of (By, value)
            timeout: Wait timeout in seconds
        """
        element = self.find_element(locator, timeout)
        self.actions.move_to_element(element).perform()
        self.logger.info(f"Hovered over element: {locator}")

    def take_screenshot(self, filename=None):
        """
        Take screenshot

        Args:
            filename: Screenshot filename

        Returns:
            Screenshot path
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_dir = self.config.get("screenshots", {}).get(
            "directory", "screenshots"
        )
        os.makedirs(screenshot_dir, exist_ok=True)

        screenshot_path = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(screenshot_path)
        self.logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def get_page_title(self):
        """Get page title"""
        return self.driver.title

    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url

    def navigate_to(self, url):
        """
        Navigate to URL

        Args:
            url: URL to navigate to
        """
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")

    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.logger.info("Page refreshed")

    def go_back(self):
        """Go back to previous page"""
        self.driver.back()
        self.logger.info("Navigated back")

    def go_forward(self):
        """Go forward to next page"""
        self.driver.forward()
        self.logger.info("Navigated forward")

    def close_browser(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")

    def switch_to_window(self, window_index=0):
        """
        Switch to window by index

        Args:
            window_index: Window index (0-based)
        """
        windows = self.driver.window_handles
        if window_index < len(windows):
            self.driver.switch_to.window(windows[window_index])
            self.logger.info(f"Switched to window {window_index}")

    def close_window(self):
        """Close current window"""
        self.driver.close()
        self.logger.info("Window closed")

    def execute_javascript(self, script, *args):
        """
        Execute JavaScript

        Args:
            script: JavaScript code
            *args: Arguments to pass to script

        Returns:
            Script result
        """
        return self.driver.execute_script(script, *args)
