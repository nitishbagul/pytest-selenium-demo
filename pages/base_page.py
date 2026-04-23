"""BasePage: every Page Object inherits from this. Centralizes waits, clicks,
and text reads so individual pages stay small and consistent."""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config.config import Config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        """Wait until the element is present in the DOM, then return it."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """Wait until clickable, then click."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text

    def is_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
