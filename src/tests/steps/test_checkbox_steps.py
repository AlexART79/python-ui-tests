import allure
from pytest_bdd import parsers, scenario, given, when, then

from src.elements.prime_react.react_checkbox import ReactCheckbox
from src.pages.checkbox_page import CheckboxPage
from .conftest import step


# scenarios definition
@allure.epic("React controls")
@allure.feature("Checkbox")
@allure.story("Basic checkbox")
@scenario('react_controls/checkbox.feature', 'Basic checkbox toggle')
def test_checkbox_basic():
    pass


@allure.epic("React controls")
@allure.feature("Checkbox")
@allure.story("Advanced checkbox on/off, label test")
@scenario('react_controls/checkbox.feature', 'Advanced checkbox on off')
def test_checkbox_advanced():
    pass


# Basic autocomplete steps

@given('I have basic checkbox control', target_fixture='checkbox_control')
@step
def basic_checkbox_control(checkbox_demo_page: CheckboxPage):
    return checkbox_demo_page.first_checkbox


@then(parsers.cfparse('Checkbox checked state should be \'{state}\''))
@step
def checkbox_checked_state_should_be(checkbox_control: ReactCheckbox, state: str):
    checked = state == 'On'
    assert checkbox_control.checked is checked


@when('I toggle checkbox state')
@step
def i_toggle_checkbox_state(checkbox_control: ReactCheckbox):
    checkbox_control.click()


@when(parsers.cfparse('I set checkbox state to \'{state}\''))
@step
def i_set_checkbox_state_to(checkbox_control: ReactCheckbox, state: str):
    checked = state == 'On'
    checkbox_control.checked = checked


# Advanced autocomplete steps

@given('I have advanced checkbox control', target_fixture='checkbox_control')
@step
def advanced_checkbox_control(checkbox_demo_page: CheckboxPage):
    return checkbox_demo_page.second_checkbox


@then(parsers.cfparse('Checkbox label should be \'{label_text}\''))
@step
def checkbox_label_should_be(checkbox_control: ReactCheckbox, label_text: str):
    assert checkbox_control.label == label_text
