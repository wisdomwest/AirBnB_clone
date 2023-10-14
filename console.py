#!/usr/bin/python3
"""Entry point to the command line, Our user interface."""

import cmd
import re
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
        """Usage: create <class>
        Create a new class instance and print its id.
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
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of class instance of a id.
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
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
            Delete a class instance of a id."""
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
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        """
        args = arg.split()
        if not args:
            print([str(obj) for obj in storage.all().values()])
        elif args[0] in self.classes:
            class_name = args[0]
            print([str(obj) for key, obj in storage.all().items()
                   if class_name in key])
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>)
        Update a class instance of a given id"""
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        cls = self.classes.get(class_name)

        if not instance_id:
            print("** instance id missing **")
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
                        try:
                            if isinstance(getattr(obj, attribute_name), int):
                                attribute_value = int(attribute_value)
                            elif isinstance(getattr(obj, attribute_name), float):
                                attribute_value = float(attribute_value)
                            setattr(obj, attribute_name, attribute_value)
                            storage.save()
                        except (TypeError, ValueError):
                            print("** invalid value for the attribute **")
                        else:
                            print("** attribute name is not valid or can't be updated **")

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
