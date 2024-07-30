from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from project.database import base as Base, engine, SessionLocal
from project import schemas, crud

Base.metadata.create_all(engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users", response_model=list[schemas.UsersRequest])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.post("/jokes", response_model=schemas.Joke)
async def create_joke(joke: schemas.JokeCreate, db: Session = Depends(get_db)):
    return crud.create_joke(db=db, joke=joke)

@app.get("/jokes", response_model=list[schemas.JokesRequest])
async def read_jokes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jokes = crud.get_jokes(db, skip=skip, limit=limit)
    return jokes