import base64
from enum import Enum


class Browser(Enum):
    chrome = 1
    firefox = 2
    edge = 3
    safari = 3

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
    def __init__(self, browser_type=None, headless=False, window_size=None, timeout=10):
        self.browser_type = browser_type
        self.headless = headless
        self.window_size = window_size
        self.timeout = timeout

    def __str__(self):
        wsize = "None" if self.window_size is None else "{}x{}".format(self.window_size[0], self.window_size[1])

        return "{} (window_size: {}, headless: {}, wait_timeout: {})".format(
            self.browser_type,
            wsize,
            self.headless,
            self.timeout)
