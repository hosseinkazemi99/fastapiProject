import datetime
import time

import requests
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer
from dependencies.finduserid import find_instagram_id_by_username as userid
from database import Instagram_Collection, Followers_Collection
from dependencies.token import verify_token
from schemas.instagram import UserFollower

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post("/insta/followers/")
async def followers(userfollowers: UserFollower,
                    token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if type(payload) is not dict:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you cant access this endpoint")
    user: str = payload.get("sub")
    userid_traget = str(userid(userfollowers.username))
    if userid_traget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="your username not found")
    insta_data = await Instagram_Collection.find_one({"instagram_account": userfollowers.useraccount})
    if insta_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="your username account  not found")
    insta_data_cookie = insta_data.model_dump()
    X_Csrftoken = insta_data_cookie['cookie']['csrftoken']
    referer = f"https://www.instagram.com/{userfollowers.username}/followers/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "X-Ig-App-Id": "936619743392459",
        "X-Asbd-Id": "129477",
        "Viewport-Width": "833",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": referer,
        "X-Csrftoken": X_Csrftoken
    }
    url = f"https://www.instagram.com/api/v1/friendships/{userid_traget}/followers/?count=12&search_surface=follow_list_page"
    url2 = f"https://www.instagram.com/api/v1/friendships/{userid_traget}/followers/?count=12&max_id=25&search_surface=follow_list_page"

    first_response = requests.get(url=url, headers=headers, cookies=insta_data_cookie['cookie'])
    time.sleep(2)
    second_response = requests.get(url=url2, headers=headers, cookies=insta_data_cookie['cookie'])
    print(first_response.status_code)
    print(second_response.status_code)
    if first_response.status_code != int(200) or second_response.status_code != int(200):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="we have have problem to request")

    first_response = first_response.json()
    second_response = second_response.json()
    followers_user = []

    for user in first_response["users"]:
        followers_user.append(user["username"])
    for user in second_response["users"]:
        followers_user.append(user["username"])

    follower_collection = await Followers_Collection.find_one({"user_account": userfollowers.username})

    if follower_collection is None:

        follower_collection = Followers_Collection(
            user_account=userfollowers.username,
            followers=followers_user,
            last_update=str(datetime.datetime.utcnow()),
        )
        follower_collection.instagram_account.append(insta_data)

        await follower_collection.save()

    else:
        follower_collection.followers = followers_user
        follower_collection.last_update = str(datetime.datetime.utcnow())
        await follower_collection.replace()


    return {"follower": followers_user}
