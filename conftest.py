"""Root conftest.py — pytest auto-discovers this file. Fixtures and hooks
defined here are available to every test in the project."""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.config import Config


# ---------- Command-line options ----------
def pytest_addoption(parser):
    """Add custom CLI flags. Usage: pytest --browser=firefox --headless"""
    parser.addoption("--browser", action="store", default=Config.BROWSER,
                     help="Browser to run: chrome or firefox")
    parser.addoption("--headless", action="store_true",
                     help="Run browser in headless mode")


# ---------- Fixtures ----------
@pytest.fixture(scope="session")
def browser_name(request):
    """Session-scoped: resolved once per test run."""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request):
    return request.config.getoption("--headless") or Config.HEADLESS


@pytest.fixture
def driver(browser_name, headless):
    """Function-scoped: a fresh browser per test.
    Setup runs before the test; teardown runs after (yield splits them)."""
    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        drv = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        drv = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    drv.implicitly_wait(Config.IMPLICIT_WAIT)
    yield drv                       # ← test executes at this point
    drv.quit()                      # ← teardown, always runs


# ---------- Hook: screenshot on failure ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """After each test phase, if it failed, grab a screenshot and attach
    it to the HTML report. This is pytest's equivalent of a TestNG listener."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"screenshots/{item.name}.png"
            import os
            os.makedirs("screenshots", exist_ok=True)
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
