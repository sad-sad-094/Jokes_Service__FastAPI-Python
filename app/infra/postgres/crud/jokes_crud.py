from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.infra.postgres.models.joke import Joke
from app.schemas import jokes


def create_joke(db: Session, joke: jokes.JokeCreate) -> Joke | None:
    db_joke = Joke(
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
) -> Joke:
    return db.query(Joke).where(Joke.owner_id == user_id).offset(skip).limit(limit).all()