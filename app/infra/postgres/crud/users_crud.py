from sqlalchemy.orm import Session

from app.infra.postgres.models.user import User
from app.schemas import users


def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: users.UserCreate) -> User:
    db_user = User(
        email=user.email, 
        display_name=user.display_name,
        hashed_password=user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).where(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> User:
    return db.query(User).offset(skip).limit(limit).all()