import os
import shutil
from time import sleep

import psutil
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.DriverManager.managers import ChromeManager, FirefoxManager, EdgeManager
from src.DriverManager.support import Browser, BrowserOptions
from src.utils.test_logger import TestLog


log = TestLog()


class DriverManager:

    @staticmethod
    def cleanup(path):
        DriverManager.kill_webdriver()

        log.debug("Remove all previously downloaded drivers")
        try:
            shutil.rmtree(path)
        except Exception as e:
            log.warn("Looks like something went wrong: {}".format(e))
            pass

    @staticmethod
    def kill_webdriver():
        log.debug("Kill all running webdriver instances")
        for proc in psutil.process_iter():
            if any(procstr in proc.name() for procstr in ['chromedriver', 'geckodriver']):
                try:
                    proc.kill()
                except:
                    log.warn("Not all webdriver instances was successfully terminated. Please double-check manually")
                    pass

    @staticmethod
    def download_drivers():
        for browser in [Browser.chrome, Browser.firefox]:
            log.debug("Download webdriver binaries for '{}'".format(str(browser)))

            drv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src', 'webdriver', str(browser))
            DriverManager.cleanup(drv_path)

            path = None
            for k in range(1, 5):
                try:
                    if browser == Browser.chrome:
                        path = ChromeDriverManager(path=drv_path).install()
                    else:
                        path = GeckoDriverManager(path=drv_path).install()
                except:
                    sleep(6)

            if path is None:
                raise Exception("Unable to install driver for '{}'".format(browser))

            os.environ["{}_driver_path".format(browser)] = path

    @staticmethod
    def get_driver(btype, options: BrowserOptions):

        key = btype

        if type(btype) == type(str):
            key = Browser[btype]

        drivers = {Browser.chrome: ChromeManager(options),
                   Browser.firefox: FirefoxManager(options),
                   Browser.edge: EdgeManager(options)}

        return drivers[key]()
