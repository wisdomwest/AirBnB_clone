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

    def do_quit(self, _):
        """Quit command to exit the program."""

        sys.exit(0)

    def do_EOF(self, _):
        """End of file command to exit the program."""

        sys.exit(0)


    def do_help(self, arg):
        """The help manual for the commands.

        Args:
            arg: Argument passed to the help command.
        """

        if arg:
            try:
                doc_func = getattr(self, f"help_{arg}")
                if doc_func:
                    doc_string = doc_func.__doc__
                    if doc_string:
                        print("{}".format(doc_string))
                    else:
                        print("No help for {}".format(arg))
                else:
                    print("No such command {}".format(arg))
            except AttributeError:
                print("No such command {}".format(arg))
        else:
            doc_cmds = [name[3:] for name in self.get_names() if name.startswith("do_")]
            print("Documented commands (type help <topic>):")
            print("========================================")
            print(" ".join(doc_cmds))

    def help_quit(self):
        """Quit command to exit the program"""

        pass

    def help_EOF(self):
        """EOF command to exit the program"""

        pass

    def emptyline(self):
        """Disable last command repetition if no command is entered."""

        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
