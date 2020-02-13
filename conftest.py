import inspect
import pytest

from src.DriverManager import DriverManager, BrowserOptions


#
# Register cmd-line options
#
def pytest_addoption(parser):
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
                     default="1600x800",
                     help="Run in headless mode (FF, Chrome). Values: yes|no")

#
# configure webdriver based on cmd-line arguments
#
def pytest_configure(config):
    # headless/normal mode
    hdls = config.getoption("headless")
    # window size
    win_size = get_window_size_option(config)
    # browsers to run tests in
    browsers_list = get_browser_option(config)

    browser_opt = BrowserOptions(hdls, win_size)

    # create plugin class
    class Plugin:
        #
        # web driver fixture
        #
        @pytest.fixture(autouse=True, params=browsers_list, scope="function")
        def driver(self, request):
            # prepare webdriver
            browser_type = request.param

            d = DriverManager.get_driver(browser_type)(browser_opt)
            d.implicitly_wait(5)

            # return prepared webdriver
            yield d

            # finalization
            try:
                d.close()
            except:
                if d is not None:
                    d.quit()
                    del d


    # register plugin
    config.pluginmanager.register(Plugin())


# get -B (--browser) cmd-line option and return it as browsers list
def get_browser_option(conf):
    # browsers to run tests in
    browser_option = conf.getoption("browser")

    # if there is no -B option provided, use chrome
    if browser_option is None:
        browser_option = ["chrome"]

    browsers_list = []
    if browser_option == ["all"]:
        return ["chrome", "firefox", "edge"]
    else:
        return browser_option


# get --windows_size cmd-line option and return it as a tuple
def get_window_size_option(conf):
    return size(conf.getoption("window_size"))


# convert string dimension '1234x321' into tuple (1234,321)
def size(wsize):
    sz = wsize.split('x')
    return int(sz[0]), int(sz[1])
