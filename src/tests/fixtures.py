import pytest

from src.utils.helpers import Helpers
from ..pages.autocomplete_page import AutoCompletePage
from ..pages.checkbox_page import CheckboxPage
from ..pages.demos_page import DemosPage


@pytest.fixture(scope="function")
def start_page(driver, base_url):
    Helpers.print("start_page fixture created")

    _page = DemosPage(driver)
    _page.goto(base_url)

    # verify page header
    assert _page.page_header.text == "The Most Complete UI Framework"

    yield _page

    del _page
    Helpers.print("start_page fixture destroyed")


@pytest.fixture(scope="function")
def checkbox_page(start_page):
    Helpers.print("checkbox_page fixture created")
    # goto Checkbox demo page
    start_page.sidebar.goto("Checkbox")
    _page = CheckboxPage(start_page.driver)

    # verify page header
    assert _page.page_header.text == "Checkbox"

    yield _page

    del _page
    Helpers.print("checkbox_page fixture destroyed")


@pytest.fixture(scope="function")
def autocomplete_page(start_page):
    Helpers.print("autocomplete_page fixture created")
    # goto Autocomplete demo page
    start_page.sidebar.goto("AutoComplete")
    _page = AutoCompletePage(start_page.driver)

    # verify page header
    assert _page.page_header.text == "AutoComplete"

    yield _page

    del _page
    Helpers.print("autocomplete_page fixture created")

