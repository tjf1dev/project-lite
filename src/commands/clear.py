from parser import command
from functions import clear


@command(name="clear", aliases=["cls"], description="clears the console.")
def clear_c():
    clear()
