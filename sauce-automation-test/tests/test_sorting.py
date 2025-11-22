import os
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def test_sort_products_low_to_high_and_screenshot(driver, config):
    login = LoginPage(driver, base_url=config["base_url"], timeout=config["timeout"])
    login.open()
    login.login("standard_user", "secret_sauce")
    products = ProductsPage(driver, timeout=config["timeout"])
    assert products.is_loaded()
    products.sort_low_to_high()
    prices = products.get_product_prices()
    assert prices == sorted(prices)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    screenshots_dir = os.path.join(base_dir, "reports", "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    driver.save_screenshot(os.path.join(screenshots_dir, "sorted_products.png"))