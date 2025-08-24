from typing import Callable, List, Dict, Any


class Command:
    def __init__(
        self,
        name: str,
        aliases: List[str],
        description: str,
        function: Callable,
        args: List[Dict[str, Any]] = None,
        require: List[Any] = None,
        returns: List[Any] = None,
        hidden: bool = False,
        module: str = "",
    ):
        self.name = name
        self.aliases = aliases
        self.description = description
        self.function = function
        self.args = args or []
        self.require = require or []
        self.returns = returns or []
        self.hidden = hidden
        self.module = module

    def usage(self):
        if not self.args:
            return self.aliases[0]
        return f"{self.aliases[0]} " + " ".join(
            f"<{arg['name']}>" if arg.get("required", True) else f"[{arg['name']}]"
            for arg in self.args
        )


class DataType:
    class ChannelID:
        """
        current channel id if in 'require'
        can also be used as an argument
        """

        type = int | str
        arg = 2

    class Token:
        """
        token of currently logged in account
        cannot be used as an argument
        """

        type = str
        arg = 0

    class String:
        """
        regular string that does not contain spaces
        example: "hello"
        example: "world!"
        """

        type = str
        arg = 1

    class WildString:
        """
        string that can contain spaces
        always use it as the last argument
        example: "hello world!"
        """

        type = str
        arg = 1

    class Flags:
        type = dict


class Argument:
    def __init__(
        self,
        datatype: DataType,
        name: str,
        required: bool = True,
        description: str = "",
    ):
        self.datatype = datatype
        self.name = name
        self.required = required
        self.description = description

    def __repr__(self):
        return f"Argument(name={self.name!r}, type={self.datatype.__name__}, required={self.required})"
