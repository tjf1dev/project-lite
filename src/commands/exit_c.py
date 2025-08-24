from parser import command


@command(name="exit", description="terminates the program.", aliases=["quit"])
def exit_c():
    exit()
