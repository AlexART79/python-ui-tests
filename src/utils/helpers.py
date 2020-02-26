import functools
import inspect
from datetime import datetime
from time import sleep
from src.utils.test_logger import Level, TestLog


log = TestLog()
log.set_level(Level.DEBUG)


class Helpers:
    @staticmethod
    def print(text: str) -> None:
        now = datetime.now()
        print("{} - {}".format(now.strftime("%d.%m.%Y %H:%M:%S"), text))

    @staticmethod
    def wait_for(cond, timeout: int, delay: int) -> bool:
        """
        wait for certain condition
        :param cond: function or bool expression
        :param timeout: in secods
        :param delay: in seconds
        :return: boolean, true if condition was satisfied in desired amount of time; otherwise - false
        """

        fn = None
        if type(cond) == type(True):
            fn = lambda: cond # wrap boolean condition with function
        else:
            fn = cond

        itr = int(timeout / delay)
        for i in range(1, itr):
            log.debug("*")
            if fn():
                return True
            else:
                sleep(delay)

        return False

    # get -B (--browser) cmd-line option and return it as browsers list
    @staticmethod
    def get_browser_option(conf) -> list:
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


def cached(age = 5):
    """
    Caching call result for desired amount of time (in minutes)
    :param age: age of cache
    :return:
    """
    def fullname(o):
        def get_attr(name: str) -> str:
            info = inspect.getmembers(o)
            for i,k in info:
                if i == name:
                    return k

            raise Exception("Attribute {} not found".format(name))

        return "{}.{}".format(get_attr("__module__"), get_attr("__qualname__"))

    def wrapper(func):
        cache = {}

        # clear cache
        def clear():
            log.debug("Clear cache called")
            cache.clear()

        @functools.wraps(func)
        def internal(*args, **kwargs):
            key = "{}{}".format(fullname(func), args + tuple(sorted(kwargs.items())))
            cache_data_valid = True

            if key not in cache:
                cache_data_valid = False

                d = {}
                d["res"] = func(*args, **kwargs)
                d["last_used"] = datetime.now()

                cache[key] = d
                log.debug("New cache entry created: {}".format(key))

            else:
                # check if we need to refresh cached value
                time_diff = datetime.now() - cache[key]["last_used"]

                if time_diff.total_seconds() >= age * 60:
                    cache_data_valid = False

                    cache[key]["res"] = func(*args, **kwargs)
                    cache[key]["last_used"] = datetime.now()

                    log.debug("Cache entry updated: {}".format(key))

            if cache_data_valid:
                log.debug("Found valid entry in cache: {}".format(key))

            return cache[key]["res"]

        internal.clear = clear

        return internal

    return wrapper
