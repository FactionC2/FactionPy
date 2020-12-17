import os
import inspect
import logging
from typing import Dict, Union

import sys
from datetime import datetime


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


def current_time():
    return datetime.now().strftime("%H:%M:%S")


FACTION_LOGGING_LEVEL = os.environ.get("FACTION_LOGGING_LEVEL", "info")

logging_level = logging.INFO
if FACTION_LOGGING_LEVEL.lower() == "warning":
    logging_level = logging.WARNING
elif FACTION_LOGGING_LEVEL.lower() == "error":
    logging_level = logging.ERROR
elif FACTION_LOGGING_LEVEL.lower() == "critical":
    logging_level = logging.CRITICAL
elif FACTION_LOGGING_LEVEL.lower() == "debug":
    logging_level = logging.DEBUG


logger = logging.getLogger("factionpy")
logger.setLevel(logging_level)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def log(message: str, level="info"):
    """
    Takes a string and prints it to stdout all fancy.

    :param message: The message you want printed.
    :param level: The severity of the message (info, warning, error, critical, debug)
    :return: None
    """
    # get calling function name
    source = inspect.stack()[1].function
    formatted_message = f"({source}) {message}"
    if level.lower() == "info":
        logger.info(f"{bcolors.OKGREEN}{formatted_message}{bcolors.ENDC}")
    elif level.lower() == "warning":
        logger.warning(f"{bcolors.WARNING}{formatted_message}{bcolors.ENDC}")
    elif level.lower() == "error":
        logger.error(f"{bcolors.FAIL}{formatted_message}{bcolors.ENDC}")
    elif level.lower() == "critical":
        logger.critical(f"{bcolors.FAIL}{formatted_message}{bcolors.ENDC}")
    elif level.lower() == "debug":
        logger.debug(f"{bcolors.OKBLUE}{formatted_message}{bcolors.ENDC}")
    else:
        logger.error(f"{bcolors.FAIL}(log) Log called with invalid level: {level}. Valid levels are: info, warning, "
                     f"error, critical, and debug.{bcolors.ENDC}")


def error_out(message: str) -> Dict[str, Union[str, bool]]:
    log(message, "error")
    return {
        "success": False,
        "message": message
    }

