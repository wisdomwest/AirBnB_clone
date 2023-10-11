#!/usr/bin/python3
"""
Module contains BaseModel class
The class will be inherited by all classes
"""

from datetime import datetime
import uuid
from models import storage


class BaseModel:
    """BaseModel class defines methods"""

    def __init__(self, *args, **kwargs):
        """Create an istance of base model from a dictionary rep of to_dict.
        Else create normal public instances.

        Args:
            *args: non-keyworded arguments.
            **kwargs: Key worded args.
        """

        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        setattr(self, key, datetime.
                                strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """print: [<class name>] (<self.id>) <self.__dict__>"""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """updates the public instance attribute
        updated_at with the current datetime"""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys
            of __dict__ of the instance"""

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict
