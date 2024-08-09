from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.config import settings


class Authentication:
    def __init__(self):
        self.cripto_schema = "bcrypt"
        self.password_context = CryptContext(schemes=[self.cripto_schema], deprecated="auto")


    def get_hashed_password(self, password: str) -> str:
        return self.password_context.hash(password)


    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return self.password_context.verify(password, hashed_pass)
    

auth_service = Authentication()
