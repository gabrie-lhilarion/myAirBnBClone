#!/usr/bin/python3

import models
import uuid
from datetime import datetime



class BaseModel:
    
    def __init__(self, *args, **kwargs):
        """
        Constructor for the BaseModel class.

        Args:
            *args: Unused positional arguments.
            **kwargs: Dictionary of attribute names and values.

        If kwargs is not empty:
        - Each key is an attribute name.
        - Each value is the value of the corresponding attribute.
        - 'created_at' and 'updated_at' strings are converted to datetime objects.

        If kwargs is empty:
        - Create 'id' and 'created_at' as new instances.
        """
        
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if kwargs:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def __str__(self):
        """
        String representation of the BaseModel instance.
        """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute 'updated_at' with the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing keys and values of instance attributes.
        Includes the '__class__', 'created_at', and 'updated_at' keys.
        'created_at' and 'updated_at' are formatted as ISO strings.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict


