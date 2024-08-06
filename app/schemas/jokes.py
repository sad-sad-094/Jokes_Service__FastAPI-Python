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
