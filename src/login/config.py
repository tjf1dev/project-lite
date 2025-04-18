import json, os
from typing import List, Type
from logger import logger
class Default(object):
    """ Default configuration """
    def __init__(self) -> None:
        """
            The actual config. Remember to update this every time it changes!
        """
        self.token = ""
        self.saving = 1
        self.channelid = 0
        self.favorites = []
        
    def Get() -> dict:
        """
            Returns the default configuration as a dict.
        """
        return Default.__dict__
    def JSON() -> str:
        """
            Returns the default configuration as a JSON string.
        """
        return json.dumps(Default.Get(), indent=4)
def Load() -> dict:
    """
        Returns the current configuration file as a dict. If not found, returns the default configuration.
    """
    try:
        with open("..\\config.json", "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logger.warning("could not find config file, creating one now...")
        Save(Default().Get())
    except json.JSONDecodeError:
        return Default.Get()

def Save(config) -> None:
    """
        Save (merge) the configuration file.
    """
    config_path = "..\\config.json"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            try:
                existing_config = json.load(f)
            except json.JSONDecodeError:
                existing_config = {}
    else:
        existing_config = {}
    # making this was painful
    def deep_update(d, u):
        for k, v in u.items():
            if isinstance(v, dict) and isinstance(d.get(k), dict):
                deep_update(d[k], v)
            else:
                d[k] = v


    deep_update(existing_config, config)
    with open(config_path, "w") as f:
        json.dump(existing_config, f, indent=4)
        
class Favorite():
    """
        Class for managing favorite channels.
    """
    def add(cid,cname) -> None:
        """
            Add a new channel to favorites.
        """
        with open("..\\config.json", "r") as f:
            data = json.load(f)
            if "favorites" not in data:
                data["favorites"] = []
            if cid not in data["favorites"]:
                data["favorites"].append(
                    {
                        "id":cid,
                        "name":cname
                    }
                    )
                Save(data)
    def get() -> List[dict]:
        """
            Returns all favorite channels as a list or dicts
        """
        try:
            with open("..\\config.json", "r") as f:
                data = json.load(f)
                return data["favorites"]
        except KeyError:
            return []
        
class ChannelID():
    """
        Class for managing the stored current channel
    """
    def get() -> int:
        """
            Returns the current channel ID stored in the config.json file.
        """
        try:
            with open("..\\config.json", "r") as f:
                data = json.load(f)
                return data["channelid"]
        except KeyError:
            return 0
    def set(cid) -> None:
        """
            Sets the current channel ID in the config.json file.
        """
        with open("..\\config.json", "r") as f:
            data = json.load(f)
            data["channelid"] = cid
            Save(data)

def Wipe() -> Type[Default]:
    """
        Replaces the configuration with the default. Returns the default configuration.
    """
    with open("..\\config.json", "w") as f:
        f.writelines(Default.Get())
        return Default.Get()

Config = Load()
token = Config["token"]
saving = Config["saving"]


if __name__ == "__main__":
    raise RuntimeError("You should not run this script directly. Use the main script.")