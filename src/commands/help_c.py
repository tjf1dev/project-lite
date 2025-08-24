from registry import list_commands
from parser import command
from models import DataType
from models import Argument
from models import Command
from logger import logger
from colorama import Fore


@command(
    name="help",
    aliases=[],
    description="displays available commands",
    args=[
        Argument(
            datatype=DataType.String,
            name="command",
            required=False,
            description="the command to show",
        ),
        Argument(
            datatype=DataType.Flags,
            name="flags",
            required=False,
            description="-c: only show commands that change the channel",
        ),
    ],
)
def help_c(**kwargs):
    flags = kwargs.get("flags", {})
    commands = list_commands(True)
    command_wanted = kwargs.get("command")
    commands_text = []
    for command in commands:
        c: Command = command

        args = f"{Fore.LIGHTBLACK_EX}none{Fore.RESET}"
        if len(c.args) > 0:
            args = []
            for a in c.args:
                a: Argument
                rt = "" if a.required else f"(optional) "
                args.append(
                    f"{Fore.LIGHTBLACK_EX}{rt}{a.name}:\n{a.description}{Fore.RESET}"
                )
            args = "\n".join(args)
        aliases = ", ".join(c.aliases) if len(c.aliases) > 0 else "none"

        if c.hidden == False:
            show = True

            if command_wanted and command_wanted not in c.aliases:
                show = False
            if flags.get("c", None) and not DataType.ChannelID in c.returns:
                show = False
            if show:
                commands_text.append(
                    f"{c.name}: {Fore.LIGHTBLACK_EX}{c.description}{Fore.RESET}\narguments:{'\n' if args != f'{Fore.LIGHTBLACK_EX}none{Fore.RESET}' else ' '}{args}\naliases: {Fore.LIGHTBLACK_EX}{aliases}{Fore.RESET}\n{f'extension: {Fore.LIGHTBLACK_EX}{c.module}{Fore.RESET}' if not c.module.startswith('commands') else ''}\n"
                )
    print("available commands:\n")
    print("\n".join(commands_text))
