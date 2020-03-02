import os
import shutil
import psutil

from abc import ABCMeta, abstractmethod
from time import sleep

from webdriver_manager.chrome import ChromeDriverManager as cdm
from webdriver_manager.firefox import GeckoDriverManager as gdm
from webdriver_manager.opera import OperaDriverManager as odm

from src.driver_manager.support import Browser, BrowserOptions
from src.driver_manager.web_driver_manager import SelenoidChromeManager, SelenoidFirefoxManager, SelenoidOperaManager, \
    BsChromeManager, BsFirefoxManager, BsEdgeManager, BsSafariManager, BsOperaManager, LocalChromeManager, \
    LocalFirefoxManager, LocalEdgeManager, LocalSafariManager, LocalOperaManager
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
            if key in [Browser.chrome, Browser.firefox, Browser.opera, Browser.edge]:
                log.debug("Download webdriver binaries for '{}'".format(key))

                drv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'webdriver', str(key))
                LocalDriverFactory.cleanup(drv_path)

                path = None
                for k in range(1, 5):
                    try:
                        if key == Browser.chrome:
                            path = cdm(path=drv_path).install()
                        elif key == Browser.firefox:
                            path = gdm(path=drv_path).install()
                        elif key == Browser.opera:
                            path = odm(path=drv_path, version='v.79.0.3945.79').install()
                        elif key == Browser.edge:
                            path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                'webdriver', 'edge', 'msedgedriver.exe')
                    except:
                        sleep(6)

                if path is None:
                    raise Exception("Unable to install driver for '{}'".format(key))

                os.environ["{}_driver_path".format(key)] = path

    @staticmethod
    def get_driver(options: BrowserOptions):
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
