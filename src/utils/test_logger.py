import inspect
import os
from datetime import datetime
from enum import Enum


class Level(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4

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


class TestLog:

    level = Level.INFO

    @staticmethod
    def get_log_level() -> Level:
        lvl = os.getenv("LOG_LEVEL")
        if lvl is None:
            return Level.INFO

        return Level[lvl]

    def __init__(self):
        frame = inspect.currentframe().f_back
        self.module = frame.f_locals["__name__"]

    @staticmethod
    def configure():
        TestLog.level = TestLog.get_log_level()

    @staticmethod
    def set_level(level: Level):
        TestLog.level = level

    def __print(self, text:str, lvl: Level):
        if TestLog.level > lvl:
            return

        now = datetime.now()
        print("{}: {} - {} - {}".format(lvl, now.strftime("%d.%m.%Y %H:%M:%S"), self.module, text))

    def trace(self, text: str):
        self.__print(text, Level.TRACE)

    def debug(self, text: str):
        self.__print(text, Level.DEBUG)

    def info(self, text: str):
        self.__print(text, Level.INFO)

    def warn(self, text: str):
        self.__print(text, Level.WARN)

    def error(self, text: str):
        self.__print(text, Level.ERROR)
