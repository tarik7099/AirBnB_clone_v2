from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    __tablename__ = 'users'

    places = relationship("Place", cascade="all, delete", back_populates="user")
