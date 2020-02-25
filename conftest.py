import os
import shutil
from time import sleep

import allure
import psutil
import pytest
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.DriverManager import DriverManager, BrowserOptions
from src.utils.helpers import Helpers
from src.utils.test_logger import TestLog


log = TestLog()


#
# Register cmd-line options and ini file options
#
def pytest_addoption(parser):
    log.debug("pytest_addoption")

    # cmd-line options
    parser.addoption("-B", "--browser",
                     dest="browser",
                     action="append",
                     default=[],
                     help="Browser. Valid options are firefox, chrome or all (to test both)")
    parser.addoption("-H", "--headless",
                     dest="headless",
                     action="store_true",
                     default=False,
                     help="Run in headless mode (FF, Chrome). Values: yes|no")
    parser.addoption("--window-size",
                     dest="window_size",
                     action="store",
                     default="",
                     help="Run in headless mode (FF, Chrome). Values: yes|no")

    # ini options
    parser.addini('tests_log_level', 'Log level', default="INFO")
    parser.addini('base_url', 'base AUT url')
    parser.addini('default_wait_timeout', 'default timeout value for implicitly wait', default=5)


#
# configure webdriver based on cmd-line arguments
#
def pytest_configure(config):
    os.environ["LOG_LEVEL"] = config.getini("tests_log_level")
    TestLog.configure()

    log.debug("pytest_configure")

    # headless/normal mode
    hdls = config.getoption("headless")
    # window size
    win_size = Helpers.get_window_size_option(config)
    # browsers to run tests in
    browsers_list = Helpers.get_browser_option(config)

    # default timeout for implicitly wait from pytest.ini
    timeout = config.getini("default_wait_timeout")

    browser_opt = BrowserOptions(hdls, win_size, timeout)

    # download drivers
    download_drivers()

    # create plugin class
    class DriverPlugin:
        #
        # web driver fixture
        #
        @pytest.fixture(autouse=True, params=browsers_list, scope="function")
        def driver(self, request):
            # prepare webdriver
            browser_type = request.param

            log.debug("Create 'driver' fixture for {}".format(browser_type))

            manager = DriverManager(browser_type, browser_opt)
            d = manager.get_driver()

            # return prepared webdriver
            yield d

            if request.node.rep_call.failed:
                log.error("Test '{}' failed!".format(request.function.__name__))
                try:
                    #d.execute_script("document.body.bgColor = 'white';")
                    allure.attach(d.get_screenshot_as_png(), name='screenshot on fail',
                                  attachment_type=allure.attachment_type.PNG)
                except:
                    pass  # just ignore

            # finalization
            d.close()
            log.debug("'driver' fixture finalized")

    # register plugin
    config.pluginmanager.register(DriverPlugin())


def download_drivers():

    def cleanup(path):
        kill_webdriver()

        try:
            shutil.rmtree(path)
        except Exception as e:
            pass

    def kill_webdriver():
        for proc in psutil.process_iter():
            if any(procstr in proc.name() for procstr in ['chromedriver', 'geckodriver']):
                try:
                    proc.kill()
                except:
                    pass

    for browser in ['chrome', 'firefox']:
        log.debug("Download webdriver binaries for '{}'".format(browser))

        drv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src', 'webdriver', browser)
        cleanup(drv_path)

        path = None
        for k in range(1, 5):
            try:
                if browser == "chrome":
                    path = ChromeDriverManager(path=drv_path).install()
                else:
                    path = GeckoDriverManager(path=drv_path).install()
            except:
                sleep(6)

        if path is None:
            raise Exception("Unable to install driver for '{}'".format(browser))

        os.environ["{}_driver_path".format(browser)] = path


#
# common fixtures
#

# base URL from pytest.ini file
@pytest.fixture(scope="function")
def base_url(request):
    log.debug("Getting base_url from config (fixture)")
    url = request.config.getini("base_url")
    return url


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep
