from pydantic import BaseModel
from pydantic import field_validator


class Joke(BaseModel):
    source: str
    text: str
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class JokeCreate(BaseModel):
    source: str
    text: str
    id: int
    owner_id: int

class JokesRequest(BaseModel):
    source: str
    text: str
    id: int


# class Jokes(Joke):
#     jokes = list[Joke] = []


class User(BaseModel):
    email: str
    hashed_password: str
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

class UsersRequest(BaseModel):
    email: str
    display_name: str
    id: int

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str | None = None