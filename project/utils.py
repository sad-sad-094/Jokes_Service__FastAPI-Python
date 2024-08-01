from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Any
import jwt

from project import crud, schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(data: dict, expires_delta: int = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt        