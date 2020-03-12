from .locators import ui_definitions
from src.elements.prime_react.react_autocomplete import ReactAutoComplete
from .demo_base_page import DemoBasePage


class AutoCompletePage(DemoBasePage):
    def __init__(self, drv):
        DemoBasePage.__init__(self, drv)

    @property
    def basic_autocomplete(self):
        return ReactAutoComplete(self.driver, ui_definitions.get("autocomplete_page_locators/basic_autocomplete"))

    @property
    def advanced_autocomplete(self):
        return ReactAutoComplete(self.driver, ui_definitions.get("autocomplete_page_locators/advanced_autocomplete"))
