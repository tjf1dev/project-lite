from login import login
from login import config
from logger import logger


def logout():
    """
    Logs out from Discord by deleting the token from the config file.
    """
    c = config.Load()
    if c:
        c["token"] = None
        config.Save(c)
        logger.info("logged out successfully.")
        login.Login(5)
    else:
        logger.warning("no token found to log out.")
