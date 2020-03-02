import json
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

    @property
    def engine(self):
        if self.options.use_browserstack:
            return 'browserstack'
        if self.options.use_selenoid:
            return 'selenoid'

    def get_capabilities(self):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'webdriver', 'caps',
                            '{}_{}.json'.format(self.options.browser_type, self.engine))
        with open(path) as jf:
            cap = json.load(jf)
            return cap

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
# LOCAL web driver
#
class LocalChromeManager(LocalDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get(self):
        chrome_options = ChromeOptions()
        chrome_options.headless = self.options.headless

        sys.path.insert(0, self.driver_path)
        drv = webdriver.Chrome(self.driver_path, options=chrome_options)

        self.set_window_position(drv)
        self.set_window_size(drv)

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
