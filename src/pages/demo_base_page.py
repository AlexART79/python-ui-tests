from selenium.webdriver.common.by import By

from .locators import CommonLocators, get_def
from .base_page import BasePage
from ..Elements.page_elements import Element


class SideMenu(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @property
    def items(self):
        dct = {}
        li = self.find_elements(get_def("common_locators/side_menu_item_locator"))
        for item in li:
            key = item.text
            dct[key] = item

        return dct

    def get_item(self, item_name):
        locator = (By.XPATH, "//a[text() = '{}']".format(item_name))
        item = Element(self.driver, locator)
        return item.find(15)

    def goto(self, item_name):
        self.get_item(item_name).click()


class DemoBasePage(BasePage):
    # constructor
    def __init__(self, drv):
        super().__init__(drv)

    def goto(self, url):
        self.go_to(url)

    @property
    def sidebar(self):
        return SideMenu(self.driver, get_def("common_locators/sidebar_locator"))
