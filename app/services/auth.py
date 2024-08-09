from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.config import settings

cripto_schema = "bcrypt"
password_context = CryptContext(schemes=[cripto_schema], deprecated="auto")


class Authentication:
    def __init__(self):
        self.cripto_schema = "bcrypt"
        self.password_context = CryptContext(schemes=[self.cripto_schema], deprecated="auto")


    def get_hashed_password(self, password: str) -> str:
        return self.password_context.hash(password)


    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return self.password_context.verify(password, hashed_pass)
    

user_auth = Authentication()


def create_access_token(data: dict, expires_delta: int = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_token_expo)
    
    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, settings.jwt_algorithm)
    return encoded_jwt