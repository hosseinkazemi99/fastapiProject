from schemas.token import Token
from dependencies.token import create_access_token
from schemas.user import User, UserInDB
from dependencies.user import authenticate_user, get_password_hash
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import timedelta
import os
from dotenv import load_dotenv
from database import Users_Collection

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
hashed_password = pwd_context.hash("user_password")

router = APIRouter()


@router.get("/users/{username}")
async def get_user(username: str):
    result = await Users_Collection.find_one({"username": username})

    if result:

        return {"username": username, "result": result.to_json()}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=User)
async def register_user(
        user: UserInDB):
    result = await Users_Collection.find_one({"username": user.username})
    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registeredii",
        )
    else:
        hashed_password = get_password_hash(user.hashed_password)
        new_user = Users_Collection(username=user.username, email=user.email, hashed_password=hashed_password)
        await new_user.insert()

        return {"username": user.username, "email": user.email}


@router.get("/users", response_model=list[User])
async def get_all_users():
    cursor = Users_Collection.find_all()
    users = await cursor.to_list(length=None)
    return users
