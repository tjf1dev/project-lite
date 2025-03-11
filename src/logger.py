import logging
from colorama import Fore
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
        record.levelname = f"{log_color}{record.levelname}{Fore.RESET}"
        record.msg = f"{log_color}{record.msg}{Fore.RESET}"
        return super().format(record)
# AHHH FUCK YOU
if logger.hasHandlers():
    logger.handlers.clear()
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter(
    '%(asctime)s [ %(levelname)s ] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.propagate = False