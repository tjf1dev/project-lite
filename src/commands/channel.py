from login.config import ChannelID
from parser import command
from models import DataType
from models import Argument
from logger import logger
from functions import validate_channel
import context
from colorama import Fore
from functions import custom_get_request, get_user


@command(
    name="channel",
    aliases=["cid", "c", "pwd"],
    description="set a channel from id or name/view the current channel.",
    args=[
        Argument(
            DataType.WildString,
            name="query",
            required=False,
            description="the channel name or id to search for",
        )
    ],
)
def channel(**kwargs):
    cid = kwargs["query"]
    user = context.user
    if not cid:
        if not context.channel_id:
            logger.warning("no channel selected")
            return
        else:
            ch = validate_channel(context.token, context.channel_id).json()
            if ch["type"] == 0:
                guildid = ch.get("guild_id")
                guild = custom_get_request(f"guilds/{guildid}", context.token).json()
                print(
                    f"channel: {Fore.BLUE}{ch['name']}{Fore.RESET} {Fore.LIGHTBLACK_EX}({ch['id']}){Fore.RESET}\nserver: {Fore.BLUE}{guild['name']}{Fore.RESET} {Fore.LIGHTBLACK_EX}({guild['id']}){Fore.RESET}"
                )
            elif ch["type"] == 1:
                print(
                    f"dm: with {Fore.BLUE}{ch['recipients'][0]['username']}{Fore.RESET} {Fore.LIGHTBLACK_EX}({ch['id']}){Fore.RESET}"
                )
            elif ch["type"] == 3:
                print(
                    f"group chat: with {Fore.BLUE}{len(ch['recipients']) + 1}{Fore.RESET} people:\n"
                )
                print(f"- {Fore.BLUE}{user['username']}{Fore.RESET}")
                for r in ch["recipients"]:
                    print(f"- {Fore.BLUE}{r['username']}{Fore.RESET}")
    else:
        if str(cid) == "0":
            cid = None
        ChannelID.set(cid)
        logger.info(f"channel set to {cid}")
        return cid
