import requests
import context
from prompt_toolkit.shortcuts import radiolist_dialog
from login.config import ChannelID
from parser import command
from models import Argument
from models import DataType
from logger import logger


@command(
    name="browse",
    aliases=[],
    description="user-friendly channel picker",
    args=[
        Argument(
            datatype=DataType.String,
            name="type",
            required=False,
            description='"server": pick a server, then a channel in it.\n"channel": pick a different channel in the selected server.\n"dm" select from dms.\ndefaults to server',
        )
    ],
)
def browse_cmd(**kwargs):
    _type = kwargs.get("type", "server")
    if _type in ["channel", "c"]:
        if not context.channel_id:
            logger.error("you need to select a channel first. use 'help -c'")
            return
        browse_channels(context.token, context.channel_id)
        return
    if _type in ["dm", "direct"]:
        browse_direct(context.token)
        return
    browse(context.token)
    return


def browse(token):
    headers = {"authorization": f"{token}"}
    response = requests.get(
        "https://discord.com/api/v9/users/@me/guilds", headers=headers
    )
    if response.status_code != 200:
        print(f"failed to fetch guilds. status code: {response.status_code}")
        return None

    guilds = sorted(response.json(), key=lambda g: g["name"], reverse=True)
    guild_choices = [(g["id"], g["name"]) for g in guilds]

    guild_id = radiolist_dialog(
        title="select a server",
        text="use arrow keys to navigate and tab  to confirm or cancel.\nyou can also use your mouse",
        values=guild_choices,
    ).run()

    if guild_id is None:
        return None
    response = requests.get(
        f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=headers
    )
    if response.status_code != 200:
        print(f"failed to fetch channels. status code: {response.status_code}")
        return None
    channels = [c for c in response.json() if c["type"] == 0]  # Only text channels
    channel_choices = [
        (c["id"], c["name"]) for c in sorted(channels, key=lambda c: c["name"])
    ]

    channel_id = radiolist_dialog(
        title=f"select a text channel",
        text="use arrow keys to navigate and tab to confirm or cancel.\nyou can also use your mouse",
        values=channel_choices,
    ).run()

    if channel_id is not None:
        ChannelID.set(channel_id)

    return channel_id


def browse_channels(token, cid):
    channel_id = cid
    headers = {"authorization": f"{token}"}
    url1 = f"https://discord.com/api/v9/channels/{channel_id}"
    req1 = requests.get(url1, headers=headers)
    guild_id = req1.json()["guild_id"]
    url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
    req = requests.get(url, headers=headers)
    channels_raw = req.json()
    channels = []
    for channel in channels_raw:
        if channel["type"] == 0:
            channels.append(channel)
    channel_choices = [
        (c["id"], c["name"]) for c in sorted(channels, key=lambda c: c["name"])
    ]
    channel_id = radiolist_dialog(
        title="select a text channel",
        text="use arrow keys to navigate and tab to confirm or cancel.\nyou can also use your mouse",
        values=channel_choices,
    ).run()
    ChannelID.set(channel_id)
    return channel_id


def browse_direct(token):
    global channelid
    url = "https://discord.com/api/v9/users/@me/channels"
    headers = {"authorization": f"{token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        dms = response.json()

        # Sort DMs by last_message_id (descending: most recent first)
        dms.sort(key=lambda dm: str(dm.get("last_message_id") or "0"), reverse=True)

        dm_choices = []
        for dm in dms:
            if dm["type"] == 1:
                username = dm["recipients"][0]["username"]
                dm_choices.append((dm["id"], username))
            if dm["type"] == 3:
                dm_choices.append(
                    (
                        dm["id"],
                        dm.get("name")
                        if dm.get("name")
                        else "(gc)"
                        + " "
                        + ", ".join(r["username"] for r in dm["recipients"][:3])
                        + "...",
                    )
                )

        dm_id = radiolist_dialog(
            title="select a dm channel",
            text="use arrow keys to navigate and tab and enter to confirm or cancel.\nyou can also use your mouse",
            values=dm_choices,
        ).run()
        try:
            ChannelID.set(dm_id)
            return dm_id
        except KeyboardInterrupt:
            print("fun fact: ctrl+c stops the script.")

    else:
        print(f"failed to fetch dms. status code: {response.status_code}")
