from colored import Fore, Style


class Color:
    reset = Style.RESET
    black = Fore.rgb(0, 0, 0)
    white = Fore.rgb(255, 255, 255)
    white_1 = Fore.rgb(197, 197, 197)
    white_2 = Fore.rgb(150, 150, 150)
    white_3 = Fore.rgb(94, 94, 94)
    white_4 = Fore.rgb(64, 64, 64)
    white_5 = Fore.rgb(50, 50, 50)

    light_red = error = err = negative = Fore.rgb(255, 82, 82)
    red = Fore.rgb(255, 48, 48)
    dark_red = Fore.rgb(122, 14, 14)

    light_yellow = warning = warn = Fore.rgb(255, 255, 151)
    yellow = Fore.rgb(255, 255, 72)

    light_blue = information = info = Fore.rgb(148, 136, 255)
    blue = Fore.rgb(81, 81, 255)
    dark_blue = Fore.rgb(52, 52, 172)

    light_green = success = ok = positive = Fore.rgb(117, 255, 147)
    green = Fore.rgb(76, 250, 76)
    dark_green = Fore.rgb(44, 141, 44)

    light_purple = Fore.rgb(255, 136, 255)
    purple = Fore.rgb(239, 63, 255)
    dark_purple = Fore.rgb(150, 18, 150)


def test():
    """
    Displays all unique colors from the Color class, grouped in rows.
    """
    groups = {
        "grayscale": [
            Color.black,
            Color.white_5,
            Color.white_4,
            Color.white_3,
            Color.white_2,
            Color.white_1,
            Color.white,
        ],
        "reds": [Color.dark_red, Color.red, Color.light_red],
        "greens": [Color.dark_green, Color.green, Color.light_green],
        "yellows": [Color.yellow, Color.light_yellow],
        "blues": [Color.dark_blue, Color.blue, Color.light_blue],
        "purples": [Color.dark_purple, Color.purple, Color.light_purple],
    }

    for label, colors in groups.items():
        seen = set()
        unique = [c for c in colors if not (c in seen or seen.add(c))]

        if unique:
            # print(f"{label.title():<10}", end=" ")
            print("".join(f"{c}███" for c in unique) + Color.reset, end="", flush=True)


if __name__ == "__main__":
    test()
