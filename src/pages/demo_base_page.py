from selenium.webdriver.common.by import By
from src.utils.test_logger import TestLog
from .locators import ui_definitions
from .base_page import BasePage
from ..elements.page_elements import Element, InputElement


log = TestLog()


class SideMenu(Element):

    def __init__(self, driver, locator):
        super().__init__(driver, locator)
        log.debug("Created SideMenu class instance")

    @property
    def items(self):
        dct = {}
        li = self.find_elements(ui_definitions.get("common_locators/side_menu_item_locator"))
        for item in li:
            key = item.text
            dct[key] = item

        return dct

    def get_item(self, item_name: str) -> Element:
        locator = (By.XPATH, "//a[text() = '{}']".format(item_name))
        item = Element(self.driver, locator)
        return item.find(15)

    def goto(self, item_name):
        item = self.items[item_name]
        if item.is_displayed and item.is_enabled:
            item.click()

    @property
    def search_box(self):
        return InputElement(self.driver, ui_definitions.get("common_locators/search"))

    def search(self, text):
        self.search_box.value = text


class DemoBasePage(BasePage):
    # constructor
    def __init__(self, drv):
        super().__init__(drv)
        log.debug("Created DemoBasePage class instance")

    @property
    def page_header(self):
        return Element(self.driver, ui_definitions.get("demos_page/introduction"))

    @property
    def sidebar(self):
        return SideMenu(self.driver, ui_definitions.get("common_locators/sidebar_locator"))
