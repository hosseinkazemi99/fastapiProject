from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from schemas.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.get("/protected", response_model=dict)
async def protected(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    username: str = payload.get("sub")
    if type(payload) is not dict:
        raise payload
    return {"message": f"hello {username} to this protected", "token": token}
