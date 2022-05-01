# Standard libs
from enum import Enum

# Local Imports
import config


class Warninglevels(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRIT_ERROR = 4


ShowDebug = config.SHOWDEBUG

grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"

def notify(string : str, level : Warninglevels = Warninglevels.CRIT_ERROR) -> None:
    if level == Warninglevels.DEBUG:
        if ShowDebug:
            print(grey + "[DEBUG]: " + string + reset)
    elif level == Warninglevels.INFO:
        print(grey + "[INFO]: " + string + reset)
    elif level == Warninglevels.WARNING:
        print(yellow + "[WARNING]: " + string + reset) 
    elif level == Warninglevels.ERROR:
        print(red + "[ERROR]: " + string + reset)
    elif level == Warninglevels.CRIT_ERROR:
        print(bold_red + "[CRITICAL ERROR]: " + string + reset)
    else:
        raise ValueError("Invalid warning level")