from login import config
from functions import *
from logger import logger, deprecated
from getpass import getpass
import context

# logger.debug("starting... welcome!")

# DEBUG MODE
# please use this only you know what you are doing.
# * makes all token input fields visible.
debug = False

from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError


def Login(type: int = -1, debug: bool = False, after_fail: bool = False) -> str:
    """
    Logs into project-lite.
    Prompts the user to input their token and initial settings, and stores them in a file

    ## Parameters
    ### `type`
    Determines the type of login.\n
    -1 - Automatically determine type. Default\n
    0 - Normal login (not first time, on startup)\n
    1 - First time login (on startup)\n
    2 - After fail login (replaces after_fail)\n
    3 - Fail, unknown cause\n
    4 - Fail after crash\n
    5 - Manual log out
    ### `after_fail`
    **Deprecated, use `type=2` instead. Will be removed in v0.2.4**\n
    Determines if the login should be performed after an authentication failure
    """
    logger.info("logging in...")
    conf = config.Load()
    token = conf.get("token", "").strip()
    val = validate_token(token)
    if type == -1:
        if val:
            type = 0
        elif conf == config.Default.Get():
            type = 1
        if not val and conf != config.Default.Get():
            type = 3
    if not val or type in [5]:
        while True:
            if type in [0]:
                logger.info("Welcome back!")
                logger.warning(
                    "The token you had saved is invalid. Please reauthenticate"
                )
                logger.info("Enter your Discord token:")
            elif type in [1]:
                logger.info("Welcome to project-lite.")
                logger.info("To start, enter your Discord token:")
                logger.info(
                    "Don't know what your token is? https://github.com/tjf1dev/project-lite#how-do-i-get-my-token"
                )
            elif type in [2] or after_fail:
                logger.debug("restarting after auth failure")
                logger.info("Invalid token entered, try again:")
            elif type in [3]:
                logger.warning("Last authentication attempt failed.")
                logger.info("Enter your Discord token:")
            elif type in [4]:
                logger.warning(
                    "The token you had saved is invalid. Please reauthenticate"
                )
                logger.info("Enter your Discord token:")
            elif type in [5]:
                logger.info("Logged out successfully.")
                logger.info("Enter your Discord token:")
            if debug:
                token = input("(visible) > ")
            else:
                token = prompt("> ", is_password=True, mouse_support=True)
            logger.debug(f"checking {token}")
            val = validate_token(token)
            if val:
                break
    context.token = token
    config.Save({"token": token})  # if the token is valid save it
    return token
