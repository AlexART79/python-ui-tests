from .locators import ui_definitions #CheckboxPageLocators,
from ..Elements.react_components import ReactCheckbox
from .demo_base_page import DemoBasePage


class CheckboxPage(DemoBasePage):
    def __init__(self, drv):
        DemoBasePage.__init__(self, drv)

        self.key = "checkbox_page_locators"
        self.ui_defs = next((x for x in ui_definitions if x.key == self.key), None)

        if self.ui_defs is None:
            raise Exception("UI definition not found: {}".format(self.key))

        pass

    @property
    def first_checkbox(self):
        loc = next((x.value for x in self.ui_defs.locators if x.name == "first_checkbox_locator"), None)
        return ReactCheckbox(self.driver, loc)

    @property
    def second_checkbox(self):
        loc = next((x.value for x in self.ui_defs.locators if x.name == "second_checkbox_locator"), None)
        return ReactCheckbox(self.driver, loc)
