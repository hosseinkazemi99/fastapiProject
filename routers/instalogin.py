import datetime
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

    if type(payload) is not dict:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you cant access this endpoint")
    user: str = payload.get("sub")
    try:

        cookie = await login(username=instagram.username, password=instagram.password)


    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username or password is incorrect")
    collection = db["users"]
    update_data = {
        "$set": {
            f"instagram_accounts.{instagram.username}": {"username": instagram.username, "password": instagram.password,
                                                         "created_at": datetime.datetime.utcnow(),
                                                         "cookie": cookie}}
    }

    result = await collection.update_one({"username": user}, update_data,
                                         upsert=True)

    inserted_id = result.upserted_id

    if inserted_id is None:
        existing_record = await collection.find_one({"username": user})
        inserted_id = existing_record["_id"]

    return {"data_id": str(inserted_id)}


