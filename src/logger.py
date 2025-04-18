import logging
from colorama import *
import warnings
import functools
# sourced from my other project, codygen (https://github.com/tjf1dev/codygen)
logger = logging.getLogger("project-lite")
class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.LIGHTBLACK_EX,
        'INFO': Fore.BLUE,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA,
        'OK': Fore.GREEN
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
handler.setFormatter(ColorFormatter(
    '%(asctime)s %(module)s [ %(levelname)s ] %(message)s',
    datefmt='%H:%M:%S'
))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.propagate = False
def deprecated(reason: str = "This function is deprecated."):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            message = f"{func.__name__}() is deprecated: {reason}"
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            logger.warning(message)
            return func(*args, **kwargs)
        return wrapper
    return decorator