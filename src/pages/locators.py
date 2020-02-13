import json
from collections import namedtuple


# Load UI definitions from a JSON file

def load_ui_definitions(file_name):
    def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
    def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

    with open(file_name, "r") as read_file:
        ui_defs = json2obj(read_file.read())

    return ui_defs


ui_definitions = load_ui_definitions("src/pages/ui_definitions.json").ui_definitions

# Get UI definition by it's 'path' - "section_name/locator_name"

def get_def(path):
    # split path
    section_name, locator_name = path.split('/')

    # get section
    section = next((x for x in ui_definitions if x.key == section_name), None)
    # check section validity
    if section is None:
        raise Exception("Section definition not found: {}".format(section_name))

    # get locator
    locator = next((x.value for x in section.locators if x.name == locator_name), None)
    # check locator validity
    if locator is None:
        raise Exception("Locator definition not found: {}".format(locator_name))

    # return locator
    return locator


# Locator storage classes

class CommonLocators(object):
    sidebar_locator = get_def("common_locators/sidebar_locator")
    side_menu_item_locator = get_def("common_locators/side_menu_item_locator")


class CheckboxPageLocators(object):
    first_checkbox_locator = get_def("checkbox_page_locators/first_checkbox_locator")
    second_checkbox_locator = get_def("checkbox_page_locators/second_checkbox_locator")


class AutoCompletePageLocators(object):
    basic_autocomplete = get_def("autocomplete_page_locators/basic_autocomplete")
    advanced_autocomplete = get_def("autocomplete_page_locators/advanced_autocomplete")
