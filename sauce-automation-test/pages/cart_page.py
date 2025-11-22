from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.locators.cart_locators import CartLocators


class CartPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def get_cart_items_names(self):
        WebDriverWait(self.driver, self.timeout).until(EC.presence_of_all_elements_located(CartLocators.CART_ITEM))
        return [el.find_element(By.CLASS_NAME, "inventory_item_name").text for el in self.driver.find_elements(*CartLocators.CART_ITEM)]

    def checkout(self):
        btn = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(CartLocators.CHECKOUT_BUTTON))
        btn.click()
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.url_contains("checkout-step-one.html"))
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)
            WebDriverWait(self.driver, self.timeout).until(EC.url_contains("checkout-step-one.html"))