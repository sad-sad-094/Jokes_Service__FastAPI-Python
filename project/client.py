import requests
import random

from project import schemas

URL_CHUCK = "https://api.chucknorris.io/jokes/random"
URL_DAD = "https://icanhazdadjoke.com"

REQUEST_OPTIONS = ["chucknorris", "dadjoke"]


def request_chuck(user_id: int) -> schemas.JokeCreate | None:
    response = requests.get(URL_CHUCK)
    if response.status_code != 200:
        return None
    parsed_response = response.json()
    joke = schemas.JokeCreate(source="Chuck Norris", text=parsed_response["value"], id=parsed_response["id"], owner_id=user_id)
    return joke


def request_dad(user_id: int) -> schemas.JokeCreate | None:
    response = requests.get(URL_DAD, headers={"Accept": "application/json"})
    if response.status_code != 200:
        return None
    parsed_response = response.json()
    if parsed_response["status"] != 200:
        return None
    joke = schemas.JokeCreate(source="Dad Joke", text=parsed_response["joke"], id=parsed_response["id"], owner_id=user_id)
    return joke
    

def get_random_joke(user_id: int) -> schemas.JokeCreate | None:
    selected_joke = random.choice(REQUEST_OPTIONS)
    if selected_joke == "chucknorris":
        final_joke = request_chuck(user_id)
    else:
        final_joke = request_dad(user_id)
    return final_joke