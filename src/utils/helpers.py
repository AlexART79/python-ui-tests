import functools
from datetime import datetime
from time import sleep


class Helpers:

    @staticmethod
    def print(str):
        now = datetime.now()
        print("{} - {}".format(now.strftime("%d.%m.%Y %H:%M:%S"), str))


    @staticmethod
    def wait_for(cond, timeout, delay):
        itr = int(timeout/delay)
        for i in range(1, itr):
            if cond():
                return True
            else:
                sleep(delay)

        return False


    # get -B (--browser) cmd-line option and return it as browsers list
    @staticmethod
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
    @staticmethod
    def get_window_size_option(conf):
        opt = conf.getoption("window_size")

        if opt is None or opt == '':
            return None

        return Helpers.size(conf.getoption("window_size"))


    # convert string dimension '1234x321' into tuple (1234,321)
    @staticmethod
    def size(wsize):
        sz = wsize.split('x')
        return int(sz[0]), int(sz[1])


def cached(age=5):
    """
    Caching call result for desired amount of time (in minutes)
    :param age: age of cache
    :return:
    """
    def wrapper(func):
        cache = {}

        # clear cache
        def clear():
            Helpers.print("Clear cache called")
            cache.clear()

        @functools.wraps(func)
        def internal(*args, **kwargs):
            key = args + tuple(sorted(kwargs.items()))
            cache_data_valid = True

            if key not in cache:
                cache_data_valid = False

                d = {}
                d["res"] = func(*args, **kwargs)
                d["last_used"] = datetime.now()

                cache[key] = d
                Helpers.print("New cache entry created: {}".format(key))

            else:
                # check if we need to refresh cached value
                time_diff = datetime.now() - cache[key]["last_used"]

                if time_diff.total_seconds() >= age*60:
                    cache_data_valid = False

                    cache[key]["res"] = func(*args, **kwargs)
                    cache[key]["last_used"] = datetime.now()

                    Helpers.print("Cache entry updated: {}".format(key))

            if cache_data_valid:
                Helpers.print("Found valid entry in cache: {}".format(key))

            return cache[key]["res"]

        internal.clear = clear

        return internal

    return wrapper
