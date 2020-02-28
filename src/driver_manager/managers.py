from abc import ABCMeta, abstractmethod
import os
import platform
import sys

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FFOptions
from src.driver_manager.support import BrowserOptions, Platform


#
# TODO: move harcode to config!!!
#

class WebDriverManager(metaclass=ABCMeta):

    """ Base class for driver manager """

    def __init__(self, options:BrowserOptions):
        self.browser = options.browser_type
        self.options = options
        self.desired_cap = {}

    @staticmethod
    def get_platform():
        return Platform[platform.system()]

    @property
    def driver_path(self):
        return os.environ.get("{}_driver_path".format(self.browser))

    def __call__(self):
        return self.get()

    def _get_browserstack_driver(self):
        """ get driver for browserstack """

        drv = webdriver.Remote(
            command_executor='https://alexart1:uMueNv4mgQHTAzapSiFq@hub-cloud.browserstack.com/wd/hub',
            desired_capabilities=self.desired_cap)

        # set window size
        if self.options.window_size is not None:
            drv.set_window_size(self.options.window_size[0], self.options.window_size[1])
        else:
            drv.maximize_window()

        return drv

    @abstractmethod
    def _get_local_driver(self):
         pass

    def _get_selenoid_driver(self):
        drv = webdriver.Remote(
            command_executor=self.options.selenoid_hub_url,
            desired_capabilities=self.desired_cap)

        # set window size
        if self.options.window_size is not None:
            drv.set_window_size(self.options.window_size[0], self.options.window_size[1])
        else:
            drv.maximize_window()

        return drv

    def get(self):

        """ Gets webdriver for browserstack or local driver """

        drv = None
        if self.options.use_browserstack:
            drv = self._get_browserstack_driver()
        elif self.options.use_selenoid:
            drv = self._get_selenoid_driver()
        else:
            drv = self._get_local_driver()

        # set default wait timeout
        drv.implicitly_wait(self.options.timeout)

        return drv


class ChromeManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

        # TODO: get capability from external storage?

        if self.options.use_browserstack:
            self.desired_cap = {
                'browser': 'Chrome',
                'browser_version': '79.0',
                'os': 'Windows',
                'os_version': '10',
                'resolution': '1920x1200',
                'name': 'Bstack-[Python] React UI test'
            }
        elif self.options.use_selenoid:
            self.desired_cap = {
                "browserName": "chrome",
                "version": "79.0",
                "enableVNC": True,
                "enableVideo": False
            }

    def _get_local_driver(self):
        chrome_options = Options()

        if self.options.window_size is not None:
            chrome_options.add_argument(
                "window-size={},{}".format(self.options.window_size[0], self.options.window_size[1]))
        else:
            chrome_options.add_argument("--start-maximized")

        if self.options.headless:
            chrome_options.add_argument("--headless")

        sys.path.insert(0, self.driver_path)
        drv = webdriver.Chrome(self.driver_path, options=chrome_options)

        return drv


class FirefoxManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

        if self.options.use_browserstack:
            self.desired_cap = {
                'browser': 'Firefox',
                'browser_version': '73.0',
                'os': 'Windows',
                'os_version': '10',
                'resolution': '1920x1200',
                'name': 'Bstack-[Python] React UI test'
            }
        elif self.options.use_selenoid:
            self.desired_cap = {
                "browserName": "firefox",
                "version": "73.0",
                "enableVNC": True,
                "enableVideo": False
            }

    def _get_local_driver(self):
        options = FFOptions()
        options.headless = self.options.headless
        # options.binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'

        cap = DesiredCapabilities().FIREFOX
        sys.path.insert(0, self.driver_path)
        drv = webdriver.Firefox(options=options, capabilities=cap,
                                executable_path=self.driver_path)

        if self.options.window_size is not None:
            drv.set_window_size(self.options.window_size[0], self.options.window_size[1])
        else:
            drv.maximize_window()

        return drv


class EdgeManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)
        if self.options.use_browserstack:
            self.desired_cap = {
                'browser': 'Edge',
                'browser_version': '80.0',
                'os': 'Windows',
                'os_version': '10',
                'resolution': '1920x1200',
                'name': 'Bstack-[Python] React UI test'
            }
        elif self.options.use_selenoid:
            self.desired_cap = DesiredCapabilities.EDGE

    def _get_local_driver(self):
        if WebDriverManager.get_platform() != Platform.Windows:
            raise Exception("Edge is supported on Windows only")

        sys.path.insert(0, os.path.dirname(self.driver_path))
        sys.path.insert(0, r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

        cap = DesiredCapabilities().EDGE

        drv = webdriver.Edge(capabilities=cap, executable_path=self.driver_path)
        if self.options.window_size is not None:
            drv.set_window_size(self.options.window_size[0], self.options.window_size[1])
        else:
            drv.maximize_window()

        return drv


class SafariManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

        if self.options.use_browserstack:
            self.desired_cap = {
                'browser': 'Safari',
                'browser_version': '13.0',
                'os': 'OS X',
                'os_version': 'Catalina',
                'resolution': '1920x1080',
                'name': 'Bstack-[Python] React UI test'
            }
        elif self.options.use_selenoid:
            self.desired_cap = DesiredCapabilities.SAFARI

    # TODO: figure out how to test with local safary
    def _get_local_driver(self):
        raise NotImplementedError("Testing on local Safari browser is not implemented yet!")


#
# TODO: Opera driver manager!
#