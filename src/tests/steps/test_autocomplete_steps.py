import allure
from flaky import flaky
from pytest_bdd import parsers, scenario, given, when, then

from src.utils.helpers import Helpers
from .conftest import step
from ..fixtures import autocomplete_page, start_page


# scenarios definition

@flaky(max_runs=5)
@allure.epic("React controls")
@allure.feature("Autocomplete")
@allure.story("Basic autocomplete select")
@scenario('autocomplete.feature', 'Basic autocomplete select')
def test_autocomplete_basic():
    pass


@allure.epic("React controls")
@allure.feature("Autocomplete")
@allure.story("Advanced autocomplete select")
@scenario('autocomplete.feature', 'Advanced autocomplete select')
def test_autocomplete_advanced():
    pass


# Basic autocomplete steps

@given('I have basic autocomplete control', target_fixture='autocomplete_control')
@step
def basic_autocomplete_control(autocomplete_page):
    return autocomplete_page.basic_autocomplete


@when('I start typing <text> in basic autocomplete control')
@step
def start_typing_value_into_basic_autocomplete(basic_autocomplete_control, text):
    basic_autocomplete_control.value = text


@when('I selected value <value> in autocomplete dropdown')
@when(parsers.cfparse('I selected value \'{value}\' in autocomplete dropdown'))
@step
def select_value_in_basic_autocomplete_dropdown(autocomplete_control, value):
    autocomplete_control.select_value(value)


@then('Autocomplete control value should be <value>')
@then(parsers.cfparse('Autocomplete control value should be \'{value}\''))
@step
def autocomplete_control_value_should_be(autocomplete_control, value, driver):
    allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=allure.attachment_type.PNG)
    actual_val = autocomplete_control.value
    assert actual_val == value


# Advanced autocomplete steps

@given('I have advanced autocomplete control', target_fixture='autocomplete_control')
@step
def advanced_autocomplete_control(autocomplete_page):
    return autocomplete_page.advanced_autocomplete


@when('I click dropdown button in advanced autocomplete control')
@step
def i_click_dropdown_button_in_advanced_autocomplete_control(advanced_autocomplete_control):
    advanced_autocomplete_control.expand()


@then('Autocomplete should became expanded')
@step
def autocomplete_control_should_became_expanded(autocomplete_control, driver):
    allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=allure.attachment_type.PNG)
    assert Helpers.wait_for(lambda: autocomplete_control.is_expanded, 10, 2)


@then('Autocomplete should became collapsed')
@step
def autocomplete_control_should_became_collapsed(autocomplete_control, driver):
    allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=allure.attachment_type.PNG)
    assert Helpers.wait_for(lambda: not autocomplete_control.is_expanded, 10, 2)
