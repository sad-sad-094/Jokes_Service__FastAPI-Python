from typing import Any

import requests


def request_chuck(url: str) -> dict | None:
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    parsed_response = response.json()
    return parsed_response


def request_dad(url: str, header: dict[str, Any]) -> dict | None:
    response = requests.get(url, headers=header)

    if response.status_code != 200:
        return None
    parsed_response = response.json()

    if parsed_response["status"] != 200:
        return None

    return parsed_response
