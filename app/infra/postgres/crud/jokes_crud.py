from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.infra.postgres import models
from app.schemas import jokes


def create_joke(db: Session, joke: jokes.JokeCreate) -> models.Joke | None:
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