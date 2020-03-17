import os

from src.utils.helpers import Helpers, str2bool


class TestConfig:

    def set_defaults(self):
        self.headless = False
        self.win_size = Helpers.size("1600x900")
        self.browsers_list = ['chrome']
        self.timeout = 15
        self.base_url = ''
        self.use_selenoid = False
        self.use_browserstack = False
        self.hub_url = ''

    def process_ini(self, config):
        self.headless = str2bool(config.getini("headless"))
        self.win_size = Helpers.size(config.getini('window_size'))
        # browser option from ini is 'str' (comma separated), so we need to split it
        self.browsers_list = Helpers.get_browsers(config.getini("browser").split(','))
        self.timeout = config.getini("default_wait_timeout")
        self.base_url = config.getini("base_url")

        # use selenoid
        self.use_selenoid = str2bool(config.getini("use_selenoid"))
        # use browserstack (have less priority than selenoid, so if used both - selenoid will be selected)
        self.use_browserstack = False if self.use_selenoid else str2bool(config.getini("use_browserstack"))
        self.hub_url = config.getini("hub_url")

    def process_commandline(self, config):
        if config.getoption('headless'):
            self.headless = config.getoption("headless")

        if not (config.getoption('window_size') is None or config.getoption('window_size') == ''):
            self.win_size = Helpers.size(config.getoption('window_size'))

        if not (config.getoption('browser') is None or config.getoption('browser') == []):
            self.browsers_list = Helpers.get_browsers(config.getoption('browser'))

    def __init__(self, config):
        # set log level
        os.environ["LOG_LEVEL"] = self.tests_log_level = config.getini("tests_log_level")

        self.set_defaults()
        self.process_ini(config)
        self.process_commandline(config)

    def __str__(self):
        return "Browsers: {}\nWindow size: {}\nHeadless: {}\nApp base URL: {}\nExecution engine: {}\nHub URL: {}\nWait timeout: {}\n".format(
            self.browsers_list,
            self.win_size,
            self.headless,
            self.base_url,
            "Selenoid" if self.use_selenoid else ("BrowserStack" if self.use_browserstack else "Local driver"),
            self.hub_url if self.use_selenoid or self.use_browserstack else "Not used",
            self.timeout)