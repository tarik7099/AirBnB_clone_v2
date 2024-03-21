#!/usr/bin/python3

"""Defines the BaseModel class"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models
from sqlalchemy.orm import relationship

Base = declarative_base()

T_fmt = '%Y-%m-%dT%H:%M:%S.%f'

class BaseModel(Base):
    """A base class for all HBNB models"""

    __tablename__ = "base_models"
    __tbl_args__ = {'extend_existing': True}

    id = Column(String(60), nullable=False, primary_key=True)
    created_at_o = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at_o = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if (kwargs.get("created_at", None) and
                    isinstance(kwargs["created_at"], str)):
                self.created_at_o = datetime.strptime(
                    kwargs["created_at"], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.created_at_o = datetime.utcnow()
            if (kwargs.get("updated_at", None) and
                    isinstance(kwargs["updated_at"], str)):
                self.updated_at_o = datetime.strptime(
                    kwargs["updated_at"], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.updated_at_o = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at_o = datetime.utcnow()
            self.updated_at_o = self.created_at

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        dic = self.__dict__.copy()
        if "_sa_instance_state" in dict:
            dict.pop("_sa_instance_state")
        return '[{}] ({}) {}'.format(cls, self.id, dict)

    def save(self):
        """Update updated_at with current datime """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                           (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary:
            dictionary.pop("_sa_instance_state")

        return dictionary

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)

