from sqlalchemy.orm import Session

from app.infra.postgres import models
from app.schemas import users


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: users.UserCreate) -> models.User:
    db_user = models.User(
        email=user.email, 
        display_name=user.display_name,
        hashed_password=user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).where(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> models.User:
    return db.query(models.User).offset(skip).limit(limit).all()