import os
import shutil
import psutil

from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from src.driver_manager.managers import ChromeManager, FirefoxManager, EdgeManager, SafariManager
from src.driver_manager.support import Browser, BrowserOptions
from src.utils.test_logger import TestLog


log = TestLog()

#
# TODO: implement driver factory!!!
#

class DriverManager:

    @staticmethod
    def cleanup(path):

        """ Delete previously downloaded drivers """

        DriverManager.kill_webdriver()

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
                DriverManager.cleanup(drv_path)

                path = None
                for k in range(1, 5):
                    try:
                        if key == Browser.chrome:
                            path = ChromeDriverManager(path=drv_path).install()
                        else:
                            path = GeckoDriverManager(path=drv_path).install()
                    except:
                        sleep(6)

                if path is None:
                    raise Exception("Unable to install driver for '{}'".format(key))

                os.environ["{}_driver_path".format(key)] = path

            # edge browser
            os.environ["{}_driver_path".format(Browser.edge)] = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                               'webdriver', 'edge', 'msedgedriver.exe')

    @staticmethod
    def get_driver(options: BrowserOptions):

        """
        WebDriver fabric method
        :param options: webdriver options (window size, headless etc.)
        :return: WebDriver
        """

        key = options.browser_type

        if type(options.browser_type) == type(""):
            key = Browser[options.browser_type]

        drivers = {Browser.chrome: ChromeManager(options),
                   Browser.firefox: FirefoxManager(options),
                   Browser.edge: EdgeManager(options),
                   Browser.safari: SafariManager(options)}

        return drivers[key]()
