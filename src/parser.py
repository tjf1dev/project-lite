from typing import Callable, List, Dict, Any
from registry import COMMANDS
from models import Argument
from models import DataType
from models import Command
from logger import logger


def command(
    *,
    name: str,
    aliases: List[str] = [],
    description: str,
    args: List[Argument] = None,
    returns: List[Any] = None,
    hidden: bool = False,
):
    def wrapper(func: Callable):
        if args:
            for i, arg in enumerate(args):
                if isinstance(arg.datatype, DataType.WildString) and i != len(args) - 1:
                    raise ValueError(
                        f"wildstring argument '{arg.name}' must be the last in the list."
                    )
            flags_count = sum(1 for a in args if isinstance(a.datatype, DataType.Flags))
            if flags_count > 1:
                raise ValueError("only one flags argument is allowed per command.")
            for arg in args:
                if isinstance(arg.datatype, DataType.Token):
                    raise ValueError(
                        f"token is not a valid command-line argument: {arg.name}"
                    )
        cmd = Command(
            name=name,
            aliases=aliases,
            description=description,
            function=func,
            args=args,
            returns=returns,
            hidden=hidden,
            module=func.__module__,
        )
        COMMANDS[name] = cmd
        return func

    return wrapper


def parse_flags(arg_string: str) -> dict:
    flags = {}
    args = [arg for arg in arg_string.strip().split(" ") if arg]
    for arg in args:
        if arg.startswith("--"):
            if "=" in arg:
                key, val = arg[2:].split("=", 1)
                flags[key] = val
            else:
                flags[arg[2:]] = True
        elif arg.startswith("-") and len(arg) > 1:
            for c in arg[1:]:
                flags[c] = True
    return flags
