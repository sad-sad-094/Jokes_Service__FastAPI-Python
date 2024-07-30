import requests

headers = {"Accept": "application/json"}

response_dad = requests.get('https://icanhazdadjoke.com/', headers=headers)
response_chuck = requests.get("https://api.chucknorris.io/jokes/random")


if response_chuck.status_code == 200:
    print("Chuck Success!")
    parsed_response = response_chuck.json()

    print(parsed_response["value"], parsed_response["id"])
elif response_chuck.status_code == 404:
    print("Chuck Not Found.")

if response_dad.status_code == 200:
    print("Dad Success!")
    parsed_response = response_dad.json()

    print(parsed_response["joke"], parsed_response["id"])
elif response_dad.status_code == 404:
    print("Dad Not Found.")