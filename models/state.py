#!/usr/bin/python3
        
""" State Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv
import models

class State(BaseModel, Base):
    """State class"""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        _tablename_ = "states"

        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        name = ""
    if storage_type != 'db':
        @property
        def cities(self):
            """Return the list of City objects from storage linked"""
            from models.city import City
            cities_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
           Getter attribute for cities
            """
            city_list_ = []
            for city in list(models.storage.all("City").values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list_
