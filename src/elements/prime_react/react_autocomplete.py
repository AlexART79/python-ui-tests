from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from src.utils.helpers import Helpers
from src.elements.element import Element


class ReactAutoComplete(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @property
    def _input(self) -> WebElement or None:
        input_locator = (By.XPATH, "./input")
        input_element = self.find_element(input_locator)
        return input_element

    @property
    def _list(self) -> WebElement or None:
        list_locator = (By.XPATH, self.locator[1] + "/descendant-or-self::ul[contains(@class, 'p-autocomplete-list')]")
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(list_locator))

    @property
    def _dropdown(self) -> WebElement or None:
        dd_locator = (By.XPATH, "./button")
        button = self.find_element(dd_locator)
        return button

    @property
    def value(self) -> str:
        return self._input.get_attribute("value")

    @value.setter
    def value(self, val: str) -> None:
        input_element = self._input
        input_element.send_keys(val)

    @property
    def is_expanded(self) -> bool:
        return self._list.is_displayed()

    def expand(self) -> None:
        while not self.is_expanded:
            # workaround for SAFARI issue with click
            if self.driver.name.lower() == 'safari':
                self.driver.execute_script("arguments[0].click();", self._dropdown)
            else:
                self._dropdown.click()

            sleep(1)

    def select_value(self, val: str):
        def find_item():
            global item
            list_element = self._list
            item_path = "./li[. = '{}']".format(val)

            try:
                item = list_element.find_element(By.XPATH, item_path)
                return True, item
            except:
                return False, None

        Helpers.wait_for(lambda : find_item()[0], 10, 1)
        res, item = find_item()

        if res:
            # workaround for SAFARI issue with click
            if self.driver.name.lower() == 'safari':
                self.driver.execute_script("arguments[0].click();", item)
            else:
                item.click()
