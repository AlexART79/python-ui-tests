import json
from collections import namedtuple

from selenium.webdriver.common.by import By


class CommonLocators(object):
    sidebar_locator = (By.CLASS_NAME, "layout-sidebar")
    side_menu_item_locator = (By.XPATH, "//ul[@class='layout-submenu']/li[@role='presentation']/a")


class CheckboxPageLocators(object):
    first_checkbox_locator = (By.XPATH,
          "//h3[@class='first']/following-sibling::div/div[contains(@class, 'p-checkbox') and @role='checkbox']")
    second_checkbox_locator = (By.XPATH,
          "(//div[contains(@class, 'p-checkbox') and @role='checkbox'])[2]")


class AutoCompletePageLocators(object):
    basic_autocomplete = (By.XPATH,
          "(//span[contains(@class, 'p-autocomplete')])[1]")
    advanced_autocomplete = (By.XPATH,
          "(//span[contains(@class, 'p-autocomplete')])[2]")


def load_ui_definitions(file_name):
    def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
    def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

    with open(file_name, "r") as read_file:
        ui_defs = json2obj(read_file.read())

    return ui_defs


ui_definitions = load_ui_definitions("src/pages/ui_definitions.json").ui_definitions