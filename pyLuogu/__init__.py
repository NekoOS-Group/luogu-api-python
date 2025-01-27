import logging
import typing

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[97m',  # White
        'INFO': '\033[94m',   # Blue
        'WARNING': '\033[93m',  # Orange
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[91m'  # Red
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.msg = f"{log_color}{record.msg}{self.RESET}"
        return super().format(record)

logger = logging.getLogger("LuoguAPI")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = ColoredFormatter('[%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def set_log_level(level: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]):
    level_dict = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    logger.setLevel(level_dict.get(level, logging.WARNING))

set_log_level("WARNING")

from .api import luoguAPI
from .async_api import asyncLuoguAPI
from .static_api import staticLuoguAPI, luogu
from .types import *