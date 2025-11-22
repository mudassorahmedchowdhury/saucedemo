from selenium.webdriver.common.by import By


class CartLocators:
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")