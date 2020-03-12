from src.elements.element import Element


class Checkbox(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @property
    def is_checked(self) -> bool:
        checked = self.find().is_selected()
        return checked

    @is_checked.setter
    def is_checked(self, value: bool):
        if (value and not self.is_checked) or (self.is_checked and not value):
            self.click()
