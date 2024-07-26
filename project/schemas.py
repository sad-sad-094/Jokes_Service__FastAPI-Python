from pydantic import BaseModel
from pydantic import field_validator


class Joke(BaseModel):
    source: str
    text: str
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# class Jokes(Joke):
#     jokes = list[Joke] = []


class User(BaseModel):
    email: str
    password: str
    password_confirm: str
    display_name: str
    id: int
    # jokes: list[Joke] = []
    # is_active: bool

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str
    password_confirm: str
    display_name: str
    id: int

class UserRequestModel(BaseModel):
  id: int
  username: str