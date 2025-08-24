from logger import logger
from functions import get_discord_user_info, get_discord_username
from parser import command
from models import DataType
from models import Argument
import context


@command(
    name="dev",
    description="developer options for testing purposes",
    hidden=True,
    args=[Argument(DataType.WildString, name="content", required=False)],
)
def dev(**kwargs):
    token = context.user
    logger.debug(token)
