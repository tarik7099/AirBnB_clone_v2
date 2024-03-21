#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from os import getenv
# from dotenv import load_dotenv

# This line brings all environment variables from .env into os.environ
# load_dotenv()


class State(BaseModel, Base):
    """ State class """

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "states"

        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        name = ""

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
            getter attribute cities that returns the list of City instances
            with state_id equals to the current State.id => It will be the
            FileStorage relationship between State and City
            """
            return [city for city in models.storage.all("City").values()
                    if city.state_id == self.id]
