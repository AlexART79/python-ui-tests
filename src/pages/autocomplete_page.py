from .locators import AutoCompletePageLocators
from ..Elements.react_components import ReactAutoComplete
from .demo_base_page import DemoBasePage


class AutoCompletePage(DemoBasePage):
    def __init__(self, drv):
        DemoBasePage.__init__(self, drv)

    @property
    def basic_autocomplete(self):
        return ReactAutoComplete(self.driver, AutoCompletePageLocators.basic_autocomplete)

    @property
    def advanced_autocomplete(self):
        return ReactAutoComplete(self.driver, AutoCompletePageLocators.advanced_autocomplete)
