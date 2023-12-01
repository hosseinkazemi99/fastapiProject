import requests
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient
from database import get_database
from dependencies.token import verify_token
from schemas.instagram import UserFollower
from bs4 import BeautifulSoup

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post("/insta/followers/")
async def followers(userfollowers: UserFollower, db: AsyncIOMotorClient = Depends(get_database),
                    token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if type(payload) is not dict:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you cant access this endpoint")
    user: str = payload.get("sub")

    baseurl = "https://www.instagram.com/"
    usertarget = userfollowers.username
    userurl = f"{baseurl}{usertarget}/"
    targeturl = f"{userurl}followers/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": userurl,
        "x-csrftoken": 'Vouc7J0oJSpBciIJptNQAxRA5dDkKWq2'
    }

    users_collection = db["users"]
    instagram_collection = db["instagram"]
    try:
        my_user_data =await users_collection.find_one({"username": user})
        insta_account_data =await instagram_collection.find_one({"instagram_account": userfollowers.useraccount})
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user data or instagram data not found")

    if my_user_data["instagram_account"][userfollowers.useraccount] is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="you cant access to this account")

    headers["x-csrftoken"] = insta_account_data["cookie"]["csrftoken"]

    cookie = insta_account_data["cookie"]

    response = requests.get(url=targeturl, headers=headers, cookies=cookie)
    print(targeturl)
    print(response.status_code)
    content = BeautifulSoup(response.text, 'html.parser')
    print(content.find(attrs={"class": "x7r02ix xf1ldfh x131esax xdajt7p xxfnqb6 xb88tzc xw2csxc x1odjw0f x5fp0pe"}))

    return {"data": str(content.find(attrs={"class": "Followers"}))}

