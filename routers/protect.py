from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from dependencies.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.get("/protected", response_model=dict)
async def protected(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    username: str = payload.get("sub")
    if type(payload) is not dict:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": f"Hello {username} to this protected resource", "token": token}