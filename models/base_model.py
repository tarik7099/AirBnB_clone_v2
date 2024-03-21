#!/usr/bin/python3

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models

Base = declarative_base()

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
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.created_at_o = kwargs.get("created_at", datetime.utcnow())
            self.updated_at_o = kwargs.get("updated_at", datetime.utcnow())
        else:
            self.id = str(uuid.uuid4())
            self.created_at_o = datetime.utcnow()
            self.updated_at_o = self.created_at_o

    def save(self):
        """Saves the current instance to the database"""
        self.updated_at_o = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Deletes the current instance from the storage"""
        models.storage.delete(self)

    def to_dict(self):
        """Returns a dictionary representation of the instance"""
        dictionary = self.__dict__.copy()
        dictionary.pop('_sa_instance_state', None)
        return dictionary

