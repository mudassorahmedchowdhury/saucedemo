from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_add_to_cart_and_checkout(driver, config):
    login = LoginPage(driver, base_url=config["base_url"], timeout=config["timeout"])
    login.open()
    login.login("standard_user", "secret_sauce")
    products = ProductsPage(driver, timeout=config["timeout"])
    assert products.is_loaded()
    products.add_to_cart_by_name("Sauce Labs Backpack")
    products.add_to_cart_by_name("Sauce Labs Bike Light")
    products.open_cart()
    cart = CartPage(driver, timeout=config["timeout"])
    names = cart.get_cart_items_names()
    assert "Sauce Labs Backpack" in names and "Sauce Labs Bike Light" in names
    cart.checkout()
    checkout = CheckoutPage(driver, timeout=config["timeout"])
    checkout.fill_information("Test", "User", "12345")
    checkout.continue_to_overview()
    checkout.finish()
    success = checkout.get_success_message()
    assert "Thank you for your order!" in success
    driver.get(config["base_url"] + "cart.html")
    products_count = products.cart_badge_count()
    assert products_count == 0