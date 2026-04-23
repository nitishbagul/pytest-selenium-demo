"""CartPage: the shopping cart view."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def item_names(self):
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))
