import requests
import climage
from io import BytesIO
from PIL import Image
from logger import logger
from login.config import ChannelID
from functions import get_user, get_profile_picture, validate_channel
from parser import command
import context
from models import Argument
from models import DataType


@command(
    name="about",
    aliases=["me"],
    description="shows information about the logged in user.",
    args=[
        Argument(
            DataType.Flags,
            name="flags",
            description="--img: also render profile picture",
            required=False,
        )
    ],
)
def about(**kwargs) -> None:
    """
    print the information about the user.
    (from arguments) if the image flag is True, it will also display the user's profile picture.
    """
    render_image = False
    flags = kwargs.get("flags", {})
    if flags.get("img"):
        render_image = True
    token = context.token
    channelid = ChannelID.get()
    user = context.user
    if user is None:
        logger.error("unable to get info.")
        pass
    else:
        if render_image:
            logger.debug("rendering profile picture")
            response = requests.get(get_profile_picture(user))
            img = Image.open(BytesIO(response.content))
            print(climage.convert_pil(img, width=50))
        logger.info(f"display name: {user['global_name']}")
        logger.info(f"username: {user['username']}")
        logger.info(f"id: {user['id']}")
        if validate_channel(token, channelid):
            logger.info(f"channel: {channelid}")
        elif channelid in [0, None, "0"]:
            logger.warning("channel not selected.")
        else:
            logger.error(f"invalid channel selected.")
            logger.error(f"please select a valid channel.")
            logger.error(f"you can do it by one of the commands in 'help -c'.")
