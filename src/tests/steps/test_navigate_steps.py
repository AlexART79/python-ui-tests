import allure
from pytest_bdd import scenario, given, when, then

from src.pages.demo_base_page import SideMenu
from src.pages.demos_page import DemosPage
from src.utils.helpers import Helpers
from .conftest import step
from ..fixtures import start_page


# scenarios definition
@allure.epic("Demo portal")
@allure.feature("Navigation")
@allure.story("Navigate through demos")
@scenario('DemoPortal/sidebar_navigation.feature', 'Navigate throug demos')
def test_navigate():
    pass


@given("I am on a demos page")
@step
def demos_page(start_page):
    return start_page


@given("Sidebar is displayed on left side", target_fixture="sidebar")
@step
def sidebar_is_displayed(demos_page) -> SideMenu:
    sidebar = demos_page.sidebar
    assert Helpers.wait_for(lambda: sidebar.is_displayed, 10, 2)

    return sidebar


@when("I click <control_name> link in the sidebar")
@step
def i_click_link_in_sidebar(sidebar, control_name: str):
    sidebar.get_item(control_name).click()


@then("<control_name> demo page should be displayed")
@step
def go_through_all_links(demos_page: DemosPage, control_name: str):
    Helpers.wait_for(lambda: demos_page.page_header.is_displayed, 10, 2)
    assert str.lower(demos_page.page_header.text) in str.lower(control_name)
