
from enum import Enum

class Warninglevels(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRIT_ERROR = 4


grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"

def format(string : str, level : Warninglevels = Warninglevels.CRIT_ERROR) -> str:
    if level == Warninglevels.DEBUG:
        return grey + "[DEBUG]: " + string + reset
    elif level == Warninglevels.INFO:
        return grey + "[INFO]: " + string + reset
    elif level == Warninglevels.WARNING:
        return yellow + "[WARNING]: " + string + reset 
    elif level == Warninglevels.ERROR:
        return red + "[ERROR]: " + string + reset
    elif level == Warninglevels.CRIT_ERROR:
        return bold_red + "[CRITICAL ERROR]: " + string + reset
    else:
        raise ValueError("Invalid warning level")