import threading
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import ANSI

_result = None
_done = threading.Event()
_input_canceled = False  # New flag


def _input_worker(prompt: str):
    global _result, _input_canceled
    session = PromptSession()
    try:
        with patch_stdout():
            _result = session.prompt(ANSI(prompt))
        _input_canceled = False
    except KeyboardInterrupt:
        print("\n^C (input canceled)")
        _result = None
        _input_canceled = True
    print("\033[F\033[K", end="")  # Clear the previous input line
    _done.set()


def iinput(prompt: str = ""):
    """Starts the input prompt in a background thread."""
    global _done
    _done.clear()  # Clear before starting new input
    thread = threading.Thread(target=_input_worker, args=(prompt,), daemon=True)
    thread.start()
    return thread


def input_ready():
    """Returns True if the user has submitted input."""
    return _done.is_set()


def input_value():
    """Returns the user's submitted input (after they hit enter)."""
    if not _done.is_set():
        raise RuntimeError("Input not ready yet.")
    return _result


def input_canceled():
    """Returns True if the last input was canceled by Ctrl+C."""
    return _input_canceled
