import logging
import logging.config

from os import environ
from datetime import datetime

default_level = logging.INFO
logging.basicConfig(level=default_level)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    DEBUG = '\033[10m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def set_logging_level(level):
    logging.basicConfig(level=(getattr(logging, level.upper(), default_level)))


def get_logging_level(level):
    return getattr(logging, level.upper())


def current_time():
    return datetime.now().strftime("%H:%M:%S")


def log(source, message, level="info"):
    msg = f"[{str(source)}] - {str(message)}"

    if int(environ.get("USE_NATIVE_LOGGER", 0)) == 1:
        if not isinstance(level, int):
            level = getattr(logging, level.upper(), default_level)
        logger = logging.getLogger()
        logger.log(level, msg)
    else:
        if default_level < get_logging_level(level):
            if level == "info":
                color = bcolors.OKGREEN
            elif level == "warning":
                color = bcolors.WARNING
            elif level == "error":
                color = bcolors.FAIL
            elif level == "critical":
                color = bcolors.FAIL
            else:
                color = bcolors.DEBUG
            print("{0}[{1}] ({2}) {3}{4}".format(color, current_time(), source, message, bcolors.ENDC))

