import os
import platform
import sys

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FFOptions

from src.DriverManager.support import Browser, BrowserOptions, Platform


class WebDriverManager():
    """ Base class for driver manager """

    def __init__(self, type:Browser, options:BrowserOptions):
        self.browser = type
        self.options = options

    @staticmethod
    def get_platform():
        return Platform[platform.system()]

    def __call__(self):
        return self.get()

    def get(self):
        """ Implement this method in subclasses! """


class ChromeManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        WebDriverManager.__init__(self, Browser.chrome, options)

    def get(self):
        chrome_options = Options()

        if self.options.winsize is not None:
            chrome_options.add_argument("window-size={},{}".format(self.options.winsize[0], self.options.winsize[1]))
        else:
            chrome_options.add_argument("--start-maximized")

        if self.options.headless:
            chrome_options.add_argument("--headless")

        drv_path = os.environ.get("{}_driver_path".format(self.browser))
        sys.path.insert(0, drv_path)

        drv = webdriver.Chrome(drv_path, options=chrome_options)

        drv.implicitly_wait(self.options.timeout)

        return drv


class FirefoxManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        WebDriverManager.__init__(self, Browser.firefox, options)

    def get(self):
        options = FFOptions()
        options.headless = self.options.headless
        # options.binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'

        cap = DesiredCapabilities().FIREFOX

        drv_path = os.environ.get("{}_driver_path".format(self.browser))
        sys.path.insert(0, drv_path)

        drv = webdriver.Firefox(options=options, capabilities=cap,
                                executable_path=drv_path)

        if self.options.winsize is not None:
            drv.set_window_size(self.options.winsize[0], self.options.winsize[1])
        else:
            drv.maximize_window()

        drv.implicitly_wait(self.options.timeout)

        return drv


class EdgeManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        WebDriverManager.__init__(self, Browser.edge, options)

    def get(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        if WebDriverManager.get_platform() != Platform.Windows:
            raise Exception("Edge is supported on Windows only")

        sys.path.insert(0, os.path.join(dir_path, 'webdriver', 'edge'))
        sys.path.insert(0, r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

        cap = DesiredCapabilities().EDGE

        drv = webdriver.Edge(capabilities=cap, executable_path=os.path.join(dir_path, 'webdriver', 'msedgedriver.exe'))
        if self.options.winsize is not None:
            drv.set_window_size(self.options.winsize[0], self.options.winsize[1])
        else:
            drv.maximize_window()

        drv.implicitly_wait(self.options.timeout)

        return drv
