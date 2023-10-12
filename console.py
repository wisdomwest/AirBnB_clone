#!/usr/bin/python3
"""Entry point to the command line, Our user interface."""

import cmd
import sys


class HBNBCommand(cmd.Cmd):
    """A class defination to create a custom command intepreter.

    Args:
        cmd.Cmd: Allow custom methods for the command intepreter.
    """

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program."""

        return True

    def do_EOF(self, arg):
        """End of file command to exit the program."""

        print("")
        return True

    def emptyline(self):
        """Disable last command repetition if no command is entered."""

        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
