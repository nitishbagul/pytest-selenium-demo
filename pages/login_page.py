"""LoginPage: exposes business actions for the login screen.
Tests call login(user, pass) — they don't know or care what the selectors are."""
from selenium.webdriver.common.by import By

from config.config import Config
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    # Locators live at the top, as tuples: (strategy, value)
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def load(self):
        self.open(Config.BASE_URL)
        return self

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        return InventoryPage(self.driver)  # returns the next page, fluent-style

    def login_expecting_failure(self, username, password):
        """Use when you EXPECT login to fail — stays on the login page."""
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def error_message(self):
        return self.text_of(self.ERROR_MESSAGE)
