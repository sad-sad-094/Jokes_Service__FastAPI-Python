from sqlalchemy import Column, ForeignKey, Integer, String

from .database import base as Base

class User(Base):
    __tablename__ = "users"

    display_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    id = Column(Integer, unique=True, primary_key=True)


class Joke(Base):
    __tablename__ = "joke"

    source = Column(String)
    text = Column(String)
    id = Column(String, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))