import random

from app.schemas import jokes
from app.infra.requests import request_chuck, request_dad


class JokeService:
    def __init__(self):
        self.url_chuck = "https://api.chucknorris.io/jokes/random"
        self.url_dad = "https://icanhazdadjoke.com"
        self.dad_headers = {"Accept": "application/json"}
        self.request_options = ["chucknorris", "dadjoke"]

    def get_random_joke(self, user_id: int) -> jokes.JokeCreate | None:
        selected_joke = random.choice(self.request_options)
        
        if selected_joke == "chucknorris":
            response = request_chuck(self.url_chuck)
            final_joke = jokes.JokeCreate(
                source="Chuck Norris",
                text=response["value"],
                id=response["id"],
                owner_id=user_id
            )
        else:
            response = request_dad(self.url_dad, self.dad_headers)
            final_joke = jokes.JokeCreate(
                source="Dad Joke",
                text=response["joke"],
                id=response["id"],
                owner_id=user_id
            )
        return final_joke
    

joke_services = JokeService()
