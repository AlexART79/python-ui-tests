import os
import allure
import pytest

from src.DriverManager.DriverManager import DriverManager
from src.DriverManager.support import BrowserOptions, Browser
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
    DriverManager.download_drivers()

    # create plugin class
    class DriverPlugin:
        #
        # web driver fixture
        #
        @pytest.fixture(autouse=True, params=browsers_list, scope="function")
        def driver(self, request):
            browser_type = request.param
            log.debug("Create 'driver' fixture for {}".format(browser_type))

            d = DriverManager.get_driver(Browser[browser_type], browser_opt)

            yield d

            if request.node.rep_call.failed:
                log.error("Test '{}' failed!".format(request.function.__name__))
                try:
                    allure.attach(d.get_screenshot_as_png(), name='screenshot on fail',
                                  attachment_type=allure.attachment_type.PNG)
                except:
                    pass  # just ignore

            # finalization
            d.close()
            log.debug("'driver' fixture finalized")

    # register plugin
    config.pluginmanager.register(DriverPlugin())


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
