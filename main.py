import os
import json
import requests
from getpass import getpass
from io import BytesIO
from PIL import Image
import time
import climage,platform,webbrowser
if platform.system() == "Windows":
    clearcmd = "cls"
else:
    clearcmd = "clear"
if not os.path.exists("config.json"):
    f = open("config.json", "x")
# Global variables
logged_in=False
channelid = 0
config = {}
__version__ = "0.1.0"
__versioncode__ = 10    
os.system(clearcmd)
print(f"""PROJECT_LITE {__version__}\nKNOWN ISSUES FOR THIS VERSION:\n- Username displaying as None\n- Config sometimes not saved
""")
time.sleep(1)
# Function to load configuration from config.json
def load_config():
    global token,saving
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        config = {
            "token": "",
            "saving": "",
            "favorites":{
                "channels":{

                }
            }
        }
    token = config['token']
    return config
config = load_config()
# Function to save configuration to config.json
def save_config(config):
    if config['saving'] == 0:
        save_config_no_save()
    else:
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
def save_config_no_save():
    config_no_save = {
        "token":"",
        "saving":0
    }
    with open('config.json','w') as f:
        json.dump(config_no_save,f,indent=4)

# Function to wipe configuration (logout)
def wipe_config():
    with open("config.json", "w") as f:
        f.writelines("")
def token_recovery():
    os.system(clearcmd)
    print("PROJECT_LITE - TOKEN RECOVERY\nOPTIONS:\n1 - WIPE CONFIG\n2 - GET HELP")
    recoveryinput = int(input("SELECT OPTION >> "))
    if recoveryinput not in [1,2]:
        print("INVALID OPTION, ABORTING...")
        token_recovery()
    elif recoveryinput == 1:
        wipe_config()
        print("CONFIG WIPED.")
        time.sleep(1)
        os.system(clearcmd)
        login()
    elif recoveryinput ==2:
        webbrowser.open("https://github.com/tjf1dev/project-lite/blob/14d73f69806b6639951044f1b68cb8d4f70b7373/help.md", new=0, autoraise=True)

def gettoken():
    token = input("DON'T KNOW YOUR TOKEN?\nPRESS ENTER FOR RECOVERY OPTIONS\nENTER YOUR TOKEN >> ")
    if token == "":
        token_recovery()
    return token

# Function for user login
def login():
    global config,token,username
    config = load_config()

    saving = config['saving']

    token = config['token']
    if saving == 0:
        token = gettoken()
    if saving == 1:
        main()
    elif saving != 0 and saving !=1:
        saves = input("ENABLE SAVING DATA? (stored in config.json)\nY/n >> ")
        if saves in [None, "", "Y", "y"]:
            saving = 1
        else:
            saving = 0
        if saving == 0:
            token = gettoken()
        else:
            token = gettoken()

    config = {
        "token": "",
        "saving": "",
        "favorites":{
            "channels":{

            }
        }
    }
    logged_in=True
    save_config(config)
    username=get_discord_username(get_discord_user_info(token))
    main()
    
# Function to fetch username from user info
def get_discord_username(user_info):
    if logged_in == False:
        pass
    else:
        if user_info["discriminator"] != "0":
            return f"{user_info['username']}#{user_info['discriminator']}"
        else:
            return f"{user_info['username']}"
# Function to fetch user info from Discord API
def get_discord_user_info(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": f"{token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"FATAL ERROR: get_discord_user_info() FAILED.\n\nYour token is invalid.\nRequest failed with OK: {response.ok}\nStatus code: {response.status_code}\n\n")
        return None



# Function to fetch profile picture URL from user info
def get_profile_picture_url(user_info):
    if logged_in == False:
        pass
    else:
        return f"https://cdn.discordapp.com/avatars/{user_info['id']}/{user_info['avatar']}.png"
def showpfp(url):
    if logged_in == False:
        pass
    else:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        con = climage.convert_pil(img)
        return con
# Function to list guilds
def list_guilds(token):
    global channelid
    url = "https://discord.com/api/v9/users/@me/guilds"
    headers = {
        "Authorization": f"{token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        guilds = response.json()
        print(f"GUILDS ({len(guilds)}):")
        for guild in guilds:
            print(f"- {guild['name']} (ID: {guild['id']})")
        guild_id = input("Select guild ID to list channels: ")
        list_guild_channels(guild_id, token)
    else:
        print(f"Failed to fetch guilds. Status code: {response.status_code}")

# Function to list channels of a guild
def list_guild_channels(guild_id, token):
    global channelid
    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        channels = response.json()
        print(f"CHANNELS OF GUILD ID: {guild_id}")
        for channel in channels:
            print(f"- {channel['name']} (ID: {channel['id']})")
        channel_id = input("Select channel ID: ")
        channelid = channel_id
    else:
        print(f"Failed to fetch channels. Status code: {response.status_code}")

# Function to send message to a channel
def send_message(channel_id, content, token):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json"
    }
    data = {
        "content": content
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}")
    elif response.status_code == 403:
        print(f"You don't have permissions to message this channel")
# Leave guild
def leave_guild(guild_id,token:str):
    url = f"https://discord.com/api/v9/users/@me/guilds/{guild_id}"
    headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code==200:
        print(f"Successfully left {guild_id}!")
    if response.status_code != 200:
        print(f"Failed to leave server. Status code: {response.status_code}")
    elif response.status_code == 403:
        print(f"You don't have permissions to message this channel")    

# Function to change user status
def change_status(status, content, token):
    url = f"https://discord.com/api/v10/users/@me/settings"
    headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json"
    }
    data = {}
    if status and content:
        data = {
            "custom_status": {
                "text": f"{content}"
            },
            "status": status
        }
    elif status:
        data = {
            "status": status
        }
    elif content:
        data = {
            "custom_status": {
                "text": f"{content}"
            }
        }
    
    else:
        print("Please provide status or content.")
        return

    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Status updated successfully")
    else:
        print(f"Failed to update status. Status code: {response.status_code}")



