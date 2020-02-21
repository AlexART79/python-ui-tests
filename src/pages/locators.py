import json
from collections import namedtuple
from src.utils.test_logger import TestLog


log = TestLog()


class UiDefinitions:
    def __init__(self, file_path):
        self.ui_definitions = self.load_ui_definitions(file_path).ui_definitions

    # Load UI definitions from a JSON file
    def load_ui_definitions(self, file_name):
        log.debug("Loading UI definitions from {}".format(file_name))

        def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())

        def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

        with open(file_name, "r") as read_file:
            ui_defs = json2obj(read_file.read())

        return ui_defs

    # Get UI definition by it's 'path' - "section_name/locator_name"
    def get(self, path):
        log.debug("Get UI control locator: {}".format(path))

        # split path
        section_name, locator_name = path.split('/')

        # get section
        section = next((x for x in self.ui_definitions if x.key == section_name), None)
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


ui_definitions = UiDefinitions("src/pages/ui_definitions.json")
