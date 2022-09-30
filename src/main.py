"""
@author Sami Hindi
@date 30.09.2022
@version 0.0.1
@description Hacking-Tool
@license MIT License (/LICENSE)
"""

"""
Import necessary modules and libraries for flash to run.
colored -> Color text in terminal
Action -> Base class for all actions
sys -> System-specific parameters and functions
"""
from termcolor import colored
import sys
from action import Action

def main() -> None:
    """
    Main function
    :return None
    """
    print(colored("*************** Flash ***************", "green"))

    # Take the action provided by the user arguments
    action = sys.argv[1]

    # Take any additional arguments for the action itself
    args = sys.argv[2:]

    # Create an Action object
    action = Action(action=action, args=args)

    # Delegate the action performing to the Action object
    return_value = action.perform()
    print(colored(f"INFO: Finished Action with exit code {return_value}", "blue"))
    print(colored("*************** Flash ***************", "green"))

if __name__ == '__main__':
    """
    Catch any incoming KeyboardInterrupts and exit the program accordingly.
    Catch any incoming not existing user-arguments and exit the program accordingly.
    """
    try:
        main()
    except KeyboardInterrupt:
        quit("User has stopped the program manually.")
    except IndexError:
        quit("Please provide an action to perform.")