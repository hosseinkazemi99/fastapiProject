from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer
from dependencies.instagram import login
from motor.motor_asyncio import AsyncIOMotorClient
from database import get_database
from dependencies.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post("/insta/login")
async def login_insta(username: str, password: str, db: AsyncIOMotorClient = Depends(get_database),
                      token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    user: str = payload.get("sub")
    if type(payload) is not dict:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you cant access this endpoint")

    try:
        credentials = await login(username=username, password=password)

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username or password is incorrect")
    collection = db["users"]

    result = await collection.update_one({"username": user}, {"$Set": {f"instagram_accounts.{username}": credentials}},
                                         upsert=True)

    return {"credentials": str(result.inserted_id)}
