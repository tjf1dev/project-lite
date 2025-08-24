import logging
from colorama import *
import warnings
import functools

# sourced from my other project, codygen (https://github.com/tjf1dev/codygen)

logger = logging.getLogger("project-lite")


class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": Fore.LIGHTBLACK_EX,
        "INFO": Fore.BLUE,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
        "OK": Fore.GREEN,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Fore.WHITE)
        record.module = f"{Fore.LIGHTBLACK_EX}{record.module}{Fore.RESET}"
        record.levelname = f"{log_color}{record.levelname}{Fore.RESET}"
        record.msg = f"{log_color}{record.msg}{Fore.RESET}"
        return super().format(record)


if logger.hasHandlers():
    logger.handlers.clear()
handler = logging.StreamHandler()
logger.addHandler(handler)

logger.setLevel(logging.INFO)
logger.propagate = False


def set_level(num: int = 0):
    if num == 0:  # debug
        logger.setLevel(logging.DEBUG)
        handler.setFormatter(
            ColorFormatter(
                "%(asctime)s %(funcName)s [ %(levelname)s ] %(message)s",
                datefmt="%H:%M:%S",
            )
        )
    if num == 1:
        logger.setLevel(logging.INFO)
        handler.setFormatter(
            ColorFormatter("[ %(levelname)s ] %(message)s", datefmt="%H:%M:%S")
        )
    if num == 2:
        logger.setLevel(logging.CRITICAL)
        handler.setFormatter(
            ColorFormatter("[ %(levelname)s ] %(message)s", datefmt="%H:%M:%S")
        )
    if num == 3:
        handler.setFormatter(
            ColorFormatter("[ %(levelname)s ] %(message)s", datefmt="%H:%M:%S")
        )
    if num == 4:
        handler.setFormatter(
            ColorFormatter(
                "%(asctime)s %(funcName)s [ %(levelname)s ] %(message)s",
                datefmt="%H:%M:%S",
            )
        )


set_level(0)


def deprecated(reason: str = "this function is deprecated."):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            message = f"{func.__name__}() is deprecated: {reason}"
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            logger.warning(message)
            return func(*args, **kwargs)

        return wrapper

    return decorator
