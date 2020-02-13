import pytest

from ..pages.autocomplete_page import AutoCompletePage
from ..pages.checkbox_page import CheckboxPage
from ..pages.demos_page import DemosPage


@pytest.fixture(scope="function")
def start_page(driver):
    _page = DemosPage(driver)
    _page.goto()

    yield _page

    del _page


@pytest.fixture(scope="function")
def checkbox_page(start_page):
    # goto Checkbox demo page
    start_page.sidebar.goto("Checkbox")
    _page = CheckboxPage(start_page.driver)

    yield _page

    del _page


@pytest.fixture(scope="function")
def autocomplete_page(start_page):
    # goto Autocomplete demo page
    start_page.sidebar.goto("AutoComplete")
    _page = AutoCompletePage(start_page.driver)

    yield _page

    del _page

