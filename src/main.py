import sys
import os
from login import login,config
from functions import *
from os.path import abspath, dirname
import pytz, tzlocal, dateutil.parser
os.chdir(dirname(abspath(__file__)))
__version__ = '0.2.0-alpha'
def change_channel_id(cid):
    config.ChannelID.set(cid)
    print(f"Channel ID changed to {cid}.")
def help_func():
    print("Available commands:\n")
    commands = Command.list()
    for command in commands:
        command_class = getattr(Command, command)

        args = "none"
        if command_class.args > 0:
            args = str(command_class.args)
        requires_list = []

        if 0 in command_class.require:
            requires_list.append("token")
        if 1 in command_class.require:
            requires_list.append("channel_id")
        requires = ", ".join(requires_list)
        aliases = ", ".join(command_class.syntax[1:]) if len(command_class.syntax) > 1 else "none"
        if command_class.hidden == False:
            print(f"{command_class.syntax[0]}:\n{command_class.description}\nArguments: {args}\nRequires: {requires}\nAliases: {aliases}\n")
        
class Command:
    """# Command
        ## This class contains definitions for all available commands.\n
        ### Command.list\n
        returns a list of all available commands.\n
        
        ### args\n
        argument count.\n

        ### syntax\n
        the command syntax (used to trigger the command)\n

        ### function\n
        the function getting called\n

        ### require\n
        required values for the command\n
        0 - token\n
        1 - channel id\n

        ### returns\n
        what does the command return\n
        1 - channel id"""
    def list():
        command_names = []
        for key in dir(Command):  # Iterate over attributes of Commands
            attr = getattr(Command, key)
            if hasattr(attr, 'args') and isinstance(attr.args, int):
                command_names.append(key)
        return command_names
    class read:
        args = 0
        syntax = ["read"]
        description = "Reads messages from the selected channel."
        usage = syntax[0]
        function = receive_messages
        require = [0, 1]
        returns = []
        hidden = False
    class help:
        args = 0
        syntax = ["help"]
        description = "Shows information about project-lite and displays all available commands"
        function = help_func
        usage = syntax[0]
        require = []
        returns = []
        hidden = False
    class browse:
        args = 0
        syntax = ["browse","browse guild", "guilds"]
        description = "Selects a guild"
        function = browse
        usage = syntax[0]
        require = [0]
        returns = [1]
        hidden = False
    class browse_direct:
        args = 0
        syntax = ["browse direct", "browse dm", "dms"]
        description = "Selects a dm"
        function = browse_direct
        usage = syntax[0]
        require = [0]
        returns = [1]
        hidden = False
    class browse_channel:
        args = 0
        syntax = ["browse channels", "channels"]
        description = "Selects a channel"
        function = browse_channel
        usage = syntax[0]
        require = [0,1]
        returns = [1]
        hidden = False
    class rs_mode:
        args = 0
        syntax = ["rs"]
        description = "Starts the Read-Send mode in a selected channel"
        function = rs
        usage = syntax[0]
        require = [0, 1]
        returns = []
        hidden = False
    class fav_add:
        args = 0
        syntax = ["fav add"]
        description = "Adds the current channel to favorites."
        function = fav
        usage = syntax[0]
        require = [0,1]
        returns = []
        hidden = False
    class fav:
        args = 0
        syntax = ["fav"]
        description = "Shows a list of favorite channels."
        function = fav_select
        usage = syntax[0]
        require = []
        returns = [1]
        hidden = False
    class me:
        args = 0
        syntax = ["me","about"]
        description = "Shows info about the current logged in user."
        function = about
        usage = syntax[0]
        require = [0]
        returns = []
        hidden = False
    class dev:
        args = 0
        syntax = ["dev"]
        description = "Opens developer mode."
        function = dev
        usage = syntax[0]
        require = [0]
        returns = []
        hidden = True
    class channel:
        args = 1
        syntax = ["channel","cid","cc"]
        description = "Changes the current channel."
        function = channel
        usage = f"{syntax[0]} <channel id>"
        require = []
        returns = [1]
        hidden = False
login.Login()
token = login.token
if get_discord_user_info(token) is None:
    print("Failed to authenticate. Please check your token.")
    exit()
channelid = None


def main():
    global channelid, token
    
    
    print("project-lite \na cli discord client.\nhint: try running \"help\".")

    try:
        while True:
            channelid = config.ChannelID.get()
            channel_id = channelid
            if channelid == 0 or channelid== None:
                command_raw = input(": ").lower().strip()
            else:
                channel = custom_get_request(f"channels/{channelid}",token)
                guildid = channel["guild_id"]
                guild = custom_get_request(f"guilds/{guildid}",token)
                command_raw = input(f"[{channel["name"]} in {guild["name"]}][CMD]: ").lower().strip()
            command_list = Command.list()
            command_name = None
            command_class = None

            for command in command_list:
                cls = getattr(Command, command)
                if command_raw in cls.syntax:
                    command_name = command
                    command_class = cls
                    break

            if command_class:
                requires = command_class.require
                args = command_class.args
                if args == 0:
                    if requires == []:
                        command_class.function()
                    
                    elif requires == [0]:
                        command_class.function(token)
                    
                    elif requires == [1]:
                        if channel_id == 0:
                            print(f"Error: This command requires a valid channel ID.")
                        else:
                            command_class.function(channelid)
                    elif requires == [0, 1]:
                        if channel_id == 0 or channelid == None:
                            print(f"Error: This command requires a valid channel ID.")
                        else:
                            result = command_class.function(channelid, token)

                            if command_class.returns == [1]:
                                change_channel_id(result)
            else:
                print(f"Unknown command: {command_raw}. Type 'help' for a list of available commands.")

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt, goodbye!")
if __name__ == '__main__':
    main()