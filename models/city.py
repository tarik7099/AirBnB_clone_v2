#!/usr/bin/python3


""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class City(BaseModel, Base):
    """
    The city class, contains state ID and name
    """

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tblnm__ = 'cities'

        name_o = Column(String(128), nullable=False)
        state_id_o = Column(String(60), ForeignKey('states.id'), nullable=False)
        plcs_o = relationship('Place', backref='cities', cascade='all, delete')

    else:
        name = ""
        state_id = ""
