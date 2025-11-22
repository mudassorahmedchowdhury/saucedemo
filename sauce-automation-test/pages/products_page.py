from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pages.locators.products_locators import ProductsLocators


class ProductsPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def is_loaded(self):
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(ProductsLocators.TITLE))
            return "Products" in self.driver.find_element(*ProductsLocators.TITLE).text
        except Exception:
            return False

    def add_to_cart_by_name(self, product_name):
        self.driver.execute_script("window.scrollTo(0,0)")
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(ProductsLocators.INVENTORY_CONTAINER)
        )
        names = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_all_elements_located(ProductsLocators.ITEM_NAME)
        )
        for name_el in names:
            if name_el.text.strip() == product_name:
                container = name_el.find_element(By.XPATH, "./ancestor::div[@class='inventory_item']")
                add_btn = WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable(container.find_element(By.XPATH, ".//button[contains(@id,'add-to-cart')]")
                ))
                add_btn.click()
                WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((By.XPATH, ".//button[starts-with(@id,'remove-')]"))
                )
                return
        raise AssertionError(f"Product not found: {product_name}")

    def open_cart(self):
        link = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(ProductsLocators.CART_LINK)
        )
        link.click()
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.url_contains("cart.html"))
        except Exception:
            WebDriverWait(self.driver, self.timeout).until(
                EC.text_to_be_present_in_element(ProductsLocators.TITLE, "Your Cart")
            )

    def sort_low_to_high(self):
        select_el = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(ProductsLocators.SORT_SELECT))
        Select(select_el).select_by_value("lohi")

    def get_product_prices(self):
        WebDriverWait(self.driver, self.timeout).until(EC.presence_of_all_elements_located(ProductsLocators.PRICE))
        prices = [el.text.replace("$", "") for el in self.driver.find_elements(*ProductsLocators.PRICE)]
        return [float(p) for p in prices]

    def cart_badge_count(self):
        try:
            badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            return int(badge.text)
        except Exception:
            return 0