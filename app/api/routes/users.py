from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.utils import utils
from app.infra.postgres.crud import jokes_crud, users_crud
from app.schemas import users, jokes
from app.infra.postgres.database import base as Base, engine, SessionLocal, get_db

Base.metadata.create_all(engine)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.post(
    "/users/register",
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=users.User
)
async def create_user(user: users.UserCreate, db: Session = Depends(get_db)):
    db_user = users_crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if user.password != user.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    user.password = utils.get_hashed_password(user.password)
    return users_crud.create_user(db=db, user=user)


@router.post("/users/login", summary="Login a user", response_model=users.Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user_db = users_crud.get_user_by_email(db, form_data.username)
    
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email has been not registered"
        )
    
    if not utils.verify_password(form_data.password, user_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    access_token = utils.create_access_token({"user_id": user_db.id})
    return users.Token(access_token=access_token, token_type="bearer")


@router.get(
        "/users",
        summary="Get all registered users",
        response_model=list[users.UsersRequest]
    )
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = users_crud.get_users(db, skip=skip, limit=limit)
    return users