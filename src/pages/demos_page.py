from src.Elements.page_elements import Element
from src.pages.locators import ui_definitions
from .demo_base_page import DemoBasePage


class DemosPage(DemoBasePage):
    def __init__(self, drv):
        DemoBasePage.__init__(self, drv)
