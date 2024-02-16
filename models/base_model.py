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
        
        if kwargs:
            for key, value in kwargs.items():
               
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        setattr(self, key, datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

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


