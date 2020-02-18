import allure
from pytest_bdd import parsers, scenario, given, when, then

from .conftest import step
from ..fixtures import checkbox_page, start_page


# scenarios definition
@allure.epic("React controls")
@allure.feature("Checkbox")
@allure.story("Basic checkbox")
@scenario('checkbox.feature', 'Basic checkbox toggle')
def test_checkbox_basic():
    pass


@allure.epic("React controls")
@allure.feature("Checkbox")
@allure.story("Advanced checkbox on/off, label test")
@scenario('checkbox.feature', 'Advanced checkbox on off')
def test_checkbox_advanced():
    pass


# Basic autocomplete steps

@given('I have basic checkbox control', target_fixture='checkbox_control')
@step
def basic_checkbox_control(checkbox_page):
    return checkbox_page.first_checkbox


@then(parsers.cfparse('Checkbox checked state should be \'{state}\''))
@step
def checkbox_checked_state_should_be(checkbox_control, state):
    checked = state == 'On'
    assert checkbox_control.checked is checked


@when('I toggle checkbox state')
@step
def i_toggle_checkbox_state(checkbox_control):
    checkbox_control.click()


@when(parsers.cfparse('I set checkbox state to \'{state}\''))
@step
def i_set_checkbox_state_to(checkbox_control, state):
    checked = state == 'On'
    checkbox_control.checked = checked


# Advanced autocomplete steps

@given('I have advanced checkbox control', target_fixture='checkbox_control')
@step
def advanced_autocomplete_control(checkbox_page):
    return checkbox_page.second_checkbox


@then(parsers.cfparse('Checkbox label should be \'{label_text}\''))
@step
def checkbox_label_should_be(checkbox_control, label_text):
    assert checkbox_control.label == label_text
