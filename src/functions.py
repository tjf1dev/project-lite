import requests,os,dateutil,climage,time
from io import BytesIO
from PIL import Image
from login.config import *
import pytz, tzlocal, dateutil.parser, colorama, math
import curses # AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import radiolist_dialog
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
def validate_token(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": f"{token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False
def get_discord_username(user_info):
    try:
        if user_info["discriminator"] != "0":
            return f"{user_info['username']}#{user_info['discriminator']}"
        else:
            return f"{user_info['username']}"
    except Exception:
        return None
def get_profile_picture_url(user_info):
    return f"https://cdn.discordapp.com/avatars/{user_info['id']}/{user_info['avatar']}.png"
def get_banner_url(user_info):
    return f"https://cdn.discordapp.com/banners/{user_info['id']}/{user_info['banner']}.png"



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
def browse_channel(channel_id, token):
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
def send_message(channel_id, content, token):
    if not content:
        return

    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "Referer": f"https://discord.com/channels/@me/{channel_id}"
    }
    data = {
        "content": content,
        "tts": False
    }
    
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

def fav(channelid, token):
    channel = custom_get_request(f"channels/{channelid}",token)
    Favorite.add(channelid,channel["name"])


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

def get_messages_from_channel(channel_id, token):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {"Authorization": f"{token}", "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch messages. Status code: {response.status_code}")
        return []
def receive_messages(channel_id, token):
    messages = get_messages_from_channel(channel_id, token)
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

def send_messages(channel_id, token):
    while True:
        content = input(f"[{get_discord_username(get_discord_user_info(token))}/{channel_id} (SEND MODE)]: ")
        if content.lower() == "exit":
            break
        if content == "":
            pass
        send_message(channel_id, content, token)
def rs(channelid, token):
    print("test")
    while True:
        receive_messages(channelid,token)
        channel = custom_get_request(f"channels/{channelid}",token)
        guildid = channel["guild_id"]
        guild = custom_get_request(f"guilds/{guildid}",token)
        print("\nhint: use /help")
        content = input(f"[{channel['name']} in {guild['name']}][RS]: ")
        if content == "/exit":
            break
        if content == "/help":
            print("You are currently in RS (Read-Send) mode\nTo refresh messages, hit enter with an empty message.\nPlease note that RS mode is unstable.\nCommands available in RS mode:\n/help - displays this message\n/exit - leaves RS mode.")
            input("Press enter to continue")
        else:
            send_message(channelid,content,token)
def typing(channelid, token):
    url = f"https://discord.com/api/v10/channels/{channelid}/typing"
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
        print(f"Requested {response.url} with code {response.status_code}")
        return None
def browse_root():
    print("Use 'browse guild' or 'browse direct' instead of 'browse'.")
def channel(cid):
    return cid
def dev(token):
    developers = [978596696156147754]
    id = get_discord_user_info(token)['id']
    if int(id) in developers:
        print(f"Welcome back, {get_discord_username(get_discord_user_info(token))}")
        print((get_discord_user_info(token)))
    else:
        print("This command is only available to developers. ")
def about(token):
    channelid = ChannelID.get()
    user_info = get_discord_user_info(token)
    if user_info is None:
        print("Unable to get info.")
        pass
    else:

        response = requests.get(get_profile_picture_url(user_info))
        img = Image.open(BytesIO(response.content))
        print(climage.convert_pil(img))
        time.sleep(1)
        print(f"Display Name: {user_info['global_name']}")
        print(f"Username: {get_discord_username(user_info)}")
        print(f"ID: {user_info['id']}")
        try:
            print(f"Selected channel: {channelid}")
        except NameError:
            print(f"No channel selected.")
if __name__ == "__main__":
    raise RuntimeError("You should not run this script directly. Use the main script.")