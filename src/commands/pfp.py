from parser import command
from models import Argument
from models import DataType
from logger import logger
from functions import get_profile_picture, get_user
from io import BytesIO
from PIL import Image
import climage
import requests
import context


@command(
    name="pfp",
    aliases=["avatar", "pic"],
    description="prints your pfp in pixel art",
    args=[
        Argument(
            datatype=DataType.Flags,
            name="flags",
            required=False,
            description="--res=[number]: resolution of the image.",
        )
    ],
)
def pfp(**kwargs):
    user = context.user
    logger.debug("rendering profile picture")
    response = requests.get(get_profile_picture(user))
    img = Image.open(BytesIO(response.content))
    print(climage.convert_pil(img, width=int(kwargs.get("flags", {}).get("res", 50))))
