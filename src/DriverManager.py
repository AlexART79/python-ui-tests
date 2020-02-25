import os
import platform
import shutil
import sys
from threading import Lock
from time import sleep

import psutil
from datetime import datetime
from enum import Enum

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FFOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class Platform(Enum):
    Windows = 1
    Darwin = 2
    Linux = 3

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __str__(self):
        return self.name


def get_platform():
    return Platform[platform.system()]


dir_path = os.path.dirname(os.path.realpath(__file__))


class BrowserOptions:
    def __init__(self, hdls, wsize, timeout):
        self.headless = hdls
        self.winsize = wsize
        self.timeout = timeout


class DriverManager:

    def __init__(self, type:str, options:BrowserOptions):
        self.browser = type
        self.options = options

    def chrome(self):
        sys.path.insert(0, os.path.join(dir_path, 'webdriver'))
        chrome_options = Options()

        if self.options.winsize is not None:
            chrome_options.add_argument("window-size={},{}".format(self.options.winsize[0], self.options.winsize[1]))
        else:
            chrome_options.add_argument("--start-maximized")

        if self.options.headless:
            chrome_options.add_argument("--headless")

        drv_path = ChromeDriverManager(path=os.path.join(dir_path, 'webdriver', self.browser)).install()
        drv = webdriver.Chrome(drv_path, options=chrome_options)

        return drv

    def firefox(self):
        sys.path.insert(0, os.path.join(dir_path, 'webdriver'))

        options = FFOptions()
        options.headless = self.options.headless
        #options.binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'

        cap = DesiredCapabilities().FIREFOX

        drv_path = GeckoDriverManager(path=os.path.join(dir_path, 'webdriver', self.browser)).install()
        drv = webdriver.Firefox(options=options, capabilities=cap,
                                executable_path=drv_path)

        if self.options.winsize is not None:
            drv.set_window_size(self.options.winsize[0], self.options.winsize[1])
        else:
            drv.maximize_window()

        return drv

    def edge(self):

        if get_platform() != Platform.Windows:
            raise Exception("Edge is supported on Windows only")

        sys.path.insert(0, os.path.join(dir_path, 'webdriver'))
        sys.path.insert(0, r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

        cap = DesiredCapabilities().EDGE

        drv = webdriver.Edge(capabilities=cap, executable_path=os.path.join(dir_path, 'webdriver', 'msedgedriver.exe'))
        if self.options.winsize is not None:
            drv.set_window_size(self.options.winsize[0], self.options.winsize[1])
        else:
            drv.maximize_window()

        return drv

    def get_driver(self):
        drivers = {"chrome": self.chrome,
                "firefox": self.firefox,
                "edge": self.edge}

        d = drivers[self.browser]()
        d.implicitly_wait(self.options.timeout)

        return d
