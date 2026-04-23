"""Inventory and cart tests."""
import pytest

from config.config import Config
from pages.cart_page import CartPage
from pages.login_page import LoginPage


@pytest.fixture
def logged_in_inventory(driver):
    """Composed fixture: logs in and hands back the inventory page.
    Any test that takes `logged_in_inventory` starts already logged in."""
    return LoginPage(driver).load().login(Config.STANDARD_USER, Config.PASSWORD)


@pytest.mark.smoke
def test_inventory_shows_six_items(logged_in_inventory):
    assert logged_in_inventory.item_count() == 6


@pytest.mark.regression
def test_add_single_item_to_cart(logged_in_inventory):
    logged_in_inventory.add_item_to_cart("sauce-labs-backpack")
    assert logged_in_inventory.cart_count() == 1


@pytest.mark.regression
@pytest.mark.parametrize("items_to_add", [
    ["sauce-labs-backpack"],
    ["sauce-labs-backpack", "sauce-labs-bike-light"],
    ["sauce-labs-backpack", "sauce-labs-bike-light", "sauce-labs-bolt-t-shirt"],
], ids=["one-item", "two-items", "three-items"])
def test_cart_count_matches_items_added(logged_in_inventory, driver, items_to_add):
    for item in items_to_add:
        logged_in_inventory.add_item_to_cart(item)

    assert logged_in_inventory.cart_count() == len(items_to_add)

    logged_in_inventory.click(logged_in_inventory.CART_LINK)
    cart = CartPage(driver)
    assert cart.item_count() == len(items_to_add)
