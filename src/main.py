import sys
import os
from login import login,config
from functions import *
from os.path import abspath, dirname
import pytz, tzlocal, dateutil.parser, traceback
os.chdir(dirname(abspath(__file__)))
__version__ = '0.2.2-alpha'
def change_channel_id(cid):
    config.ChannelID.set(cid)
    logger.debug(f"Channel ID changed to {cid}.")
def help_func(flags:str=None):
    print("Available commands:\n")
    commands = Command.list()
    for command in commands:
        command_class = command

        args = "none"
        if len(command_class.args) > 0:
            args = ""
            for a in command_class.args:
                if a["required"]:
                    args += f"<{a['name']}>"
                else:
                    args += f"[{a['name']}]"
        requires_list = []

        if 0 in command_class.require:
            requires_list.append("token")
        if 1 in command_class.require:
            requires_list.append("channel_id")
        requires = ", ".join(requires_list)
        aliases = ", ".join(command_class.syntax[1:]) if len(command_class.syntax) > 1 else "none"
        if command_class.hidden == False:
            if "-c" in flags and not DataType.ChannelID in command_class.returns:
                pass
            else:
                print(f"{command_class.syntax[0]}:\n{command_class.description}\nArguments: {args}\nRequires: {requires}\nAliases: {aliases}\n")
class DataType:
    class ChannelID:
        type = int | str
    class Token:
        type = str
    class Flag:
        type = str
        
class Command:
    """# Command
        ## This class contains definitions for all available commands.\n
        ### Command.list\n
        returns a list of all available commands.\n
        
        ### args\n
        list of arguments.\n

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
    class read:
        args = []
        syntax = ["read"]
        description = "Reads messages from the selected channel."
        usage = syntax[0]
        function = receive_messages
        require = [DataType.Token, DataType.ChannelID]
        returns = []
        hidden = False
    class help:
        args = [
            {
                "type":DataType.Flag,
                "name":"flags",
                "required":False
            }
        ]
        syntax = ["help"]
        description = "Shows information about project-lite and displays all available commands"
        function = help_func
        usage = syntax[0]
        require = []
        returns = []
        hidden = False
    class browse:
        args = []
        syntax = ["browse","browse guild", "guilds", "browse server", "servers"]
        description = "Selects a guild"
        function = browse
        usage = syntax[0]
        require = [DataType.Token]
        returns = [DataType.ChannelID]
        hidden = False
    class browse_direct:
        args = []
        syntax = ["browse direct", "browse dm", "dms"]
        description = "Selects a dm"
        function = browse_direct
        usage = syntax[0]
        require = [DataType.Token]
        returns = [DataType.ChannelID]
        hidden = False
    class browse_channel:
        args = []
        syntax = ["browse channels", "channels"]
        description = "Selects a channel"
        function = browse_channel
        usage = syntax[0]
        require = [DataType.Token,DataType.ChannelID]
        returns = [DataType.ChannelID]
        hidden = False
    class rs_mode:
        args = []
        syntax = ["rs"]
        description = "Starts the Read-Send mode in a selected channel"
        function = rs
        usage = syntax[0]
        require = [DataType.Token, DataType.ChannelID]
        returns = []
        hidden = False
    class fav_add:
        args = []
        syntax = ["fav-add"]
        description = "Adds the current channel to favorites."
        function = fav
        usage = syntax[0]
        require = [DataType.Token, DataType.ChannelID]
        returns = []
        hidden = False
    class fav:
        args = []
        syntax = ["fav"]
        description = "Shows a list of favorite channels."
        function = fav_select
        usage = syntax[0]
        require = []
        returns = [1]
        hidden = False
    class me:
        args = []
        syntax = ["me","about"]
        description = "Shows info about the current logged in user."
        function = about
        usage = syntax[0]
        require = [DataType.Token]
        returns = []
        hidden = False
    class dev:
        args = []
        syntax = ["dev"]
        description = "Opens developer mode."
        function = dev
        usage = syntax[0]
        require = [DataType.Token]
        returns = []
        hidden = True
    class channel:
        args = [
            {
                "type":DataType.ChannelID,
                "name":"channel id",
                "required":True
            }
        ]
        syntax = ["channel","cid","cc"]
        description = "Changes the current channel."
        function = channel
        usage = f"{syntax[0]} {[f"<{a['name']}>" for a in args]}"
        require = []
        returns = [DataType.ChannelID]
        hidden = False
    class logout:
        args = []
        syntax = ["logout","log-out"]
        description = "Logs out the current user."
        function = logout
        require = []
        returns = []
    @staticmethod
    def list():
        command_classes = Command.__dict__.values()
        command_classes = [
            cls for cls in command_classes
            if isinstance(cls, type)
            and not cls.__name__.startswith('__')
        ]
        command_class_names = [cls for cls in command_classes]
        return command_class_names


login.Login()
token = login.token
channelid = None


def main():
    global channelid, token
    
    
    print("project-lite \na cli discord client.\nhint: try running \"help\".")
    try:
        while True:
            channelid = config.ChannelID.get()
            if channelid in [0, None, '0']:
                cmdraw = input("[CMD]: ").lower().strip()
            else:
                channel = custom_get_request(f"channels/{channelid}",token)
                if not channel and not validate_channel(token,channelid):
                    cmdraw = input("[invalid cid, run 'about' for more info][CMD]: ").lower().strip()
                else:
                    guildid = channel["guild_id"]
                    guild = custom_get_request(f"guilds/{guildid}",token)
                    cmdraw = input(f"[{channel["name"]} in {guild["name"]}][CMD]: ").lower().strip()
            cmdfull = cmdraw.split(" ")
            cmdname = cmdfull[0]
            cmdargs = cmdfull[1:]
            cmdlist = Command.list()
            cmdfound = False
            for cmdc in cmdlist:
                if cmdname in cmdc.syntax:
                    cmdfound = True
                    logger.debug(f"Executing command {cmdc.__name__}...")
                    cmdi = cmdc() 
                    args = {}
                    if DataType.Token in cmdi.require:
                        val = validate_token(token)
                        if val!= True:
                            logger.error("Invalid token, please reauthenticate")
                            login.Login(4)
                            break
                        args["token"] = token
                    if DataType.ChannelID in cmdi.require:
                        if channelid in [None, 0]:
                            logger.error("No channel ID selected. Use 'help -c' to select one.")
                            continue
                        args["cid"] = channelid
                    if len(cmdi.args) != 0:
                        # here is the scary part
                        for arg in cmdi.args:
                            try:
                                if arg["type"] == DataType.ChannelID:
                                    args["cid"] = cmdargs[0]
                                elif arg["type"] == DataType.Flag:
                                    args["flags"] = cmdargs[0]
                            except IndexError:
                                if args.get("required", False):
                                    logger.error(f"Missing required argument for {arg['name']}.")
                                    continue
                                else:
                                    args = {}
                    try:
                        #* the actual call
                        logger.debug(f"Arguments that will be passed: {", ".join(args.keys())}")
                        cmdc.function(**args)
                    except TypeError as e:
                        ft = traceback.format_exc()
                        logger.error("An issue occured while trying to execute this command.")
                        logger.error("Please report this issue with the full logs.")
                        logger.error(ft)
                        logger.error(f"{type(e).__name__}: {e}")
                        logger.info(f"Version: {__version__}, Command: {cmdc.__name__}")
                        logger.info("https://github.com/tjf1dev/project-lite/issues")
            if not cmdfound:
                logger.error(f"Command {cmdname} not found. Use 'help' for a list of available commands.")

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt, goodbye!")
if __name__ == '__main__':
    main()