"""
Allow user to control robot using natural English language via command line IO
"""

import re
from r2d2_commands import *

def main():
    print("Welcome to CommandDroid, where we will try our best to understand what you want our R2D2 to do.")
    print("In this environment, type 'exit', 'quit', 'bye', or 'goodbye' to quit.")
    print("***********************************************")

    # Replace this with your own robot serial ID
    robot = Robot('D2-152E', 0.70, False)

    while(True):
        command = input("You: ").lower()
        if len(command) == 0:
            print("Please type something")
        if re.search(r"\b(exit|quit|bye|goodbye)\b", command, re.I):
            print('Exiting...')
            break
        robot.inputCommand(command)
    robot.disconnect()

if __name__ == "__main__":
    main()
