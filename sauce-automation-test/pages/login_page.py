from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.locators.login_locators import LoginLocators


class LoginPage:
    def __init__(self, driver, base_url, timeout=10):
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout

    def open(self):
        self.driver.get(self.base_url)

    def login(self, username, password):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(LoginLocators.USERNAME)).send_keys(username)
        self.driver.find_element(*LoginLocators.PASSWORD).send_keys(password)
        self.driver.find_element(*LoginLocators.LOGIN_BUTTON).click()
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.url_contains("inventory.html"))
        except Exception:
            pass

    def get_error_message(self):
        el = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(LoginLocators.ERROR))
        return el.text

    def is_at_login_page(self):
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(LoginLocators.LOGIN_BUTTON))
            return True
        except Exception:
            return False