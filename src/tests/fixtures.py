import pytest

from src.utils.helpers import Helpers
from src.utils.test_logger import TestLog
from ..pages.demos_page import DemosPage


log = TestLog()


@pytest.fixture(scope="function")
def start_page(driver, base_url):
    log.debug("start_page fixture created")

    _page = DemosPage(driver)
    _page.goto(base_url)

    # verify page header
    assert Helpers.wait_for(_page.page_header.text == "The Most Complete UI Framework", 50, 5)

    yield _page

    del _page
    log.debug("start_page fixture destroyed")
