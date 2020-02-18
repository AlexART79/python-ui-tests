import allure
from allure_commons._allure import StepContext

from src.utils.helpers import Helpers


def pytest_bdd_before_scenario(request, feature, scenario):
    Helpers.print("pytest_bdd_before_scenario hook started")

# step error hook (attach screenshot on failure)
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    driver = request.getfixturevalue('driver')
    allure.attach(driver.get_screenshot_as_png(), name='{} {} {}'.format(feature.name, scenario.name, step.name), attachment_type=allure.attachment_type.PNG)


# custom step def
def step(title):
    if callable(title):
        return StepContext(title.__name__.replace('_', ' '), {})(title)
    else:
        return StepContext(title.replace('_', ' '), {})
