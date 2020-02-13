from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from src.utils.helpers import wait_for
from .page_elements import Element


class ReactCheckbox(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    def click(self):
        self.find().click()

    @property
    def checked(self):
        cb_locator = (By.XPATH, '..//input')
        cb = self.find().find_element(*cb_locator)
        val = cb.get_attribute("checked")

        return val is not None and (val == True or val == 'true')

    @checked.setter
    def checked(self, val):
        if val and not self.checked:
            self.click()
        if not val and self.checked:
            self.click()

    @property
    def label(self):
        by, val = self.locator
        label_locator = (by, val+"/../following-sibling::label")

        try:
            label_element = self.find().find_element(*label_locator)

            if label_element is not None:
                return label_element.text

        except:
            return ""


class ReactAutoComplete(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @property
    def _input(self):
        input_locator = (By.XPATH, "./input")
        input_element = self.find_element(input_locator)
        return input_element

    @property
    def _list(self):
        list_locator = (By.XPATH, self.locator[1] + "/descendant-or-self::ul[contains(@class, 'p-autocomplete-list')]")
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(list_locator))

    @property
    def _dropdown(self):
        dd_locator = (By.XPATH, "./button")
        button = self.find_element(dd_locator)
        return button

    @property
    def value(self):
        return self._input.get_attribute("value")

    @value.setter
    def value(self, val):
        input_element = self._input
        input_element.send_keys(val)

    @property
    def is_expanded(self):
        return self._list.is_displayed()

    def expand(self):
        action = ActionChains(self.driver).move_to_element(self._dropdown).click().pause(1)

        while not self.is_expanded:
            action.perform()

    def select_value(self, val):
        def find_item():
            global item
            list_element = self._list
            item_path = "./li[. = '{}']".format(val)

            try:
                item = list_element.find_element(By.XPATH, item_path)
                return True, item
            except:
                item = None
                return False, None

        wait_for(lambda : find_item()[0], 10, 1000)
        res, item = find_item()


        if res:
            item.click()
