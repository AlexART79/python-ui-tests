import pytest
from src.DriverManager import DriverManager, BrowserOptions
from src.utils.helpers import Helpers


@pytest.hookimpl()
def pytest_sessionstart(session):
    Helpers.print("pytest_sessionstart")

#
# Register cmd-line options and ini file options
#
def pytest_addoption(parser):
    Helpers.print("pytest_addoption")

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
    parser.addini('base_url', 'base AUT url')
    parser.addini('default_wait_timeout', 'default timeout value for implicitly wait', default=5)


#
# configure webdriver based on cmd-line arguments
#
def pytest_configure(config):
    Helpers.print("pytest_configure")

    # headless/normal mode
    hdls = config.getoption("headless")
    # window size
    win_size = Helpers.get_window_size_option(config)
    # browsers to run tests in
    browsers_list = Helpers.get_browser_option(config)

    # default timeout for implicitly wait from pytest.ini
    timeout = config.getini("default_wait_timeout")

    browser_opt = BrowserOptions(hdls, win_size)

    # create plugin class
    class DriverPlugin:
        #
        # web driver fixture
        #
        @pytest.fixture(autouse=True, params=browsers_list, scope="function")
        def driver(self, request):
            # prepare webdriver
            browser_type = request.param

            Helpers.print("Create 'driver' fixture for {}".format(browser_type))

            d = DriverManager.get_driver(browser_type)(browser_opt)
            d.implicitly_wait(timeout)

            # return prepared webdriver
            yield d

            # finalization
            try:
                d.close()
            except:
                if d is not None:
                    d.quit()
                    del d

            Helpers.print("'driver' fixture finalized")

    # register plugin
    config.pluginmanager.register(DriverPlugin())

#
# common fixtures
#

# base URL from pytest.ini file
@pytest.fixture(scope="function")
def base_url(request):
    Helpers.print("Getting base_url from config (fixture)")
    url = request.config.getini("base_url")
    return url
