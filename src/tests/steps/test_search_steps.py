import allure
from pytest_bdd import scenario, given, when, then

from src.utils.helpers import Helpers
from .conftest import step
from ..fixtures import start_page


# scenarios definition

@allure.epic("Demo portal")
@allure.feature("Search")
@allure.story("Search on a demos portal")
@scenario('demo_portal/search.feature', 'Search for certain control')
def test_search():
    pass


@given("I am on a demos page")
@step
def demos_page(start_page):
    return start_page


@given("Search box is displayed in sidebar")
@step
def search_box_is_displayed(demos_page):
    search_box = demos_page.sidebar.search_box
    assert Helpers.wait_for(lambda: search_box.is_displayed, 10, 2)


@when("I type <control_name> in the search box")
@step
def type_text_in_the_search_box(demos_page, control_name):
    demos_page.sidebar.search(control_name)


@then("There should be <N> expected results in the list")
@step
def there_should_be_n_elements_in_results(demos_page, N):
    assert Helpers.wait_for(lambda: int(N) == len(demos_page.sidebar.items), 10, 2)
