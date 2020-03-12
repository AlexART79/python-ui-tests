from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.utils.helpers import Helpers


class Element(object):
    """
    base element for all UI elements
    """
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    def find(self, timeout=30) -> WebElement:
        _element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(self.locator))

        return _element

    @property
    def text(self):
        return self.find().text

    @property
    def is_displayed(self):
        try:
            def func():
                e = self.find(1)
                return e.is_displayed()

            return Helpers.wait_for(func, 30, 3)

        except TimeoutException:
            return False

    @property
    def is_enabled(self):
        try:
            def func():
                e = self.find(1)
                return e.is_enabled()

            return Helpers.wait_for(func, 30, 3)

        except TimeoutException:
            return False

    def click(self):
        self.find().click()
        sleep(1)

    def clear(self):
        self.find().clear()
        sleep(1)

    def find_element(self, locator):
        """
        Triyng to fing a sub-element inside the current element
        :param locator: locator of sub-element (relative to current element)
        :return: IWebElement or None in case element not found
        """
        e = self.find()

        def func():
            found_element = None
            try:
                found_element = e.find_element(*locator)
            except:
                pass

            if found_element is not None:
                return True

            return False

        if Helpers.wait_for(func, 60, 5):
            return e.find_element(*locator)

        return None

    def find_elements(self, locator):
        """
        Triyng to fing a sub-elements inside the current element
        :param locator: locator of sub-elements (relative to current element)
        :return: IWebElements collection or None in case element not found
        """
        e = self.find()

        def func():
            found_elements = None
            try:
                found_elements = e.find_elements(*locator)
            except:
                pass

            if found_elements is not None:
                return True

            return False

        if Helpers.wait_for(func, 60, 5):
            return e.find_elements(*locator)

        return None

    def get_attribute(self, name):
        return self.find().get_attribute(name)

    def get_property(self, name):
        return self.find().get_property(name)

    def send_keys(self, value):
        self.find().send_keys(value)
        sleep(1)

    def wait(self, cond, timeout=60):
        return WebDriverWait(self.driver, timeout).until(cond)

    def wait_to_be_displayed(self, timeout=60):
        return self.wait(EC.visibility_of_element_located(self.locator), timeout)

    def wait_to_be_hidden(self, timeout=60):
        return self.wait(EC.invisibility_of_element_located(self.locator), timeout)

    def wait_to_be_enabled(self, timeout=60):
        return self.wait(EC.element_to_be_clickable(self.locator), timeout)

    def scroll_into_view(self):
        element = self.find()
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        sleep(1)

    def highlight(self, element, color='red', border=2, effect_time = 0.5):

        """Highlights a Selenium Webdriver element"""

        driver = self.driver

        def apply_style(s):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                  element, s)

        def apply_style_delay(s, delay):
            driver.execute_script("setTimeout(() => { arguments[0].setAttribute('style', arguments[1]);}, arguments[2])",
                                  element, s, delay*1000)

        original_style = element.get_attribute('style')

        apply_style("border: {0}px solid {1};".format(border, color))
        apply_style_delay(original_style, effect_time)
