import requests

from app.schemas import jokes
from app.services import random_jokes


def request_chuck(user_id: int) -> jokes.JokeCreate | None:
    response = requests.get(random_jokes.URL_CHUCK)

    if response.status_code != 200:
        return None
    
    parsed_response = response.json()

    joke = jokes.JokeCreate(
        source="Chuck Norris",
        text=parsed_response["value"],
        id=parsed_response["id"],
        owner_id=user_id
    )
    return joke


def request_dad(user_id: int) -> jokes.JokeCreate | None:
    response = requests.get(random_jokes.URL_DAD, headers=random_jokes.DAD_HEADERS)

    if response.status_code != 200:
        return None
    parsed_response = response.json()

    if parsed_response["status"] != 200:
        return None
    
    joke = jokes.JokeCreate(
        source="Dad Joke",
        text=parsed_response["joke"],
        id=parsed_response["id"],
        owner_id=user_id
    )
    return joke
