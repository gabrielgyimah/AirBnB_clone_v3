#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """
        1. Returns an object of the class (cls) from File with id == id
        """

        cls = str(cls)
        cls = cls.split('.')[2]
        cls = cls[:-2]
        if classes[cls]:
            self.reload()
            data = self.__objects

            if data:
                for obj in data:
                    obj_cls = obj.split(" ")[0].split(".")[0]
                    obj_id = obj.split(" ")[0].split(".")[1]
                    if obj_cls == cls and obj_id == id:
                        return data[obj]
            return None
        else:
            raise TypeError('Model type not recognized')
            return None

    def count(self, cls=None):
        """
        1. Returns count of objects of class (cls) in File Storage if cls
        2. Returns count of all objects in File Storage if not cls
        """
        count = 0;
        data = []

        if cls is not None:
            data = self.all(cls)
        else:
            data = self.all()
        for obj in data:
            count += 1
        return count
