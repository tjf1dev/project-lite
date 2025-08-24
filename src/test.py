from ext.iinput import iinput, input_ready, input_value, _done
import time

while True:
    # Start prompt
    iinput("\x1b[38;2;150;150;150mC/$ \x1b[0m")

    # Wait for user input
    while not input_ready():
        time.sleep(0.05)

    # Get and process input
    msg = input_value()
    print(f"You typed: {msg}")

    # Reset event for next input
    _done.clear()
