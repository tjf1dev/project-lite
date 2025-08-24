from functions import custom_get_request
from login.config import Favorite
from parser import command
from logger import logger
import context
import models
import curses


@command(
    name="fav",
    description="add the current channel to favorites",
    args=[
        models.Argument(
            datatype=models.DataType.String,
            name="options",
            description="select: pick a channel from favorites",
            required=False,
        )
    ],
)
def fav(**kwargs):
    cid = context.channel_id
    if not cid:
        logger.error("select a channel first.")
    opt = kwargs.get("options", "")
    if opt == "select":
        context.channel_id = fav_select()
        return
    token = context.token
    channel = custom_get_request(f"channels/{cid}", token).json()
    Favorite.add(cid, channel)


def fav_select():
    favorites = Favorite.get()
    if favorites == []:
        print(
            "you don't have any favorite channels. use fav add in a channel to save it."
        )
        return
    favorites.append({"id": 10, "data": {"name": "back"}})
    fav_names = [fav["data"] for fav in favorites]
    title = "select a channel with your arrow keys."

    def menu(stdscr):
        curses.curs_set(0)
        stdscr.keypad(True)
        selected = 0

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            title_x = (w // 2) - (len(title) // 2)
            stdscr.addstr(
                h // 2 - len(fav_names) // 2 - 2, title_x, title, curses.A_BOLD
            )

            for i, name in enumerate(fav_names):
                text = f"> {name}" if i == selected else f"  {name}"
                x = (w // 2) - (len(text) // 2)
                y = (h // 2) - (len(fav_names) // 2) + i
                stdscr.addstr(
                    y, x, text, curses.A_REVERSE if i == selected else curses.A_NORMAL
                )

            key = stdscr.getch()

            if key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(fav_names) - 1:
                selected += 1
            elif key in [10, 13]:
                id = favorites[selected]["id"]
                return None if id == 10 else id

    return curses.wrapper(menu)
