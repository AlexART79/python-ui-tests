from time import sleep

import allure
import pytest
from allure_commons._allure import step, attach

from src.pages.checkbox_page import CheckboxPage
from src.utils.helpers import Helpers
from src.utils.test_logger import TestLog
from src.tests.fixtures import start_page


log = TestLog()


@pytest.fixture
def checkbox_demo_page(start_page):
    log.debug("checkbox_page created")
    # goto Checkbox demo page
    start_page.sidebar.goto("Checkbox")
    _page = CheckboxPage(start_page.driver)

    # verify page header
    assert Helpers.wait_for(lambda:  _page.page_header.text == "Checkbox", 50, 5)

    yield _page

    del _page
    log.debug("checkbox_page fixture destroyed")


@allure.epic("React controls")
@allure.feature("Checkbox")
@pytest.mark.checkbox
class TestCheckbox:

    @allure.story("Basic checkbox")
    @allure.title("Test basic checkbox")
    @pytest.mark.basic
    def test_basic_checkbox(self, driver, checkbox_demo_page):

        checkbox = None

        with step("Get basic checkbox"):
            checkbox = checkbox_demo_page.first_checkbox

        with step("Check initial checkbox state"):
            attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert not checkbox.checked

        with step("Toggle checkbox"):
            checkbox.click()

        with step("Checkbox should be checked"):
            attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert checkbox.checked

    @allure.story("Advanced checkbox")
    @allure.title("Test advanced checkbox")
    @pytest.mark.advanced
    def test_advanced_checkbox(self, driver, checkbox_demo_page):

        checkbox = None

        with step("Get advanced checkbox"):
            checkbox = checkbox_demo_page.second_checkbox

        with step("Check initial checkbox state"):
            attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert not checkbox.checked

        with step("Checkbox label should be 'New York'"):
            attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert checkbox.label == 'New York'

        with step("Set checkbox state to 'ON'"):
            checkbox.checked = True

        with step("Checkbox should be checked"):
            attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert checkbox.checked

        with step("Set checkbox state to 'OFF'"):
            checkbox.checked = False

        with step("Checkbox should be NOT checked"):
            attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert not checkbox.checked
