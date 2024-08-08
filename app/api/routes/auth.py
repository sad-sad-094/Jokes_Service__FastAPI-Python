from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.infra.postgres.database import get_db
from app.config import settings


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
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id: int | None = payload.get("user_id", None)

        if user_id is None:
            raise credentials_exception
        
    except InvalidTokenError:
        raise credentials_exception
    return user_id
