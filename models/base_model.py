import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        """
        Constructor for the BaseModel class.
        Initializes common attributes for all inherited classes.
        """
        self.id = str(uuid.uuid4())  # Unique identifier for each instance
        self.created_at = datetime.now()  # Creation timestamp
        self.updated_at = datetime.now()  # Last update timestamp

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


