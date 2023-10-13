#!/usr/bin/python3
"""Entry point to the command line, Our user interface."""

import cmd
import sys
import os
import json
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """A class defination to create a custom command intepreter.

    Args:
        cmd.Cmd: Allow custom methods for the command intepreter.
    """

    prompt = "(hbnb) "
    instances = {}
    classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
            }

    def do_create(self, arg):
        """A command that creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id.

        Args:
            arg: A class name from Basemodel.
        """

        if not arg:
            print("** class name missing **")
            return
        try:
            cls = self.classes[arg]
            instance = cls()
            instance.save()
            print(instance.id)
        except KeyError:
                print("** class doesn't exist **")

    def do_show(self, line):
        """A command that prints the string representation of an instance
        based on the class name and id.

        Args:
            line: The command entered by the user.
        """

        args = line.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = class_name + "." + instance_id
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id.

        Args:
            arg: Argumants passed to the command.
        """

        args = arg.split()

        if not args:
            print("** class name missing **")
            return
        class_name = args[0]

        if len(args) > 1:
            instance_id = args[1]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        cls = globals()[class_name]

        if not instance_id:
            print("** instance id missing **")
            return
        if not issubclass(cls, BaseModel):
            print("** class doesn't exist **")
            return
        key = class_name + "." + instance_id
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints a string representation of all instances base or
        not on the class name.

        Args:
            arg: Argument passed to the command.
        """

        args = arg.split()
        if not args:
            print([str(obj) for obj in storage.all().values()])
        elif args[0] in self.classes:
            class_name = args[0]
            print([str(obj) for key, obj in storage.all().items() if class_name in key])
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or
        updating attribute.

        Args:
            arg: Argument given to the command.
        """

        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        instance_id = None

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        cls = globals()[class_name]

        if not instance_id:
            print("** instance id missing **")
            return

        if not issubclass(cls, BaseModel):
            print("** class doesn't exist **")
            return
        key = class_name + "." + instance_id
        if key in storage.all():
            if len(args) < 3:
                print("** attribute name missing **")
            else:
                attribute_name = args[2]
                if len(args) < 4:
                    print("** value missing **")
                else:
                    attribute_value = args[3]
                    obj = storage.all()[key]
                    if hasattr(obj, attribute_name):
                        if True:
                            try:
                                attribute_value = eval(attribute_value)
                                setattr(obj, attribute_name, attribute_value)
                                storage.save()
                            except (NameError, SyntaxError):
                                print("** invalid value for the attribute **")
                    else:
                        print("** attribute name is not valid or can't be updated **")
        else:
            print("** no instance found **")

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
