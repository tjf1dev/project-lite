import os
from login import login, config
from functions import *
from os.path import abspath, dirname
import commands
from registry import COMMANDS
import argparse
from logger import set_level, logger
import context
from ext.color import Color as c

# if disabled, add verbose and qquiet arguments.
# if enabled, add quiet and qquiet arguments.
is_debug_base = True
parser = argparse.ArgumentParser(
    description="project-lite",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
if is_debug_base:
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="disable debug logging"
    )
else:
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable debug logging"
    )
parser.add_argument("-qq", "--qquiet", action="store_true", help="disable all logging")
parser.add_argument(
    "--no-welcome", action="store_true", help="don't show welcome message"
)
parser.add_argument("--show-input", action="store_true", help="show token input fields")
parser.add_argument("--logout", action="store_true", help="force login")
parser.add_argument(
    "--logout-conf", action="store_true", help="remove token from config"
)
parser.add_argument(
    "--no-expand-logs",
    action="store_true",
    help="dont show timestamp and function on debug logs",
)
parser.add_argument("-k", type=str, help="run a command and keep running")
parser.add_argument("-c", type=str, help="run a command and stop")
args = parser.parse_args()
if is_debug_base:
    if args.quiet:
        set_level(1)
    elif args.qquiet:
        set_level(2)
    else:
        set_level(0)
else:
    if args.verbose:
        set_level(0)
    elif args.qquiet:
        set_level(2)
    else:
        set_level(1)
if args.no_expand_logs:
    set_level(3)
logger.debug(f"loaded {len(COMMANDS.keys())} commands.")
from models import DataType

os.chdir(dirname(abspath(__file__)))
__version__ = "0.2.3-alpha"


def change_channel_id(cid):
    config.ChannelID.set(cid)
    logger.debug(f"Channel ID changed to {cid}.")


channelid = None
EXTENSIONS_PATH = os.path.join(os.path.dirname(__file__), "..", "extensions")
EXTENSIONS_PATH = os.path.abspath(EXTENSIONS_PATH)


def run_command(cmdraw: str):
    cmdfull = cmdraw.strip().split()
    if not cmdfull:
        return

    cmdname = cmdfull[0]
    cmdargs = cmdfull[1:]

    command_obj = None
    for cmd in COMMANDS.values():
        if cmdname == cmd.name or cmdname in cmd.aliases:
            command_obj = cmd
            break

    if not command_obj:
        logger.error(f"unknown command: {cmdname}")
        return

    logger.debug(f"executing command `{command_obj.name}`")

    from parser import parse_flags

    try:
        args = {}
        expected_args = command_obj.args or []
        flags_arg_def = next(
            (a for a in expected_args if a.datatype is DataType.Flags), None
        )
        if flags_arg_def:
            non_flag_args = []
            flag_like_args = []

            for arg in cmdargs:
                if arg.startswith("-"):
                    flag_like_args.append(arg)
                else:
                    non_flag_args.append(arg)

            flags_dict = parse_flags(" ".join(flag_like_args))
            args[flags_arg_def.name] = flags_dict

            expected_args = [a for a in expected_args if a != flags_arg_def]
            cmdargs = non_flag_args
        else:
            cmdargs = cmdargs

        arg_index = 0
        for expected in expected_args:
            arg_name = expected.name
            arg_type = expected.datatype

            if arg_type is DataType.WildString:
                if arg_index < len(cmdargs):
                    args[arg_name] = " ".join(cmdargs[arg_index:])
                elif expected.required:
                    logger.error(f"missing required argument: {arg_name}")
                    return
                else:
                    args[arg_name] = ""
                break

            else:
                if arg_index >= len(cmdargs):
                    if expected.required:
                        logger.error(f"missing required argument: {arg_name}")
                        return
                    else:
                        args[arg_name] = None  # TODO add defaults maybe
                        continue

                try:
                    args[arg_name] = arg_type.type(cmdargs[arg_index])
                except Exception:
                    logger.error(
                        f"Invalid type for argument `{arg_name}`: expected {arg_type.type}"
                    )
                    return

                arg_index += 1

        logger.debug(
            f"arguments that will be passed: {', '.join(f'{k}={v}' for k, v in args.items())}"
        ) if args.keys else None

        command_obj.function(**args)

    except Exception:
        import traceback

        logger.error("An issue occurred while trying to execute this command.")
        logger.error("Please report this issue with the full logs.")
        logger.error(traceback.format_exc())
        logger.info(f"Version: {__version__}, Command: {command_obj.name}")
        logger.info("https://github.com/tjf1dev/project-lite/issues")


import cmd


import cmd


class CLI(cmd.Cmd):
    intro = f'project-lite \n{c.white_1}a cli discord client.\nhint: try running "help".{c.reset}'
    prompt = "$ "

    def __init__(self, token, args, config, logger):
        super().__init__()
        self.token = token
        self.args = args
        self.config = config
        self.logger = logger
        self.channelid = None
        self.user = get_user(token)
        if not args.no_welcome:
            self.logger.info(f"welcome, {self.user['username']}")

        # If args.k or args.c is set, execute those commands once then exit or continue
        if self.args.k:
            self.onecmd(self.args.k)
        if self.args.c:
            self.onecmd(self.args.c)
            exit()

    def preloop(self):
        """Called before the cmd loop starts."""
        self.channelid = self.config.ChannelID.get()
        self.prompt = self.get_prompt()
        context.user = self.user

    def get_prompt(self):
        """Build dynamic prompt depending on channel and guild info"""
        # TODO extensions; change prompt
        channelid = self.config.ChannelID.get()  # ← always get the latest
        self.channelid = channelid  # ← update internal reference too

        if not channelid:
            return f"{c.white_1}~$ {c.white}"

        channel = custom_get_request(f"channels/{channelid}", self.token).json()
        if not channel or not validate_channel(self.token, channelid):
            return (
                f"{c.white_4}[run {c.white_3}'c'{c.white_4}]\n{c.white_2}~${c.white} "
            )

        guildid = channel.get("guild_id")
        if guildid:
            guild = custom_get_request(f"guilds/{guildid}", self.token).json()
            return f"{c.white_2}[{c.white_1}{channel['name']}{c.white_2} in {guild['name']}{c.white_2}]{c.white_1}~${c.white} "
        else:
            if channel["type"] == 1:
                return f"{c.white_2}[dms with {c.white_1}{channel['recipients'][0]['username']}{c.white_2}]{c.white_1}~${c.white}{c.reset} "
            elif channel["type"] == 3:
                return f"[gc with {len(channel['recipients']) + 1} people]\n~$ "
            else:
                return "$ "

    def postcmd(self, stop, line):
        """Called after a command is executed. Update the prompt dynamically."""
        self.prompt = self.get_prompt()
        return stop

    def default(self, line):
        """Fallback for commands that aren't defined, call your run_command"""
        run_command(line)

    def do_exit(self, arg):
        """Exit the CLI."""
        self.logger.info("exiting...")
        return True

    def do_EOF(self, arg):
        """Handle Ctrl-D / EOF to exit."""
        print()
        return self.do_exit(arg)

    def do_help(self, arg):
        if arg:
            run_command(f"help {arg}")
        else:
            run_command("help")

    def emptyline(self):
        pass


def main():
    commands.load_extensions()
    cli = CLI(token, args, config, logger)
    cli.prompt = cli.get_prompt()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    token = login.Login(5 if args.logout else -1, args.show_input)
    main()
