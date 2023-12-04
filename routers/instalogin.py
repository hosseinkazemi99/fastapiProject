import datetime
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer
from dependencies.instagram import login
from dependencies.token import verify_token
from schemas.instagram import Instagram
from database import Instagram_Collection, Users_Collection
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post("/insta/login")
async def login_insta(instagram: Instagram,
                      token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if type(payload) is not dict:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you cant access this endpoint")
    user: str = payload.get("sub")

    try:
        cookie = await login(username=instagram.username, password=instagram.password)

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username or password is incorrect")

    insta_data = await Instagram_Collection.find_one({"instagram_account": instagram.username})

    if insta_data is None:
        insta_data = Instagram_Collection(
            instagram_account=instagram.username,
            password=instagram.password,
            cookie=cookie,
            last_update=str(datetime.datetime.utcnow())
        )

        await insta_data.insert()
    else:
        insta_data.password = instagram.password
        insta_data.cookie=cookie
        insta_data.last_update=str(datetime.datetime.utcnow())
        await insta_data.replace()

    insta_data_ID = insta_data.model_dump(include={"id"})
    user_data = await Users_Collection.find_one({"username": user})
    if user_data is not None:
        user_data.instagram_account.append(insta_data)

        await user_data.save()

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="your account not find or disable ")

    return {"instagram_dataID": insta_data_ID["id"]}
