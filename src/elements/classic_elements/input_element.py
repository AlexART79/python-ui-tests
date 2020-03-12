from src.elements.element import Element


class InputElement(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @property
    def value(self):
        return self.find().get_attribute("value")

    @value.setter
    def value(self, val):
        self.clear()
        self.send_keys(val)
