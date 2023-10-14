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
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

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
