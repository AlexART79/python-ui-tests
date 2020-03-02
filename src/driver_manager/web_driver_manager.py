import os
import platform
import sys
from abc import ABCMeta, abstractmethod

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.firefox.options import Options as FFOptions

from src.driver_manager.support import BrowserOptions, Platform


class WebDriverManager(metaclass=ABCMeta):

    """ Base class for driver manager """

    def __init__(self, options: BrowserOptions):
        self.options = options

    @staticmethod
    def get_platform():
        return Platform[platform.system()]

    @staticmethod
    def get_architecture():
        return 64 if '64' in platform.architecture()[0] else 32

    def __call__(self):
        return self.get()

    def set_window_size(self, drv):
        # set window size
        if self.options.window_size is not None:
            drv.set_window_size(self.options.window_size[0], self.options.window_size[1])
        else:
            drv.maximize_window()

    def set_window_position(self, drv):
        drv.set_window_position(0, 0)

    @abstractmethod
    def get(self):
        pass


class LocalDriverManager(WebDriverManager):

    """ Base class for local web driver """

    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    @property
    def driver_path(self):
        return os.environ.get("{}_driver_path".format(self.options.browser_type))

    @abstractmethod
    def get(self):
        pass


class RemoteDriverManager(WebDriverManager):

    """ Base class for remote web driver """

    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    @abstractmethod
    def get_capabilities(self):
        return {}

    def get_hub(self):
        return self.options.hub_url

    def get(self):
        drv = webdriver.Remote(
            command_executor=self.get_hub(),
            desired_capabilities=self.get_capabilities())

        self.set_window_size(drv)
        self.set_window_position(drv)

        return drv


#
# SELENOID remote web driver
#
class SelenoidChromeManager(RemoteDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get_capabilities(self):
        return {
                    "browserName": "chrome",
                    "version": "79.0",
                    "enableVNC": True,
                    "enableVideo": False
               }


class SelenoidFirefoxManager(RemoteDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get_capabilities(self):
        return {
                    "browserName": "firefox",
                    "version": "73.0",
                    "enableVNC": True,
                    "enableVideo": False
               }


class SelenoidOperaManager(RemoteDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get_capabilities(self):
        return {
                    "browserName": "Opera",
                    "version": "66.0",
                    "enableVNC": True,
                    "enableVideo": False
               }


#
# BROWSERSTACK remote web driver
#
class BsChromeManager(RemoteDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get_capabilities(self):
        return {
                    'browser': 'Chrome',
                    'browser_version': '79.0',
                    'os': 'Windows',
                    'os_version': '10',
                    'resolution': '1920x1200',
                    'name': 'Bstack-[Python] React UI test'
               }


class BsFirefoxManager(RemoteDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get_capabilities(self):
        return {
                    'browser': 'Firefox',
                    'browser_version': '73.0',
                    'os': 'Windows',
                    'os_version': '10',
                    'resolution': '1920x1200',
                    'name': 'Bstack-[Python] React UI test'
               }


class BsEdgeManager(RemoteDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get_capabilities(self):
        return {
                    'browser': 'Edge',
                    'browser_version': '80.0',
                    'os': 'Windows',
                    'os_version': '10',
                    'resolution': '1920x1200',
                    'name': 'Bstack-[Python] React UI test'
               }


class BsSafariManager(RemoteDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get_capabilities(self):
        return {
                    'browser': 'Safari',
                    'browser_version': '13.0',
                    'os': 'OS X',
                    'os_version': 'Catalina',
                    'resolution': '1920x1080',
                    'name': 'Bstack-[Python] React UI test'
               }


class BsOperaManager(RemoteDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get_capabilities(self):
        return {
                    'browser': 'Opera',
                    'browser_version': '66.0',
                    'os': 'Windows',
                    'os_version': '10',
                    'resolution': '1920x1200',
                    'name': 'Bstack-[Python] React UI test'
               }


#
# LOCAL web driver
#
class LocalChromeManager(LocalDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get(self):
        chrome_options = ChromeOptions()

        if self.options.window_size is not None:
            chrome_options.add_argument(
                "window-size={},{}".format(self.options.window_size[0], self.options.window_size[1]))
        else:
            chrome_options.add_argument("--start-maximized")

        if self.options.headless:
            chrome_options.add_argument("--headless")

        sys.path.insert(0, self.driver_path)
        drv = webdriver.Chrome(self.driver_path, options=chrome_options)

        self.set_window_position(drv)

        return drv


class LocalFirefoxManager(LocalDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get(self):
        options = FFOptions()
        options.headless = self.options.headless

        cap = DesiredCapabilities().FIREFOX
        sys.path.insert(0, self.driver_path)
        drv = webdriver.Firefox(options=options, capabilities=cap,
                                executable_path=self.driver_path)

        self.set_window_size(drv)
        self.set_window_position(drv)

        return drv


class LocalEdgeManager(LocalDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get(self):
        if not WebDriverManager.get_platform() in [Platform.Windows, Platform.Darwin]:
            raise Exception("Edge is supported on Windows or OS-X only")

        sys.path.insert(0, os.path.dirname(self.driver_path))
        sys.path.insert(0, r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

        cap = DesiredCapabilities().EDGE

        drv = webdriver.Edge(capabilities=cap, executable_path=self.driver_path)

        self.set_window_size(drv)
        self.set_window_position(drv)

        return drv


class LocalSafariManager(LocalDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get(self):
        if not WebDriverManager.get_platform() == Platform.Darwin:
            raise Exception("Safari is supported on OS-X only")

        raise NotImplementedError("Implement this!")


class LocalOperaManager(LocalDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

        self.binary_location = r"C:\Users\aartemov\AppData\Local\Programs\Opera\66.0.3515.115\opera.exe" \
            if WebDriverManager.get_platform() == Platform.Windows \
            else "path/to/opera/"

    def get(self):
        cap = DesiredCapabilities.OPERA.copy()

        opt = OperaOptions()
        opt.binary_location = self.binary_location

        drv = webdriver.Opera(executable_path=self.driver_path, desired_capabilities=cap, options=opt)

        self.set_window_size(drv)
        self.set_window_position(drv)

        return drv
