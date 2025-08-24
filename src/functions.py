from logger import logger, deprecated
import requests
import os
import tzlocal
import dateutil


@deprecated("please use get_user()['username'] instead. will be removed in v0.2.4")
def get_discord_username(user_info):
    try:
        if user_info["discriminator"] != "0":
            return f"{user_info['username']}#{user_info['discriminator']}"
        else:
            return f"{user_info['username']}"
    except Exception:
        return None


@deprecated("please use get_user() instead. will be removed in v0.2.4")
def get_discord_user_info(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {"authorization": f"{token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_user(token) -> dict | None:
    """
    Get user info from Discord API using token.
    Args:
        token (str): Discord token.
    Returns:
        dict: User info from Discord API, None if failed.
    """
    url = "https://discord.com/api/v10/users/@me"
    if not isinstance(token, str):
        logger.error(f"token is: {type(token).__name__}. it should be a string.")
        logger.info(
            "hint: report issues at https://github.com/tjf1dev/project-lite/issues"
        )
        return None
    response = requests.get(url, headers={"authorization": f"{token}"})
    if not response.ok or response.json().get("code", 1) == 0:
        logger.error(f"failed to get user. responded with code: {response.status_code}")
        if response.status_code == 401:
            logger.error("your token is invalid. use 'logout' to reauthenticate.")
        return None
    logger.debug("user fetch ok")
    return response.json()


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def typing(token, cid):
    url = f"https://discord.com/api/v10/channels/{cid}/typing"
    headers = {"authorization": f"{token}", "content-type": "application/json"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(response.json())
        return response.json()

    else:
        return []


def get_messages(token, cid):
    messages = get_messages_from_channel(cid, token)
    if not messages:  # More Pythonic check for an empty list
        return

    user_timezone = tzlocal.get_localzone()  # Dynamically fetch system timezone
    for message in reversed(messages):
        timestamp_str = message["timestamp"]
        timestamp = dateutil.parser.isoparse(timestamp_str)
        timestamp_user_timezone = timestamp.astimezone(user_timezone)
        readable_timestamp = timestamp_user_timezone.strftime("%m/%d/%Y %H:%M:%S")

        if message["attachments"]:
            if len(message["attachments"]) == 1:
                print(
                    f"[{message['author']['username']} {readable_timestamp}]: {message['content']} [with attachment]"
                )
            else:
                print(
                    f"[{message['author']['username']} {readable_timestamp}]: {message['content']} [with {len(message['attachments'])} attachments]"
                )
        else:
            print(
                f"[{message['author']['username']} {readable_timestamp}]: {message['content']}"
            )


def send_message(
    token,
    cid,
    content,
):
    if not content:
        return

    url = f"https://discord.com/api/v9/channels/{cid}/messages"
    headers = {
        "authorization": token,
        "content-type": "application/json",
        "referer": f"https://discord.com/channels/@me/{cid}",
    }
    data = {"content": content}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print(
            f"failed to send message. status code: {response.status_code}, response: {response.text}"
        )


def validate_token(token: str) -> bool:
    """
    Validates the token. Returns a bool indicating whether the token is valid
    """
    logger.debug("validating token...")
    if not isinstance(token, str):
        logger.error(f"token is: {type(token).__name__}. it should be a string")
        return False
    url = "https://discord.com/api/v10/users/@me"
    headers = {"authorization": f"{token.strip()}"}
    response = requests.get(url, headers=headers)
    if not response.ok:
        logger.error(
            f"failed to validate token. server responded with code {response.status_code}"
        )
    else:
        logger.debug("token is ok")
    return response.ok


def validate_channel(token, cid):
    if isinstance(cid, str):
        if not cid.isdigit() or not cid:
            return False
    if not cid:
        return False
    else:
        c = custom_get_request(f"channels/{cid}", token)
        if not c.ok:  # type:ignore
            return False
        return c
    # return True


def custom_get_request(
    path: str, token: str, api_version: int = 10
) -> requests.Response | None:
    allowed_api_version = [6, 7, 8, 9, 10]  # currently supported discord api versions
    if api_version not in allowed_api_version:
        logger.error(
            "invalid api version, only allowed versions are: "
            + ", ".join([str(v) for v in allowed_api_version])
        )
    url = f"https://discord.com/api/v{api_version}/{path}"
    headers = {"authorization": f"{token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response
    else:
        logger.debug(f"requested {response.url} with code {response.status_code}")
        return None


def get_messages_from_channel(token, cid):
    url = f"https://discord.com/api/v10/channels/{cid}/messages"
    headers = {"authorization": f"{token}", "content-type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"failed to fetch messages. status code: {response.status_code}")
        return []


def get_profile_picture(user) -> str:
    return f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"


def get_banner(user) -> str:
    return f"https://cdn.discordapp.com/banners/{user['id']}/{user['banner']}.png"
