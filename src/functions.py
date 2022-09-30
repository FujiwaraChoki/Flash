from termcolor import colored

def quit(msg: str) -> None:
    """
    The quit() function is used to exit the program.
    :return None
    """
    print(colored("FAILURE: " + msg, "red"))
    exit(0)