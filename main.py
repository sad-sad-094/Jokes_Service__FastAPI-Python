from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from typing import Annotated

from project.client import get_random_joke
from project.database import base as Base, engine, SessionLocal
from project import schemas, crud, utils

Base.metadata.create_all(engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )


    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        
    except InvalidTokenError:
        raise credentials_exception
    return user_id


@app.post(
    "/users/register",
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if user.password != user.password_confirm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    user.password = utils.get_hashed_password(user.password)
    return crud.create_user(db=db, user=user)


@app.post("/users/login", summary="Login a user", response_model=schemas.Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user_db = crud.get_user_by_email(db, form_data.username)
    
    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email has been not registered"
        )
    
    if not utils.verify_password(form_data.password, user_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    access_token = utils.create_access_token({"user_id": user_db.id})
    return schemas.Token(access_token=access_token, token_type="bearer")


@app.get(
        "/users",
        summary="Get all registered users",
        response_model=list[schemas.UsersRequest]
    )
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/jokes/new",
    summary="Get a new joke" ,
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Joke
)
async def create_joke(joke: schemas.JokeCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Session = Depends(get_db)
):
    new_joke = get_random_joke(user_id)

    if not new_joke:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    joke_db = crud.create_joke(db=db, joke=new_joke)

    if not joke_db:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return joke_db
    

@app.get(
    "/jokes",
    summary="Get all jokes from an registered user",
    response_model=list[schemas.JokesRequest]
)
async def read_user_jokes(
    user_id: Annotated[int, Depends(get_current_user_id)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    jokes = crud.get_jokes(db, user_id, skip=skip, limit=limit)
    return jokes