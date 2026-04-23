"""Login tests — demonstrates basic pytest, parametrize, and markers."""
import pytest

from config.config import Config
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.login
def test_valid_user_can_login(driver):
    """Happy path: standard user logs in and lands on the inventory page."""
    inventory = LoginPage(driver).load().login(Config.STANDARD_USER, Config.PASSWORD)
    assert inventory.title() == "Products"


@pytest.mark.login
@pytest.mark.parametrize("username,password,expected_error", [
    ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
    ("standard_user",   "wrong_pass",    "Username and password do not match"),
    ("",                "secret_sauce",  "Username is required"),
    ("standard_user",   "",              "Password is required"),
], ids=["locked-user", "bad-password", "empty-username", "empty-password"])
def test_invalid_login_shows_error(driver, username, password, expected_error):
    """Data-driven negative tests. Each row becomes its own test case,
    each identified by the `ids` label in the report."""
    login_page = LoginPage(driver).load().login_expecting_failure(username, password)
    assert expected_error in login_page.error_message()
