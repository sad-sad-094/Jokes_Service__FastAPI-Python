from sqlalchemy import Column, Integer, String

from app.infra.postgres.database import base as Base

class User(Base):
    __tablename__ = "users"

    display_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    id = Column(Integer, unique=True, primary_key=True)