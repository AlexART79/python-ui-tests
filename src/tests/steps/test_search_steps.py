import allure
from pytest_bdd import scenario, given, when, then

from .conftest import step
from ..fixtures import start_page


# scenarios definition

@allure.epic("Demo portal")
@allure.feature("Search")
@allure.story("Search on a demos portal")
@scenario('search.feature', 'Search for certain control')
def test_search():
    pass


@given("I am on a demos page")
@step
def page(start_page):
    return start_page


@given("Search box is displayed in sidebar")
@step
def search_box_is_displayed(page):
    search_box = page.sidebar.search_box
    assert search_box.is_displayed


@when("I type <control_name> in the search box")
@step
def type_text_in_the_search_box(page, control_name):
    page.sidebar.search(control_name)


@then("There should be <N> expected results in the list")
@step
def there_should_be_n_elements_in_results(page, N):
    assert int(N) == len(page.sidebar.items)
