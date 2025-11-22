import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


@pytest.mark.parametrize("username,password", [("standard_user", "secret_sauce")])
def test_successful_login(driver, config, username, password):
    login = LoginPage(driver, base_url=config["base_url"], timeout=config["timeout"])
    login.open()
    login.login(username, password)
    products = ProductsPage(driver, timeout=config["timeout"])
    assert products.is_loaded()


def test_unsuccessful_login_invalid_password(driver, config):
    login = LoginPage(driver, base_url=config["base_url"], timeout=config["timeout"])
    login.open()
    login.login("standard_user", "wrong_sauce")
    msg = login.get_error_message()
    assert "Username and password do not match" in msg


def test_access_inventory_without_login_redirects_to_login(driver, config):
    driver.get(config["base_url"] + "inventory.html")
    login = LoginPage(driver, base_url=config["base_url"], timeout=config["timeout"])
    assert login.is_at_login_page()