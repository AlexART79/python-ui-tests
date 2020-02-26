import allure
import pytest
from flaky import flaky

from src.pages.autocomplete_page import AutoCompletePage
from src.utils.helpers import Helpers
from src.utils.test_logger import TestLog
from src.tests.fixtures import start_page


log = TestLog()


def autocomplete_data():
    return [
        ["Uni", "United States"],
        ["Uni", "United Kingdom"],
        ["Uk", "Ukraine"]
    ]


@pytest.fixture
def autocomplete_demo_page(start_page):
    log.debug("autocomplete_page fixture created")
    # goto Autocomplete demo page
    start_page.sidebar.goto("AutoComplete")
    _page = AutoCompletePage(start_page.driver)

    # verify page header
    assert Helpers.wait_for(_page.page_header.text == "AutoComplete", 50, 5)

    yield _page

    del _page
    log.debug("autocomplete_page fixture destroyed")


@allure.epic("React controls")
@allure.feature("Autocomplete")
@pytest.mark.autocomplete
class TestAutocomplete:

    @flaky(max_runs=3, min_passes=1)
    @allure.story("Basic autocomplete")
    @allure.title("Test basic autocomplete")
    @pytest.mark.basic
    @pytest.mark.parametrize("text, value", autocomplete_data())
    def test_basic_autocomplete(self, driver, autocomplete_demo_page, text, value):

        autocomplete = None

        with allure.step("Get basic autocomplete"):
            autocomplete = autocomplete_demo_page.basic_autocomplete

        with allure.step("start typing '{}' in basic autocomplete control".format(text)):
            autocomplete.value = text

        with allure.step("selected value '{}' in autocomplete dropdown".format(value)):
            autocomplete.select_value(value)

        with allure.step("Autocomplete should became collapsed"):
            allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=allure.attachment_type.PNG)
            assert Helpers.wait_for(lambda: not autocomplete.is_expanded, 10, 2)

        with allure.step("Autocomplete control value should be '{}'".format(value)):
            allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=allure.attachment_type.PNG)
            actual_val = autocomplete.value
            assert actual_val == value

    @allure.story("Advanced autocomplete")
    @allure.title("Test advanced autocomplete")
    @pytest.mark.advanced
    def test_advanced_autocomplete(self, driver, autocomplete_demo_page):

        autocomplete = None
        exp_value = 'Audi'

        with allure.step("Get advanced autocomplete"):
            autocomplete = autocomplete_demo_page.advanced_autocomplete

        with allure.step("I click dropdown button in advanced autocomplete control"):
            autocomplete.expand()

        with allure.step("Autocomplete should became expanded"):
            allure.attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert Helpers.wait_for(lambda: autocomplete.is_expanded, 10, 2)

        with allure.step("Select value '{}' in autocomplete dropdown".format(exp_value)):
            autocomplete.select_value(exp_value)

        with allure.step("Autocomplete should became collapsed"):
            allure.attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert Helpers.wait_for(lambda: not autocomplete.is_expanded, 10, 2)

        with allure.step("Autocomplete control value should be '{}'".format(exp_value)):
            allure.attach(driver.get_screenshot_as_png(), name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            assert autocomplete.value == exp_value
