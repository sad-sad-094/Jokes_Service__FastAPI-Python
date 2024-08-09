import random

from app.schemas import jokes
from app.infra.requests.client import request_chuck, request_dad

URL_CHUCK = "https://api.chucknorris.io/jokes/random"
URL_DAD = "https://icanhazdadjoke.com"
DAD_HEADERS = {"Accept": "application/json"}

REQUEST_OPTIONS = ["chucknorris", "dadjoke"]

def get_random_joke(user_id: int) -> jokes.JokeCreate | None:
    selected_joke = random.choice(REQUEST_OPTIONS)
    
    if selected_joke == "chucknorris":
        final_joke = request_chuck(user_id)
    else:
        final_joke = request_dad(user_id)
    return final_joke
