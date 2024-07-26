from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, MetaData
from sqlalchemy.orm import relationship

from .database import base as Base


# metadata = MetaData()

class User(Base):
    __tablename__ = "users"

    display_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    hashed_password_confirm = Column(String)
    id = Column(Integer, unique=True, primary_key=True)
    # is_active = Column(Boolean, default=True)

    # items = relationship("Item", back_populates="owner")


class Joke(Base):
    __tablename__ = "joke"

    source = Column(String)
    text = Column(String)
    id = Column(Integer, unique=True, primary_key=True)
    owner_id = Column(Integer)
    # owner_id = Column(Integer, ForeignKey("users.id"))

    # owner = relationship("User", back_populates="items")