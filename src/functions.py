import requests,os,dateutil,climage,time, readchar
from io import BytesIO
from PIL import Image
from login.config import *
import pytz, tzlocal, dateutil.parser, colorama, math
import curses # AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import radiolist_dialog
from logger import logger, deprecated
from login import login
from login import config
@deprecated("Please use get_user() instead. Will be removed in v0.2.4")
def get_discord_user_info(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": f"{token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_user(token) -> dict | None:
    """
        Get user info from Discord API using token.
        Args:
            token (str): Discord token.
        Returns:
            dict: User info from Discord API, None if failed.
    """
    url = "https://discord.com/api/v10/users/@me"
    if not isinstance(token, str):
        logger.error(f"Token is: {type(token).__name__}. It should be a string.")
        logger.info("Hint: Report issues at https://github.com/tjf1dev/project-lite/issues")
        return None
    response = requests.get(url, headers={"Authorization": f"{token}"})
    if not response.ok or response.json().get("code", 1) == 0:
        logger.error(f"Failed to get user. Responded with code: {response.status_code}")
        if response.status_code == 401:
            logger.error("Your token is invalid. Use 'logout' to reauthenticate.")
        return None
    logger.debug("User fetch OK")
    return response.json()
def logout():
    """
        Logs out from Discord by deleting the token from the config file.
    """
    c = config.Load()
    if c:
        c["token"] = None
        config.Save(c)
        logger.info("Logged out successfully.")
        login.Login(5)
    else:
        logger.warning("No token found to log out.")
def validate_token(token: str) -> bool:
    """
        Validates the token. Returns a bool indicating whether the token is valid
    """
    logger.debug("Validating token...")
    if not isinstance(token, str): 
        logger.error(f"Token is: {type(token).__name__}. It should be a string")
        return False
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": f"{token.strip()}"
    }
    response = requests.get(url, headers=headers)
    if not response.ok: 
        logger.error(f"Failed to validate token. Server responded with code {response.status_code}")
    else: logger.debug("Token is ok")
    return response.ok
@deprecated("Please use get_user()['username'] instead. Will be removed in v0.2.4")
def get_discord_username(user_info):
    try:
        if user_info["discriminator"] != "0":
            return f"{user_info['username']}#{user_info['discriminator']}"
        else:
            return f"{user_info['username']}"
    except Exception:
        return None

def get_profile_picture(user) -> str:
    return f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
def get_banner(user) -> str:
    return f"https://cdn.discordapp.com/banners/{user['id']}/{user['banner']}.png"


def clear():
    os.system("cls" if os.name == "nt" else "clear")
def browse(token):
    headers = {"Authorization": f"{token}"}

    # Fetch guilds
    response = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch guilds. Status code: {response.status_code}")
        return None

    guilds = sorted(response.json(), key=lambda g: g["name"], reverse=True)
    guild_choices = [(g["id"], g["name"]) for g in guilds]

    # Select a guild
    guild_id = radiolist_dialog(
        title="Select a server",
        text="Use arrow keys to navigate and TAB  to confirm or cancel.\nYou can also use your mouse",
        values=guild_choices
    ).run()

    if guild_id is None:
        return None  # User canceled

    # Fetch channels in the selected guild
    response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch channels. Status code: {response.status_code}")
        return None
    channels = [c for c in response.json() if c["type"] == 0]  # Only text channels
    channel_choices = [(c["id"], c["name"]) for c in sorted(channels, key=lambda c: c["name"])]

    # Select a channel
    channel_id = radiolist_dialog(
        title=f"Select a text channel",
        text="Use arrow keys to navigate and TAB to confirm or cancel.\nYou can also use your mouse",
        values=channel_choices
    ).run()

    if channel_id is not None:
        ChannelID.set(channel_id)

    return channel_id  # Returns None if canceled
def browse_channel(token, cid):
    channel_id = cid
    headers = {
        "Authorization": f"{token}"
    }
    url1 = f"https://discord.com/api/v9/channels/{channel_id}"
    req1 = requests.get(url1,headers=headers)
    guild_id = req1.json()["guild_id"]
    url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
    req=requests.get(url,headers=headers)
    channels_raw = req.json()
    channels = []
    for channel in channels_raw:
        if channel["type"] == 0:
            channels.append(channel)
    channel_choices = [(c["id"], c["name"]) for c in sorted(channels, key=lambda c: c["name"])]
    channel_id = radiolist_dialog(
            title="Select a text channel",
            text="Use arrow keys to navigate and TAB to confirm or cancel.\nYou can also use your mouse",
            values=channel_choices
        ).run()
    ChannelID.set(channel_id)
    return channel_id
def browse_direct(token):
    global channelid
    url = "https://discord.com/api/v9/users/@me/channels"
    headers = {
        "Authorization": f"{token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        dms = response.json()
        dm_choices = [(c["id"], c["name"]) for c in sorted(dms, key=lambda c: c["name"])]
        dm_id = radiolist_dialog(
            title="Select a server",
            text="Use arrow keys to navigate and TAB and ENTER to confirm or cancel.\nYou can also use your mouse",
            values=dm_choices,
        ).run()
        try:
            ChannelID.set(dm_id)
            return dm_id
        except KeyboardInterrupt:
            print("Fun Fact: Ctrl+C stops the script.")        

    else:
        print(f"Failed to fetch dms. Status code: {response.status_code}")
def send_message(token, cid, content, ):
    if not content:
        return

    url = f"https://discord.com/api/v9/channels/{cid}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "Referer": f"https://discord.com/channels/@me/{cid}"
    }
    data = {
        "content": content
    }
    
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

def fav(token, cid):
    channel = custom_get_request(f"channels/{cid}",token)
    Favorite.add(cid, channel["name"])


def fav_select():
    favorites = Favorite.get()
    if favorites == []:
        print("You don't have any favorite channels. Use fav add in a channel to save it.")
        return
    favorites.append({"id": 10, "name": "Back"})
    fav_names = [fav["name"] for fav in favorites]
    title = "Select a channel with your arrow keys."

    def menu(stdscr):
        curses.curs_set(0)
        stdscr.keypad(True)
        selected = 0

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            title_x = (w // 2) - (len(title) // 2)
            stdscr.addstr(h // 2 - len(fav_names) // 2 - 2, title_x, title, curses.A_BOLD)

            for i, name in enumerate(fav_names):
                text = f"> {name}" if i == selected else f"  {name}"
                x = (w // 2) - (len(text) // 2)
                y = (h // 2) - (len(fav_names) // 2) + i
                stdscr.addstr(y, x, text, curses.A_REVERSE if i == selected else curses.A_NORMAL)

            key = stdscr.getch()

            if key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(fav_names) - 1:
                selected += 1
            elif key in [10, 13]:
                id = favorites[selected]["id"]
                return None if id == 10 else id

    return curses.wrapper(menu)

def get_messages_from_channel(token, cid):
    url = f"https://discord.com/api/v10/channels/{cid}/messages"
    headers = {"Authorization": f"{token}", "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch messages. Status code: {response.status_code}")
        return []
def receive_messages(token, cid):
    messages = get_messages_from_channel(cid, token)
    if not messages:  # More Pythonic check for an empty list
        return

    user_timezone = tzlocal.get_localzone()  # Dynamically fetch system timezone
    for message in reversed(messages):
        timestamp_str = message['timestamp']
        timestamp = dateutil.parser.isoparse(timestamp_str)
        timestamp_user_timezone = timestamp.astimezone(user_timezone)
        readable_timestamp = timestamp_user_timezone.strftime('%H:%M:%S')

        if message["attachments"]:
            if len(message["attachments"]) == 1:
                print(f"[{message['author']['username']} {readable_timestamp}]: {message['content']} [with attachment]")
            else:
                print(f"[{message['author']['username']} {readable_timestamp}]: {message['content']} [with {len(message['attachments'])} attachments]")
        else:
            print(f"[{message['author']['username']} {readable_timestamp}]: {message['content']}")

def send_messages(token, cid):
    while True:
        content = input(f"[{get_discord_username(get_discord_user_info(token))}/{cid} (SEND MODE)]: ")
        if content.lower() == "exit":
            break
        if content == "":
            pass
        send_message(cid, content, token)
def rs(token, cid):
    while True:
        try:
            
                receive_messages(cid, token)
                channel = custom_get_request(f"channels/{cid}", token)
                guildid = channel["guild_id"]
                guild = custom_get_request(f"guilds/{guildid}", token)
                print("\nhint: use /help\nuse Ctrl+C to quit")
                content = input(f"[{channel['name']} in {guild['name']}][RS]: ")

                if content.startswith("/"):
                    if content == "/exit":
                        break
                    if content == "/help":
                        print("You are currently in RS (Read-Send) mode\nTo refresh messages, hit enter with an empty message.\nPlease note that RS mode is unstable.\nCommands available in RS mode:\n/help - displays this message\n/exit - leaves RS mode.")
                        print("press any key to continue")
                        readchar.readkey()
                    else:
                        print(f"invalid command! use /help to get a list of commands.\nwanted to use a slash command instad? {colorama.Style.BRIGHT}slash commands are not available in project-lite yet.{colorama.Style.RESET_ALL}")
                        print("press any key to continue")
                        readchar.readkey()
                else:
                    send_message(token, cid, content)
        except KeyboardInterrupt:
            clear()
            print("\n")
            break
            
def typing(token, cid):
    url = f"https://discord.com/api/v10/channels/{cid}/typing"
    headers = {"Authorization": f"{token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    
    else:
        return []
def custom_get_request(path,token):
    url = f"https://discord.com/api/v9/{path}"
    headers={
        "Authorization":f"{token}"
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logger.debug(f"Requested {response.url} with code {response.status_code}")
        return None
def browse_root():
    print("Use 'browse guild' or 'browse direct' instead of 'browse'.")
def validate_channel(token, cid):
    if not cid.isdigit() or cid in ['0', 0, None]:
        return False
    else:
        c = custom_get_request(f"/channels/{cid}", token)
        if not c:
            return False
    return True
def channel(cid):
    ChannelID.set(cid)
    return cid
def dev(token):
    developers = [978596696156147754]
    
    #* if you know what you're doing, set this flag to True, this will skip the check.
    skip = False
    
    id = get_discord_user_info(token)['id']
    if int(id) in developers or skip:
        logger.info(f"Welcome back, {get_discord_username(get_discord_user_info(token))}")
        logger.debug((get_discord_user_info(token)))
    else:
        logger.error("This command is only available to developers. ")
def about(token: str, img: bool = True, **kwargs) -> None:
    """
        Print the information about the user.
        If the image flag is True, it will also display the user's profile picture.
        Args:
            token (str): Discord token.
            img (bool, optional): Whether to display the user's profile picture. Defaults to True.
    """
    channelid = ChannelID.get()
    user = get_user(token)
    if user is None:
        logger.error("Unable to get info.")
        pass
    else:
        logger.debug("Rendering profile picture")
        response = requests.get(get_profile_picture(user))
        img = Image.open(BytesIO(response.content))
        print(climage.convert_pil(img, width=50))
        logger.info(f"Display Name: {user['global_name']}")
        logger.info(f"Username: {user['username']}")
        logger.info(f"ID: {user['id']}")
        if validate_channel(token, channelid):
            logger.info(f"Channel: {channelid}")
        elif channelid in [0, None, '0']:
            logger.warning("Channel not selected.")
        else:
            logger.error(f"Invalid channel selected.")
            logger.error(f"Please select a valid channel.")
            logger.error(f"You can do it by one of the commands in 'help -c'.")
            
if __name__ == "__main__":
    raise RuntimeError("You should not run this script directly. Use the main script.")