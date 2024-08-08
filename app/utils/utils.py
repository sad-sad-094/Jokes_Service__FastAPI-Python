from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(data: dict, expires_delta: int = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_token_expo)
    
    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, settings.jwt_algorithm)
    return encoded_jwt        