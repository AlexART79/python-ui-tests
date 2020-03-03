import os
import allure
import pytest

from src.driver_manager.support import BrowserOptions, Browser
from src.driver_manager.driver_factory import BsDriverFactory, SelenoidDriverFactory, LocalDriverFactory
from src.utils.helpers import Helpers, str2bool
from src.utils.test_logger import TestLog


log = TestLog()


class TestConfig:
    def __init__(self, config):
        # set log level
        os.environ["LOG_LEVEL"] = self.tests_log_level = config.getini("tests_log_level")

        self.headless = config.getoption("headless")
        self.win_size = Helpers.get_window_size_option(config)
        self.browsers_list = Helpers.get_browser_option(config)
        self.timeout = config.getini("default_wait_timeout")
        self.base_url = config.getini("base_url")

        # use selenoid
        self.use_selenoid = str2bool(config.getini("use_selenoid"))
        # use browserstack
        self.use_browserstack = False if self.use_selenoid else str2bool(config.getini("use_browserstack"))
        # remote hub url
        self.hub_url = config.getini("hub_url")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


def pytest_addoption(parser):

    """ Register cmd-line options and ini file options """

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
    parser.addini('default_wait_timeout', 'default timeout value for implicitly wait', default=15)
    parser.addini('headless', 'Run tests in headless mode', default=False)
    parser.addini('window_size', 'Browser window size', default='1920x1080')

    parser.addini('use_browserstack', 'Run tests in browserstack', default="False")
    parser.addini('use_selenoid', 'Run tests in selenoid', default="False")
    parser.addini('hub_url', 'Remote hub URL', default='http://localhost:4444/wd/hub')


def pytest_configure(config):

    """ configure webdriver based on cmd-line arguments """

    # load config (ini and cmd-line)
    test_config = TestConfig(config)
    TestLog.configure()

    log.debug("pytest_configure")

    # download drivers (if using Local drivers)
    if not (test_config.use_browserstack or test_config.use_selenoid):
        LocalDriverFactory.download_drivers(test_config.browsers_list)

    class DriverPlugin:

        """ Driver plugin class """

        @pytest.fixture(autouse=True, params=test_config.browsers_list, scope="function")
        def driver(self, request):

            """ web driver fixture """

            # init browser options
            options = BrowserOptions()

            options.browser_type = Browser[request.param]
            options.headless = test_config.headless
            options.window_size = test_config.win_size
            options.timeout = test_config.timeout
            options.use_browserstack = test_config.use_browserstack
            options.use_selenoid = test_config.use_selenoid
            options.hub_url = test_config.hub_url

            log.debug("Create 'driver' fixture: {}".format(options))

            # get webdriver instance
            if options.use_browserstack:
                d = BsDriverFactory.get_driver(options)
            elif options.use_selenoid:
                d = SelenoidDriverFactory.get_driver(options)
            else:
                d = LocalDriverFactory.get_driver(options)

            yield d

            try:
                if request.node.rep_call.failed:
                    log.error("Test '{}' failed!".format(request.function.__name__))
                    try:
                        allure.attach(d.get_screenshot_as_png(), name='screenshot on fail',
                                      attachment_type=allure.attachment_type.PNG)
                    except:
                        log.warn("Unable to attch screenshot to allure report")
                        pass
            finally:
                # finalization
                d.quit()
                log.debug("'driver' fixture finalized")

    # register plugin
    config.pluginmanager.register(DriverPlugin())


#
# common fixtures
#

@pytest.fixture(scope="function")
def base_url(request):

    """ base URL from pytest.ini file """

    log.debug("Getting base_url from config (fixture)")
    url = request.config.getini("base_url")
    return url
