from src.elements.element import Element


class Radio(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @property
    def is_selected(self) -> bool:
        checked = self.find().is_selected()
        return checked

    def select(self):
        self.click()
