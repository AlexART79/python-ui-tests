from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from ..utils.helpers import wait_for


class Element(object):
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    def find(self, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(self.locator))

    @property
    def text(self):
        return self.find().text

    def is_displayed(self):
        try:
            def func():
                e = self.find(1)
                return e.is_displayed()

            return wait_for(func, 30, 3)

        except TimeoutException:
            return False

    def click(self):
        self.find().click()
        sleep(1)

    def clear(self):
        self.find().clear()
        sleep(1)

    def find_element(self, locator):
        e = self.find()

        def func():
            found_elements = None
            try:
                found_elements = e.find_element(*locator)
            except:
                pass

            if found_elements is not None:
                return True

            return False

        if wait_for(func, 60, 5):
            return e.find_element(*locator)

        return None

    def find_elements(self, locator):
        if self.find() is not None:
            return WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located(locator))

        return None

    def find_all(self, locator):
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

        if wait_for(func, 60, 5):
            return e.find_element(*locator)


        return self.find().find_elements(*locator)

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


class Checkbox(Element):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @property
    def is_checked(self):
        checked = self.find().get_attribute("checked")
        return checked is not None


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



