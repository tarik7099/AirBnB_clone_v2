#!/usr/bin/python3

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv
import models

class State(BaseModel, Base):
    """State class"""

    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        @property
        def cities(self):
            city_list = []
            for city in list(models.storage.all("City").values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list

