from datetime import datetime
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer
from dependencies.instagram import login
from motor.motor_asyncio import AsyncIOMotorClient
from database import get_database
from dependencies.token import verify_token
from schemas.instagram import Instagram
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post("/insta/login")
async def login_insta(instagram: Instagram, db: AsyncIOMotorClient = Depends(get_database),
                      token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    user: str = payload.get("sub")
    if type(payload) is not dict:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you cant access this endpoint")

    try:

        credentials = await login(username=instagram.username, password=instagram.password)


    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username or password is incorrect")
    collection = db["users"]
    update_data = {
        "$set": {f"instagram_accounts.{instagram.username}": credentials},
        "$setOnInsert": {"created_at": datetime.utcnow()}
    }

    result = await collection.update_one({"username": user}, update_data,
                                         upsert=True)

    return {"data_id": str(result.inserted_id)}
