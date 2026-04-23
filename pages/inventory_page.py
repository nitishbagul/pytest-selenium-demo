"""InventoryPage: the product listing shown after successful login."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class InventoryPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def title(self):
        return self.text_of(self.PAGE_TITLE)

    def item_count(self):
        return len(self.driver.find_elements(*self.INVENTORY_ITEMS))

    def add_item_to_cart(self, item_name):
        # Dynamic locator — built at runtime from the item name
        locator = (By.ID, f"add-to-cart-{item_name.lower().replace(' ', '-')}")
        self.click(locator)
        return self

    def cart_count(self):
        if not self.is_visible(self.CART_BADGE):
            return 0
        return int(self.text_of(self.CART_BADGE))
