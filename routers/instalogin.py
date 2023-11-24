from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from schemas.instagram import Instagram
from motor.motor_asyncio import AsyncIOMotorClient
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
from database import get_database


router = APIRouter()


@router.post("/insta/login")
async def login_insta(username: str, password: str, db: AsyncIOMotorClient = Depends(get_database())):
    try:
        credentials= await Instagram.login(username, password)
        result = await db.insert_one(credentials)
        return {"credentials": str(result.inserted_id)}
    except HTTPException as e:
        raise e







