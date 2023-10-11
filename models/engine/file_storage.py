#!/usr/bin/python3
"""Module contains class FileStorage"""
import datetime
import json
import os


class FileStorage:

    """Class for serializtion and deserialization of base classes."""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with
            key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        data = {}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            for key, value in FileStorage.__objects.items():
                data[key] = value.to_dict()
            json.dump(data, f)

    def reload(self):
        """deserializes the JSON file"""
        from models.base_model import BaseModel

        classes = {'BaseModel': BaseModel}

        try:
            data = {}
            with open(FileStorage.__file_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    self.all()[key] = classes[value['__class__']](**value)
        except FileNotFoundError:
            pass
