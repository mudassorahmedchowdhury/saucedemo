from selenium.webdriver.common.by import By


class ProductsLocators:
    TITLE = (By.CLASS_NAME, "title")
    CART_LINK = (By.CSS_SELECTOR, "#shopping_cart_container a")
    SORT_SELECT = (By.CSS_SELECTOR, "select.product_sort_container")
    PRICE = (By.CLASS_NAME, "inventory_item_price")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item .inventory_item_name")
    CART_CONTENTS = (By.ID, "cart_contents_container")