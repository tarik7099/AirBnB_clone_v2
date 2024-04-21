#!/usr/bin/python3


"""This module defines the DBStorage class for HBNB project"""

from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """DBStorage class to map tables in MySQLdb"""

    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine"""
        user_ot = getenv("HBNB_MYSQL_USER")
        passwd_ot = getenv("HBNB_MYSQL_PWD")
        host_ot = getenv("HBNB_MYSQL_HOST")
        db_ot = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user_ot, passwd_ot, host_ot, db_ot),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

        def all(self, cls=None):
            """Returns a dictionary of all instances"""
        obj_dict_ot = {}
        classes = [User, State, City, Amenity, Place, Review]
        if cls:
            classes = [cls]
        for class_ in classes:
            objs = self.__session.query(class_).all()
            for obj in objs:
                key_ot = "{}.{}".format(obj.__class__.__name__, obj.id)
                obj_dict_ot[key_ot] = obj
        return obj_dict_ot


    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Serialize __objects to the JSON file __file_path"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete a given object from __objects, if it exists"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and creates session"""
        Base.metadata.create_all(self.__engine)
        session_ot = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_ot)
        self.__session.close()

    def close(self):
        """Call the reload method."""
        self.__session.remove()
