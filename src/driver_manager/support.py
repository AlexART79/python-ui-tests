from enum import Enum


class Browser(Enum):
    chrome = 1
    firefox = 2
    edge = 3
    safari = 3

    def __str__(self):
        return self.name


class BrowserOptions:
    def __init__(self, hdls, wsize, timeout):
        self.headless = hdls
        self.winsize = wsize
        self.timeout = timeout


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
