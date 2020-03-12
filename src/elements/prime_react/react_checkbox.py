from selenium.webdriver.common.by import By

from src.elements.element import Element


class ReactCheckbox(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    def click(self) -> None:
        self.find().click()

    @property
    def checked(self) -> bool:
        cb_locator = (By.XPATH, '..//input')
        cb = self.find().find_element(*cb_locator)
        val = cb.get_attribute("checked")

        return val is not None and (val == True or val == 'true')

    @checked.setter
    def checked(self, val: bool) -> None:
        if val and not self.checked:
            self.click()
        if not val and self.checked:
            self.click()

    @property
    def label(self) -> str:
        by, val = self.locator
        label_locator = (by, val+"/../following-sibling::label")

        try:
            label_element = self.find().find_element(*label_locator)

            if label_element is not None:
                return label_element.text

        except:
            return ""