from sqlalchemy.orm import Session

from project import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, 
        display_name=user.display_name,
        hashed_password=user.password,
        hashed_password_confirm=user.password_confirm
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).where(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_joke(db: Session, joke: schemas.JokeCreate):
    db_joke = models.Joke(
        source = joke.source,
        text = joke.text,
        id = joke.id,
        owner_id = joke.owner_id,
    )    
    db.add(db_joke)
    db.commit()
    db.refresh(db_joke)

    return db_joke

def get_jokes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Joke).offset(skip).limit(limit).all()