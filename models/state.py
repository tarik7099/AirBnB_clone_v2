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
        __tblname__ = "states"

        name_ot = Column(String(128), nullable=False)
        cities_ot = relationship('City', backref='state', cascade='all, delete')
    else:
        name_ot = ""

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
           Getter attribute for cities
            """
            city_list_ot = []
            for city_ot in list(models.storage.all("City").values()):
                if city_ot.state_id == self.id:
                    city_list_ot.append(city_ot)
            return city_list_ot
