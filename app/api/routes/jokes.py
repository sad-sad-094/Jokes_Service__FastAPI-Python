from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.utils import utils
from app.infra.postgres.crud import jokes_crud, users_crud
from app.schemas import users, jokes
from app.infra.requests.client import get_random_joke
from app.infra.postgres.database import base as Base, engine, SessionLocal, get_db


Base.metadata.create_all(engine)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )


    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        
    except InvalidTokenError:
        raise credentials_exception
    return user_id


@router.post(
    "/jokes/new",
    summary="Get a new joke" ,
    status_code=status.HTTP_201_CREATED,
    response_model=jokes.Joke
)
async def create_joke(
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Session = Depends(get_db)
):
    new_joke = get_random_joke(user_id)

    if not new_joke:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    joke_db = jokes_crud.create_joke(db=db, joke=new_joke)

    if not joke_db:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return joke_db
    

@router.get(
    "/jokes",
    summary="Get all jokes from an registered user",
    response_model=list[jokes.JokesRequest]
)
async def read_user_jokes(
    user_id: Annotated[int, Depends(get_current_user_id)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    jokes = jokes_crud.get_jokes(db, user_id, skip=skip, limit=limit)
    return jokes