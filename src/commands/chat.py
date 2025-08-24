import asyncio
import threading
import time
import json
import websockets
import zlib
from queue import Queue
from ext.iinput import iinput, input_ready, input_value, _done, input_canceled
from parser import command
import context
from logger import logger
from ext.color import Color as c
import datetime
import tzlocal
import dateutil
from functions import send_message, get_messages_from_channel

GATEWAY_URL = "wss://gateway.discord.gg/?v=9&encoding=json"
zlib_decompressor = zlib.decompressobj()
print_queue = Queue()
typing_users = {}


async def heartbeat(ws, interval, stop_event):
    try:
        while not stop_event.is_set():
            await asyncio.sleep(interval / 1000)
            await ws.send(json.dumps({"op": 1, "d": None}))
    except websockets.exceptions.ConnectionClosed:
        pass  # connection closed, exit heartbeat


async def identify(ws):
    payload = {
        "op": 2,
        "d": {
            "token": context.token,
            "capabilities": 4093,
            "properties": {
                "os": "Windows",
                "browser": "Chrome",
                "device": "",
                "system_locale": "en-US",
                "browser_user_agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0.0.0 Safari/537.36"
                ),
                "browser_version": "115.0.0.0",
                "os_version": "10",
                "referrer": "",
                "referring_domain": "",
                "referrer_current": "",
                "referring_domain_current": "",
                "release_channel": "stable",
                "client_build_number": 265965,
                "client_event_source": None,
            },
            "presence": {
                "status": "online",
                "since": 0,
                "activities": [],
                "afk": False,
            },
            "compress": False,
            "client_state": {
                "guild_versions": {},
                "highest_last_message_id": "0",
                "read_state_version": 0,
                "user_guild_settings_version": -1,
                "user_settings_version": -1,
                "private_channels_version": "0",
                "api_code_version": 0,
            },
        },
    }
    await ws.send(json.dumps(payload))


async def receive_messages(ws, stop_event):
    async for message in ws:
        if isinstance(message, bytes):
            message = zlib_decompressor.decompress(message).decode("utf-8")
        data = json.loads(message)
        op = data.get("op")
        t = data.get("t")

        if op == 10:
            interval = data["d"]["heartbeat_interval"]
            print(
                f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] log: connected to discord socket"
            )
            asyncio.create_task(heartbeat(ws, interval, stop_event))
            await identify(ws)

        elif op == 9:
            print(
                f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] log: session invalidated"
            )

        elif op == 0 and t == "TYPING_START":
            typing = data["d"]
            user_id = typing["user_id"]
            channel_id = typing["channel_id"]

            if channel_id == context.channel_id:
                username = context.user_cache.get(user_id, f"User {user_id}")
                typing_users[user_id] = time.time()
                print_queue.put(f"{c.white_3}{username} is typing...{c.reset}")

        elif op == 0 and t == "MESSAGE_CREATE":
            msg = data["d"]
            author = msg["author"]["username"]
            content = msg["content"]
            channel_id = msg["channel_id"]
            if channel_id == context.channel_id:
                print_queue.put(
                    f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {author}: {content}"
                )


async def discord_client_forever(stop_flag: threading.Event):
    while not stop_flag.is_set():
        try:
            async with websockets.connect(
                GATEWAY_URL, compression=None, max_size=50 * 1024 * 1024
            ) as ws:
                stop_event = asyncio.Event()
                await receive_messages(ws, stop_event)
        except Exception as e:
            print(
                f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] log: connection lost: {e}"
            )
            await asyncio.sleep(2)  # wait before reconnect


def run_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def clean_expired_typing():
    now = time.time()
    expired = [uid for uid, t in typing_users.items() if now - t > 5]
    for uid in expired:
        del typing_users[uid]


def print_from_queue():
    while not print_queue.empty():
        print(print_queue.get())


def main_loop(user: dict):
    loop = asyncio.new_event_loop()
    threading.Thread(target=run_async_loop, args=(loop,), daemon=True).start()

    should_exit = threading.Event()
    asyncio.run_coroutine_threadsafe(discord_client_forever(should_exit), loop)

    prompt = f"{c.white_1}C/$ {c.reset}"
    prompt_first = f"{c.white_2}[type /help]{c.white_1}C/$ {c.reset}"
    iinput(prompt_first)

    while True:
        print_from_queue()
        clean_expired_typing()

        if input_ready():
            if input_canceled():
                should_exit.set()
                print(
                    f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] log: exited"
                )
                break

            msg = input_value()
            _done.clear()
            iinput(prompt)
            send_message(context.token, context.channel_id, msg)

        time.sleep(0.05)


def prefetch_messages():
    messages = get_messages_from_channel(context.token, context.channel_id)
    user_timezone = tzlocal.get_localzone()
    for message in reversed(messages):
        timestamp = dateutil.parser.isoparse(message["timestamp"]).astimezone(
            user_timezone
        )
        print(
            f"[{timestamp.strftime('%d/%m/%Y %H:%M:%S')}] {message['author']['username']}: {message['content']}"
        )


@command(name="chat", description="enter chat mode")
def chat():
    if not context.channel_id:
        logger.error("select a channel first.")
        return
    prefetch_messages()
    main_loop(context.user)
