import functools
import inspect
from datetime import datetime
from time import sleep
from .test_logger import TestLog


log = TestLog()


class Helpers:

    @staticmethod
    def wait_for(cond, timeout: int, delay: int, title = None) -> bool:
        """
        wait for certain condition
        :param cond: function or bool expression
        :param timeout: in secods
        :param delay: in seconds
        :return: boolean, true if condition was satisfied in desired amount of time; otherwise - false
        """

        if title is not None:
            log.debug(title)

        fn = None
        if type(cond) == type(True):
            fn = lambda: cond # wrap boolean condition with function
        else:
            fn = cond

        itr = int(timeout / delay)
        for i in range(1, itr):
            log.trace("*")
            if fn():
                return True
            else:
                sleep(delay)

        return False

    # get -B (--browser) cmd-line option and return it as browsers list
    @staticmethod
    def get_browsers(browser_option) -> list:
        # if there is no -B option provided, use chrome
        if browser_option is None:
            browser_option = ["chrome"]

        if browser_option == ["all"]:
            return ["chrome", "firefox", "edge", "safari", "opera"]
        else:
            return browser_option

    # get --windows_size cmd-line option and return it as a tuple
    @staticmethod
    def get_window_size_option(conf) -> tuple or None:
        opt = conf.getoption("window_size")

        if opt is None or opt == '':
            return None

        return Helpers.size(conf.getoption("window_size"))

    # convert string dimension '1234x321' into tuple (1234,321)
    @staticmethod
    def size(wsize: str) -> tuple:
        sz = wsize.split('x')
        return int(sz[0]), int(sz[1])


def str2bool(val: str) -> bool:
    # validate argument type
    if not type(val) == type(''):
        raise TypeError("Type of value thould be 'bool', but '{}' was passed".format(type(val)))

    # return boolean value
    return val.lower() in ['true', 't', 'yes', 'y', '1']
