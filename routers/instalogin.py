import datetime
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer
from dependencies.instagram import login
from motor.motor_asyncio import AsyncIOMotorClient
from database import get_database
from dependencies.token import verify_token
from schemas.instagram import Instagram, UserFollower

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post("/insta/login")
async def login_insta(instagram: Instagram, db: AsyncIOMotorClient = Depends(get_database),
                      token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if type(payload) is not dict:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you cant access this endpoint")
    user: str = payload.get("sub")
    try:

        cookie = await login(username=instagram.username, password=instagram.password)


    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username or password is incorrect")
    users_collection = db["users"]
    instagram_collection = db["instagram"]
    update_instagram_data = {"$set": {"password": instagram.password,
                                      "cookie": cookie},
                             "$currentDate": {"last_update": {"$type": "date"}}}

    update_instagram_collection = await instagram_collection.update_one({"instagram_account": instagram.username},
                                                                        update_instagram_data,
                                                                        upsert=True)

    instagram_account_collection = await instagram_collection.find_one({"instagram_account": instagram.username})
    instagram_account_collection_id = instagram_account_collection["_id"]
    update_user_data = {"$set": {f"instagram_account.{instagram.username}": str(instagram_account_collection_id)}}
    update_users_collection = await users_collection.update_one({"username": user}, update_user_data, upsert=True)
    return {"data_id": str(instagram_account_collection_id)}
