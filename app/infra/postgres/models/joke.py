from sqlalchemy import Column, ForeignKey, Integer, String

from app.infra.postgres.database import base as Base


class Joke(Base):
    __tablename__ = "joke"

    source = Column(String)
    text = Column(String)
    id = Column(String, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))