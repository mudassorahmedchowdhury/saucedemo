from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.locators.checkout_locators import CheckoutLocators


class CheckoutPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def fill_information(self, first_name, last_name, postal_code):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(CheckoutLocators.FIRST_NAME)).send_keys(first_name)
        self.driver.find_element(*CheckoutLocators.LAST_NAME).send_keys(last_name)
        self.driver.find_element(*CheckoutLocators.POSTAL_CODE).send_keys(postal_code)

    def continue_to_overview(self):
        btn = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(CheckoutLocators.CONTINUE_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        btn.click()
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.staleness_of(btn))
        except Exception:
            pass
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.url_contains("checkout-step-two.html"))
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)
            WebDriverWait(self.driver, self.timeout).until(EC.staleness_of(btn))
        # Robust wait for overview page ready
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.text_to_be_present_in_element(CheckoutLocators.TITLE, "Checkout: Overview"))
        except Exception:
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(CheckoutLocators.FINISH_BUTTON))

    def finish(self):
        btn = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(CheckoutLocators.FINISH_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        btn.click()
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.url_contains("checkout-complete.html"))
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(CheckoutLocators.COMPLETE_HEADER))
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(CheckoutLocators.COMPLETE_HEADER))

    def get_success_message(self):
        el = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(CheckoutLocators.COMPLETE_HEADER))
        return el.text