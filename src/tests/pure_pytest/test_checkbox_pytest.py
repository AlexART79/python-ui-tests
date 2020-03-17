import allure
import pytest

from src.elements.prime_react.react_checkbox import ReactCheckbox
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
    assert Helpers.wait_for(_page.header.text == "Checkbox", 50, 5, title="Wait for page title: 'Checkbox'")

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
        checkbox: ReactCheckbox = None

        with allure.step("Get basic checkbox"):
            checkbox = checkbox_demo_page.first_checkbox

        with allure.step("Check initial checkbox state"):
            allure.attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert not checkbox.checked

        with allure.step("Toggle checkbox"):
            checkbox.click()

        with allure.step("Checkbox should be checked"):
            allure.attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert checkbox.checked

    @allure.story("Advanced checkbox")
    @allure.title("Test advanced checkbox")
    @pytest.mark.advanced
    def test_advanced_checkbox(self, driver, checkbox_demo_page):
        checkbox: ReactCheckbox = None

        with allure.step("Get advanced checkbox"):
            checkbox = checkbox_demo_page.second_checkbox

        with allure.step("Check initial checkbox state"):
            allure.attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert not checkbox.checked

        with allure.step("Checkbox label should be 'New York'"):
            allure.attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert checkbox.label == 'New York'

        with allure.step("Set checkbox state to 'ON'"):
            checkbox.checked = True

        with allure.step("Checkbox should be checked"):
            allure.attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert checkbox.checked

        with allure.step("Set checkbox state to 'OFF'"):
            checkbox.checked = False

        with allure.step("Checkbox should be NOT checked"):
            allure.attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert not checkbox.checked
