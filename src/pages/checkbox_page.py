from .locators import ui_definitions
from ..Elements.react_components import ReactCheckbox
from .demo_base_page import DemoBasePage


class CheckboxPage(DemoBasePage):
    def __init__(self, drv):
        DemoBasePage.__init__(self, drv)

    @property
    def first_checkbox(self):
        return ReactCheckbox(self.driver, ui_definitions.get("checkbox_page_locators/first_checkbox_locator"))

    @property
    def second_checkbox(self):
        return ReactCheckbox(self.driver, ui_definitions.get("checkbox_page_locators/second_checkbox_locator"))
