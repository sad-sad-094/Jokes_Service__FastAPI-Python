from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import models, schemas

def get_user(db: Session, user_id: int)  -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
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

def create_joke(db: Session, joke: schemas.JokeCreate) -> models.Joke | None:
    db_joke = models.Joke(
        source = joke.source,
        text = joke.text,
        id = joke.id,
        owner_id = joke.owner_id,
    )    
    db.add(db_joke)
    try: 
        db.commit()
        db.refresh(db_joke)
        return db_joke
    except IntegrityError:
        db.rollback()
        return None

def get_jokes(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10
) -> models.Joke:
    return db.query(models.Joke).where(models.Joke.owner_id == user_id).offset(skip).limit(limit).all()