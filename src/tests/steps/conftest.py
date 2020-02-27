import allure
from allure_commons._allure import StepContext
from pytest_bdd import given

from src.pages.autocomplete_page import AutoCompletePage
from src.pages.checkbox_page import CheckboxPage
from src.utils.test_logger import TestLog

from ..fixtures import start_page


log = TestLog()


# pytest hooks

def pytest_bdd_before_scenario(request, feature, scenario):
    log.debug("pytest_bdd_before_scenario hook. Prepare your test and data for execution...")


# step error hook (attach screenshot on failure)
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    driver = request.getfixturevalue('driver')
    allure.attach(driver.get_screenshot_as_png(), name='{} {} {}'.format(feature.name, scenario.name, step.name),
                  attachment_type=allure.attachment_type.PNG)

# end: pytest hooks


# custom step decorator (replaces '_' to ' ' in function name for readability)
def step(title, take_screenshot=False):
    if callable(title):
        return StepContext(title.__name__.replace('_', ' '), {})(title)
    else:
        return StepContext(title.replace('_', ' '), {})


#
# shared steps
#

@given("I have Checkbox demo page")
def checkbox_demo_page(start_page):
    log.debug("checkbox_page created")
    # goto Checkbox demo page
    start_page.sidebar.goto("Checkbox")
    _page = CheckboxPage(start_page.driver)

    # verify page header
    assert _page.header.text == "Checkbox"

    yield _page

    del _page
    log.debug("checkbox_page fixture destroyed")


@given("I have Autocomplete demo page")
def autocomplete_demo_page(start_page):
    log.debug("autocomplete_page fixture created")
    # goto Autocomplete demo page
    start_page.sidebar.goto("AutoComplete")
    _page = AutoCompletePage(start_page.driver)

    # verify page header
    assert _page.header.text == "AutoComplete"

    yield _page

    del _page
    log.debug("autocomplete_page fixture destroyed")
