"""
Pytest configuration and fixtures for SwiftAssess QA Automation
"""

import pytest


def pytest_addoption(parser):
    """Add custom command line options to pytest"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome, firefox, edge",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


@pytest.fixture(scope="session")
def browser(request):
    """Fixture to get browser from command line"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request):
    """Fixture to get headless mode from command line"""
    return request.config.getoption("--headless")

