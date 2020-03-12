from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.utils.test_logger import TestLog
from .locators import ui_definitions
from .base_page import BasePage
from src.elements.classic_elements.input_element import InputElement
from src.elements.element import Element

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

    def get_item(self, item_name: str) -> WebElement:
        locator = (By.XPATH, "//a[text() = '{}']".format(item_name))
        item = Element(self.driver, locator)
        return item.find(25)

    def goto(self, item_name):
        item = self.get_item(item_name)
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
    def header(self):
        return Element(self.driver, ui_definitions.get("demos_page/introduction"))

    @property
    def sidebar(self):
        return SideMenu(self.driver, ui_definitions.get("common_locators/sidebar_locator"))
