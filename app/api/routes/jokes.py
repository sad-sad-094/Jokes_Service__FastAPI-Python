from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas import jokes
from app.infra.requests.client import get_random_joke
from app.infra.postgres.crud import jokes_crud
from app.infra.postgres.database import get_db
from app.api.routes.auth import get_current_user_id


router = APIRouter()


@router.post(
    "/new",
    summary="Get a new joke" ,
    status_code=status.HTTP_201_CREATED,
    response_class=JSONResponse,
    responses={
        201: {"description": "Joke successfully created."},
        500: {"description": "Internal server error."},
    },
    response_model=jokes.Joke
)
async def create_joke(
    # user_id: Annotated[int, Depends(get_current_user_id)],
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    new_joke = get_random_joke(user_id)

    if not new_joke:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    joke_db = jokes_crud.create_joke(db=db, joke=new_joke)

    if not joke_db:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return joke_db
    

@router.get(
    "",
    summary="Get all jokes from an registered user",
    response_class=JSONResponse,
    responses={
        200: {"description": "Successful response."},
    },
    response_model=list[jokes.JokesRequest]
)
async def read_user_jokes(
    # user_id: Annotated[int, Depends(get_current_user_id)],
    user_id: int = Depends(get_current_user_id),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    jokes = jokes_crud.get_jokes(db, user_id, skip=skip, limit=limit)
    return jokes