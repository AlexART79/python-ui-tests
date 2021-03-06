import base64
from enum import Enum

from src.utils.test_logger import TestLog

log = TestLog()

class Browser(Enum):
    chrome = 1
    firefox = 2
    edge = 3
    safari = 4
    opera = 5

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __str__(self):
        return self.name

    def __hash__(self):
        encoded = base64.b64encode(self.name.encode('ascii'))

        check_sum = 0
        for code in encoded:
            check_sum = check_sum + code

        check_sum = check_sum * self.value

        log.debug("Generating hash for '{}' --> {}".format(self.name, check_sum))

        return check_sum


class Platform(Enum):
    Windows = 1
    Darwin = 2
    Linux = 3

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __str__(self):
        return self.name


class BrowserOptions:
    def __init__(self):
        self.browser_type = None
        self.headless = False
        self.window_size = None
        self.timeout = 15
        self.use_browserstack = False
        self.use_selenoid = False
        self.hub_url = ''

    def __str__(self):
        wsize = "None" if self.window_size is None else "{}x{}".format(self.window_size[0], self.window_size[1])
        env = "local driver"
        if self.use_browserstack:
            env = "BrowserStack"
        elif self.use_selenoid:
            env = "Selenoid"

        return "{} (Run with {}) (window_size: {}, headless: {}, wait_timeout: {})".format(
            self.browser_type,
            env,
            wsize,
            self.headless,
            self.timeout)
