import os
import platform
import sys

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FFOptions
from src.driver_manager.support import BrowserOptions, Platform


class WebDriverManager():

    """ Base class for driver manager """

    def __init__(self, options:BrowserOptions):
        self.browser = options.browser_type
        self.options = options

    @staticmethod
    def get_platform():
        return Platform[platform.system()]

    @property
    def driver_path(self):
        return os.environ.get("{}_driver_path".format(self.browser))

    def __call__(self):
        return self.get()

    def get(self):
        """ Implement this method in subclasses! """


class ChromeManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        WebDriverManager.__init__(self, options)

    def get(self):
        chrome_options = Options()

        if self.options.window_size is not None:
            chrome_options.add_argument("window-size={},{}".format(self.options.window_size[0], self.options.window_size[1]))
        else:
            chrome_options.add_argument("--start-maximized")

        if self.options.headless:
            chrome_options.add_argument("--headless")

        sys.path.insert(0, self.driver_path)
        drv = webdriver.Chrome(self.driver_path, options=chrome_options)
        drv.implicitly_wait(self.options.timeout)

        return drv


class FirefoxManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        WebDriverManager.__init__(self, options)

    def get(self):
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

        drv.implicitly_wait(self.options.timeout)

        return drv


class EdgeManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        WebDriverManager.__init__(self, options)

    def get(self):
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

        drv.implicitly_wait(self.options.timeout)

        return drv
