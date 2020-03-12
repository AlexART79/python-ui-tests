from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from src.elements.classic_elements.input_element import InputElement
from src.elements.element import Element

#
# Advanced
#

class AngularCheckbox(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @property
    def is_checked(self):
        cb = self.find_element((By.TAG_NAME, "input"))
        checked = cb.get_attribute("checked")
        return checked is not None


class TinyMceEditor(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @property
    def value(self):
        self.driver.switch_to.frame(self.find())
        content = Element(self.driver, (By.ID, "tinymce"))

        self.driver.switch_to.default_content()

        return content.text

    @value.setter
    def value(self, value):
        self.driver.switch_to.frame(self.find())
        content = Element(self.driver, (By.ID, "tinymce"))

        content.send_keys(value)

        self.driver.switch_to.default_content()


class SingleSelectElement(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

        by, loc_str = locator
        input_locator = (by, loc_str+"/input")
        self.input_element = InputElement(self.driver, input_locator)

    @property
    def value(self):
        return "NOT_IMPLEMENTED_YET"

    @value.setter
    def value(self, val):
        e = self.input_element.wait_to_be_enabled()
        if e:
            e.click()
            e.clear()
            e.send_keys(val)
            e.send_keys(Keys.RETURN)
