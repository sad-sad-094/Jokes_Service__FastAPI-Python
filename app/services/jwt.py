from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings

class jwt_service: 
    def create_access_token(self, data: dict, expires_delta: int = None) -> str:
        to_encode = data.copy()
        
        if expires_delta:
            expires_delta = datetime.now(timezone.utc) + expires_delta
        else:
            expires_delta = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_token_expo)
        
        to_encode.update({"exp": expires_delta})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, settings.jwt_algorithm)
        return encoded_jwt