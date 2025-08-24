COMMANDS = {}
from models import DataType


def list_commands(include_hidden=False):
    return [cmd for cmd in COMMANDS.values() if not cmd.hidden or include_hidden]
