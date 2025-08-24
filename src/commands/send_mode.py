from functions import get_discord_user_info, get_discord_username, send_message


def send_messages(token, cid):
    while True:
        content = input(
            f"[{get_discord_username(get_discord_user_info(token))}/{cid} (send mode)]: "
        )
        if content.lower() == "exit":
            break
        if content == "":
            pass
        send_message(cid, content, token)
