import os
import sys

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FFOptions


dir_path = os.path.dirname(os.path.realpath(__file__))


class BrowserOptions:
    def __init__(self, hdls, wsize):
        self.headless = hdls
        self.winsize = wsize


class DriverManager:
    @staticmethod
    def chrome_driver(browser_opt):
        sys.path.insert(0, os.path.join(dir_path, 'webdriver'))

        chrome_options = Options()

        if browser_opt.winsize is not None:
            chrome_options.add_argument("window-size={},{}".format(browser_opt.winsize[0], browser_opt.winsize[1]))
        else:
            chrome_options.add_argument("--start-maximized")

        if browser_opt.headless:
            chrome_options.add_argument("--headless")

        return webdriver.Chrome(os.path.join(dir_path, 'webdriver', 'chromedriver.exe'), options=chrome_options)

    @staticmethod
    def gecko_driver(browser_opt):
        sys.path.insert(0, os.path.join(dir_path, 'webdriver'))

        options = FFOptions()
        options.headless = browser_opt.headless
        options.binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'

        cap = DesiredCapabilities().FIREFOX

        drv = webdriver.Firefox(options=options, capabilities=cap,
                                executable_path=os.path.join(dir_path, 'webdriver', 'geckodriver.exe'))
        if browser_opt.winsize is not None:
            drv.set_window_size(browser_opt.winsize[0], browser_opt.winsize[1])
        else:
            drv.maximize_window()

        return drv

    @staticmethod
    def edge_driver(browser_opt):
        sys.path.insert(0, os.path.join(dir_path, 'webdriver'))
        sys.path.insert(0, r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

        cap = DesiredCapabilities().EDGE

        drv = webdriver.Edge(capabilities=cap, executable_path=os.path.join(dir_path, 'webdriver', 'msedgedriver.exe'))
        if browser_opt.winsize is not None:
            drv.set_window_size(browser_opt.winsize[0], browser_opt.winsize[1])
        else:
            drv.maximize_window()

        return drv

    @staticmethod
    def get_driver(browser):
        drivers = {"chrome": DriverManager.chrome_driver,
                "firefox": DriverManager.gecko_driver,
                "edge": DriverManager.edge_driver}

        return drivers[browser]
