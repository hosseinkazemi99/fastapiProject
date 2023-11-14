import requests
from fastapi import HTTPException

async def login_to_instagram(username: str, password: str):

    login_url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"

    data = {
        "username": username,
        "password": password,
    }

    response = requests.post(login_url, data=data)


    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400,detail=f"Login failed with status code {response.status_code}")