# Function to display help information
def show_help():
    help_info = {
        "exit": "Exit the program",
        "browse": "User friendly copy & paste ID browser",
        "msg <channel_id> <message_content>": "Send a message to a channel",
        "os <command>": "Execute a command in the operating system shell",
        "channel": "Change current channel ID",
        "status": "Change user status",
        "help": "Show this help message",
        "leave": "Leave a guild",
        "send": "Switches to messaging mode",
        "about": "Shows the information about you and the client"
    }
    print("Available commands:")
    for cmd, description in help_info.items():
        print(f"- {cmd}: {description}")

# Function to display main CLI interface
def main():
    global channelid,token,username
    username = get_discord_username(get_discord_user_info(token))
    showpfp(get_profile_picture_url(get_discord_user_info(token)))
    
    user_info = get_discord_user_info(token)
    
    if not user_info:
        print("Failed to fetch user info. Check your token.")
        return

    print(f"Logged in as {username}")
    time.sleep(0.5)
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Logged in as {username}")
    print("Type 'exit' to quit.")

    while True:
        cmd = input(f"[{username}/{channelid} (CMD MODE)]~/ ")

        if cmd == "exit":
            print("Logging out...")
            time.sleep(0.5)
            break

        elif cmd == "browse":
            list_guilds(token)
        elif cmd =="wipe":
            sure = input("This will wipe your config. Are you sure? (y/N) > ")
            if sure in ["y","Y"]:
                wipe_config()
                print("Config is cahced, will remove on exit")
            else:
                pass
        elif cmd.startswith("msg"):
            try:
                parts = cmd.split()
                if len(parts) < 3:
                    raise ValueError("Invalid format. Use 'msg <channel_id> <message_content>'")
                channel_id = parts[1]
                message_content = " ".join(parts[2:])
                send_message(channel_id, message_content, token)
            except Exception as e:
                print(f"Error: {str(e)}")

        elif cmd.startswith("os"):
            try:
                user_input = cmd[3:]
                return_code = os.system(user_input)
                if return_code != 0:
                    print(f"Command '{user_input}' failed with return code {return_code}.")
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt: Exiting the CLI...")
                break
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        elif cmd.startswith("mode"):
            parts = cmd.split()
            if len(parts)<1:
                print("Invalid mode! Supported modes: SEND")
            mode = parts[1]
            if mode.lower == "send":
                print("Enter Channel ID")
                channelid = input(">> ")
                print("Enabled SEND mode. Type 'exit' to leave.")
                while True:
                    msg = input(f"[{username}/{channelid}]")
                    send_message(channel_id,msg,token)
                    if msg == "exit":
                        break

        elif cmd == "status":
            current_status = input("Status (online, dnd, idle, invisible) / exit to cancel >> ")
            custom_status = input("Activity text >> ")
            change_status(current_status, custom_status, token)

        elif cmd == "help":
            show_help()
        elif cmd == "leave":
            gid = input("Guild ID >> ")
            leave_guild(gid,token)
        elif cmd == "send":
            if channelid == 0:
                print("Select a Channel ID using 'browse' or 'channel id' first.")
            else:
                content=input(f"[{username}/{channelid}]: ")
                send_message(channelid,content,token)
        elif cmd == "channel id":
            channelid = input("Channel ID >> ")
        elif cmd == "about":
            userinfo = get_discord_user_info(token)
            print("\n\nNOT SHOWING PERSONAL INFO (email,phone)\nTYPE 'about personal' TO SHOW THESE VALUES\n\n\n")
            print(f"Welcome, {get_discord_username(user_info)}\nYour profile:\bUsername: {userinfo["username"]}\nGlobal Name: {userinfo["global_name"]}\n\nBio:\n{userinfo["bio"]}\n\nRunning project_lite {__version__} ({__versioncode__})")
        elif cmd == "about personal":
            userinfo = get_discord_user_info(token)
            print(f"PERSONAL INFO:\nPHONE: {userinfo['phone']}\nEMAIL: {userinfo['email']}")
        else:
            print("Invalid command.")


login()
