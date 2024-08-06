from pydantic import BaseModel

class Joke(BaseModel):
    source: str
    text: str
    id: str

    class Config:
        orm_mode = True

class JokeCreate(BaseModel):
    source: str
    text: str
    id: str
    owner_id: int

class JokesRequest(BaseModel):
    source: str
    text: str
    id: str


class User(BaseModel):
    email: str
    hashed_password: str
    display_name: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str
    password_confirm: str
    display_name: str

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
    user_id: int | None = None
    