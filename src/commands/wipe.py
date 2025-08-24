from parser import command
from models import DataType
from models import Argument
from logger import logger
import login
import login.config
import readchar


@command(
    name="wipe",
    description="clears the configuration.",
    args=[
        Argument(
            DataType.Flags,
            name="flags",
            description="--nologout: doesn't log out after finished.",
        )
    ],
)
def wipe(**kwargs):
    flags = kwargs.get("flags", {})
    logger.info("(y/N) are you sure you want to wipe the config?")
    key = readchar.readkey().lower()
    if key == "y":
        login.config.Wipe()
        if flags.get("nologout"):
            login.Login(5)
    else:
        logger.warning("cancelled.")
