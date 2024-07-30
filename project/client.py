import requests
import random

headers = {"Accept": "application/json"}
url_chuck = "https://api.chucknorris.io/jokes/random"
url_dad = "https://icanhazdadjoke.com"

response_chuck = requests.get(url_chuck)
response_dad = requests.get(url_dad, headers=headers)

request_options = ["chucknorris", "dadjoke"]

selected_joke = random.choice(request_options)

if selected_joke == "chucknorris":
    if response_chuck.status_code == 200:
        print(f"Your selected joke is: {selected_joke}. Here it goes:")
        parsed_response = response_chuck.json()
        print(f"{parsed_response["value"]}.")
    elif response_chuck.status_code == 404:
        print("Chuck Not Found. Try again later.")
elif selected_joke == "dadjoke":
    if response_dad.status_code == 200:
        print(f"Your selected joke is: {selected_joke}. Here it goes:")
        parsed_response = response_dad.json()
        print(f"{parsed_response["joke"]}.")
    elif response_dad.status_code == 404:
        print("Dad Not Found. Try again later.")


    #     elif selected_joke == "dadjoke":
    # parsed_response = response_dad.text
    # print(parsed_response)
    # if response_dad.status_code == 200:
    #     evaluated_response = parsed_response["status"]
    #     if evaluated_response == 404:
    #         print(f"Something went wrong. Please check out your request. {response_dad.message}.")
    #     else:
    #         print(f"Your selected joke is: {selected_joke}. Here it goes:")
    #         parsed_response = response_dad.json()
    #         print(f"{parsed_response["joke"]}.")
    # elif response_dad.status_code == 404:
    #     print("Dad Not Found. Try again later.")