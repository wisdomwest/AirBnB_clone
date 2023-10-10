#!/usr/bin/python3
"""
Module contains BaseModel class
The class will be inherited by all classes
"""

from datetime import datetime
import uuid


class BaseModel:
    """BaseModel class defines methods"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """print: [<class name>] (<self.id>) <self.__dict__>"""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """updates the public instance attribute
        updated_at with the current datetime"""

        self.updated_at = datetime.now()

    def to_dict(self):
        """returns a dictionary containing all keys
            of __dict__ of the instance"""

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict