from pydantic import BaseModel


class Instagram(BaseModel):
    username: str
    password: str


class UserFollower(BaseModel):
    username: str
    useraccount: str
