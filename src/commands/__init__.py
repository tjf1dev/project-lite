#! make sure to actually put the commands here
# im gonna forget about this am i
from . import (
    about,
    browse,
    channel,
    chat,
    help_c,
    dev,
    fav_select,
    fav,
    logout,
    read,
    send_mode,
    pfp,
    clear,
    exit_c,
    projectlite,
    wipe,
    ext,
)
import os
import sys
import importlib.util
from logger import logger

EXTENSIONS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "extensions")
)


def load_extensions():
    logger.debug("loading extensons...")
    extensions = []
    if not os.path.isdir(EXTENSIONS_PATH):
        return
    else:
        logger.debug(f"found directory: {EXTENSIONS_PATH}")
    for filename in os.listdir(EXTENSIONS_PATH):
        if filename.endswith(".py") and not filename.startswith(("__", "-")):
            path = os.path.join(EXTENSIONS_PATH, filename)
            module_name = f"ext_{filename[:-3]}"
            extensions.append(module_name)
            logger.debug(f"loading extension {module_name}")

            try:
                spec = importlib.util.spec_from_file_location(module_name, path)
                if spec is None or spec.loader is None:
                    logger.error(f"cannot load spec for {module_name}")
                    continue

                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                logger.debug(f"{module_name}: extension loaded.")

            except Exception as e:
                logger.error(f"failed to load extension {module_name}: {e}")
    logger.debug(f"finished loading extensions. {len(extensions)} found.")
