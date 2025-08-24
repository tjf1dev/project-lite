from parser import command
from functions import get_messages_from_channel
from logger import logger
import dateutil
import context
import tzlocal
import models
import sys
import importlib
from registry import COMMANDS
import os
from collections import defaultdict

import sys
import os
import importlib
from logger import logger

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
extensions_path = os.path.join(project_root, "extensions")

if extensions_path not in sys.path:
    sys.path.insert(0, extensions_path)


def reload_extensions(name: str = None):
    base_dir = extensions_path
    prefix = "ext_"

    def should_reload(file):
        return (
            file.endswith(".py")
            and file.startswith(prefix)
            and not file.startswith("__")
        )

    for filename in os.listdir(base_dir):
        if not should_reload(filename):
            continue

        module_short = filename[:-3]  # remove .py
        if name and module_short != f"{prefix}{name}":
            continue
        logger.debug(f"reloading: {module_short}")
        if module_short in sys.modules:
            try:
                importlib.reload(sys.modules[module_short])
                logger.debug(f"reloaded: {module_short}")
            except Exception as e:
                logger.debug(f"failed to reload {module_short}: {e}")
        else:
            try:
                importlib.import_module(module_short)
                logger.debug(f"loaded: {module_short}")
            except Exception as e:
                logger.debug(f"failed to load {module_short}: {e}")


def list_extensions():
    grouped = defaultdict(list)

    for name, command_obj in COMMANDS.items():
        mod = getattr(command_obj.function, "__module__", "unknown")
        # collapse full module paths like "commands.ping" → "ping"
        if mod.startswith("commands."):
            mod = mod.split(".", 1)[1]
        grouped[mod].append(name)

    for mod in sorted(grouped):
        logger.info(f"{mod}: {', '.join(sorted(grouped[mod]))}")


@command(
    name="ext",
    description="Manage extensions",
    args=[
        models.Argument(
            datatype=models.DataType.String,
            name="subcommand",
            required=True,
            description="reload: refreshes extensions | list: shows commands per module",
        ),
        models.Argument(
            datatype=models.DataType.WildString,
            name="extension",
            required=False,
            description="defaults to all",
        ),
    ],
)
def ext(**kwargs):
    subcommand = kwargs.get("subcommand")
    module = kwargs.get("extension")

    if subcommand == "reload":
        reload_extensions(module)
    elif subcommand == "list":
        list_extensions()
    else:
        logger.error(f"Unknown subcommand: {subcommand}")
