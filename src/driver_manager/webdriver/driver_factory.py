import sys
import os
import shutil
import platform
import psutil

from abc import ABCMeta, abstractmethod
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager as cdm
from webdriver_manager.firefox import GeckoDriverManager as gdm

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FFOptions

from src.driver_manager.support import Browser, BrowserOptions, Platform
from src.utils.test_logger import TestLog


log = TestLog()


class DriverFactory(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_driver(options: BrowserOptions):
        pass


class LocalDriverFactory(DriverFactory):
    @staticmethod
    def cleanup(path):

        """ Delete previously downloaded drivers """

        LocalDriverFactory.kill_webdriver()

        log.debug("Remove all previously downloaded drivers")
        try:
            shutil.rmtree(path)
        except Exception as e:
            log.warn("Looks like something went wrong: {}".format(e))
            pass

    @staticmethod
    def kill_webdriver():

        """ Kill all running webdriver instances """

        log.debug("Kill all running webdriver instances")
        for proc in psutil.process_iter():
            if any(procstr in proc.name() for procstr in ['chromedriver', 'geckodriver']):
                try:
                    proc.kill()
                except:
                    log.warn("Not all webdriver instances was successfully terminated. Please double-check manually")
                    pass

    @staticmethod
    def download_drivers(browser_list):

        """ Download drivers for chrome and firefox """

        for browser in browser_list:
            key = Browser[browser]
            if key in [Browser.chrome, Browser.firefox]:
                log.debug("Download webdriver binaries for '{}'".format(key))

                drv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'webdriver', str(key))
                LocalDriverFactory.cleanup(drv_path)

                path = None
                for k in range(1, 5):
                    try:
                        if key == Browser.chrome:
                            path = cdm(path=drv_path).install()
                        else:
                            path = gdm(path=drv_path).install()
                    except:
                        sleep(6)

                if path is None:
                    raise Exception("Unable to install driver for '{}'".format(key))

                os.environ["{}_driver_path".format(key)] = path

            # edge browser
            os.environ["{}_driver_path".format(Browser.edge)] = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'webdriver', 'edge', 'msedgedriver.exe')

    @staticmethod
    def get_driver(options: BrowserOptions):

        # create LocalDriverManager instance
        # get appropriate WebDriver

        if options.browser_type == Browser.chrome:
            return LocalChromeManager(options).get()
        if options.browser_type == Browser.firefox:
            return LocalFirefoxManager(options).get()
        if options.browser_type == Browser.edge:
            return LocalEdgeManager(options).get()
        if options.browser_type == Browser.safari:
            return LocalSafariManager(options).get()
        if options.browser_type == Browser.opera:
            return LocalOperaManager(options).get()

        raise Exception("Unsupported browser: {}".format(options.browser_type))


class SelenoidDriverFactory(DriverFactory):
    @staticmethod
    def get_driver(options: BrowserOptions):

        # create SelenoidDriverManager
        # get driver

        if options.browser_type == Browser.chrome:
            return SelenoidChromeManager(options).get()
        if options.browser_type == Browser.firefox:
            return SelenoidFirefoxManager(options).get()
        if options.browser_type == Browser.opera:
            return SelenoidOperaManager(options).get()

        raise Exception("Unsupported browser: {}".format(options.browser_type))


class BsDriverFactory(DriverFactory):
    @staticmethod
    def get_driver(options: BrowserOptions):

        # create BrowserStackManager
        # get driver

        if options.browser_type == Browser.chrome:
            return BsChromeManager(options).get()
        if options.browser_type == Browser.firefox:
            return BsFirefoxManager(options).get()
        if options.browser_type == Browser.edge:
            return BsEdgeManager(options).get()
        if options.browser_type == Browser.safari:
            return BsSafariManager(options).get()
        if options.browser_type == Browser.opera:
            return BsOperaManager(options).get()

        raise Exception("Unsupported browser: {}".format(options.browser_type))


####################################################


class WebDriverManager(metaclass=ABCMeta):
    def __init__(self, options: BrowserOptions):
        self.options = options

    @staticmethod
    def get_platform():
        return Platform[platform.system()]

    def __call__(self):
        return self.get()

    @abstractmethod
    def get(self):
        pass


class LocalDriverManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    @property
    def driver_path(self):
        return os.environ.get("{}_driver_path".format(self.options.browser_type))

    @abstractmethod
    def get(self):
        pass


class RemoteDriverManager(WebDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    @abstractmethod
    def get_capabilities(self):
        return {}

    @abstractmethod
    def get_hub(self):
        return ""

    def get(self):
        drv = webdriver.Remote(
            command_executor=self.get_hub(),
            desired_capabilities=self.get_capabilities())

        # set window size
        if self.options.window_size is not None:
            drv.set_window_size(self.options.window_size[0], self.options.window_size[1])
        else:
            drv.maximize_window()

        return drv


class SelenoidDriverManager(RemoteDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    @abstractmethod
    def get_capabilities(self):
        return {}

    def get_hub(self):
        return self.options.selenoid_hub_url


class BsDriverManager(RemoteDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    @abstractmethod
    def get_capabilities(self):
        return {}

    def get_hub(self):
        return "https://alexart1:uMueNv4mgQHTAzapSiFq@hub-cloud.browserstack.com/wd/hub"


class SelenoidChromeManager(SelenoidDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get_capabilities(self):
        return {
                    "browserName": "chrome",
                    "version": "79.0",
                    "enableVNC": True,
                    "enableVideo": False
               }


class SelenoidFirefoxManager(SelenoidDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get_capabilities(self):
        return {
                    "browserName": "firefox",
                    "version": "73.0",
                    "enableVNC": True,
                    "enableVideo": False
               }


class SelenoidOperaManager(SelenoidDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get_capabilities(self):
        return {
                    "browserName": "Opera",
                    "version": "66.0",
                    "enableVNC": True,
                    "enableVideo": False
               }


class BsChromeManager(BsDriverManager):
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


class BsFirefoxManager(BsDriverManager):
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


class BsEdgeManager(BsDriverManager):
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


class BsSafariManager(BsDriverManager):
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


class BsOperaManager(BsDriverManager):
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


class LocalChromeManager(LocalDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get(self):
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


class LocalFirefoxManager(LocalDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

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

        return drv


class LocalEdgeManager(LocalDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

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

        return drv


class LocalSafariManager(LocalDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get(self):
        raise NotImplementedError("Testing on local Safari browser is not implemented yet!")


class LocalOperaManager(LocalDriverManager):
    def __init__(self, options: BrowserOptions):
        super().__init__(options)

    def get(self):
        raise NotImplementedError("Testing on local Opera browser is not implemented yet!")


