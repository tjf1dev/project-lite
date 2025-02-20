import json, os
def Load():
    try:
        with open("..\\config.json", "r") as f:
            config = json.load(f)
        return config
    except (json.JSONDecodeError, FileNotFoundError):
        return {"token": "", "saving": 0}

def Save(config):
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
    def add(cid,cname):
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
    def get():
        try:
            with open("..\\config.json", "r") as f:
                data = json.load(f)
                return data["favorites"]
        except KeyError:
            return []
class ChannelID():
    def get():
        try:
            with open("..\\config.json", "r") as f:
                data = json.load(f)
                return data["channelid"]
        except KeyError:
            return 0
    def set(cid):
        with open("..\\config.json", "r") as f:
            data = json.load(f)
            data["channelid"] = cid
            Save(data)

def Wipe():
    with open("..\\config.json", "w") as f:
        f.writelines("")
Config = Load()
token = Config["token"]
saving = Config["saving"]


if __name__ == "__main__":
    raise RuntimeError("You should not run this script directly. Use the main script.")